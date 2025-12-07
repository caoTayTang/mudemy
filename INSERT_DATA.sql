-- =======================================================
-- INSERT DATA
-- =======================================================
USE MUDemy;
GO
SET DATEFORMAT ymd;
GO


-- 1. USER: 13 rows
INSERT INTO [USER] (UserID, User_name, Email, [Password], Full_name, City, Country, Phone, Date_of_birth, Last_login, IFlag, Bio_text, Year_of_experience, Average_rating, SFlag) VALUES
('USR00001', N'Đạt Phạm',    'dat.pham@mudemy.edu.vn',     'P@ssw0rd123!', N'Phạm Lê Tiến Đạt',        N'TP. Hồ Chí Minh', N'Việt Nam', '0903123456', '1986-06-15', '2025-11-23 19:30:00', 1, N'Giảng viên MUdemy', 15, 1.0, 0), 
('USR00002', N'Thịnh Võ',     'thinh.vo@mudemy.edu.vn',       'v@ssw0rD312!', N'Võ Văn Thịnh',      N'TP. Hồ Chí Minh', N'Việt Nam', '0904123457', '1985-03-20', '2025-11-23 19:29:01', 1, N'Giảng viên MUdemy', 14, 2.3, 0), 
('USR00003', N'Thuận Lương',     'thuan.luong@mudemy.edu.vn',     'b@ssW0rd231!', N'Lương Minh Thuận',  N'TP. Hồ Chí Minh', N'Việt Nam', '0905123458', '1987-09-10', '2025-11-23 16:30:00', 1, N'Giảng viên MUdemy', 12, 3.0, 0), 
('USR00004', N'Huy Nguyễn',     'huy.nguyen@mudemy.edu.vn',        'h@cKd00r555!', N'Nguyễn Quốc Huy',       N'TP. Hồ Chí Minh', N'Việt Nam', '0906123459', '1988-11-05', '2025-11-23 20:05:36', 1, N'Giảng viên MUdemy', 13, 4.0, 0), 
('USR00005', N'Đại Lê',     'dai.lechi@mudemy.edu.vn',        'b@ckd00rSiu!', N'Lê Chí Đại',       N'TP. Hồ Chí Minh', N'Việt Nam', '0906123459', '1988-11-05', '2025-11-23 23:05:25', 1, N'Giảng viên MUdemy', 13, 3.5, 0), 
('USR00006', N'Tuấn BK',       'anhtuan@hcmut.edu.vn','t@ssw0R123!', N'Nguyễn Anh Tuấn',          N'TP. Hồ Chí Minh', N'Việt Nam', '0938111222', '2005-04-12', '2025-11-23 15:06:03', 0, N'SV Bách Khoa TP.HCM', NULL, NULL, 1), 
('USR00007', N'Linh Cute',     'ngoclinh@fpt.edu.vn',         'Y@ssh0rd102!', N'Trần Ngọc Linh',           N'TP. Hồ Chí Minh', N'Việt Nam', '0938222333', '2006-08-25', '2025-11-22 07:03:05', 0, N'SV Đại Học FPT', NULL, NULL, 1), 
('USR00008', N'Thọ Fan MU',        'ductho@gmail.com',            'Tho#w0rd123!', N'Lê Đức Thọ',               N'TP. Hồ Chí Minh', N'Việt Nam', '0938333444', '2005-12-30', '2025-11-22 08:03:24', 0, N'SV KHTN TP.HCM', NULL, NULL, 1), 
('USR00009', N'Trang Kute',     'thuytrang98@gmail.com',       'traNgp@ssw0rd22!', N'Phạm Thúy Trang',          N'TP. Hồ Chí Minh', N'Việt Nam', '0938444555', '2007-05-18', '2025-11-22 07:03:05', 0, N'SV UEH', NULL, NULL, 1), 
('USR00010', N'baokhanh', 'baokhanh@gmail.com',        'h%w0Rd345!', N'Vũ Bảo Khanh',             N'TP. Hồ Chí Minh', N'Việt Nam', '0938555666', '2004-02-14', '2025-11-22 13:03:05', 0, N'SV FTU', NULL, NULL, 1), 
('USR00011', N'vinhpro', 'vinhnguyen@gmail.com',       'P@SSw0rd123!', N'Nguyễn Hữu Vinh',          N'TP. Hồ Chí Minh', N'Việt Nam', '0938666777', '2000-10-10', '2025-11-21 07:03:05', 0, N'SV UEH', NULL, NULL, 1), 
('USR00012', N'LAnh',        'lananh@gmail.com',            'T@ssw0rh788!', N'Đỗ Lan Anh',               N'TP. Hồ Chí Minh', N'Việt Nam', '0938777888', '2004-07-19', '2025-11-23 08:03:05', 0, N'SV UFM', NULL, NULL, 1), 
('USR00013', N'Khoa Wibu',        'khoamu.nguyen@provn.vn',        'f@nM0rd666!', N'Nguyễn Đặng Khoa',         N'TP. Hồ Chí Minh', N'Việt Nam', '0938888999', '2005-01-01', '2025-11-22 07:04:07', 0, N'Fan MU', NULL, NULL, 1);
GO

