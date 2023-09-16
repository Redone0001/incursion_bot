# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 19:40:52 2023

@author: Loick
"""
# import sys

# sys.path.append(r"C:\Users\Loick\AppData\Local\Programs\Python\Python311\Lib\site-packages")

import os
import base64
import logging
from time import sleep
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook
from eve_incursion_data import eve_incursion_data


def _load_kube_config():
    bot_name = "Incursion Bot V3"
    table_discord_webhook_url = os.environ.get("ping-discord-webhook-url")
    ping_discord_webhook_url = os.environ.get("table-discord-webhook-url")
    message_id = int(os.environ.get("message-id"))
    print(table_discord_webhook_url, ping_discord_webhook_url, message_id)
    webhook = DiscordWebhook(url=table_discord_webhook_url, id=str(message_id), username=bot_name)
    webhook_notify = DiscordWebhook(url=ping_discord_webhook_url, username=bot_name)

    return webhook, webhook_notify


def _notify(text, webhook_notify):
    if len(text) == 0:
        return
    text = "@everyone \n" + text
    webhook_notify.content = text + f"\n\nlast update at {str(datetime.now())[:-7]}"
    webhook_notify.execute()


def _compare_state(prev_state, eve_state):
    text = ""
    list_stag = [(inc.stag_system, inc.region) for inc in eve_state.in_horde]
    list_prev_stag = [(inc.stag_system, inc.region) for inc in prev_state.in_horde]
    diff_stag = set(list_stag) - set(list_prev_stag)
    if len(prev_state.in_horde) > len(eve_state.in_horde):
        text += f"Focus in {diff_stag} despawn\nNew spawn from {str(datetime.now() + timedelta(hours = 12))[:-7]} to {str(datetime.now() + timedelta(hours = 36))[:-7]}"
    elif len(prev_state.in_horde) < len(eve_state.in_horde):
        text += f"Focus in {diff_stag} spawn\n"
    else:
        for id, inc in enumerate(eve_state.in_horde):
            if prev_state.in_horde[id].state != inc.state:
                text += f"Focus in {inc.region}, {inc.stag_system} went {inc.state}\n"
    return text


def main(webhook, webhook_notify, prev_state):
    logger.info(f"message id = {webhook.id}")
    logger.info(f"process id = {os.getpid()}")

    eve_state = eve_incursion_data()
    eve_state._process_incursion()
    eve_state._update_state_eve()

    header_text = f"{len(eve_state.in_horde)} focus in our space\n{3-(eve_state.NS_count)} spaw brewing for null sec"
    logger.info(header_text + eve_state.to_print)
    footer_text = f"\n\nlast update at {str(datetime.now())[:-7]}"
    webhook.content = header_text + eve_state.to_print + footer_text
    webhook.edit()
    _notify(_compare_state(prev_state, eve_state), webhook_notify)

    return eve_state


# %%
if __name__ == "__main__":
    header_text = "Incursion info\n"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    webhook, webhook_notify = _load_kube_config()
    prev_state = eve_incursion_data()
    prev_state._process_incursion()
    prev_state._update_state_eve()
    while True:
        prev_state = main(webhook, webhook_notify, prev_state)
        sleep(5)
