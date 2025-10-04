USE msdb;
SELECT USER_NAME() AS user_name;
SELECT IS_MEMBER(db_owner) AS is_dbo;
SELECT IS_MEMBER(SQLAgentUserRole) AS is_agent_user;
SELECT IS_MEMBER(SQLAgentReaderRole) AS is_agent_reader;
SELECT IS_MEMBER(SQLAgentOperatorRole) AS is_agent_operator;
