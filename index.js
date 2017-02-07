'use strict';

require('dotenv').config();
const pm2 = require('pm2');

pm2.connect((err) => {
  if(err) {
    console.error(err);
    process.exit(2);
  }

  pm2.start({
    script: 'app.js',
    exec_mode: 'cluster',
    instances: 1
  }, function(err, apps) {
    pm2.disconnect();
    if (err) throw err;
  });

  pm2.start({
    script: 'twitch_indexer.js',
    exec_mode: 'cluster',
    instances: 1,
    interpreter_args: '--harmony-async-await'
  }, (err, apps) => {
    pm2.disconnect();
    if (err) throw err;
  });
});