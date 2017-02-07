const express = require('express');
const dbinfo = require('./db');

const app = express();
const db = dbinfo.db;

app.get('/random', (req, res) => {
  db.query(`SELECT c.name, c.mature, c.partner
            FROM streams s
            INNER JOIN channels c ON s.channel_id = c.channel_id
            WHERE ($1 IS NULL OR c.mature = $1)
              AND ($2 IS NULL OR c.partner = $2)
              AND ($3 IS NULL OR s.viewers >= $3)
              AND ($4 IS NULL OR s.viewers <= $4)
              AND s.online = true
            ORDER BY RANDOM() limit 20`, 
            [true, false, 400, 700])
  .then((results) => {
    res.json(results);
  })
  .catch((err) => {
    res.send(err);
  });
});

app.listen(3000, () => {
  console.log('Example app listening on port 3000!')
})