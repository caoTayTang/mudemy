-- Trigger 1
select UserID, User_name, Email, Full_name, Total_enrollments from [USER]


-- Trigger 2, 3, 4
BEGIN TRANSACTION;
------------------------------------------------------
-- 1. TEST TRIGGER ASSIGNMENT DEADLINE (trg_check_assignment_deadline)
------------------------------------------------------
PRINT '--- TEST ASSIGNMENT DEADLINE TRIGGER ---';
SELECT * FROM ASSIGNMENT WHERE AssID = 'ASS005'
SELECT * FROM ASSIGN_SUBMISSION WHERE UserID = 'USR00006'

BEGIN TRY
    INSERT INTO ASSIGN_SUBMISSION (SubID, UserID, AssID, Sub_date, Sub_content)
    VALUES ('TEST', 'USR00006', 'ASS005', '2025-12-30 14:52:36', N'Test assignment submission');

    PRINT 'Assignment submission inserted successfully (NO deadline violation).';
END TRY
BEGIN CATCH
    PRINT 'Error (Assignment Trigger): ' + ERROR_MESSAGE();
END CATCH

SELECT * FROM ASSIGN_SUBMISSION WHERE UserID = 'USR00006'

------------------------------------------------------
-- 2. TEST TRIGGER QUIZ DEADLINE (trg_check_quiz_deadline)
------------------------------------------------------
PRINT '--- TEST QUIZ DEADLINE TRIGGER ---';
SELECT * FROM QUIZ WHERE QuizID = 'QUI003';
SELECT * FROM QUIZ_SUBMISSION WHERE UserID = 'USR00006'

BEGIN TRY
    INSERT INTO QUIZ_SUBMISSION (SubID, UserID, QuizID, Sub_date, Grade)
    VALUES ('TEST', 'USR00006', 'QUI003', '2025-12-27 23:59:22', 9);

    PRINT 'Quiz submission inserted successfully (NO deadline violation).';
END TRY
BEGIN CATCH
    PRINT 'Error (Quiz Trigger): ' + ERROR_MESSAGE();
END CATCH

SELECT * FROM QUIZ_SUBMISSION WHERE UserID = 'USR00006';


------------------------------------------------------
-- 3. TEST TRIGGER COURSE PREREQUISITE (trg_check_course_prerequisites)
------------------------------------------------------
PRINT '--- TEST COURSE PREREQUISITE TRIGGER ---';
SELECT * FROM REQUIRES WHERE CourseID = 'CRS00001';
SELECT * FROM CERTIFICATE WHERE StudentID = 'USR00007';

BEGIN TRY
    INSERT INTO ENROLLMENT (EnrollmentID, StudentID, CourseID, PaymentID , Enroll_date)
    VALUES ('TEST','USR00007', 'CRS00001', 'PAY008', GETDATE());

    PRINT 'Enrollment inserted successfully (Prerequisites satisfied).';
END TRY
BEGIN CATCH
    PRINT 'Error (Prerequisite Trigger): ' + ERROR_MESSAGE();
END CATCH

SELECT * FROM ENROLLMENT WHERE StudentID = 'USR00007';


ROLLBACK TRANSACTION;

PRINT '=========== ALL CHANGES ROLLED BACK ===========';


-- Trigger 5
SELECT * FROM COURSE;


-- Trigger 6
select * from TAKE where UserID = 'USR00013';

SELECT 
    C.CourseID,
    M.ModuleID,
    L.LessonID
FROM LESSON_REF L
LEFT JOIN CONTENT CT ON L.LessonID = CT.ContentID
LEFT JOIN ASSIGNMENT A ON L.LessonID = A.AssID
LEFT JOIN QUIZ Q ON L.LessonID = Q.QuizID
LEFT JOIN MODULE M 
    ON M.ModuleID = CT.ModuleID 
    OR M.ModuleID = A.ModuleID 
    OR M.ModuleID = Q.ModuleID
LEFT JOIN COURSE C ON C.CourseID = M.CourseID
where c.CourseID = 'CRS00001'
ORDER BY C.CourseID, M.ModuleID, L.LessonID;

select * from ENROLLMENT