-- 2. COURSE: 6 rows 
INSERT INTO COURSE (CourseID, Difficulty, [Language], Title, [Description]) VALUES
('CRS00001', N'Intermediate', N'Tiếng Việt', N'Python cho DeepLearning', N'Học cách xây dựng, huấn luyện và tối ưu các mô hình mạng nơ-ron phức tạp (CNN, RNN, Transformers) sử dụng TensorFlow và PyTorch.'),
('CRS00002', N'Advanced',     N'Tiếng Việt', N'Full-stack React + Node.js', N'Phát triển ứng dụng web hiện đại từ giao diện người dùng (React, Redux) đến API backend và cơ sở dữ liệu (Node.js, Express, MongoDB/PostgreSQL).'),
('CRS00003', N'Beginner',     N'Tiếng Việt', N'Figma UI/UX từ A-Z', N'Làm chủ công cụ Figma, học các nguyên tắc cơ bản của thiết kế giao diện (UI) và trải nghiệm người dùng (UX), thực hành qua dự án thiết kế ứng dụng di động.'),
('CRS00004', N'Advanced',     N'Tiếng Việt', N'DevOps & AWS thực tế', N'Triển khai tự động hóa CI/CD, quản lý hạ tầng bằng mã (IaC) với Terraform, sử dụng các dịch vụ cốt lõi của AWS (EC2, S3, RDS, Lambda) trong môi trường thực tế.'),
('CRS00005', N'Intermediate', N'Tiếng Việt', N'Phân Tích Dữ Liệu với Python', N'Sử dụng thư viện Pandas, NumPy và Matplotlib để làm sạch, xử lý, trực quan hóa và rút ra insight từ các bộ dữ liệu phức tạp.'),
('CRS00006', N'Beginner',     N'Tiếng Việt', N'Lập trình ngôn ngữ C++', N'Giới thiệu cơ bản về C++, cấu trúc dữ liệu và giải thuật (DSA), và lập trình hướng đối tượng (OOP)');
GO

-- KÍCH HOẠT LẠI TRIGGERS 
ENABLE TRIGGER trg_user_id_auto_increment ON [USER];
ENABLE TRIGGER trg_course_id_auto_increment ON COURSE;
GO

-- 3. CATEGORY: 14 rows
INSERT INTO CATEGORY (CourseID, Category) VALUES
('CRS00001',N'Python'),('CRS00001',N'Deep Learning'),
('CRS00002',N'React'),('CRS00002',N'Node.js'),('CRS00002',N'Full-stack'),
('CRS00003',N'Figma'),('CRS00003',N'UI/UX'),('CRS00003',N'Thiết kế'),
('CRS00004',N'DevOps'),('CRS00004',N'AWS'),
('CRS00005',N'Data Analysis'),('CRS00005',N'Python'),
('CRS00006',N'Ngôn ngữ C++'),('CRS00006',N'OOP');
GO

