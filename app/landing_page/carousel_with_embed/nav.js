//Available globals
var domo = window.domo;
var datasets = window.datasets;
 
//Form the data query
var fields = ['TileRow', 'TileColumn', 'TileName', 'TileColor', 'Icon', 'MetricType', 'Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6', 'Item7', 'Item8', 'Item9', 'Item10', 'Item11', 'Item12'];
var orderby = ['TileRow', 'TileColumn'];
var query = `/data/v1/${datasets[0]}?fields=${fields.join()}&orderby=${orderby.join()}`;

var randomnotificationnumber = Math.floor(Math.random() * 10);
if(randomnotificationnumber == 0){
	randomnotificationnumber = 1
}

// SVG Icon Library for Tiles (if adding new one, add class="ico" inside svg tag)
// ---------------------------
var icons = {};
icons.Eye = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="30px" height="30px" viewBox="0 0 12 12" enable-background="new 0 0 12 12" id="Слой_1" version="1.1" xml:space="preserve"><g><circle cx="6" cy="6" fill="white" r="1.5"/><path d="M6,2C4,2,2,3,0,6c2,3,4,4,6,4s4-1,6-4C10,3,8,2,6,2z M6,8.5C4.621582,8.5,3.5,7.3789063,3.5,6   S4.621582,3.5,6,3.5S8.5,4.6210938,8.5,6S7.378418,8.5,6,8.5z" fill="white"/></g></svg>';
icons.Contact = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" viewBox="0 0 24 24" fill="none"><path d="M9 9.5V7.5C9 5.84315 10.3431 4.5 12 4.5C13.6569 4.5 15 5.84315 15 7.5V9.5C15 10.6104 14.3967 11.5799 13.5 12.0987V13.323C13.5 13.7319 13.749 14.0996 14.1286 14.2514L16.1788 15.0715C17.5807 15.6323 18.5 16.9901 18.5 18.5H5.5C5.5 16.9901 6.41927 15.6323 7.82119 15.0715L9.87139 14.2514C10.251 14.0996 10.5 13.7319 10.5 13.323V12.0987C9.6033 11.5799 9 10.6104 9 9.5Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
icons.Favorite = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" fill="#000000" width="30px" height="30px" viewBox="0 0 1000 1000"><path d="M476 801l-181 95q-18 10-36.5 4.5T229 879t-7-36l34-202q2-12-1.5-24T242 596L95 453q-15-14-15.5-33.5T91 385t32-18l203-30q12-2 22-9t16-18l90-184q10-18 28-25t36 0 28 25l90 184q6 11 16 18t22 9l203 30q20 3 32 18t11.5 34.5T905 453L758 596q-8 9-12 21t-2 24l34 202q4 20-7 36t-29.5 21.5T705 896l-181-95q-11-6-24-6t-24 6z"/></svg>';
icons.Goal = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" version="1.1" id="Capa_1" width="30px" height="30px" viewBox="0 0 412 412" xml:space="preserve"><g><g><g><path d="M206,0C92.411,0,0,92.411,0,206s92.411,206,206,206s206-92.411,206-206S319.589,0,206,0z M206,380     c-95.944,0-174-78.057-174-174c0-95.944,78.056-174,174-174c95.944,0,174,78.056,174,174C380,301.943,301.944,380,206,380z"/><path d="M206,80c-69.477,0-126,56.523-126,126c0,69.477,56.523,126,126,126c23.45,0,45.42-6.447,64.243-17.65l-8.818-9.138     c-0.955,2.227-2.335,4.222-4.096,5.92c-3.415,3.298-7.922,5.119-12.684,5.119c-7.452-0.022-14.061-4.458-16.885-11.3     l-2.833-6.866C218.812,299.34,212.482,300,206,300c-51.832,0-94-42.168-94-94s42.168-94,94-94s94,42.168,94,94     c0,7.398-0.862,14.598-2.486,21.508l7.137,3.246c6.743,3.071,10.938,9.835,10.692,17.235     c-0.241,7.331-4.801,13.759-11.632,16.418l8.691,9.008C324.806,253.908,332,230.779,332,206C332,136.523,275.477,80,206,80z"/><path d="M206.836,188.056c2.619,0,5.157,0.549,7.543,1.63l29.5,13.421C242.398,183.473,226.012,168,206,168     c-20.987,0-38,17.013-38,38c0,19.822,15.18,36.092,34.548,37.837l-12.602-30.546c-2.879-6.977-1.229-14.873,4.205-20.114     C197.564,189.878,202.073,188.056,206.836,188.056z"/><path d="M278.439,258.434l21.138-7.991c1.232-0.47,2.065-1.632,2.109-2.951c0.046-1.318-0.711-2.534-1.912-3.082l-90.251-41.06     c-1.223-0.554-2.657-0.307-3.624,0.625c-0.965,0.931-1.264,2.356-0.752,3.597l37.815,91.657c0.503,1.222,1.69,2.021,3.011,2.022     c0.867,0.002,1.681-0.339,2.279-0.917c0.314-0.303,0.57-0.669,0.745-1.088l8.741-20.84l32.472,33.649     c1.252,1.3,3.321,1.336,4.621,0.082l15.995-15.435c1.299-1.254,1.336-3.323,0.081-4.621L278.439,258.434z"/></g></g></g></svg>';
icons.Community = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" version="1.1" id="Layer_1" width="30px" height="30px" viewBox="0 0 256 240" enable-background="new 0 0 256 240" xml:space="preserve"><path d="M127.826,39.584c10.308,0,18.7-8.392,18.7-18.7s-8.392-18.7-18.7-18.7s-18.7,8.392-18.7,18.7S117.518,39.584,127.826,39.584  z M26.21,39.584c-10.308,0-18.7-8.392-18.7-18.7s8.392-18.7,18.7-18.7s18.7,8.392,18.7,18.7S36.518,39.584,26.21,39.584z   M229.79,39.584c10.308,0,18.7-8.392,18.7-18.7s-8.392-18.7-18.7-18.7c-10.308,0-18.7,8.392-18.7,18.7S219.482,39.584,229.79,39.584  z M253.966,130.048c0,3.167-4.598,95.372-4.598,95.372c0,6.998-5.398,12.396-12.396,12.396c-6.998,0-12.396-5.398-12.396-12.396  c0,0-8.617-95.972-10.995-131.806l-19.741,23.724c-1.694,2.035-4.194,3.192-6.808,3.192c-0.339,0-0.68-0.019-1.021-0.059  c-2.972-0.345-5.569-2.165-6.905-4.842l-23.665-47.388v156.056c0,7.435-5.504,13.517-12.359,13.517  c-6.855,0-12.359-6.082-12.359-13.517V138.85c0-1.352-1.159-2.511-2.511-2.511c-1.352,0-2.511,1.159-2.511,2.511v85.448  c0,7.435-5.504,13.517-12.359,13.517c-6.855,0-12.359-6.082-12.359-13.517V67.387l-24.092,48.243  c-1.336,2.677-3.933,4.497-6.904,4.842c-0.341,0.039-0.682,0.059-1.021,0.059c-2.613,0-5.114-1.157-6.808-3.192L42.419,93.614  c-2.378,35.834-10.995,131.805-10.995,131.805c0,6.998-5.398,12.396-12.396,12.396s-12.396-5.398-12.396-12.396  c0,0-4.598-92.204-4.598-95.371c0,0-0.034-71.339-0.034-71.57c0-7.97,6.091-13.605,13.605-13.605c5.692,0,10.073,1.924,14.649,6.516  c0.131,0.132,36.851,44.193,36.851,44.193c-0.062-0.074,16.261-33.095,19.507-39.002c4.344-7.903,10.612-11.71,18.6-11.765  c0.019,0,0.041-0.005,0.059-0.005c0,0,45.073,0.012,45.348,0.022c8.069-0.022,14.396,3.788,18.772,11.752  c0.091,0.157,19.506,38.998,19.506,38.998s36.714-44.061,36.854-44.196c4.473-4.689,9.55-6.513,14.645-6.513  c7.514,0,13.605,6.091,13.605,13.605C254,61.212,253.966,130.048,253.966,130.048z"/></svg>';
icons.Apps = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" fill="#000000" width="15px" height="15px" viewBox="0 0 32 32"><g id="Group_11" data-name="Group 11" transform="translate(-165.998 -465.695)"><rect id="Rectangle_50" data-name="Rectangle 50" width="8" height="8" transform="translate(165.998 465.695)"/><rect id="Rectangle_51" data-name="Rectangle 51" width="8" height="8" transform="translate(189.998 465.695)"/><rect id="Rectangle_52" data-name="Rectangle 52" width="8" height="8" transform="translate(177.999 465.695)"/><rect id="Rectangle_53" data-name="Rectangle 53" width="8" height="8" transform="translate(165.998 477.695)"/><rect id="Rectangle_54" data-name="Rectangle 54" width="8" height="8" transform="translate(189.998 477.695)"/><rect id="Rectangle_55" data-name="Rectangle 55" width="8" height="8" transform="translate(177.999 477.695)"/><rect id="Rectangle_56" data-name="Rectangle 56" width="8" height="8" transform="translate(165.998 489.695)"/><rect id="Rectangle_57" data-name="Rectangle 57" width="8" height="8" transform="translate(189.998 489.695)"/><rect id="Rectangle_58" data-name="Rectangle 58" width="8" height="8" transform="translate(177.999 489.695)"/></g></svg>';
icons.Groups = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" fill="#000000" width="30px" height="30px" viewBox="0 0 52 52" enable-background="new 0 0 52 52" xml:space="preserve"><g><path d="M15.9,28c-1.4-2.1-2.1-4.5-2.1-7.2c0-4.6,1.9-8.4,4.9-10.7c-1-1.8-3-3.1-5.6-3.1c-4.4,0-6.9,3.6-6.9,7.7   c0,2.2,0.7,4.1,2.2,5.4c0.8,0.8,1.5,1.8,1.5,2.8S9.5,24.9,7,26c-3.6,1.6-6.9,3.8-7,7.1C0.1,35.3,1.5,37,3.6,37h3.3   c0.5,0,1-0.3,1.3-0.8c1.6-2.9,4.6-4.7,7.1-6C16.2,29.8,16.4,28.7,15.9,28z"/><path d="M45.1,26c-2.5-1.1-2.9-2-2.9-3.1s0.7-2.1,1.5-2.8c1.5-1.4,2.2-3.2,2.2-5.4c0-4.1-2.4-7.7-6.9-7.7   c-2.6,0-4.6,1.3-5.7,3.1c3,2.3,4.9,6.1,4.9,10.7c0,2.7-0.7,5.1-2.1,7.2c-0.5,0.8-0.2,1.8,0.6,2.2c2.5,1.2,5.5,3.1,7.1,6   c0.3,0.5,0.8,0.8,1.3,0.8h3.3c2.1,0,3.5-1.7,3.5-3.9C52,29.8,48.7,27.6,45.1,26z"/><path d="M32.7,33.3c-2.7-1.2-3.2-2.3-3.2-3.4c0-1.2,0.8-2.3,1.7-3.1c1.6-1.5,2.5-3.6,2.5-6c0-4.5-2.7-8.4-7.6-8.4   s-7.6,3.9-7.6,8.4c0,2.4,0.9,4.5,2.5,6c0.9,0.9,1.7,2,1.7,3.1c0,1.2-0.4,2.2-3.2,3.4c-4,1.7-7.8,3.6-7.9,7.2c0,2.4,1.8,4.4,4.1,4.4   h10.4h10.4c2.3,0,4.1-2,4.1-4.4C40.5,37,36.7,35.1,32.7,33.3z"/></g></svg>';
icons.ContactUs = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" viewBox="0 0 24 24" fill="white"><path fill-rule="evenodd" clip-rule="evenodd" d="M16.1267 22.1995C16.7081 22.5979 17.4463 23.0228 18.3121 23.3511C19.9904 23.9874 21.244 24.0245 21.8236 23.9917C23.1167 23.9184 23.2907 23.0987 22.5972 22.0816C21.8054 20.9202 21.0425 19.6077 21.1179 18.1551C22.306 16.3983 23 14.2788 23 12C23 5.92487 18.0751 1 12 1C5.92488 1 1.00001 5.92487 1.00001 12C1.00001 18.0751 5.92488 23 12 23C13.4578 23 14.8513 22.7159 16.1267 22.1995ZM12 3C7.02945 3 3.00001 7.02944 3.00001 12C3.00001 16.9706 7.02945 21 12 21C13.3697 21 14.6654 20.6947 15.825 20.1494C16.1635 19.9902 16.5626 20.0332 16.8594 20.261C17.3824 20.6624 18.1239 21.1407 19.0212 21.481C19.4111 21.6288 19.7674 21.7356 20.0856 21.8123C19.7533 21.2051 19.4167 20.4818 19.2616 19.8011C19.1018 19.0998 18.8622 17.8782 19.3281 17.2262C20.3808 15.7531 21 13.9503 21 12C21 7.02944 16.9706 3 12 3ZM12 14C9.76094 14 8.4671 15.169 8.10992 16.3009C7.94372 16.8276 7.38202 17.1198 6.85534 16.9536C6.32866 16.7874 6.03643 16.2257 6.20263 15.6991C6.61242 14.4005 7.59994 13.2939 8.9933 12.6382C8.37493 11.934 8.00001 11.0108 8.00001 10C8.00001 7.79086 9.79087 6 12 6C14.2092 6 16 7.79086 16 10C16 11.0108 15.6251 11.934 15.0067 12.6382C16.4001 13.2939 17.3876 14.4005 17.7974 15.6991C17.9636 16.2257 17.6714 16.7874 17.1447 16.9536C16.618 17.1198 16.0563 16.8276 15.8901 16.3009C15.5329 15.169 14.2391 14 12 14ZM10 10C10 8.89543 10.8954 8 12 8C13.1046 8 14 8.89543 14 10C14 11.1046 13.1046 12 12 12C10.8954 12 10 11.1046 10 10Z" fill="white"/></svg>';
icons.Collections = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" viewBox="0 0 16 16" fill="white"><g fill="white"><path d="M3.05 4.75a.7.7 0 01.7-.7h3.5a.7.7 0 110 1.4h-3.5a.7.7 0 01-.7-.7zM3.75 7.05a.7.7 0 100 1.4h2.5a.7.7 0 100-1.4h-2.5z"/><path fill-rule="evenodd" d="M0 3.25A2.25 2.25 0 012.25 1h6.5c.883 0 1.648.51 2.016 1.25h.984c.698 0 1.3.409 1.582 1h.918c.966 0 1.75.784 1.75 1.75v6a1.75 1.75 0 01-1.75 1.75h-.918c-.281.591-.884 1-1.582 1h-.984A2.25 2.25 0 018.75 15h-6.5A2.25 2.25 0 010 12.75v-9.5zm13.5 8h.75a.25.25 0 00.25-.25V5a.25.25 0 00-.25-.25h-.75v6.5zm-2.5 1v-8.5h.75A.25.25 0 0112 4v8a.25.25 0 01-.25.25H11zM2.25 2.5a.75.75 0 00-.75.75v9.5c0 .414.336.75.75.75h6.5a.75.75 0 00.75-.75v-9.5a.75.75 0 00-.75-.75h-6.5z" clip-rule="evenodd"/></g></svg>';
icons.Fire = '<svg class="ico" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="svg2" sodipodi:docname="fire.svg" inkscape:version="0.48.4 r9939" width="800px" height="800px" viewBox="0 0 1200 1200" enable-background="new 0 0 1200 1200" xml:space="preserve"><sodipodi:namedview inkscape:cy="580.6024" inkscape:cx="312.39671" inkscape:zoom="0.37249375" showgrid="false" id="namedview30" guidetolerance="10" gridtolerance="10" objecttolerance="10" borderopacity="1" bordercolor="#666666" pagecolor="#ffffff" inkscape:current-layer="svg2" inkscape:window-maximized="1" inkscape:window-y="24" inkscape:window-height="876" inkscape:window-width="1535" inkscape:pageshadow="2" inkscape:pageopacity="0" inkscape:window-x="65"></sodipodi:namedview><path id="path8046" inkscape:connector-curvature="0" d="M381.64,1200C135.779,1061.434,71.049,930.278,108.057,751.148  c27.321-132.271,116.782-239.886,125.36-371.903c38.215,69.544,54.183,119.691,58.453,192.364  C413.413,422.695,493.731,216.546,498.487,0c0,0,316.575,186.01,337.348,466.98c27.253-57.913,40.972-149.892,13.719-209.504  c81.757,59.615,560.293,588.838-64.818,942.524c117.527-228.838,30.32-537.611-173.739-680.218  c13.628,61.319-10.265,290.021-100.542,390.515c25.014-167.916-23.8-238.918-23.8-238.918s-16.754,94.054-81.758,189.065  C345.537,947.206,304.407,1039.291,381.64,1200L381.64,1200z"/></svg>';
icons.Magic = '<svg class="ico" xmlns="http://www.w3.org/2000/svg" fill="white" width="30px" height="30px" viewBox="0 0 32 32" version="1.1"><title>magic</title><path d="M9.5 9.625l-0.906 2.906-0.875-2.906-2.906-0.906 2.906-0.875 0.875-2.938 0.906 2.938 2.906 0.875zM14.563 8.031l-0.438 1.469-0.5-1.469-1.438-0.469 1.438-0.438 0.5-1.438 0.438 1.438 1.438 0.438zM0.281 24l17.906-17.375c0.125-0.156 0.313-0.25 0.531-0.25 0.281-0.031 0.563 0.063 0.781 0.281 0.094 0.063 0.219 0.188 0.406 0.344 0.344 0.313 0.719 0.688 1 1.063 0.125 0.188 0.188 0.344 0.188 0.5 0.031 0.313-0.063 0.594-0.25 0.781l-17.906 17.438c-0.156 0.156-0.344 0.219-0.563 0.25-0.281 0.031-0.563-0.063-0.781-0.281-0.094-0.094-0.219-0.188-0.406-0.375-0.344-0.281-0.719-0.656-0.969-1.063-0.125-0.188-0.188-0.375-0.219-0.531-0.031-0.313 0.063-0.563 0.281-0.781zM14.656 11.375l1.313 1.344 4.156-4.031-1.313-1.375zM5.938 13.156l-0.406 1.438-0.438-1.438-1.438-0.469 1.438-0.438 0.438-1.469 0.406 1.469 1.5 0.438zM20.5 12.063l0.469 1.469 1.438 0.438-1.438 0.469-0.469 1.438-0.469-1.438-1.438-0.469 1.438-0.438z"/></svg>';
icons.GoalsNotification = '<svg class="not" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="30px" height="30px" viewBox="0 0 20 20" aria-hidden="true" role="img" class="iconify iconify--emojione" preserveAspectRatio="xMidYMid meet"><g><circle cx="10" cy="10" r="10" fill="#d90419"></circle><text x="50%" y="50%" text-anchor="middle" stroke="white" stroke-width=".5px" dy=".33em" font-size=".8em" dx="-0.02em">' + randomnotificationnumber + '</text></g></svg>'
// ---------------------------

