USE MUdemy;
GO
-- ================================================
-- FUNCTION   
-- ================================================


-- 1. CalculateContentCompletionRate: tỉ lệ hoàn thành khóa học của SV đối với môn học
-- ARGS:
--      + StudentID(VARCHAR(10))
--      + CourseID(VARCHAR(10)) 
CREATE OR ALTER FUNCTION CalculateContentCompletionRate (
    @StudentID VARCHAR(10),
    @CourseID VARCHAR(10)
)
RETURNS DECIMAL(5, 2)
AS
BEGIN
    DECLARE @TotalContent INT;
    DECLARE @CompletedContent INT;
    
    SELECT @TotalContent = COUNT(C.ContentID)
    FROM CONTENT C
    JOIN MODULE M ON C.ModuleID = M.ModuleID
    WHERE M.CourseID = @CourseID;

    SELECT @CompletedContent = COUNT(T.LessonID)
    FROM TAKE T
    JOIN CONTENT C ON T.LessonID = C.ContentID
    JOIN MODULE M ON C.ModuleID = M.ModuleID
    WHERE T.UserID = @StudentID AND M.CourseID = @CourseID AND T.is_finished = 1;

    IF @TotalContent = 0
        RETURN 0.00;
    
    RETURN (@CompletedContent * 100.00) / @TotalContent;
END;
GO
-- TEST
SELECT dbo.CalculateContentCompletionRate('USR00006', 'CRS00001') AS CompletionRate;
GO
-- 2. GetInstructorsByQualificationKeyword:Tìm kiếm giảng viên phù hợp với chuyên ngành mình học
-- ARGS:
--      + Keyword(NVARCHAR(50))
-- RETURNS: TABLE
CREATE OR ALTER FUNCTION GetInstructorsByQualificationKeyword (
    @Keyword NVARCHAR(50)
)
RETURNS @QualifiedInstructors TABLE (
    UserID VARCHAR(10),
    FullName NVARCHAR(100),
    QualificationDetail NVARCHAR(200)
)
AS
BEGIN
    INSERT INTO @QualifiedInstructors (UserID, FullName, QualificationDetail)
    SELECT
        U.UserID,
        U.Full_name,
        Q.Qualification
    FROM [USER] U
    JOIN QUALIFICATION Q ON U.UserID = Q.UserID
    WHERE Q.Qualification LIKE '%' + @Keyword + '%';
    RETURN;
END;
GO
-- TEST
SELECT * FROM dbo.GetInstructorsByQualificationKeyword('Sci')
GO
-- ================================================
-- PROCEDURE
-- ================================================


-- 1. GetInstructorCourseDetails: QUERY thông tin các khóa học có Instructor quản lí, sắp xếp theo Độ khó giảm và title theo alphabet
-- ARGS:
--      + InstructorID(VARCHAR(10)): ID của User
CREATE OR ALTER PROCEDURE GetInstructorCourseDetails (
    @InstructorID VARCHAR(10)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM [USER] WHERE UserID = @InstructorID)
    BEGIN
        THROW 50001, N'Lỗi: UserID không tồn tại trong hệ thống.', 1;
        RETURN;
    END
    IF NOT EXISTS (SELECT 1 FROM INSTRUCT WHERE UserID = @InstructorID)
    BEGIN
        THROW 50002, N'Lỗi: UserID này không phải là giảng viên.', 1;
        RETURN;
    END
    SELECT
        U.Full_name AS InstructorName,
        C.CourseID,
        C.Title AS CourseTitle,
        C.Difficulty,
		C.[Language],
		C.[Description]
    FROM [USER] U
    JOIN INSTRUCT I ON U.UserID = I.UserID
    JOIN COURSE C ON I.CourseID = C.CourseID 
    WHERE U.UserID = @InstructorID
    ORDER BY C.Difficulty DESC, C.Title;
END;
GO
-- TEST
EXEC GetInstructorCourseDetails 'USR00005'
GO
-- 2. GetQuizPerformanceStats: Query Thống kê Điểm theo Module, có lọc theo số lần submission
-- ARGS:
--      + ModuleID(VARCHAR(10))
--      + MinSubmission(INT): Ngưỡng hỗ trợ lọc
CREATE OR ALTER PROCEDURE GetQuizPerformanceStats 
    @ModuleID VARCHAR(10),
    @MinSubmissions INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM [MODULE] WHERE ModuleID = @ModuleID)
    BEGIN
        THROW 50003, N'Lỗi: ModuleID không tồn tại.', 1;
        RETURN;
    END
    SELECT
        Q.QuizID,
        Q.Title AS QuizTitle,
        CAST(AVG(S.Grade) AS DECIMAL(5, 2)) AS AverageGrade,
        MAX(S.Grade) AS HighestGrade,
		MIN(S.Grade) AS LowestGrade,
        COUNT(S.SubID) AS TotalSubmissions
    FROM QUIZ Q
    JOIN QUIZ_SUBMISSION S ON Q.QuizID = S.QuizID
    WHERE Q.ModuleID = @ModuleID
      AND S.Grade IS NOT NULL
    GROUP BY Q.QuizID, Q.Title
    HAVING COUNT(S.SubID) >= @MinSubmissions
    ORDER BY AverageGrade DESC;

END;
GO
-- TEST
EXEC GetQuizPerformanceStats 'MOD001', 1
GO

-- 3. CheckPrerequisiteCompletion: Hiển thị các môn tiên quyết cần hoàn thành nếu đăng kí TargetCourse
-- ARGS:
--      + StudentID(VARCHAR(10))
--      + TargetCourseID(VARCHAR(10))
CREATE OR ALTER PROCEDURE CheckPrerequisiteCompletion (
    @StudentID VARCHAR(10),
    @TargetCourseID VARCHAR(10)
)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM COURSE WHERE CourseID = @TargetCourseID)
    BEGIN
        THROW 50004, N'Lỗi: Khóa học đích không tồn tại.', 1;
        RETURN;
    END
    SELECT
        R.Required_courseID,
        C.Title
    FROM REQUIRES R
    JOIN COURSE C ON R.Required_courseID = C.CourseID
    LEFT JOIN ENROLLMENT E ON E.CourseID = R.Required_courseID AND E.StudentID = @StudentID
    WHERE R.CourseID = @TargetCourseID 
      AND (E.Status <> 'Completed' OR E.EnrollmentID IS NULL);
END;
GO
-- TEST
EXEC CheckPrerequisiteCompletion 'USR00008', 'CRS00001'
GO
