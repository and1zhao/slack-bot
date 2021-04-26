import slack
import os
from pathlib import Path as P
from dotenv import load_dotenv
from flask import Flask as F
from slackeventsapi import SlackEventAdapter as SEA

env_path = P('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = F(__name__)
slack_event_adapter = SEA(os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
bot_id = client.api_call("auth.test")['user_id']

restricted_words = os.environ['RESTRICTED_WORDS']
bttv_emotes = os.environ['BTTV_EMOTES']

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id, user_id, text = event.get('channel'), event.get('user'), event.get('text')
    
    if user_id != bot_id:
        client.chat_postMessage(channel=channel_id, text="i hear you, loud and clear")

if __name__ == "__main__":
    app.run(debug=True)