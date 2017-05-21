var mongoose = require('mongoose');

var donateSchema = mongoose.Schema({

    contactName: String,
    address: String,
    contactEmail: String,
    contactPhone: String,
    itemName: String,
    itemCategory: String,
    imageLink: String,
    timeStamp: Number,
    daysListed: Number


});

module.exports = mongoose.model('Donate', donateSchema);
