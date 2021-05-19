from __future__ import unicode_literals

import telegram
import praw
import logging
import html
import sys
import os
import json
import time

from time import sleep
from datetime import datetime, timedelta

credentials = {}

checktime=600

credentials["token"] = os.environ.get('TOKEN')
credentials["subreddit"] = os.environ.get('SUB')
credentials["channel"] = os.environ.get('CHANNEL')

token = credentials["token"]
channel = credentials["channel"]

bot = telegram.Bot(token=token)

while True:
    r = praw.Reddit(user_agent="Nishebrod_bot_by_Lavrenty",
                client_id=os.environ.get('CLIENT_ID'),
                client_secret=os.environ.get('CLIENT_SECRET'),
                username=os.environ.get('RUSERNAME'),
                password=os.environ.get('RPASS'))
    r.read_only = True
    for submission in r.subreddit("freegamefindings+gamedeals+ps4deals").new(limit=10):
        if ((time.time()-submission.created_utc)/60<=checktime/60):
            link = "https://redd.it/{id}".format(id=submission.id)
            image = html.escape(submission.url or '')
            title = html.escape(submission.title or '')
            user = html.escape(submission.author.name or '')
            template = "{title}\n{link}\nby {user}"
            message = template.format(title=title, link=link, user=user)
            bot.sendMessage(chat_id=channel, text=message)
    sleep(checktime)