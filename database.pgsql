CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE IF NOT EXISTS guild_settings(
    guild_id BIGINT PRIMARY KEY,
    report_channel_id BIGINT,
    staff_role_id BIGINT
);


CREATE TABLE IF NOT EXISTS temporary_ban(
    guild_id BIGINT,
    user_id BIGINT,
    expiry_time TIMESTAMP,
    PRIMARY KEY (guild_id, user_id)
);


CREATE TABLE IF NOT EXISTS actions(
    id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    guild_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    action_type TEXT NOT NULL,
    reason TEXT,
    moderator_id BIGINT NOT NULL,
    timestamp TIMESTAMP
);
CREATE INDEX IF NOT EXISTS guild_id_user_id_actions ON actions (guild_id, user_id);
CREATE INDEX IF NOT EXISTS guild_id_user_id_action_type_actions ON actions (guild_id, user_id, action_type);
CREATE INDEX IF NOT EXISTS guild_id_moderator_id_actions ON actions (guild_id, moderator_id);


CREATE TABLE IF NOT EXISTS message_logs(
    log_id UUID NOT NULL,
    message_id BIGINT NOT NULL,
    author_id BIGINT,
    author_name TEXT,
    message_content TEXT,
    PRIMARY KEY (log_id, message_id)
);
