

var query = new Query();

//Available globals
var domo = window.domo; // For more on domo.js: https://developer.domo.com/docs/dev-studio-guides/domo-js#domo.get
var datasets = window.datasets;
var $ = window.jQuery;
var header_div = document.getElementById('header_div');
var object_container = document.getElementById('object_container');

// Setup collection service

domo.get(query.query(datasets[0])).then(updateBackground);
var user_name = domo.env.userName;
header_div.innerHTML += user_name;

function updateBackground(theData) {
    object_container.data = theData[0]["video url"];

};