//Get the data and chart it
domo.get(query).then(function(data) {  
  // variables
  t = '<tr>';  
  trow = 1;
  tcol = 1;    
  
  data.forEach((item,index) => {    
    m = '<h2 id="nftitle">' + item.TileName + '</h2><div class="wrapper">'
    
    // Builds tile menu items.     Don't show "undefined" if no icon exist for a tile
    if (item.Icon === undefined || item.Icon === null || item.Icon == "") {
    	tIcon = ''
    }else{      
    	tIcon = icons[item.Icon]
    }   
    
    // Builds tile html from datasource
    if (item.TileRow != trow){
       t = t + '</tr><tr>';
      	trow = trow+=1;
    }
    
    // Creates different effects from the different template types (ex: popup netlfix style, flip effect, popup text, etc...)
    switch(item.MetricType){
      case 'Text':
        t = t + '<td class="tcell" name="' + item.TileName + '"><div class="flipbox"><div class="front">' + item.TileName + '<p>' + tIcon + '</div><div class="back"><p>' + item.Item1 + '</p></div></div></td>';
        break;
      case 'Goal':         
        t = t + '<td class="tcell" style="background-color:' + item.TileColor + ';" name="' + item.TileName + '">' + item.TileName + '<p>' + tIcon + '<div class="notbox">' + icons.GoalsNotification + '</div></td>'
        break;        
      default:
        t = t + '<td class="tcell" style="background-color:' + item.TileColor + ';" name="' + item.TileName + '">' + item.TileName + '<p>' + tIcon + '</td>'
    }
    
    // Count out how many resources exist for each tile item
    items = 0;
    for (let i=0; i<=12; i++) {      
      const d = item['Item' + i];          
      if(d && d !== null ){      
       	items=items+1      
      }    
    };
    
    var maxsections=Math.ceil(items/4)        
    var sec = 1;
    var tstart = 1;
    var tend = 1;
    var lc = 1;
    
    // Build out Netflix style scroll behavior (should it have arrows or not depending on how many items need to be shown)
    for (let i=sec; i<=maxsections; i++) {
      switch (sec){
        case 1:
          tstart = maxsections
          if(maxsections == 1){
            tend = 1
          } else{
           	tend = 2
          }
          break;
        case 2:
          tstart = 1
          if(maxsections == 2){
            tend = 1
          } else {
            tend = sec+1
          }
          break;
        case 3:
          tstart = sec-1
          tend = 1
          break;
        default:
      }      
     
      if (item.MetricType != 'Text'){
     // Build out Netflix style items
    	m = m + `<section id="section${sec}">`;
			if (maxsections != 1){      
    			m = m + `<a href="#section${tstart}" class="arrow__btn">‹</a>`;
      }
      // Loop through items and generate HTML in scroll page groupings
      for (let t=0; t<4; t++) {
        if (item["Item" + (lc+t)] !== null){
          if(item["Item" + (lc+t)].includes("iframe")){
            m = m + `<div class="item">${item["Item" + (lc+t)]}></div>`;  
          } else{
            m = m + `<div class="item"><img src="${item["Item" + (lc+t)]}"></div>`;
          }
        }
      }     
      if (maxsections != 1){      
          m = m + `<a href="#section${tend}" class="arrow__btn">›</a></section>`;
      }      
      sec = sec + 1;
      lc = lc + 4;
   	};
    }
    // Add popup html to data for later use
    m = m + '</div>';
  	item.popup = m;  	
  });  
  
  // Populate tiles with data generated from dataset
  t = t + '</tr>'; 
  $('#tb').html(t); 
  
  // Populate Netflix style menu with first menu data options
  $("#pup").html(data[0].popup); 
  
  var hov = 0; // 0 is unlocked, 1 is locked
  
  // Change content below on hover
  $(".tcell").hover(function(){     
    if(hov == 0){
    	var chosen = $(this).attr("name")  	
    	data.forEach((it,index) => {        	
      	if(it['TileName'] == chosen){       
        	 $("#pup").html(it['popup']);    
      	}      
    	});
    }
 	}, function(){  	     
	});
  
  // Lock menu option clicked so the content doesn't change
  $(".tcell").click(function(){    
    if(hov == 0){
      hov = 1;
    } else {
    	hov = 0;
    	var chosen = $(this).attr("name")  	
    	data.forEach((it,index) => {        	
      	if(it['TileName'] == chosen){       
        	 $("#pup").html(it['popup']);    
      	}      
    	}); 
    };    
	});
});