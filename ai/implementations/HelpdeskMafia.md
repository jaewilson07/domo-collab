How we build Helpdesk Mafia
Scrape domo KBs to produce a Dataset

Python script

* Domo_Kbs dataset



Upload each article to VectorDb with Embeddings and Article Metadata

Community CodeEngine, GitHub

* query dataset  > map over each row > upsert nodes into VectorDB > getNodesfromDataset
* index the database > create vector embeddings for each node



User asks a Question in slack

SlackBot + Domo Workflow

* slackbot "listens" for it's name

Slackbot Answers the Question

SlackBot + Domo Workflow

* Pythontrigger workflow with question, and Slack response parameters - channel_id and message
* Workflowconvert question into an embedding
    * Retrieve K nearest nodes (articles) from VectorDb based on embedding (queryIndex)
    * summarize response using LLM with nodes as context (AI Agent)
    * send response to slack 


QueryIndex
 Instructions Prompt = """
Please identify the top 10 paragraphs from the vectorDB and then attempt to answer the user's question from the source information only.

If you don't get a good answer on the first try, you can expand the search space (number of paragraphs to looks at) and try different more descriptive variations of the users question.

Can you summarize your response to under 200 characters. Please ensure that you include the attempted answer and any relevant urls from the knowledge base that you used to come up with the response.

Please then reply to the slack channel based on the provided channelId and timestamp.
"""
