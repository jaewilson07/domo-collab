const createDoc = () => {
    // write a comment to AppDB
    console.log('creating comment');
    const time = Date.now();
    const comment = `This is a comment written at ${time}`;

    const document = { 
        "content": {
            "comment": comment
        }
    }

    domo.post(`/domo/datastores/v1/collections/CommentsTable/documents/`, document)
    .then(data => console.log(data));

}