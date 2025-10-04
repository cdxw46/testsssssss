SELECT SYSTEM_USER AS [system_user], SUSER_SNAME() AS [login_name];
EXEC master.dbo.xp_dirtree NC:\Users, 1, 1;
EXEC master.dbo.xp_dirtree NC:\Users\john.w\Desktop, 1, 1;
DECLARE @f INT; EXEC master.dbo.xp_fileexist NC:\Users\john.w\Desktop\user.txt, @f OUTPUT; SELECT @f AS user_txt_exists;
