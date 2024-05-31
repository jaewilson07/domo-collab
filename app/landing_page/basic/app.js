//Available globals
var domo = window.domo; // For more on domo.js: https://developer.domo.com/docs/dev-studio-guides/domo-js#domo.get
var datasets = window.datasets;

// env has information about the environment / user
let whoami = domo.env.userId;
console.log(domo.env);
//whoami = 612085674 //spoof another user

// create configurable query
SQL_activityLog =
  "select `SOURCE_ID` as user_id, `Object_ID` as page_id, count(*) as viewCount FROM dataset1 where `Action` = 'VIEWED' and `Object_Type` = 'PAGE' and `SOURCE_ID` = '" +
  whoami +
  "'  GROUP BY `Object_ID`, `Source_ID` ORDER BY count(*)";

function mergeRowsColumns(rows, columns) {
  return rows.map((row) => {
    let obj = {};
    row.forEach((item, index) => {
      obj[columns[index]] = item;
    });
    return obj;
  });
}

const get_data = async (sql_str, dataset_alias) => {
  api_str = `/sql/v1/${dataset_alias}`;
  console.log(api_str, sql_str);

  res = await domo.post(api_str, sql_str, { contentType: "text/plain" });

  return mergeRowsColumns((rows = res.rows), (columns = res.columns));
};

// write a function for painting links
const paint_links = (links) => {
  return links.reduce((accum, link) => {
    accum += `<div >${link.page_id}<div>`;
    return accum;
  }, "");
};

const main = async () => {
  const whodiv = document.getElementById("whoami");
  whodiv.innerHTML = whoami;

  const mydiv = document.getElementById("myDiv");
  const data = await get_data((sql_str = SQL_activityLog), "dataset1");
  mydiv.innerHTML = paint_links(data.slice(0, 5));
};

main();