-- 4. INSTRUCT: 6 rows
INSERT INTO INSTRUCT (UserID, CourseID) VALUES
('USR00001','CRS00001'),('USR00002','CRS00002'),('USR00003','CRS00003'),
('USR00004','CRS00004'),('USR00005','CRS00005'),('USR00005','CRS00006');
GO

-- 5. QUALIFICATION: 5 rows
INSERT INTO QUALIFICATION (UserID, Qualification) VALUES
('USR00001',N'PhD in Physics, Statistics, and Data Science - Massachusetts Institute of Technology'),
('USR00002',N'Ph.D. in Computer Science - Stanford University'),
('USR00003',N'Ph.D. in Computer Science - University of Cambridge'),
('USR00004',N'Ph.D. in Computer Science and Technology - Tsinghua University'),
('USR00005',N'DPhil (Doctor of Philosophy) in Computer Science - University of Oxford');
GO

-- 6. INTERESTS: 13 rows
INSERT INTO INTERESTS (UserID, Interest) VALUES
('USR00006',N'React'),('USR00006',N'Mobile'),
('USR00007',N'DevOps'),('USR00007',N'Cloud'),('USR00008',N'Figma'),('USR00008',N'UI/UX'),
('USR00009',N'Data'),('USR00009',N'Power BI'),('USR00010',N'C++'),('USR00011',N'Python'),('USR00012',N'Web'), ('USR00013',N'Python'), ('USR00013',N'AI');
GO

-- 7. MODULE: 24 rows
INSERT INTO [MODULE] (ModuleID, Title, CourseID) VALUES
('MOD001', N'Giới thiệu Deep Learning & TensorFlow/PyTorch', 'CRS00001'),
('MOD002', N'Mô hình Mạng Nơ-ron Tích chập (CNN) và Ứng dụng', 'CRS00001'),
('MOD003', N'Mạng Nơ-ron Hồi quy (RNN) và Xử lý Chuỗi', 'CRS00001'),
('MOD004', N'Kiến trúc Transformer và Tối ưu hóa Mô hình', 'CRS00001'),
('MOD005', N'Làm chủ React JS: Components và Hooks', 'CRS00002'),
('MOD006', N'Quản lý State toàn cục với Redux/Context API', 'CRS00002'),
('MOD007', N'Phát triển RESTful API với Node.js và Express', 'CRS00002'),
('MOD008', N'Kết nối Cơ sở dữ liệu NoSQL (MongoDB)', 'CRS00002'),
('MOD009', N'Giới thiệu Figma và Nguyên lý Thiết kế Giao diện (UI)', 'CRS00003'),
('MOD010', N'Nghiên cứu và Phân tích Trải nghiệm Người dùng (UX)', 'CRS00003'),
('MOD011', N'Xây dựng Prototype và Test khả năng sử dụng', 'CRS00003'),
('MOD012', N'Thiết kế Hệ thống (Design System) trong Figma', 'CRS00003'),
('MOD013', N'Cơ bản về DevOps và Công cụ Git', 'CRS00004'),
('MOD014', N'Quản lý Hạ tầng bằng mã (IaC) với Terraform', 'CRS00004'),
('MOD015', N'Triển khai Liên tục (CI/CD) với Jenkins/GitLab CI', 'CRS00004'),
('MOD016', N'Quản lý Container với Docker và ECS/EKS trên AWS', 'CRS00004'),
('MOD017', N'Nhập môn Python và thư viện NumPy', 'CRS00005'),
('MOD018', N'Xử lý và Làm sạch Dữ liệu với Pandas', 'CRS00005'),
('MOD019', N'Trực quan hóa Dữ liệu với Matplotlib và Seaborn', 'CRS00005'),
('MOD020', N'Phân tích Thống kê và Rút ra Insight', 'CRS00005'),
('MOD021', N'C++ Cơ bản: Cấu trúc điều khiển và Hàm', 'CRS00006'),
('MOD022', N'Lập trình Hướng đối tượng (OOP) trong C++', 'CRS00006'),
('MOD023', N'Cấu trúc Dữ liệu Cơ bản và Giải thuật', 'CRS00006'),
('MOD024', N'Thư viện Chuẩn STL: Container và Iterator', 'CRS00006');
GO

