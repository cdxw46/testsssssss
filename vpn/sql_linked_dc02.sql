EXEC (SELECT SYSTEM_USER AS remote_system_user, SUSER_SNAME() AS remote_login) AT [DC02.darkzero.ext];
EXEC (SELECT name FROM sys.databases) AT [DC02.darkzero.ext];
