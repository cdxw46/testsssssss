-- context
SELECT SYSTEM_USER AS [system_user], SUSER_SNAME() AS [login_name];

-- try impersonation
BEGIN TRY
    EXECUTE AS LOGIN = Ndc01_sql_svc;
    SELECT SYSTEM_USER AS [imp_system_user], SUSER_SNAME() AS [imp_login_name];
    REVERT;
END TRY
BEGIN CATCH
    SELECT ERROR_MESSAGE() AS imp_error;
END CATCH;

BEGIN TRY
    EXECUTE AS LOGIN = Nsa;
    SELECT SYSTEM_USER AS [imp_sa_system_user], SUSER_SNAME() AS [imp_sa_login_name];
    REVERT;
END TRY
BEGIN CATCH
    SELECT ERROR_MESSAGE() AS imp_sa_error;
END CATCH;

-- list dirs if possible
BEGIN TRY
    EXEC master..xp_dirtree NC:\\Users\\john.w\\Desktop, 1, 1;
END TRY
BEGIN CATCH
    SELECT ERROR_MESSAGE() AS xp_dirtree_error;
END CATCH;

BEGIN TRY
    DECLARE @f INT; EXEC master..xp_fileexist NC:\\Users\\john.w\\Desktop\\user.txt, @f OUTPUT; SELECT @f AS user_txt_exists;
END TRY
BEGIN CATCH
    SELECT ERROR_MESSAGE() AS xp_fileexist_error;
END CATCH;

-- linked server execution
BEGIN TRY
    EXEC (NSELECT SYSTEM_USER AS remote_system_user, SUSER_SNAME() AS remote_login) AT [DC02.darkzero.ext];
END TRY
BEGIN CATCH
    SELECT ERROR_MESSAGE() AS exec_at_dc02_error;
END CATCH;

BEGIN TRY
    SELECT * FROM OPENQUERY([DC02.darkzero.ext], SELECT DB_NAME() AS db);
END TRY
BEGIN CATCH
    SELECT ERROR_MESSAGE() AS openquery_dc02_error;
END CATCH;
