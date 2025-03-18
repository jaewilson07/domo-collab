# How we build Helpdesk Mafia

## Scrape domo KBs to produce a Dataset
Python script

* [Domo\_Kbs](https://domo-community.domo.com/datasources/04c1574e-c8be-4721-9846-c6ffa491144b/details/overview) dataset

## Upload each article to VectorDb with Embeddings and Article Metadata

[Community CodeEngine](https://domo-community.domo.com/codeengine/9a2f8f7a-b0bd-49d6-8bc7-641453b3df24), [GitHub](https://github.com/jaewilson07/domo-collab/blob/main/codeengine/VectorDB%20Functions.js)

* query dataset \> map over each row \> upsert nodes into VectorDB \> getNodesfromDataset  
* index the database \> create vector embeddings for each node

## User asks a Question in slack

[SlackBot](https://github.com/jaewilson07/domo-collab/blob/main/ai/implementations/HelpdeskMafia.py) \+ Domo [Workflow](https://domo-community.domo.com/workflows/models/48707704-213c-4c82-8a7d-69505b50a8de)

* slackbot "listens" for it's name

## Slackbot Answers the Question

[SlackBot](https://github.com/jaewilson07/domo-collab/blob/main/ai/implementations/HelpdeskMafia.py) \+ Domo [Workflow](https://domo-community.domo.com/workflows/models/48707704-213c-4c82-8a7d-69505b50a8de)

* [Python](https://github.com/jaewilson07/domo-collab/blob/main/ai/implementations/HelpdeskMafia.py#L44) trigger workflow with question, and Slack response parameters \- channel\_id and message  
* [Workflow](https://domo-community.domo.com/workflows/models/48707704-213c-4c82-8a7d-69505b50a8de) convert question into an embedding  
  * Retrieve K nearest nodes (articles) from VectorDb based on embedding (queryIndex)  
  * summarize response using LLM with nodes as context (AI Agent)  
  * send response to slack

### QueryIndex  
FindKB Article // AI Agent Task
```
Instructions Prompt \= """  
Please identify the top 10 paragraphs from the vectorDB and then attempt to answer the user's question from the source information only.  
If you don't get a good answer on the first try, you can expand the search space (number of paragraphs to looks at) and try different more descriptive variations of the users question.  
Can you summarize your response to under 200 characters. Please ensure that you include the attempted answer and any relevant urls from the knowledge base that you used to come up with the response.  
Please then reply to the slack channel based on the provided channelId and timestamp.  
` `
