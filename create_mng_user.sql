USE MUDemy;
GO

CREATE OR ALTER PROCEDURE CreateMngUserForApp
    @LoginName NVARCHAR(100),
    @Password NVARCHAR(200)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @sql NVARCHAR(MAX);


    IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = @LoginName)
    BEGIN
        SET @sql = '
            CREATE LOGIN [' + @LoginName + '] 
            WITH PASSWORD = ''' + @Password + ''', CHECK_POLICY = OFF;
        ';
        EXEC(@sql);
    END


    IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = @LoginName)
    BEGIN
        SET @sql = '
            CREATE USER [' + @LoginName + '] FOR LOGIN [' + @LoginName + '];
        ';
        EXEC(@sql);
    END


    SET @sql = '
        ALTER ROLE db_owner ADD MEMBER [' + @LoginName + '];
    ';
    EXEC(@sql);

    PRINT 'User created successfully';
END
GO
