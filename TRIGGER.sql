-- ================================================
-- TRIGGERS FOR LOGIC HANDLING
-- ================================================
USE MUDemy;
GO

-- ================================================
-- 1. Trigger cập nhật số lượng enrollments
-- ================================================
CREATE OR ALTER TRIGGER trg_update_total_enrollments
ON ENROLLMENT
AFTER INSERT, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- TRƯỜNG HỢP: INSERT (Tăng số lượng)
    IF EXISTS (SELECT * FROM inserted)
    BEGIN
        WITH InsertCounts AS (
            SELECT StudentID, COUNT(*) AS CountVal
            FROM inserted
            GROUP BY StudentID
        )
        UPDATE U
        SET Total_enrollments = ISNULL(Total_enrollments, 0) + I.CountVal
        FROM [USER] U
        JOIN InsertCounts I ON U.UserID = I.StudentID;
    END

    -- TRƯỜNG HỢP: DELETE (Giảm số lượng)
    IF EXISTS (SELECT * FROM deleted)
    BEGIN
        WITH DeleteCounts AS (
            SELECT StudentID, COUNT(*) AS CountVal
            FROM deleted
            GROUP BY StudentID
        )
        UPDATE U
        SET Total_enrollments = CASE 
                                    WHEN (ISNULL(Total_enrollments, 0) - D.CountVal) < 0 THEN 0 
                                    ELSE ISNULL(Total_enrollments, 0) - D.CountVal 
                                END
        FROM [USER] U
        JOIN DeleteCounts D ON U.UserID = D.StudentID;
    END
END;
GO

