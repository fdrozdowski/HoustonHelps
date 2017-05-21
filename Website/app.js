const express = require('express');
var app = express();
var bodyParser = require('body-parser');
var mongoose = require("mongoose");
var Donate = require("./donate")
var request = require("request");
var cheerio = require("cheerio");

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
mongoose.connect(process.env.MONGODB_URI || "mongodb://localhost/houstonhelp");

var categories = ["appliances", "toys_games", "furniture", "baby_kid",
"bikes", "electronics", "clothing_accessories", "household", "computers",
"cellphones", "general", "sporting_goods", "free"];
// Clothing
//   - Shirts
//   - Shoes
//

app.use(express.static('public'));

app.set("view engine", "ejs");

app.get('/', (req, res) => {
  res.render("landing")
});

app.get( "/listings" , (req, res) => {
  res.render("listings" , {categories, items: null, donations: null})
});

app.get("/listings/c/:id", (req, res) => {
  var id = req.params.id;
  var foundData = [];
  // items.forEach(function(item) {
  //   if(item.cat === id) {
  //     foundData.push(item)
  //   }
  // })
  Donate.find({itemCategory: id}, (err, allDonations) => {
    if(err) {
      res.send(err)
    } else {

      //http://192.168.3.201:5000/items/furniture
      // Handle Request

      var url = `https://htx-craigslist-api.herokuapp.com/items/${id}`;
      request(url, (error, response, body) => {

        // console.log(body);
        // console.log(body.length)
        // var rData = JSON.stringify(body);
        var info = JSON.parse(body);

        console.log(info);

        info.forEach(function(thing) {
          if(thing.price === null){
            foundData.push(thing);
          }
        })


        res.render("listings", {categories, items: foundData, donations: allDonations})
      });


    }
  })
});

app.get('/donate', (req, res) => {
  res.render('donate', {categories})
});
app.get('/login', (req, res) => {
  res.render('login')
});

app.post("/donate/new", (req, res) => {
  var data = req.body;
  var num = Date.now() / 1000;

  var newData = {
    contactName: data.contactName,
    address: data.address,
    contactEmail: data.cEmail,
    contactPhone: data.cPhone,
    itemName: data.ItemName,
    itemCategory: data.cat,
    daysListed: data.days,
    timeStamp: num,
    imageLink : data.url
  }

  if(data.url === ""){
    newData.imageLink = "http://cumbrianrun.co.uk/wp-content/uploads/2014/02/default-placeholder-300x300.png"
  }

  // console.log(data)
  Donate.create(newData, (err, newDone) => {
    if(err) {
      res.send(err)
    } else {
      res.render("thanks_for_donating", {contactName: data.contactName});
    }
  })

});



var port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log("Server Started on Port 3000")
});
