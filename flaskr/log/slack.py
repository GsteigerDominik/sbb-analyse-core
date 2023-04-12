import os

from slack_sdk import WebClient

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def post_msg(msg):
    client.chat_postMessage(channel="#sp-arbeit", text=msg)