-- ================================================
-- 2. Trigger kiểm tra Deadline cho ASSIGNMENT
-- (Áp dụng cho bảng ASSIGN_SUBMISSION)
-- ================================================
CREATE OR ALTER TRIGGER trg_check_assignment_deadline
ON ASSIGN_SUBMISSION
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Kiểm tra ngày nộp (Sub_date) so với Deadline trong bảng ASSIGNMENT
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN ASSIGNMENT a ON i.AssID = a.AssID
        WHERE i.Sub_date > a.Deadline
    )
    BEGIN
        RAISERROR (N'Submission rejected: The assignment submission date exceeds the deadline.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END
END;
GO

-- ================================================
-- 3. Trigger kiểm tra Deadline cho QUIZ
-- (Áp dụng cho bảng QUIZ_SUBMISSION)
-- ================================================
CREATE OR ALTER TRIGGER trg_check_quiz_deadline
ON QUIZ_SUBMISSION
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Kiểm tra ngày nộp (Sub_date) so với Deadline trong bảng QUIZ
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN QUIZ q ON i.QuizID = q.QuizID
        WHERE i.Sub_date > q.Deadline
    )
    BEGIN
        RAISERROR (N'Submission rejected: The quiz submission date exceeds the deadline.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END
END;
GO

-- ================================================
-- 4. Trigger kiểm tra điều kiện tiên quyết (Prerequisites)
-- ================================================
CREATE OR ALTER TRIGGER trg_check_course_prerequisites
ON ENROLLMENT
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Kiểm tra: Nếu khóa học yêu cầu (REQUIRES) một khóa khác,
    -- thì Student phải có CERTIFICATE của khóa đó và còn hạn.
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN REQUIRES r ON i.CourseID = r.CourseID
        WHERE NOT EXISTS (
            SELECT 1 
            FROM CERTIFICATE c
            WHERE c.StudentID = i.StudentID 
              AND c.CourseID = r.Required_courseID
              AND (c.Expiry_date IS NULL OR c.Expiry_date >= CAST(GETDATE() AS DATE))
        )
    )
    BEGIN
        RAISERROR (N'Enrollment denied: Prerequisite certificate is missing or expired.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END
END;
GO

-- ================================================
-- 5. Trigger cập nhật số lượng đăng ký khóa học
-- ================================================
CREATE OR ALTER TRIGGER trg_update_course_enrollment_count
ON ENROLLMENT
AFTER INSERT, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- ======================
    -- 1. Trường hợp INSERT
    -- ======================
    IF EXISTS (SELECT 1 FROM inserted)
    BEGIN
        WITH Ins AS (
            SELECT CourseID, COUNT(*) AS Cnt
            FROM inserted
            GROUP BY CourseID
        )
        UPDATE C
        SET Enrollment_count = ISNULL(C.Enrollment_count, 0) + Ins.Cnt
        FROM COURSE C
        JOIN Ins ON C.CourseID = Ins.CourseID;
    END

    -- ======================
    -- 2. Trường hợp DELETE
    -- ======================
    IF EXISTS (SELECT 1 FROM deleted)
    BEGIN
        WITH Del AS (
            SELECT CourseID, COUNT(*) AS Cnt
            FROM deleted
            GROUP BY CourseID
        )
        UPDATE C
        SET Enrollment_count =
            CASE 
                WHEN ISNULL(C.Enrollment_count, 0) - Del.Cnt < 0 THEN 0
                ELSE C.Enrollment_count - Del.Cnt
            END
        FROM COURSE C
        JOIN Del ON C.CourseID = Del.CourseID;
    END
END;
GO


-- ================================================
-- 6. Trigger cập nhật tiến độ học tập (Progress) khi TAKE thay đổi
-- ================================================
CREATE OR ALTER TRIGGER trg_update_progress_on_take
ON TAKE
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    /*
      Bước 1: Tìm tất cả các cặp (UserID, LessonID) bị ảnh hưởng
      (bao gồm cả rows từ inserted và deleted)
    */
    ;WITH AffectedLessons AS (
        SELECT DISTINCT UserID, LessonID
        FROM (
            SELECT UserID, LessonID FROM inserted
            UNION ALL
            SELECT UserID, LessonID FROM deleted
        ) x
    ),

    /*
      Bước 2: Map LessonID -> ModuleID (lesson có thể là Content, Quiz hoặc Assignment)
      Lấy ModuleID từ từng bảng tương ứng (nếu tồn tại)
    */
    LessonModules AS (
        SELECT al.UserID, al.LessonID,
               COALESCE(c.ModuleID, q.ModuleID, a.ModuleID) AS ModuleID
        FROM AffectedLessons al
        LEFT JOIN CONTENT c ON c.ContentID = al.LessonID
        LEFT JOIN QUIZ q      ON q.QuizID     = al.LessonID
        LEFT JOIN ASSIGNMENT a ON a.AssID     = al.LessonID
    ),

    /*
      Bước 3: Map ModuleID -> CourseID và lấy danh sách các cặp (UserID, CourseID) cần cập nhật
    */
    AffectedEnrollments AS (
        SELECT DISTINCT lm.UserID, m.CourseID
        FROM LessonModules lm
        JOIN [MODULE] m ON m.ModuleID = lm.ModuleID
        WHERE lm.ModuleID IS NOT NULL
    )

    /*
      Bước 4: Cập nhật progress cho mỗi cặp (StudentID, CourseID) trong ENROLLMENT
      - TotalLessons: số lesson (content+quiz+assignment) thuộc course
      - FinishedLessons: số lesson đã is_finished = 1 của user thuộc course
    */
    UPDATE E
    SET Progress = 
        CASE 
            WHEN calc.TotalLessons = 0 THEN CAST(0.0 AS DECIMAL(3,1))
            ELSE CAST( ROUND( (CAST(calc.FinishedLessons AS FLOAT) * 100.0) / calc.TotalLessons, 1) AS DECIMAL(3,1) )
        END
    FROM ENROLLMENT E
    INNER JOIN AffectedEnrollments AE
        ON E.StudentID = AE.UserID
       AND E.CourseID = AE.CourseID
    CROSS APPLY
    (
        -- Tính TotalLessons và FinishedLessons cho AE.UserID / AE.CourseID
        SELECT
            -- Total lessons in the course (distinct lesson ids)
            (
                SELECT COUNT(*) FROM
                (
                    -- Content lessons
                    SELECT c.ContentID AS LessonID
                    FROM CONTENT c
                    JOIN [MODULE] mm ON c.ModuleID = mm.ModuleID
                    WHERE mm.CourseID = AE.CourseID

                    UNION

                    -- Quiz lessons
                    SELECT q.QuizID AS LessonID
                    FROM QUIZ q
                    JOIN [MODULE] mm2 ON q.ModuleID = mm2.ModuleID
                    WHERE mm2.CourseID = AE.CourseID

                    UNION

                    -- Assignment lessons
                    SELECT a.AssID AS LessonID
                    FROM ASSIGNMENT a
                    JOIN [MODULE] mm3 ON a.ModuleID = mm3.ModuleID
                    WHERE mm3.CourseID = AE.CourseID
                ) AS AllLessons
            ) AS TotalLessons,

            -- Finished lessons for this student in this course
            (
                SELECT COUNT(*) FROM
                (
                    -- Finished content lessons
                    SELECT t.LessonID
                    FROM TAKE t
                    JOIN CONTENT c2 ON c2.ContentID = t.LessonID
                    JOIN [MODULE] mm4 ON c2.ModuleID = mm4.ModuleID
                    WHERE t.UserID = AE.UserID AND t.is_finished = 1 AND mm4.CourseID = AE.CourseID

                    UNION

                    -- Finished quiz lessons
                    SELECT t2.LessonID
                    FROM TAKE t2
                    JOIN QUIZ q2 ON q2.QuizID = t2.LessonID
                    JOIN [MODULE] mm5 ON q2.ModuleID = mm5.ModuleID
                    WHERE t2.UserID = AE.UserID AND t2.is_finished = 1 AND mm5.CourseID = AE.CourseID

                    UNION

                    -- Finished assignment lessons
                    SELECT t3.LessonID
                    FROM TAKE t3
                    JOIN ASSIGNMENT a3 ON a3.AssID = t3.LessonID
                    JOIN [MODULE] mm6 ON a3.ModuleID = mm6.ModuleID
                    WHERE t3.UserID = AE.UserID AND t3.is_finished = 1 AND mm6.CourseID = AE.CourseID
                ) AS DoneLessons
            ) AS FinishedLessons
    ) AS calc
    ;
END;
GO
