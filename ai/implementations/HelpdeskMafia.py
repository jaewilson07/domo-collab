#pip install domolibrary
#pip install agent_mafia

import os
import asyncio
import re

from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

import domolibrary.client.DomoAuth as dmda
import agent_mafia.routes.domo as domo_routes


def remove_slack_user_mentions(text):
    """
    Removes Slack user mentions (e.g., <@U08HGSAP9K9>) from a text string.

    Args:
        text (str): The input text containing potential Slack user mentions.

    Returns:
        str: The text with Slack user mentions removed.
    """
    pattern = r"<@U[A-Z0-9]+>"

    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text
  
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]

async_slack_app = AsyncSlackApp(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)

domo_auth = dmda.DomoTokenAuth(
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    domo_instance=os.environ["DOMO_INSTANCE"],
)

async def trigger_domo_llms_workflow(
    question,
    channel_id,
    message_id,
    user_id,
    debug_api: bool = False,
    slack_bot_token: str = None,
):
    domo_starting_block = "Start HelpDeskMafia"
    domo_model_id = "48707704-213c-4c82-8a7d-69505b50a8de"
    domo_model_version_id = "1.0.9"

    execution_params = {
        "question": question,
        "channel_id": channel_id,
        "message_id": message_id,
        "user_id": user_id,
        "slack_token": slack_bot_token or SLACK_BOT_TOKEN,
    }

    return await domo_routes.trigger_workflow(
        auth=domo_auth,
        starting_tile=domo_starting_block,
        model_id=domo_model_id,
        version_id=domo_model_version_id,
        execution_parameters=execution_params,
        debug_api=debug_api,
    )


@async_slack_app.event("app_mention")  # Listen for app mentions
async def handle_app_mention(event, say, debug_api:bool = False):
    """Handles app mentions and responds with a random yes/no."""

    message_id = event["ts"]
    user_id = event["user"]

    channel_id = event["channel"]
    question = event["text"]
    clean_question = remove_slack_user_mentions(question)

    said = await say(
        f'<@{user_id}> asked: "{clean_question}"\nGive me a sec to think about it.  But in the meantime, have you tried googling it?',
        thread_ts=message_id,
    )  # Send the response back to Slack

    await trigger_domo_llms_workflow(
        question=clean_question,
        channel_id=channel_id,
        message_id=said["ts"],
        user_id=user_id,
        debug_api=debug_api,
    )


async def main():
    handler = AsyncSocketModeHandler(async_slack_app, SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
