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
    user: 'mentions_insert',
    host: 'localhost',
    database: 'stock_scraper',
    password: 'Ins3rt1on!',
    port: '5432'});

//sets our view engine to be able to render html
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

//handles requests for the index page
app.get('/', function (req, res) {
    res.render('index', {});
  });

app.get('/*', function(req, res){
  console.log(req.url.replace("/",""));
  res.render(req.url.replace("/",""));
});

app.listen(port, () => console.log(`Listening on port ${port}...`));