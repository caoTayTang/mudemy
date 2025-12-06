-- ================================================
-- MUDemy Database DDL Statements
-- Microsoft SQL Server 2022
-- ================================================

-- Xóa database nếu đã tồn tại
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'MUDemy')
BEGIN
    ALTER DATABASE MUDemy SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE MUDemy;
END
GO

-- Tạo database mới với collation hỗ trợ Unicode và tiếng Việt
CREATE DATABASE MUDemy 
COLLATE Vietnamese_CI_AS;
GO

USE MUDemy;
GO

-- ================================================
-- 1. BẢNG USER
-- ================================================
CREATE TABLE [USER] (
    UserID VARCHAR(10) PRIMARY KEY,
    User_name NVARCHAR(100) NOT NULL UNIQUE,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    [Password] VARCHAR(255) NOT NULL, 

    Full_name NVARCHAR(100),
    City NVARCHAR(100),
    Country NVARCHAR(100),
    Phone VARCHAR(10),
    Date_of_birth DATE,
    Age INT DEFAULT 18 CHECK (Age > 0),
    Last_login DATETIME,
    IFlag BIT,
    Bio_text NVARCHAR(MAX),
    Year_of_experience INT CHECK (Year_of_experience >= 0),
    Average_rating DECIMAL(2,1) DEFAULT NULL CHECK (Average_rating >= 0 AND Average_rating <= 5),
    SFlag BIT,
    Total_enrollments INT DEFAULT 0 CHECK (Total_enrollments >= 0),

    CONSTRAINT chk_email_format CHECK (Email LIKE '%@%.%'),
    CONSTRAINT chk_password_length CHECK (LEN([Password]) >= 6),
    CONSTRAINT chk_password_lowercase CHECK ([Password] COLLATE Latin1_General_BIN2 LIKE '%[a-z]%'),
    CONSTRAINT chk_password_uppercase CHECK ([Password] COLLATE Latin1_General_BIN2 LIKE '%[A-Z]%'),
    CONSTRAINT chk_password_digit CHECK ([Password] LIKE '%[0-9]%'),
    CONSTRAINT chk_password_special CHECK ([Password] LIKE '%[^a-zA-Z0-9]%')
);
GO

