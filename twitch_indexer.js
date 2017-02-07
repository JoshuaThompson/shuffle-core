'use strict';

const axios = require('axios');
const dbinfo = require('./db');

const db = dbinfo.db;
const pgp = dbinfo.pgp;

const timeout = ms => new Promise(res => setTimeout(res, ms));

const channel_column_set = new pgp.helpers.ColumnSet(['channel_id', 
                                        'mature', 
                                        'status', 
                                        'broadcaster_language', 
                                        'display_name', 
                                        'game', 
                                        'language', 
                                        'name', 
                                        'created_at', 
                                        'updated_at', 
                                        'partner', 
                                        'logo',
                                        'video_banner', 
                                        'profile_banner', 
                                        'profile_banner_background_color', 
                                        'url', 
                                        'views', 
                                        'followers'], 
                                        {table: 'channels'});

const streams_column_set = new pgp.helpers.ColumnSet(['stream_id',
                                        'channel_id',
                                        'game',
                                        'viewers',
                                        'video_height',
                                        'average_fps',
                                        'delay',
                                        'created_at',
                                        'is_playlist',
                                        'preview',
                                        'online'],
                                        {table: 'streams'});

const twitch_axios = axios.create({
  baseURL: 'https://api.twitch.tv/kraken/',
  headers: {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'CLIENT-ID': process.env.TWITCH_CLIENTID
  }
});

async function get_streams() {
  try {
    let streams = [];
    const stream_summary = await twitch_axios.get(`/streams/summary`);
    let requests_required = Math.ceil(stream_summary.data.channels / 100);
    
    if (stream_summary.data.channels % 100 !== 0) {
      requests_required += 1;
    }

    for (let i = 0; i < requests_required; i++) {
      const next_streams = await twitch_axios.get(`/streams?limit=100&offset=${i*100}`);
      streams = streams.concat(next_streams.data.streams);
      await timeout(1000);
    }

    return streams;
  } catch (err) {
    return [];
  }
}

async function index_streams() {
  const streams = await get_streams();
  
  const channels = streams.map((stream) => {
    const channel = stream.channel;
    channel.channel_id = channel._id;

    return channel;
  });

  let query = pgp.helpers.insert(channels, channel_column_set);
  query += ` ON CONFLICT (channel_id) DO UPDATE SET 
              mature = EXCLUDED.mature,
              status = EXCLUDED.status,
              broadcaster_language =  EXCLUDED.broadcaster_language,
              display_name = EXCLUDED.display_name,
              game = EXCLUDED.game,
              language = EXCLUDED.language,
              name = EXCLUDED.name,
              created_at = EXCLUDED.created_at,
              updated_at = EXCLUDED.updated_at,
              partner = EXCLUDED.partner,
              logo = EXCLUDED.logo,
              video_banner = EXCLUDED.video_banner,
              profile_banner = EXCLUDED.profile_banner,
              url = EXCLUDED.url,
              views = EXCLUDED.views,
              followers = EXCLUDED.followers`;

  await db.none(query);

  await db.none('UPDATE streams SET online = false');

  const streams_to_upsert = streams.map((stream) => {
    stream.stream_id = stream._id;
    stream.channel_id = stream.channel._id;
    stream.online = true;
    delete stream.channel;

    return stream;
  });

  query = pgp.helpers.insert(streams_to_upsert, streams_column_set);
  query += ` ON CONFLICT (stream_id, channel_id, created_at) DO UPDATE SET
              game = EXCLUDED.game,
              viewers = EXCLUDED.viewers,
              video_height = EXCLUDED.video_height,
              average_fps = EXCLUDED.average_fps,
              delay = EXCLUDED.delay,
              is_playlist = EXCLUDED.is_playlist,
              preview = EXCLUDED.preview,
              online = EXCLUDED.online`;

  return await db.none(query);
}

db.task(index_streams)
  .then((results) => {
    console.log('success!');
    process.exit(-1);
  })
  .catch((err) => {
    console.log(err);
    process.exit(-1);
  });