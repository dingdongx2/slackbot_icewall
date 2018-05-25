import os
import re
import json
from random import choice
# from random import choice
with open('./direction.json', encoding="UTF8") as f:
    data = json.load(f)
with open('./store.json') as f:
    store = json.load(f)
# with open('./inform.json', encoding="UTF8") as f:
#     inform = json.load(f)

from time import sleep
from slackclient import SlackClient

config = json.load(open('config.json'))
slack_client = SlackClient(store["key"])
starterbot_id = 'overaction'

RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
EXAMPLE_COMMAND = "do"
# istel = 0 0: ready 1:direction catch 2:know

# notification
# def notify(user, message) :


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            # user_id, message = parse_direct_mention(event["text"])
            message = event["text"]

            if message in data["talk"]:
                return message, event["channel"]

            if message.startswith("전번"):
                message = message.split("전번 ")[1]
                return message, event["channel"]
            elif message.endswith("번호뭐야"):
                message = message.split(" 번호뭐야")[0]
                return message, event["channel"]
            elif message.endswith("번호뭐야?"):
                message = message.split(" 번호뭐야?")[0]
                return message, event["channel"]
            elif message.endswith("번호 뭐야?"):
                message = message.split(" 번호 뭐야?")[0]
                return message, event["channel"]
            elif message.endswith("번호 뭐야"):
                message = message.split(" 번호 뭐야")[0]
                return message, event["channel"]
            elif message.endswith("번호 알아?"):
                message = message.split(" 번호 알아?")[0]
                return message, event["channel"]
            elif message.endswith("번호알아?"):
                message = message.split(" 번호알아?")[0]
                return message, event["channel"]
            elif message.endswith("번호내놔"):
                message = message.split(" 번호내놔")[0]
                return message, event["channel"]

            elif message.startswith("마법의 소라고동님"):
                message = "마법의 소라고동님"
                return message, event["channel"]

            # return message, event["channel"]

    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    #response = command + " 물어봤니?"

    try:
        if command in data["number"]: #asking tel
            if isinstance(data["number"][command],list):
                response = choice(data["number"][command])

            else:
                response = data["number"][command]
        else:
            response = command + "? 몰라!"

        if command in data["talk"]: #normal talking
            if isinstance(data["talk"][command],list):
                response = choice(data["talk"][command])

            else:
                response = data["talk"][command]
    except:
        pass

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

# def __init__ :

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Bot connected")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
                # print(command)
                # print(channel)
            sleep(config['RTM_READ_DELAY'])
    else:
        print("Connection failed.")
