const codeengine = require('codeengine');

/**
 * Create a new vectorDB index
 *
 * @param {text} indexId - the name of the vector index
 * @returns {object} page - the new page
 */
async function createVectorDBIndex(indexId) {
  try {
    const url = '/api/recall/v1/indexes';
    return await codeengine.sendRequest('post', url, {
      "indexId": indexId,
      "embeddingModel": "domo.domo_ai.domo-embed-text-multilingual-v1:cohere"
  });
  } catch (err) {
    throw new Error(
      `Could not create the vectorDB index`
    );
  }
}


async function getVectorDBIndex() {
  try {
    const url = '/api/recall/v1/indexes';
    return await codeengine.sendRequest('get', url);
  } catch (err) {
    throw new Error(
      `Could not get the vectorDB index`
    );
  }
}

/**
 * Upsert nodes into a vector index
 *
 * @param {text} indexId - the name of the vector index to upsert nodes into
 * @param {array} nodeArray - an array of nodes which have the following structure. [ { "content": string, "type": string, "groupId": string } ]
 * content includes a string, type can be "TEXT" or "IMAGE" and the groupId (optional) is a way to group nodes together by an identifier.
 * @returns {object} response - the ids of upserted nodes
 */
async function upsertNodes(indexId, nodeArray) {
  try {
    const url = `/api/recall/v1/indexes/${indexId}/upsert`;
    return await codeengine.sendRequest('post', url, {
      "nodes": nodeArray
  });
  } catch (err) {
    throw new Error(
      `Could not upsert nodes`
    );
  }
}

/**
 * Create a new vectorDB index
 *
 * [TODO Docs]
 */
async function queryIndex(indexId, input, topK) {
  try {
    const url = `/api/recall/v1/indexes/${indexId}/query`;
    return await codeengine.sendRequest('post', url, {
      "input": input,
      "topK": topK
  });
  } catch (err) {
    throw new Error(
      `Could not query index`
    );
  }
}



//write function  to build nodes from dataset KB
//Upsert nodes

const DATASOURCE = {
  v2: 'api/data/v2/datasources',
  v3: 'api/data/v3/datasources',
};
const DATASET_URL = `${DATASOURCE.v3}/:id`;
const UPLOADS_URL = `${DATASET_URL}/uploads`;
const UPLOADS_PARTS_URL = `${UPLOADS_URL}/:uploadId/parts/1`;
const UPLOADS_COMMIT_URL = `${UPLOADS_URL}/:uploadId/commit`;
const QUERY_URL = 'api/query/v1/execute/:id';

// Helpers
const DATASET_PARTS = [
  'core',
  'permission',
  'status',
  'pdp',
  'rowcolcount',
  'certification',
  'functions',
];

/**
 * Query for data matching the provided SQL statement
 *
 * @param {Dataset} dataset - The DataSet
 * @param {text} sql - The SQL statement to execute
 * @returns {{ rows: text[], data: any[][]}} - The result of the query
 */
async function queryWithSql(dataset, sql) {
  const convertResponseToList = ({rows, columns}) => {
    return rows.map(row => {
      return row.reduce((acc, curr, index) => {
        acc[columns[index]] = curr;
        return acc;
      }, {});
    });
  };

  try {
    const url = QUERY_URL.replace(':id', dataset);
    const body = {sql};
    const response = await codeengine.sendRequest('post', url, body);
    return convertResponseToList(response);
  } catch (error) {
    console.error(error);
  }
}
async function getNodesfromDataset(dataset, sql) {
  const rows_ls = await queryWithSql(dataset, sql)
  try {
    var nodes_ls = []
    rows_ls.forEach((row) => {
      nodes_ls.push({content : row.article, type:'TEXT',properties:{"url": row.url, "title": row.Title}});

    });
    return nodes_ls
    
  } catch (error) {
    console.error(error);
  }

  }

async function setupNodesfromDataset (indexId, dataset, sql) {

  var nodeArray = await getNodesfromDataset(dataset, sql)
  return await upsertNodes(indexId, nodeArray)
}






