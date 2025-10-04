EXEC master..xp_dirtree C:\Users, 1, 1;
EXEC master..xp_dirtree C:\Users\john.w\Desktop, 1, 1;
DECLARE @f INT; EXEC master..xp_fileexist C:\Users\john.w\Desktop\user.txt, @f OUTPUT; SELECT @f AS user_txt_exists;
