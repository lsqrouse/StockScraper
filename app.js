const express = require('express');
const path = require('path');
const html = require('html');
const fs = require('fs');
const pg = require('pg');
const Alpaca = require('@alpacahq/alpaca-trade-api')
const dateFns = require('date-fns');
const e = require('express');
const format = 'yyyy-MM-dd'
const date = dateFns.format(new Date(), format)


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

//connects to alpaca which allows us to get stock data
const alpaca = new Alpaca({
  keyId: "PKJPX0IF1DLG6SWEL6IA",
  secretKey: "AcZgy8G23yhDMbOVO2QRhnvnMHc32Vf3oGZko6v2",
  paper: true,
  usePolygon: false
})


//sets our view engine to be able to render html
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use(express.static(__dirname + '/public'));

//handles requests for the index page
app.get('/', function (req, res) {
    db_client.query("SELECT ticker, SUM(mentions) as mentions, SUM(sentiment) as sentiment FROM mentions_nyse GROUP BY ticker ORDER BY mentions desc LIMIT 10", (err, ment_res) => {
      db_client.query("SELECT ticker, SUM(mentions) as mentions, SUM(sentiment) as sentiment FROM mentions_nyse GROUP BY ticker ORDER BY sentiment desc LIMIT 10", (err, sent_res) => {
        if (err) {
          console.log(err);
        }
        let today = new Date()
        const to = dateFns.format(today, format)
        today.setMonth(today.getMonth() - 3)
        const from = dateFns.format(today, format)
        let stock = 'SNP'

        alpaca.getAggregates(stock, 'day', from, to).then(data => {
          //console.table(data.results);
          const results = data.results.map(res => res.startEpochTime = dateFns.format(res.startEpochTime, format))
          res.render('index.ejs', {
            ment_rows: ment_res.rows,
            sent_rows: sent_res.rows,
            rows: data.results
          });
        }).catch((err) => {
          console.log(err);
        })

      });
    });
});

app.get('/alltickers', function (req, res) {
  var order;
  if (req.query.sortBy) {
    console.log(req.query)
    order = req.query.sortBy;
  } else {
    order = "mentions";
  }

  var search;
  if (req.query.searchText) {
    search = "WHERE ticker LIKE '%" + req.query.searchText + "%'";
  } else {
    search = "";
  }
  console.log("Query was");
  console.log("SELECT ticker, SUM(mentions) as mentions, SUM(sentiment) as sentiment FROM mentions_nyse " + search + " GROUP BY ticker ORDER BY " + order + " desc")


  db_client.query("SELECT ticker, SUM(mentions) as mentions, SUM(sentiment) as sentiment FROM mentions_nyse " + search + " GROUP BY ticker ORDER BY " + order + " desc", (err, all_res) => {
    if (err) {
      console.log(err)
    }
    res.render("alltickers.ejs", {
      all_rows: all_res.rows
    });

  });
});

app.get('/about', function (req, res) {
  res.render("about.ejs");
});

//gets the individual ticker data
app.get('/[A-Z]{1,4}', function (req, res) {
  //gets the ticker
  var ticker = req.url.substring(1);

  //queries the db for the grouping and then just raw data
  db_client.query("SELECT ticker, SUM(mentions) as mentions, SUM(sentiment) as sentiment FROM mentions_nyse WHERE ticker = '" + ticker + "' GROUP BY ticker ", (err, group_res) => {
    db_client.query("SELECT * FROM mentions_nyse WHERE ticker = '" + ticker + "'", (err, allrows_res) => {
      if (err) {
        console.log(err)
        res.render("error.ejs");
      } else {
        //queries alpaca to get the stocks data
        let today = new Date()
        const to = dateFns.format(today, format)
        today.setMonth(today.getMonth() - 3)
        const from = dateFns.format(today, format)

        alpaca.getAggregates(ticker, 'day', from, to).then(data => {
          console.table(data.results);
          const results = data.results.map(res => res.startEpochTime = dateFns.format(res.startEpochTime, format))
          res.render('ticker.ejs', {
            ticker: ticker,
            total_mentions: group_res.rows[0].mentions,
            total_sentiment: group_res.rows[0].sentiment,
            rows: allrows_res.rows,
            alpaca_rows: data.results
          });
        }).catch((err) => {
          console.log(err);
        })
      }
    });
  });
});

//gets the individual ticker data
app.post('/[A-Z]{1,4}_data', function (req, res) {
  //gets the ticker
  var ticker = req.url.substring(1);
  console.log("ticker is");
  console.log(ticker)
});

app.get('/*', function(req, res){
  console.log("File Not Found for:")
  console.log(req.url)
  res.render("fnf.ejs");
});

app.listen(port, () => console.log(`Listening on port ${port}...`));