-- ================================================
-- 4. BẢNG QUALIFICATION
-- ================================================
CREATE TABLE QUALIFICATION (
    UserID VARCHAR(10) NOT NULL,
    Qualification NVARCHAR(200) NOT NULL,
    PRIMARY KEY (UserID, Qualification),
    CONSTRAINT FK_Qualification_Instructor FOREIGN KEY (UserID) 
        REFERENCES [USER](UserID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- 5. BẢNG INTERESTS
-- ================================================
CREATE TABLE INTERESTS (
    UserID VARCHAR(10) NOT NULL,
    Interest NVARCHAR(100) NOT NULL,
    PRIMARY KEY (UserID, Interest),
    CONSTRAINT FK_Interests_Student FOREIGN KEY (UserID) 
        REFERENCES [USER](UserID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- 6. BẢNG CATEGORY
-- ================================================
CREATE TABLE CATEGORY (
    CourseID VARCHAR(10) NOT NULL,
    Category NVARCHAR(100) NOT NULL,
    PRIMARY KEY (CourseID, Category)
);
GO

-- ================================================
-- 7. BẢNG COURSE
-- ================================================
CREATE TABLE COURSE (
    CourseID VARCHAR(10) PRIMARY KEY,
    Difficulty NVARCHAR(20) CHECK (Difficulty IN (N'Beginner', N'Intermediate', N'Advanced')),
    [Language] NVARCHAR(50) NOT NULL,
    Title NVARCHAR(200) NOT NULL,
    [Description] NVARCHAR(MAX),
    Enrollment_count INT DEFAULT 0 CHECK (Enrollment_count >= 0),
    CONSTRAINT chk_course_title_length CHECK (LEN(Title) >= 5)
);
GO

-- Thêm foreign key cho CATEGORY sau khi COURSE đã được tạo
ALTER TABLE CATEGORY 
ADD CONSTRAINT fk_category_course 
FOREIGN KEY (CourseID) REFERENCES COURSE(CourseID) ON DELETE NO ACTION ON UPDATE NO ACTION;
GO

-- ================================================
-- 8. BẢNG REQUIRES (Course Prerequisites)
-- ================================================
CREATE TABLE REQUIRES (
    CourseID VARCHAR(10) NOT NULL,
    Required_courseID VARCHAR(10) NOT NULL,
    PRIMARY KEY (CourseID, Required_CourseID),
    CONSTRAINT FK_Requires_Course FOREIGN KEY (CourseID) 
        REFERENCES COURSE(CourseID) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT FK_Requires_RequiredCourse FOREIGN KEY (Required_CourseID) 
        REFERENCES COURSE(CourseID) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT chk_no_self_requirement CHECK (CourseID != Required_CourseID)
);
GO

-- ================================================
-- 9. BẢNG INSTRUCT (Instructor teaches Course)    
-- ================================================
CREATE TABLE INSTRUCT (
    UserID VARCHAR(10) NOT NULL,
    CourseID VARCHAR(10) NOT NULL,
    PRIMARY KEY (UserID, CourseID),
    CONSTRAINT FK_Instruct_Instructor FOREIGN KEY (UserID) 
        REFERENCES [USER](UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Instruct_Course FOREIGN KEY (CourseID) 
        REFERENCES COURSE(CourseID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- 10. BẢNG ENROLLMENT
-- ================================================
CREATE TABLE ENROLLMENT (
    EnrollmentID VARCHAR(10) NOT NULL UNIQUE,
    CourseID VARCHAR(10) NOT NULL,
    PaymentID VARCHAR(10) NOT NULL,
    StudentID VARCHAR(10) NOT NULL,
    [Status] NVARCHAR(20) DEFAULT N'Active' CHECK ([Status] IN (N'Active', N'Completed', N'Dropped', N'Suspended')),
    Enroll_date DATETIME NOT NULL DEFAULT GETDATE(),
    Progress DECIMAL(3,1) DEFAULT 0.0 CHECK (Progress >= 0 AND Progress <= 100),
    PRIMARY KEY (EnrollmentID, CourseID, PaymentID, StudentID),
    CONSTRAINT FK_Enrollment_Course FOREIGN KEY (CourseID) 
        REFERENCES COURSE(CourseID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Enrollment_Student FOREIGN KEY (StudentID) 
        REFERENCES [USER](UserID) ON DELETE NO ACTION ON UPDATE NO ACTION
    
);
GO

-- ================================================
-- 11. BẢNG PAYMENT
-- ================================================
CREATE TABLE PAYMENT (
    PaymentID VARCHAR(10) PRIMARY KEY,
    Amount INT NOT NULL CHECK (Amount >= 0),
    Payment_date DATETIME NOT NULL DEFAULT GETDATE(),
    Payment_method NVARCHAR(50) CHECK (Payment_method IN (N'Credit Card', N'Debit Card', N'PayPal', N'Bank Transfer', N'Cash')),
    UserID VARCHAR(10) NOT NULL,
    CONSTRAINT FK_Payment_User FOREIGN KEY (UserID) 
        REFERENCES [USER](UserID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- Thêm foreign key cho ENROLLMENT sau khi PAYMENT đã được tạo
ALTER TABLE ENROLLMENT 
ADD CONSTRAINT fk_enrollment_payment 
FOREIGN KEY (PaymentID) REFERENCES PAYMENT(PaymentID) ON DELETE NO ACTION ON UPDATE NO ACTION;
GO

-- ================================================
-- 12. BẢNG CERTIFICATE
-- ================================================
CREATE TABLE CERTIFICATE (
    CertificateID VARCHAR(10) NOT NULL UNIQUE,
    CourseID VARCHAR(10) NOT NULL,
    StudentID VARCHAR(10) NOT NULL,
    Expiry_date DATE, -- NULL = no expiration
    Issue_date DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    Certificate_number VARCHAR(50) NOT NULL,
    PRIMARY KEY (CertificateID, CourseID, StudentID),
    CONSTRAINT FK_Certificate_Course FOREIGN KEY (CourseID) 
        REFERENCES COURSE(CourseID) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT FK_Certificate_Student FOREIGN KEY (StudentID) 
        REFERENCES [USER](UserID) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT chk_certificate_dates CHECK (Expiry_date IS NULL OR Expiry_date > Issue_date)
);
GO

-- ================================================
-- 13. BẢNG MODULE
-- ================================================
CREATE TABLE [MODULE] (
    ModuleID VARCHAR(10) PRIMARY KEY,
    Title NVARCHAR(200) NOT NULL,
    CourseID VARCHAR(10) NOT NULL,
    CONSTRAINT FK_Module_Course FOREIGN KEY (CourseID) 
        REFERENCES COURSE(CourseID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- 14. BẢNG LESSON_REF (CHỈ ĐỂ LẤY ID CỦA QUIZ, ASSIGNMENT VÀ CONTENT)
-- ================================================
CREATE TABLE LESSON_REF (
    LessonID VARCHAR(10) PRIMARY KEY
);
GO

-- ================================================
-- 15. BẢNG CONTENT (Superclass cho TEXT, VIDEO, IMAGE)
-- ================================================
CREATE TABLE CONTENT (
    ContentID VARCHAR(10) PRIMARY KEY,
    Slides NVARCHAR(100), -- Link to slides dir
    Title NVARCHAR(200),
    ModuleID VARCHAR(10) NOT NULL,
    CONSTRAINT FK_Content_LessonRef FOREIGN KEY (ContentID) 
        REFERENCES LESSON_REF(LessonID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Content_Module FOREIGN KEY (ModuleID) 
        REFERENCES [MODULE](ModuleID) ON DELETE NO ACTION ON UPDATE NO ACTION
);
GO

-- ================================================
-- 16. BẢNG TEXT (Subclass của CONTENT)
-- ================================================
CREATE TABLE [TEXT] (
    ContentID VARCHAR(10) NOT NULL,
    TextID VARCHAR(10) NOT NULL UNIQUE,
    [Text] NVARCHAR(200), -- Link to text content
    PRIMARY KEY (ContentID, TextID),
    CONSTRAINT FK_Text_Content FOREIGN KEY (ContentID) 
        REFERENCES CONTENT(ContentID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- 17. BẢNG VIDEO (Subclass của CONTENT)
-- ================================================
CREATE TABLE VIDEO (
    ContentID VARCHAR(10) NOT NULL,
    VideoID VARCHAR(10) NOT NULL UNIQUE,
    Video NVARCHAR(200), -- Link to video
    PRIMARY KEY (ContentID, VideoID),
    CONSTRAINT FK_Video_Content FOREIGN KEY (ContentID) 
        REFERENCES CONTENT(ContentID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- 18. BẢNG IMAGE (Subclass của CONTENT)
-- ================================================
CREATE TABLE [IMAGE] (
    ContentID VARCHAR(10) NOT NULL,
    ImageID VARCHAR(10) NOT NULL UNIQUE,
    [Image] NVARCHAR(200), -- Link to Image
    PRIMARY KEY (ContentID, ImageID),
    CONSTRAINT FK_Image_Content FOREIGN KEY (ContentID) 
        REFERENCES CONTENT(ContentID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- 19. BẢNG RESOURCE
-- ================================================
CREATE TABLE RESOURCE (
    ResourceID VARCHAR(10) PRIMARY KEY,
    File_Name NVARCHAR(255) NOT NULL,
    File_link NVARCHAR(500) NOT NULL,
    External_link NVARCHAR(200)
);
GO

-- ================================================
-- 20. BẢNG PROVIDE_RESOURCE (Lesson provides Resource)
-- ================================================
CREATE TABLE PROVIDE_RESOURCE (
    ResourceID VARCHAR(10) NOT NULL,
    LessonID VARCHAR(10) NOT NULL,
    PRIMARY KEY (ResourceID, LessonID),
    CONSTRAINT FK_ProvideResource_Resource FOREIGN KEY (ResourceID) 
        REFERENCES RESOURCE(ResourceID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_ProvideResource_Lesson FOREIGN KEY (LessonID) 
        REFERENCES LESSON_REF(LessonID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- 21. BẢNG ASSIGNMENT
-- ================================================
CREATE TABLE ASSIGNMENT (
    AssID VARCHAR(10) PRIMARY KEY,
    Deadline DATETIME NOT NULL DEFAULT GETDATE(),
    [Description] NVARCHAR(MAX),
    Title NVARCHAR(200) NOT NULL,
    ModuleID VARCHAR(10) NOT NULL,
    CONSTRAINT FK_Assignment_LessonRef FOREIGN KEY (AssID) 
        REFERENCES LESSON_REF(LessonID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Assignment_Module FOREIGN KEY (ModuleID) 
        REFERENCES [MODULE](ModuleID) ON DELETE NO ACTION ON UPDATE NO ACTION
);
GO

-- ================================================
-- 22. BẢNG QUIZ
-- ================================================
CREATE TABLE QUIZ (
    QuizID VARCHAR(10) PRIMARY KEY,
    Time_limit INT CHECK (Time_limit > 0), -- Seconds
    Num_attempt INT DEFAULT 1 CHECK (Num_attempt > 0),
    Deadline DATETIME NOT NULL DEFAULT GETDATE(),
    Title NVARCHAR(200) NOT NULL,
    ModuleID VARCHAR(10) NOT NULL,
    CONSTRAINT FK_Quiz_LessonRef FOREIGN KEY (QuizID) 
        REFERENCES LESSON_REF(LessonID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Quiz_Module FOREIGN KEY (ModuleID) 
        REFERENCES [MODULE](ModuleID) ON DELETE NO ACTION ON UPDATE NO ACTION
);
GO

-- ================================================
-- 23. BẢNG QUESTION
-- ================================================
CREATE TABLE QUESTION (
    QuestionID VARCHAR(10) NOT NULL UNIQUE,
    QuizID VARCHAR(10) NOT NULL,
    Correct_answer NVARCHAR(MAX) NOT NULL,
    Content NVARCHAR(MAX) NOT NULL,
    CONSTRAINT FK_Question_Quiz FOREIGN KEY (QuizID) 
        REFERENCES QUIZ(QuizID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- 24. BẢNG ANSWER
-- ================================================
CREATE TABLE ANSWER (
    QuestionID VARCHAR(10) NOT NULL,
    QuizID VARCHAR(10) NOT NULL,
    AnswerID VARCHAR(10) NOT NULL UNIQUE,
    Answer NVARCHAR(MAX) NOT NULL,
    PRIMARY KEY (QuestionID, QuizID, AnswerID),
    CONSTRAINT FK_Answer_Question FOREIGN KEY (QuestionID) 
        REFERENCES QUESTION(QuestionID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Answer_Quiz FOREIGN KEY (QuizID) 
        REFERENCES QUIZ(QuizID) ON DELETE NO ACTION ON UPDATE NO ACTION
);
GO

-- ================================================
-- 25. BẢNG SUBMISSION
-- ================================================
CREATE TABLE ASSIGN_SUBMISSION (
    SubID VARCHAR(10),
    UserID VARCHAR(10),
    AssID VARCHAR(10),
    Sub_content NVARCHAR(MAX), -- MAY CHANGE TO LINK/ DIR
    Grade DECIMAL(5,2) CHECK (Grade >= 0 AND Grade <= 100),
    Sub_date DATETIME NOT NULL DEFAULT GETDATE(),
    PRIMARY KEY (SubID),
    CONSTRAINT FK_Submission_Assign FOREIGN KEY (AssID) 
        REFERENCES ASSIGNMENT(AssID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Assign_Submission_User FOREIGN KEY (UserID)
        REFERENCES [USER](UserID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO


CREATE TABLE QUIZ_SUBMISSION (
    SubID VARCHAR(10),
    UserID VARCHAR(10),
    QuizID VARCHAR(10),
    Sub_content NVARCHAR(MAX), -- MAY CHANGE TO LINK/ DIR
    Grade DECIMAL(5,2) CHECK (Grade >= 0 AND Grade <= 100),
    Sub_date DATETIME NOT NULL DEFAULT GETDATE(),
    PRIMARY KEY (SubID),
    CONSTRAINT FK_Submission_Quiz FOREIGN KEY (QuizID) 
        REFERENCES QUIZ(QuizID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Quiz_Submission_User FOREIGN KEY (UserID)
        REFERENCES [USER](UserID) ON DELETE CASCADE ON UPDATE CASCADE 
);
GO
-- ================================================
-- 26. BẢNG TAKE (Student takes Lesson)
-- ================================================
CREATE TABLE TAKE (
    UserID VARCHAR(10) NOT NULL, 
    LessonID VARCHAR(10) NOT NULL,
    is_finished BIT DEFAULT 0,
    PRIMARY KEY (UserID, LessonID),
    CONSTRAINT FK_Take_Student FOREIGN KEY (UserID) 
        REFERENCES [USER](UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Take_Lesson FOREIGN KEY (LessonID) 
        REFERENCES LESSON_REF(LessonID) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

-- ================================================
-- TRIGGERS để tự động đồng bộ LESSON_REF và tạo ID với prefix
-- ================================================

-- Trigger thêm LessonID vào LESSON_REF từ QUIZ
CREATE TRIGGER trg_quiz_insert_lesson_ref
ON QUIZ
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Thêm vào LESSON_REF trước
    INSERT INTO LESSON_REF (LessonID)
    SELECT QuizID FROM inserted;
    
    -- Sau đó thêm vào QUIZ
    INSERT INTO QUIZ (QuizID, Time_limit, Num_attempt, Title, Deadline, ModuleID)
    SELECT QuizID, Time_limit, Num_attempt, Title, Deadline, ModuleID
    FROM inserted;
END;
GO

-- Trigger xóa LessonID từ LESSON_REF khi xóa QUIZ
CREATE TRIGGER trg_quiz_delete_lesson_ref
ON QUIZ
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    DELETE FROM LESSON_REF
    WHERE LessonID IN (SELECT QuizID FROM deleted);
END;
GO

-- Trigger thêm LessonID vào LESSON_REF từ ASSIGNMENT
CREATE TRIGGER trg_ass_insert_lesson_ref
ON ASSIGNMENT
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Thêm vào LESSON_REF trước
    INSERT INTO LESSON_REF (LessonID)
    SELECT AssID FROM inserted;
    
    -- Sau đó thêm vào ASSIGNMENT
    INSERT INTO ASSIGNMENT (AssID, Deadline, [Description], Title, ModuleID)
    SELECT AssID, Deadline, [Description], Title, ModuleID
    FROM inserted;
END;
GO

-- Trigger xóa LessonID từ LESSON_REF khi xóa ASSIGNMENT
CREATE TRIGGER trg_ass_delete_lesson_ref
ON ASSIGNMENT
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    DELETE FROM LESSON_REF
    WHERE LessonID IN (SELECT AssID FROM deleted);
END;
GO

-- Trigger thêm LessonID vào LESSON_REF từ CONTENT
CREATE TRIGGER trg_content_insert_lesson_ref
ON CONTENT
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Thêm vào LESSON_REF trước
    INSERT INTO LESSON_REF (LessonID)
    SELECT ContentID FROM inserted;
    
    -- Sau đó thêm vào CONTENT
    INSERT INTO CONTENT (ContentID, Slides, Title, ModuleID)
    SELECT ContentID, Slides, Title, ModuleID
    FROM inserted;
END;
GO

-- Trigger xóa LessonID từ LESSON_REF khi xóa CONTENT
CREATE TRIGGER trg_content_delete_lesson_ref
ON CONTENT
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    DELETE FROM LESSON_REF
    WHERE LessonID IN (SELECT ContentID FROM deleted);
END;
GO

-- ================================================
-- TRIGGERS để tự động tạo ID với prefix
-- ================================================

-- Trigger cho USER ID (USR00001, USR00002, ...)
CREATE TRIGGER trg_user_id_auto_increment
ON [USER]
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    INSERT INTO [USER] (UserID, User_name, Email, [Password], Full_name, City, Country, 
                        Phone, Date_of_birth, Last_login, IFlag, Bio_text, 
                        Year_of_experience, SFlag, Total_enrollments)
    SELECT 
        CASE 
            WHEN i.UserID IS NULL OR i.UserID = '' THEN
                'USR' + RIGHT('00000' + CAST(
                    ISNULL((SELECT MAX(CAST(SUBSTRING(UserID, 4, 5) AS INT)) FROM [USER]), 0) + 
                    ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR), 5)
            ELSE i.UserID
        END,
        i.User_name, i.Email, i.[Password], i.Full_name, i.City, i.Country,
        i.Phone, i.Date_of_birth, i.Last_login, i.IFlag, i.Bio_text,
        i.Year_of_experience, i.SFlag, i.Total_enrollments
    FROM inserted i;
END;
GO

-- Trigger cho COURSE ID (CRS00001, CRS00002, ...)
CREATE TRIGGER trg_course_id_auto_increment
ON COURSE
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    INSERT INTO COURSE (CourseID, Difficulty, [Language], Title, [Description])
    SELECT 
        CASE 
            WHEN i.CourseID IS NULL OR i.CourseID = '' THEN
                'CRS' + RIGHT('00000' + CAST(
                    ISNULL((SELECT MAX(CAST(SUBSTRING(CourseID, 4, 5) AS INT)) FROM COURSE), 0) + 
                    ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR), 5)
            ELSE i.CourseID
        END,
        i.Difficulty, i.[Language], i.Title, i.[Description]
    FROM inserted i;
END;
GO

-- ================================================
-- Hoàn thành
-- ================================================