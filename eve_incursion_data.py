# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 18:40:25 2023

@author: Loick
"""
import requests
import incursion
import sys

sys.path.append(r"c:\users\loick\appdata\local\programs\python\python311\lib\site-packages")
from tabulate import tabulate


class eve_incursion_data:
    def __init__(self):
        self.list_data = []
        self.in_horde = []
        self.horde_space = [
            "Etherium Reach",
            "The Kalevala Expanse",
            "Malpais",
            "Perrigen Falls",
            "Oasa",
            "Outer Passage",
            "The Spire",
            "Cobalt Edge",
            "Cache",
        ]
        self.to_print = ""
        self.NS_count = 0

    def _get_data_incursion(self):
        url = "https://eve-incursions.de"
        incursion_web_page = requests.get(url)
        body = incursion_web_page.text[
            incursion_web_page.text.find('<div class="active-spawns">') + 27 : incursion_web_page.text.find("</body>")
        ]
        body = body.replace("</div>", "\n")
        return body

    def _process_incursion(self):
        body = self._get_data_incursion()
        list_spawn = body.split('<div class="spawn">')
        list_spawn.pop(0)
        self.list_data = [incursion.incursion(_) for _ in list_spawn]
        col_names = ["Region", "System", "Sec.", "Time left", "State", "Sov Owner", "Profile"]
        self.to_print = (
            "```\n" + tabulate(([inc.data() for inc in self.list_data]), headers=col_names, tablefmt="github") + "\n```"
        )

    def _update_state_eve(self):
        self.in_horde = []
        self.NS_count = 0
        _ = self._process_incursion()
        for inc in self.list_data:
            if inc.region in self.horde_space:
                self.in_horde.append(inc)
            if inc.sec < 0.0:
                self.NS_count += 1