-- 8. REQUIRES: 2 rows
INSERT INTO REQUIRES (CourseID, Required_courseID) VALUES
('CRS00001', 'CRS00005'), 
('CRS00002', 'CRS00006'),
('CRS00002', 'CRS00003'),
('CRS00005', 'CRS00006');
GO

-- 9. PAYMENT: 12 rows
INSERT INTO PAYMENT (PaymentID, Amount, Payment_method, UserID) VALUES
('PAY001', 890000, N'Bank Transfer', 'USR00013'), ('PAY002', 1190000, N'Bank Transfer', 'USR00013'),
('PAY003',1590000,N'Bank Transfer','USR00013'), ('PAY004', 990000, N'Bank Transfer', 'USR00006'),
('PAY005',890000,N'PayPal','USR00006'), ('PAY006',2490000,N'Bank Transfer','USR00006'),
('PAY007',990000,N'PayPal','USR00008'),('PAY008',2990000,N'Credit Card','USR00007'),
('PAY009',890000,N'Bank Transfer','USR00009'),
('PAY010',1190000,N'Bank Transfer','USR00009'),
('PAY011',2990000,N'Credit Card','USR00010'),
('PAY012', 890000, N'Bank Transfer', 'USR00012');
GO

-- 10. ENROLLMENT: 12 rows
DISABLE TRIGGER trg_check_course_prerequisites ON ENROLLMENT;
INSERT INTO ENROLLMENT (EnrollmentID,CourseID,PaymentID,StudentID,[Status]) VALUES
('ENR001', 'CRS00006', 'PAY001', 'USR00013', N'Completed'),
('ENR002', 'CRS00005', 'PAY002', 'USR00013', N'Completed'),
('ENR003','CRS00001','PAY003','USR00013',N'Active'),
('ENR004', 'CRS00003', 'PAY004', 'USR00006', N'Completed'),
('ENR005', 'CRS00006', 'PAY005', 'USR00006', N'Completed'),
('ENR006','CRS00002','PAY006','USR00006',N'Active'),
('ENR007','CRS00003','PAY007','USR00008',N'Completed'),
('ENR008','CRS00004','PAY008','USR00007',N'Active'),
('ENR009','CRS00006','PAY009','USR00009',N'Completed'),
('ENR010','CRS00005','PAY010','USR00009',N'Active'),
('ENR011','CRS00004','PAY011','USR00010',N'Active'),
('ENR012','CRS00006','PAY012','USR00012',N'Active');
GO
ENABLE TRIGGER trg_check_course_prerequisites ON ENROLLMENT;

