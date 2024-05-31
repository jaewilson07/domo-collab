

var query = new Query();

//Available globals
var domo = window.domo; // For more on domo.js: https://developer.domo.com/docs/dev-studio-guides/domo-js#domo.get
var datasets = window.datasets;
var $ = window.jQuery;
var header_div = document.getElementById('header_div');
var iframe_container = document.getElementById('iframe_container');

// Setup collection service

domo.get(query.query(datasets[0])).then(updateBackground);
var user_name = domo.env.userName;
header_div.innerHTML += user_name;

//Actually create the table with the data
function updateBackground(theData) {

  iframe_container.src = theData[0]["video url"];

};