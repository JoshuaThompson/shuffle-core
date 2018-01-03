CREATE TABLE channels (
  id SERIAL PRIMARY KEY,
  channel_id BIGINT UNIQUE,
  mature BOOLEAN,
  status TEXT,
  broadcaster_language TEXT,
  display_name TEXT,
  game TEXT,
  language TEXT,
  name TEXT,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ,
  partner BOOLEAN,
  logo TEXT,
  video_banner TEXT,
  profile_banner TEXT,
  profile_banner_background_color TEXT,
  url TEXT,
  views BIGINT,
  followers BIGINT
);

CREATE TABLE streams (
  id SERIAL PRIMARY KEY,
  stream_id BIGINT,
  channel_id BIGINT references channels(channel_id),
  game TEXT,
  viewers INT,
  video_height INT,
  average_fps INT,
  delay INT,
  created_at TIMESTAMPTZ,
  is_playlist BOOLEAN
);

CREATE UNIQUE INDEX stream_id_channel_id_created_at_index ON streams(stream_id, channel_id, created_at)