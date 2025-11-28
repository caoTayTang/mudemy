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
-- 3. Trigger kiểm tra Deadline cho QUIZ (MỚI THÊM)
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