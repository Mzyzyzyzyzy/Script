# -*- coding: utf-8 -*-
# @Time : 2022/3/21 10:37
# @Author : Mzy
# @Email : mazhenya@xiaoduotech.com
# @File : .py
# @Project : scripts

import requests


# developer_all = '()'


def send_to_feishu_developer(text, feishu_url):
    """
    发送飞书消息
    :param title:标题
    :param text:发送文本
    :param feishu_url:群组 feishu_url
    :return:
    """
    headers = {'Content-Type': 'application/json'}
    data = {"msg_type": "text", "content": {"text": text}}
    res = requests.post(feishu_url, json=data, headers=headers)
    if res.status_code == 200:
        return True
    else:
        return False


feishu_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/f90f3bec-29c6-4f72-8916-fbb70f8df437'
text = "恰饭"

if __name__ == '__main__':
    send_to_feishu_developer(text=text, feishu_url=feishu_url)
