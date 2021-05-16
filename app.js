const express = require('express');
const path = require('path');
const html = require('html');
const fs = require('fs');
const pg = require('pg');

//sets up express so that the html can be served
const app = express();
const port = process.env.PORT || 3000;

//connects to the database, user has all privileges on Tables: test, gamefiles_test
const db_client = new pg.Pool({
    user: 'ruwwlubbxnwdsk',
    host: 'ec2-3-214-3-162.compute-1.amazonaws.com',
    database: 'd3vemptti50aoo',
    password: '979a396bba68831aac97d498fca8ef91cef26c322def58c8e859ca219bbe956f',
    port: '5432',            
    ssl: {
      rejectUnauthorized: false
  }});

//sets our view engine to be able to render html
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

//handles requests for the index page
app.get('/', function (req, res) {
    db_client.query("SELECT ticker, COUNT(*) as mentions FROM mentions_nyse GROUP BY ticker ORDER BY mentions desc LIMIT 10", (err, db_res) => {
      if (err) {
        console.log(err);
      }
      res.render('index.ejs', {
        rows: db_res.rows,
        test: "hi" 
      });
    });
  });

app.get('/*', function(req, res){
  console.log(req.url.replace("/",""));
  res.render(req.url.replace("/",""));
});

app.listen(port, () => console.log(`Listening on port ${port}...`));