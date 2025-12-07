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

    -- =============================================================
    -- Bước 1: Tìm tất cả các cặp (UserID, LessonID) bị ảnh hưởng
    -- =============================================================
    ;WITH AffectedLessons AS (
        SELECT DISTINCT UserID, LessonID
        FROM (
            SELECT UserID, LessonID FROM inserted
            UNION ALL
            SELECT UserID, LessonID FROM deleted
        ) x
    ),

    -- =============================================================
    -- Bước 2: Map LessonID -> ModuleID 
    -- (Lesson có thể nằm trong bảng CONTENT, QUIZ hoặc ASSIGNMENT)
    -- =============================================================
    LessonModules AS (
        SELECT al.UserID, al.LessonID,
               COALESCE(c.ModuleID, q.ModuleID, a.ModuleID) AS ModuleID
        FROM AffectedLessons al
        LEFT JOIN CONTENT c ON c.ContentID = al.LessonID
        LEFT JOIN QUIZ q      ON q.QuizID      = al.LessonID
        LEFT JOIN ASSIGNMENT a ON a.AssID      = al.LessonID
    ),

    -- =============================================================
    -- Bước 3: Map ModuleID -> CourseID để lấy danh sách cần update
    -- =============================================================
    AffectedEnrollments AS (
        SELECT DISTINCT lm.UserID, m.CourseID
        FROM LessonModules lm
        JOIN [MODULE] m ON m.ModuleID = lm.ModuleID
        WHERE lm.ModuleID IS NOT NULL
    )

    -- =============================================================
    -- Bước 4: Cập nhật Progress và Status trong bảng ENROLLMENT
    -- =============================================================
    UPDATE E
    SET 
        -- Cập nhật Progress
        Progress = FinalCalc.NewProgress,
        
        -- Cập nhật Status dựa trên Progress mới
        [Status] = CASE 
            -- Trường hợp 1: Hoàn thành 100% -> Set thành Completed
            WHEN FinalCalc.NewProgress = 100.0 THEN N'Completed'
            
            -- Trường hợp 2: Nếu đã từng Completed nhưng giờ < 100% (ví dụ xóa bớt bài đã học) -> Quay về Active
            WHEN FinalCalc.NewProgress < 100.0 AND E.[Status] = N'Completed' THEN N'Active'
            
            -- Trường hợp 3: Giữ nguyên trạng thái cũ (Active, Dropped, Suspended...)
            ELSE E.[Status]
        END
    FROM ENROLLMENT E
    INNER JOIN AffectedEnrollments AE 
        ON E.StudentID = AE.UserID 
        AND E.CourseID = AE.CourseID
    -- Tính toán số lượng bài học (Counts)
    CROSS APPLY (
        SELECT 
            -- Tổng số bài học trong khóa
            (
                SELECT COUNT(*) FROM
                (
                    SELECT c.ContentID FROM CONTENT c JOIN [MODULE] m ON c.ModuleID = m.ModuleID WHERE m.CourseID = AE.CourseID
                    UNION ALL
                    SELECT q.QuizID FROM QUIZ q JOIN [MODULE] m ON q.ModuleID = m.ModuleID WHERE m.CourseID = AE.CourseID
                    UNION ALL
                    SELECT a.AssID FROM ASSIGNMENT a JOIN [MODULE] m ON a.ModuleID = m.ModuleID WHERE m.CourseID = AE.CourseID
                ) AS AllLessons
            ) AS TotalLessons,

            -- Tổng số bài đã hoàn thành (is_finished = 1)
            (
                SELECT COUNT(*) FROM
                (
                    SELECT t.LessonID FROM TAKE t JOIN CONTENT c ON t.LessonID = c.ContentID JOIN [MODULE] m ON c.ModuleID = m.ModuleID WHERE t.UserID = AE.UserID AND t.is_finished = 1 AND m.CourseID = AE.CourseID
                    UNION ALL
                    SELECT t.LessonID FROM TAKE t JOIN QUIZ q ON t.LessonID = q.QuizID JOIN [MODULE] m ON q.ModuleID = m.ModuleID WHERE t.UserID = AE.UserID AND t.is_finished = 1 AND m.CourseID = AE.CourseID
                    UNION ALL
                    SELECT t.LessonID FROM TAKE t JOIN ASSIGNMENT a ON t.LessonID = a.AssID JOIN [MODULE] m ON a.ModuleID = m.ModuleID WHERE t.UserID = AE.UserID AND t.is_finished = 1 AND m.CourseID = AE.CourseID
                ) AS DoneLessons
            ) AS FinishedLessons
    ) AS Counts
    -- Tính toán % Progress cuối cùng (FinalCalc) để dùng chung cho cả cột Progress và Status
    CROSS APPLY (
        SELECT CAST(
            CASE 
                WHEN Counts.TotalLessons = 0 THEN 0.0
                ELSE ROUND((CAST(Counts.FinishedLessons AS FLOAT) * 100.0) / Counts.TotalLessons, 1)
            END 
        AS DECIMAL(4,1)) AS NewProgress
    ) AS FinalCalc;
END;
GO