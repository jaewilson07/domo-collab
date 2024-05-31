
window.onload = function(){ 
  

document.getElementById("bt").onclick = function() {myFunction()};


const startFunction = (functionAlias, inputParameters = {}) => {
  domo.post(`/domo/codeengine/v2/packages/${functionAlias}`, inputParameters
  ).then(data => {
      console.log(data);
      result_text = "<b>Total number of pages : "+data["response"]["totalPageCount"]+"</b><br>";
    
      data["response"]["pageAdminSummaries"].forEach(function (item) {
        result_text += "<a onclick='domo.navigate(\"https://"+inputParameters.instance+".domo.com/page/"+item["pageId"]+"\", true); 'target='_blank' href='#'>"+item["pageTitle"]+"</a>"+"<br>";

      });
      document.getElementById('divResult').innerHTML = result_text;
  }).catch(err => {
      console.log(err);
      document.getElementById('divResult').innerText = '__'+err;
  })
};

function myFunction() {
    document.getElementById("divResult").innerHTML = "Code engine is working! please wait";
    var instance = document.getElementById('instance').value
    var account  = document.getElementById('account').value
 
  
    startFunction("getPages", {"auth": account,"instance": instance} );
  }
  
};
  