-- 11. CONTENT: 15 rows
INSERT INTO CONTENT (ContentID,Title,ModuleID,Slides) VALUES
('CON001',N'Python cơ bản và thư viện NumPy', 'MOD001',N'/slides/[CRS00001]python_numpy.pdf'),
('CON002',N'Giới thiệu TensorFlow và PyTorch','MOD001',NULL),
('CON003',N'Khái niệm về Mạng Nơ-ron (MLP)','MOD001',N'/slides/[CRS00001]mlp.pdf'),
('CON004',N'Cấu trúc Project và Functional Components','MOD005',NULL),
('CON005',N'React Hooks: useState và useEffect','MOD005',N'/slides/[CRS00002]react.pdf'),
('CON006',N'Thiết lập Server Node.js và Express','MOD007',N'/slides/[CRS00002]node-server.pdf'),
('CON007',N'Xây dựng các Route API cơ bản','MOD007',NULL),
('CON008',N'Figma cho người mới: Giao diện và Công cụ chính','MOD009',NULL),
('CON009',N'Nguyên lý Thiết kế Giao diện (UI) cơ bản','MOD009',N'/slides/[CRS00003]ui-principles.pdf'),
('CON010',N'Giới thiệu về DevOps và Lợi ích','MOD013',NULL),
('CON011',N'Làm việc với Git/GitHub cơ bản','MOD013',N'/slides/[CRS00004]git-intro.pdf'),
('CON012',N'Biến, kiểu dữ liệu và Toán tử Python','MOD017',N'/slides/[CRS00005]var-python.pdf'),
('CON013',N'Giới thiệu thư viện NumPy','MOD017',NULL),
('CON014',N'C++ Hello World và Cấu trúc chương trình','MOD021',NULL),
('CON015',N'Vòng lặp (Loops) và Câu lệnh điều kiện','MOD021',N'/slides/[CRS00006]cpp-loops.pptx');
GO

-- 12. VIDEO: 5 rows
INSERT INTO VIDEO (ContentID,VideoID,Video) VALUES
('CON001','VID001',N'https://www.youtube.com/watch?v=nLRL_NcnK-4'),
('CON005','VID002',N'https://www.youtube.com/watch?v=6wf5dIrryoQ'),
('CON008','VID003',N'https://www.youtube.com/watch?v=jQ1sfKIl50E'),
('CON010','VID004',N'https://www.youtube.com/watch?v=Xrgk023l4lI'),
('CON014','VID005',N'https://www.youtube.com/watch?v=SeR2aDYoJAI');
GO

-- 13. TEXT: 4 rows
INSERT INTO [TEXT] (ContentID,TextID,[Text]) VALUES
('CON002','TXT001',N'/text/[CON002]tf-vs-pytorch.txt'),
('CON007','TXT002',N'/text/[CON007]express-route-guide.txt'),
('CON012','TXT003',N'/text/[CON012]python-data-types.txt'),
('CON013','TXT004',N'/text/[CON013]numpy-doc.txt');
GO

-- 14. IMAGE: 2 rows
INSERT INTO [IMAGE] (ContentID, ImageID, [Image]) VALUES
('CON004', 'IMG001', N'/images/[CON004]react-project-structure.png'), 
('CON009', 'IMG002', N'/images/[CON009]golden-ratio-ui.jpg'),
('CON010', 'IMG003', N'/images/[CON010]devops-pipeline.png'), 
('CON014', 'IMG004', N'/images/[CON014]cpp-memory-diagram.png');
GO

-- 15. RESOURCE: 4 rows
INSERT INTO RESOURCE (ResourceID,File_Name,File_link) VALUES
('RES002',N'React Hooks Cheatsheet','/res/[RES002]react-hooks-cheat.pdf'),
('RES004',N'Figma Icons Kit','/res/[RES004]figma-icons.fig'),
('RES005',N'Git Commands Handbook','/res/[RES005]git-commands.pdf'),
('RES006',N'C++ Style Guide','/res/[RES006]cpp-style.pdf');
GO

-- 16. PROVIDE_RESOURCE: 4 rows
INSERT INTO PROVIDE_RESOURCE (ResourceID, LessonID) VALUES
('RES002','CON005'),
('RES004','CON008'),
('RES005','CON011'),
('RES006','CON014');
GO

