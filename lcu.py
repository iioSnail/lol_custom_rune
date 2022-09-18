import base64
import json
import os

import requests

import utils


class LCU:

    def __init__(self, token, port):
        self.token = token
        self.port = port
        self.headers = self._build_headers()
        self.url = f"https://127.0.0.1:{port}"

    def _build_headers(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Basic " + base64.b64encode(("riot:" + self.token).encode("UTF-8")).decode("UTF-8")
        }

        return headers

    def get_runes(self):
        """
        获取符文页
        """
        url = self.url + "/lol-perks/v1/pages"

        resp = requests.get(url, headers=self.headers, verify=False)
        if not resp.ok:
            utils.error("获取符文页失败！")
            return

        resp_content = resp.text

        runes = []

        for item in json.loads(resp_content):
            if item['isDeletable']:
                runes.append(item)

        return runes

    def delete_one_runes(self, runes, index=0):
        if len(runes) <= 1:
            return

        url = self.url + "/lol-perks/v1/pages/" + str(runes[index]['id'])
        resp = requests.delete(url, headers=self.headers, verify=False)
        if not resp.ok:
            utils.error("删除符文失败！")
            return

    def load_rune(self, rune_filename):
        filepath = './runes/' + rune_filename
        with open(filepath, encoding='utf-8') as f:
            rune = f.read()

        url = self.url + "/lol-perks/v1/pages"

        resp = requests.post(url, json=json.loads(rune), headers=self.headers, verify=False)
        if not resp.ok:
            utils.error("载入符文页失败！")
            return
