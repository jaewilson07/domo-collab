// Some DataSets are massive and will bring any web browser to its knees if you
// try to load the entire thing. To keep your app performing optimally, take
// advantage of filtering, aggregations, and group by's to bring down just the
// data your app needs. Do not include all columns in your data mapping file,
// just the ones you need.
//
// For additional documentation on how you can query your data, please refer to
// https://developer.domo.com/docs/dev-studio/dev-studio-data

async function loadData() {
  const returns = await domo.get("/data/v1/returns?limit=100");
  const commentDocuments = await domo.get(
    "/domo/datastores/v1/collections/comments/documents"
  );

  const returnsElement = document.querySelector("#returns");
  returns.forEach((item, index) => {
    const row = document.createElement("li");
    row.setAttribute("class", "list-group-item"); // bootstrap class name
    row.innerHTML = generateRow(item, index, commentDocuments);
    returnsElement.appendChild(row);
  });
}

function generateRow(item, index, commentDocuments) {
  const filteredComments = commentDocuments.filter(
    (commentDocument) => commentDocument.content.id == index
  );

  return `
      <!-- Row of Return Data -->
      <div class="itemContainer">
          <div>${item.storeNumber}</div>
          <div>${item.customerName}</div>
          <div>${item.itemReturned}<div class="sku">#${item.SKU}</div></div>
          <div>${item.reasonForReturn}</div>
          <div>
            <span class="badge badge-light">${filteredComments.length}</span>
            <button class="btn btn-link" onClick="modifyCommentsContainer(${index}, 'commentsContainer')">Add Comment</button>
          </div>
      </div>

      <!-- Comments for each return  -->
      <div class="commentsContainer hidden" id="commentsContainer-${index}">
        <div class="commentHeader">
          <label>Comments</label>
          <button class="btn btn-link" onClick="modifyCommentsContainer(${index}, 'commentsContainer hidden')">Close</button>
        </div>
        <div id="comments-${index}">
          ${filteredComments
            .map((commentDocument) => {
              return `
                    ${generateCommentElement(commentDocument)}
                  `;
            })
            .join("")}
        </div>
        <div class="addCommentContainer">
          <textarea id="comment-${index}" placeholder="Add comment"></textarea>
          <button class="btn btn-info" onClick="submitComment(${index})">Submit</button>
        </div>
        <div>
          📎 <input type="file" id="attachment-${index}" class="attachment">
        </div>
      </div>      
     `;
}

function generateCommentElement(commentDocument) {
  return `
      <div class="commentDocument">
        <img src="/domo/avatars/v2/USER/${
          commentDocument.content.user
        }?size=50&defaultForeground=fff&defaultBackground=000&defaultText=D" alt="User Avatar" />
        <text>${commentDocument.content.postBody}</text>
      </div>
      <div>
        ${
          commentDocument.content.attachmentName !== undefined
            ? `📎 <a href="${commentDocument.content.attachmentURL}" download>${commentDocument.content.attachmentName}</a>`
            : ""
        }
      </div>
  `;
}

function modifyCommentsContainer(index, className) {
  const commentContainer = document.querySelector(
    `#commentsContainer-${index}`
  );
  commentContainer.setAttribute("class", className);
}

/**
 * For simplicity, we will use the return's index in the array as its unique identifier
 *
 */
async function submitComment(index) {
  const attachment = document.querySelector(`#attachment-${index}`);
  const file = attachment.files[0];
  const fileName = attachment.value.replace(/^.*\\/, "");
  const postBody = document.querySelector(`#comment-${index}`);
  let commentDocument = {
    content: {
      id: index,
      user: domo.env.userId,
      postBody: postBody.value,
    },
  };
  if (file !== undefined) {
    var formData = new FormData();
    formData.append("file", file);
    var postOptions = { contentType: "multipart" };
    const fileResponse = await domo.post(
      `domo/data-files/v1?name=${fileName}`,
      formData,
      postOptions
    );

    commentDocument = {
      content: {
        ...commentDocument.content,
        attachmentName: fileName,
        attachmentURL: `domo/data-files/v1/${fileResponse.dataFileId}`,
      },
    };
  }

  await domo.post(
    "/domo/datastores/v1/collections/comments/documents/",
    commentDocument
  );

  const comments = document.querySelector(`#comments-${index}`);
  const commentElement = document.createElement("div");
  commentElement.innerHTML = generateCommentElement(commentDocument);
  comments.appendChild(commentElement);
  postBody.value = "";
  attachment.value = "";
}

/**
 *  POSSIBLE IMPROVEMENTS
 *  1) Add loading states
 *  2) Create a search bar that filters the list of returns
 *  3) Add branding and logos
 *  4) Add ability to delete comments
 *
 */