-- 17. ASSIGNMENT: 5 rows
INSERT INTO ASSIGNMENT (AssID,Title,[Description],Deadline,ModuleID) VALUES
('ASS001',N'Xây app quản lý quán cà phê',N'React + Node','2025-12-30 23:59:00','MOD007'), 
('ASS002',N'Phân tích doanh thu quán trà sữa','Power BI','2025-12-28 23:59:00','MOD019'), 
('ASS003',N'Deploy web lên AWS','Docker + EC2','2026-01-15 23:59:00','MOD016'), 
('ASS004',N'Viết game đơn giản bằng C++','Console','2026-01-10 23:59:00','MOD022'), 
('ASS005',N'Thiết kế app giao hàng','Figma','2025-12-25 23:59:00','MOD011'); 
GO

-- 18. QUIZ: 6 rows 
INSERT INTO QUIZ (QuizID,Title,Time_limit,Num_attempt,Deadline,ModuleID) VALUES
('QUI001',N'Quiz Deep Learning Cơ bản',1800,2,'2025-12-25 23:59:00','MOD001'), 
('QUI002',N'Quiz React Hooks',1500,1,'2025-12-26 23:59:00','MOD005'), 
('QUI003',N'Quiz Figma',1200,2,'2025-12-27 23:59:00','MOD009'), 
('QUI004',N'Quiz Docker',1800,1,'2025-12-28 23:59:00','MOD016'), 
('QUI005',N'Quiz Pandas',2000,2,'2025-12-28 23:59:00','MOD018'), 
('QUI006',N'Quiz C++ cơ bản',1800,1,'2025-12-30 23:59:00','MOD021');
GO

-- 19. QUESTION + ANSWER
INSERT INTO QUESTION (QuestionID,QuizID,Content,Correct_answer) VALUES
('Q001','QUI001',N'Python được tạo năm nào?',N'1991'),
('Q002','QUI001',N'Kiểu dữ liệu list trong Python?',N'Mutable'),
('Q003','QUI002',N'Hook nào dùng để quản lý trạng thái local?',N'useState'),
('Q004','QUI002',N'useState trả về một mảng có bao nhiêu phần tử?',N'2'),
('Q005','QUI003',N'Figma sử dụng mô hình nào để đồng bộ dữ liệu?',N'Vector Network'),
('Q006','QUI003',N'Phím tắt nào dùng để tạo Frame mới trong Figma?',N'F'),
('Q007','QUI004',N'Lệnh nào dùng để xem danh sách các container đang chạy?',N'docker ps'),
('Q008','QUI004',N'File định nghĩa môi trường container gọi là gì?',N'Dockerfile'),
('Q009','QUI005',N'Cấu trúc dữ liệu chính trong Pandas?',N'DataFrame'),
('Q010','QUI005',N'Thư viện nào Pandas dựa vào để xử lý số học?',N'NumPy');

INSERT INTO ANSWER (QuestionID,QuizID,AnswerID,Answer) VALUES
('Q001','QUI001','A1',N'1989'),('Q001','QUI001','B1',N'1991'),('Q001','QUI001','C1',N'2000'),('Q001','QUI001','D1',N'1995'),
('Q002','QUI001','A2',N'Mutable'),('Q002','QUI001','B2',N'Immutable'),('Q002','QUI001','C2',N'Both'),('Q002','QUI001','D2',N'None'),
('Q003','QUI002','A3',N'useEffect'),('Q003','QUI002','B3',N'useContext'),('Q003','QUI002','C3',N'useState'),('Q003','QUI002','D3',N'useReducer'),
('Q004','QUI002','A4',N'1'),('Q004','QUI002','B4',N'2'),('Q004','QUI002','C4',N'3'),('Q004','QUI002','D4',N'Không cố định'),
('Q005','QUI003','A5',N'Layers'),('Q005','QUI003','B5',N'Vector Network'),('Q005','QUI003','C5',N'Auto Layout'),('Q005','QUI003','D5',N'Components'),
('Q006','QUI003','A6',N'R'),('Q006','QUI003','B6',N'F'),('Q006','QUI003','C6',N'C'),('Q006','QUI003','D6',N'K'),
('Q007','QUI004','A7',N'docker logs'),('Q007','QUI004','B7',N'docker info'),('Q007','QUI004','C7',N'docker images'),('Q007','QUI004','D7',N'docker ps'),
('Q008','QUI004','A8',N'Docker File'),('Q008','QUI004','B8',N'Dockerfile'),('Q008','QUI004','C8',N'Docker Compose'),('Q008','QUI004','D8',N'Dockerignore'),
('Q009','QUI005','A9',N'Series'),('Q009','QUI005','B9',N'Array'),('Q009','QUI005','C9',N'DataFrame'),('Q009','QUI005','D9',N'List'),
('Q010','QUI005','A10',N'Matplotlib'),('Q010','QUI005','B10',N'SciPy'),('Q010','QUI005','C10',N'NumPy'),('Q010','QUI005','D10',N'SciKit-Learn');
GO

