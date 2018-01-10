import os
import psycopg2
import psycopg2.extras
import requests
import time
from datetime import datetime

host = "db"
port = "5432"
dbname = os.environ.get("POSTGRES_DB", "")
user = os.environ.get("POSTGRES_USER", "")
password = os.environ.get("POSTGRES_PASSWORD", "")
client_id = os.environ.get("TWITCH_CLIENTID", "")

insert_channels_query = """
  INSERT INTO channels(
    channel_id,
    mature,
    status,
    broadcaster_language,
    display_name,
    game,
    language,
    name,
    created_at,
    updated_at,
    partner,
    logo,
    video_banner,
    profile_banner,
    profile_banner_background_color,
    url,
    views,
    followers
  )
  VALUES %s
"""

insert_channels_template = """
  (
    %(_id)s,
    %(mature)s,
    %(status)s,
    %(broadcaster_language)s,
    %(display_name)s,
    %(game)s,
    %(language)s,
    %(name)s,
    %(created_at)s,
    %(updated_at)s,
    %(partner)s,
    %(logo)s,
    %(video_banner)s,
    %(profile_banner)s,
    %(profile_banner_background_color)s,
    %(url)s,
    %(views)s,
    %(followers)s
  )
"""

insert_streams_query = """
  INSERT INTO streams(
    stream_id,
    channel_id,
    game,
    viewers,
    video_height,
    average_fps,
    delay,
    created_at,
    is_playlist
  )
  VALUES %s
"""

insert_streams_template = """
   (
    %(_id)s,
    %(channel_id)s,
    %(game)s,
    %(viewers)s,
    %(video_height)s,
    %(average_fps)s,
    %(delay)s,
    %(created_at)s,
    %(is_playlist)s
  )
"""

def get_streams(limit, offset):
  try:
    headers = {
      'Accept': 'application/vnd.twitchtv.v5+json',
      'Client-ID': client_id
    }
    r = requests.get(f'https://api.twitch.tv/kraken/streams?limit={limit}&offset={offset}', headers=headers, timeout=5)

    if r.status_code == 429:
      time.sleep(60)
      return get_streams(limit, offset)
  except requests.exceptions.ChunkedEncodingError:
    #Requests seems to be struggling at times https://github.com/requests/requests/issues/4248
    time.sleep(1)
    return get_streams(limit, offset)

  return r.json()

def get_all_streams():
  streams = []
  index_offset = 0
  total = 1000

  while (index_offset*100) <= total:
    next_streams = get_streams(100, index_offset*100)
    streams += next_streams.get('streams', [])
    index_offset += 1
    total = next_streams.get('_total', 0)

    if len(streams) > 0:
      last_stream_current = streams[len(streams)-1]

      #since we only show streams with >= 5 on frontend, stop getting streams once they are small
      if last_stream_current.get('viewers', 0) <= 5:
        return streams

    time.sleep(1)

  return streams


while True:
  print(f'Fetching streams at {datetime.now()}...')
  streams = get_all_streams()
  #Dedupe by _id in case there was some shift of position during time between requests, keep latest
  streams = list({stream['_id']: stream for stream in streams}.values())
  
  for stream in streams:
    stream['channel_id'] = stream['channel']['_id']

  channels = [stream['channel'] for stream in streams]
  #Must dedupe channels as well because it's possible for a streamer to start/stop streaming creating multiple stream_ids
  channels = list({channel['_id']: channel for channel in channels}.values())

  print('Done fetching streams!')

  conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
  cur = conn.cursor()
  
  cur.execute("SET LOCAL statement_timeout = '15s';")

  print('Clearing old data from database...')
  cur.execute('DELETE FROM streams;')
  cur.execute('DELETE FROM channels;')
  cur.execute('ALTER SEQUENCE streams_id_seq RESTART WITH 1;')
  cur.execute('ALTER SEQUENCE channels_id_seq RESTART WITH 1;')

  print('Saving streams to database...')
  psycopg2.extras.execute_values(cur, insert_channels_query, channels, insert_channels_template, 1000)
  psycopg2.extras.execute_values(cur, insert_streams_query, streams, insert_streams_template, 1000)

  conn.commit()

  cur.close()
  conn.close()

  print(f'Successfully updated streams/channels at {datetime.now()}')