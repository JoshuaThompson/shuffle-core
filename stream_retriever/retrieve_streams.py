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
  headers = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': client_id
  }
  r = requests.get(f'https://api.twitch.tv/kraken/streams?limit={limit}&offset={offset}', headers=headers)

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

    time.sleep(1.5)

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

  print('Clearing old data from database...')
  cur.execute('TRUNCATE channels RESTART IDENTITY CASCADE;')

  print('Saving streams to database...')
  psycopg2.extras.execute_values(cur, insert_channels_query, channels, insert_channels_template, 1000)
  psycopg2.extras.execute_values(cur, insert_streams_query, streams, insert_streams_template, 1000)

  conn.commit()

  cur.close()
  conn.close()

  print(f'Successfully updated streams/channels at {datetime.now()}')