-- 20. SUBMISSION: 4 rows
INSERT INTO ASSIGN_SUBMISSION (SubID, UserID, AssID, Sub_content, Grade) VALUES
('SUB001', 'USR00006', 'ASS001', N'submission/SUB002/cafe-app.zip', 88.00),
('SUB002', 'USR00009', 'ASS002', N'Chưa nộp bài', 0.00),
('SUB003', 'USR00010', 'ASS003', N'submission/SUB003/Deploy-AWS.zip', 95.00),
('SUB004', 'USR00012', 'ASS004', N'submission/SUB004/cpp-game.zip', 85.00);
GO

-- 21. QUIZ_SUBMISSION: 6 rows
INSERT INTO QUIZ_SUBMISSION (SubID, UserID, QuizID, Sub_content, Grade) VALUES
('SUB001', 'USR00013', 'QUI001', N'Hoàn thành Quiz DeepLearning lần 1', 95.00),
('SUB002', 'USR00006', 'QUI002', N'Hoàn thành Quiz FullStack lần 1', 100.00),
('SUB003', 'USR00008', 'QUI003', N'Hoàn thành Quiz Figma lần 1', 100.00),
('SUB004', 'USR00007', 'QUI004', N'Hoàn thành Quiz Docker lần 1', 100.00),
('SUB005', 'USR00009', 'QUI005', N'Hoàn thành Quiz Pandas lần 1', 90.00),
('SUB006', 'USR00009', 'QUI005', N'Hoàn thành Quiz Pandas lần 2', 92.00); 
GO

-- 21. TAKE: 17 rows
INSERT INTO TAKE (UserID,LessonID,is_finished) VALUES
('USR00013','CON001',1),('USR00013','CON003',1),('USR00006','CON004',1),
('USR00006','CON005',1),('USR00009','CON012',1),('USR00010','CON011',0),
('USR00013','QUI001',1),
('USR00006','ASS001',1),
('USR00006','QUI002',1),
('USR00009','ASS002',0),
('USR00008','QUI003',1),
('USR00007','QUI004',1),
('USR00009','QUI005',1),   
('USR00012','CON015',1),  
('USR00010','ASS003',1), 
('USR00012','ASS004',1);
GO

-- 22. CERTIFICATE: 6 rows
INSERT INTO CERTIFICATE (CertificateID,CourseID,StudentID,Certificate_number, Issue_date) VALUES
('CER001','CRS00003','USR00008','MUD-UIUX-001', '2025-11-20'),
('CER002','CRS00006','USR00013','MUD-BASIC-PROGRAMMING-001', '2025-6-15'),
('CER003', 'CRS00005', 'USR00013', 'MUD-DATA-001', '2025-11-20'),
('CER004','CRS00003','USR00006','MUD-UIUX-002', '2025-11-20'),
('CER005', 'CRS00006', 'USR00006', 'MUD-BASIC-PROGRAMMING-002', '2025-4-21'),
('CER006','CRS00006','USR00009','MUD-BASIC-PROGRAMMING-003', '2025-11-18');
GO
