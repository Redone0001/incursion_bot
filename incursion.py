# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 20:09:01 2023

@author: Loick
"""


class incursion:
    def __init__(self, text):
        (
            self.region,
            self.stag_system,
            self.sec,
            self.max_remaining,
            self.state,
            self.sov_owner,
            self.profile,
        ) = self._process_text(text)

    def _process_text(self, text):
        state = ""
        max_remaining = ""
        sec = 0.0
        stag_system = ""
        region = ""
        sov_owner = ""
        sov_owner = text[text.find('title="') + 7 :]
        sov_owner = sov_owner[: sov_owner.find('"')]

        main_text = text[text.find('</dt><dd class="col-sm-6">') : text.find("</dd></dl>")]
        main_text = main_text.replace(' class="col-sm-6"', "")
        for line in main_text.split("</dd>"):
            if "aria-valuenow=" in line:
                profile = line[line.find("aria-valuenow") + 15 : line.find("aria-valuemin") - 2]
            elif "Region" in line:
                region = line[line.find('rel="noopener">') + 15 : -4]
            elif "Stag. System" in line:
                stag_system = line[line.find('rel="noopener">') + 15 : -4]
            elif "Max. remaining" in line:
                max_remaining = line[line.find("<dd>") + 4 :]
            elif "State" in line:
                state = line[line.find('">') + 2 :]
            elif "Sec. Status" in line:
                sec = line[line.find('">') + 2 :]
        if "<!-- --> (Boss)" in state:
            state = state.replace("<!-- --> (Boss)", "")
        return region, stag_system, float(sec), max_remaining, state, sov_owner, int(float(profile))

    def data(self):
        return [self.region, self.stag_system, self.sec, self.max_remaining, self.state, self.sov_owner, self.profile]
