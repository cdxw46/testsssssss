SELECT DB_NAME() AS db, USER_NAME() AS user_name, IS_MEMBER(db_owner) AS is_dbo,
       IS_MEMBER(SQLAgentOperatorRole) AS is_agent_operator,
       IS_MEMBER(SQLAgentReaderRole) AS is_agent_reader,
       IS_MEMBER(SQLAgentUserRole) AS is_agent_user;
