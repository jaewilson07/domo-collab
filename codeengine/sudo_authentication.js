const codeEngine = require("codeengine");

async function retrieveAccountCreds(accountName, isAbstract = false) {
  const creds = await codeEngine.getAccount(accountName);
  const properties = creds.properties;

  return !isAbstract ? properties : properties.credentials;
}

async function generateAuthHeader(
  accountName,
  headers = {},
  isAbstract = false
) {
  const creds = await retrieveAccountCreds(accountName, isAbstract);

  return { ...headers, "x-domo-developer-token": creds.domoAccessToken };
}

async function getData(
  method,
  url,
  accountName,
  headers = {},
  params = {},
  bodyJson = null, // codeengine inputs must be typed
  bodyStr = null, // codeengine inputs must be typed
  debugApi = false,
  debugPrn = false
) {
  if (debugApi) {
    console.log({
      url,
      method,
      body: bodyStr || bodyJson,
    });
  }

  let res, data;
  if (!accountName || accountName === null) {
    if (debugPrn) {
      console.log("🌵 - using user_auth");
    }
    url = url.split(".domo.com/")[1];
    res = await codeEngine.sendRequest(method, url, bodyJson || bodyStr);

    return { status: 200, response: res, isSuccess: true };
  } else {
    if (debugPrn) {
      console.log("🌵 - using SUDO_auth");
    }

    headers = await generateAuthHeader(accountName, headers, false);

    res = await codeEngine.axios(url, {
      method,
      headers,
      params,
      data: bodyJson || bodyStr,
    });
    data = await res.data;
  }

  if (res.status >= 400) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return {
    status: res.status,
    response: data,
    isSuccess: res.status < 400,
  };
}

async function sharePage(
  page_id,
  group_id,
  accountName,
  domoInstance,
  debugApi = true,
  debugPrn = false
) {
  const body = {
    resources: [{ type: "page", id: page_id }],
    recipients: [{ type: "group", id: group_id }],
    message: "I thought you might find this page interesting.",
  };

  return await getData(
    "POST",
    `https://${domoInstance}.domo.com/api/content/v1/share`,
    accountName,
    null,
    null,
    body,
    null,
    debugApi,
    debugPrn
  );
}

async function getPages(
  accountName,
  domoInstance,
  debugApi = true,
  debugPrn = false
) {
  const body = {
    includeVirtual: false,
    includePageTitleClause: true,
    orderBy: "parentPageTitlePageTitle",
    pageTitleSearchText: "",
    includeDataAppViews: true,
  };

  const res = await getData(
    "POST",
    `https://${domoInstance}.domo.com/api/content/v1/pages/adminsummary`,
    accountName,
    null,
    null,
    body,
    null,
    debugApi,
    debugPrn
  );

  res.response = res.response.pageAdminSummaries;

  return res;
}
