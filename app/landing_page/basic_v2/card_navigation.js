// DDX Bricks Wiki - See https://developer.domo.com/docs/ddx-bricks/getting-started-using-ddx-bricks
// for tips on getting started, linking to Domo data and debugging your app

fakeEmail = "ar@test.com";
// fakeEmail = domo.env.userEmail;

//Available globals
var domo = window.domo; // For more on domo.js: https://developer.domo.com/docs/dev-studio-guides/domo-js#domo.get
var datasets = window.datasets;

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

const get_filter_data = async (fakeEmail) => {
  dataset_alias = "dataset0";
  sql_str = `SELECT email, card_id FROM ${dataset_alias} where email = \'${fakeEmail}\'`;

  document.getElementById("whoami").innerText =
    sql_str + "\n" + `your real email is ${domo.env.userEmail}`;

  data = await get_data(sql_str, dataset_alias);

  return data.map((obj) => obj.card_id);
};

const get_actual_data = async (filter_ids) => {
  console.log(filter_ids);
  dataset_alias = "dataset1";
  sql_str = `SELECT card_id, img_url FROM ${dataset_alias}`;

  actual_data = await get_data(sql_str, dataset_alias);

  console.log(actual_data);

  if (!filter_ids) {
    return actual_data;
  }

  return actual_data.filter((obj) => filter_ids.includes(obj.card_id));
};

function generateCardHTML(card_id, img_url) {
  return `
    <div class="col">
      <div class="card">
      <div class = "content">
          <h2 class="card-title">${card_id}</h2>
      </div>
      </div>
    </div>`;
}

const paint_container = (cards) => {
  var container = document.createElement("div");
  container.className = "container";

  var row = document.createElement("div");
  row.className = "row row-cols-1 row-cols-md-5 g-4";

  cards.forEach((card) => {
    var cardHTML = generateCardHTML(card.card_id, card.img_url);
    row.innerHTML += cardHTML;
  });

  container.appendChild(row);

  document.getElementById("app").appendChild(container);
};

const main = async () => {
  filter_ids = await get_filter_data(fakeEmail);

  data = await get_actual_data(filter_ids);
  console.log(data);

  paint_container(data);
};

main();
