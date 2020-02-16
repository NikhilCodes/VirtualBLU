#!/usr/bin/env python3
#
# Author : Nikhil Nayak (nikhil.nixel@gmail.com)
# Usage  : .py
# 

import os
import wolframalpha
from CORE.UTILS import tabulate

WOLFRAM_API_KEY = '3E5U46-KXYEAYL9LL'
client = wolframalpha.Client(WOLFRAM_API_KEY)


def get_wolfram_responses(query):
    try:
        res = client.query(query)
    except Exception as e:
        if str(e) == 'Error 0: Unknown error':
            return [["No Data Available!"], "No Data Available!"]

        print(e)
        return [["I'm Offline!"], "I'm Offline!"]

    resp = []
    speech = ''
    iter_ = 0

    if res.success == 'false':
        return [["No Data Available!"], "No Data Available!"]

    for pod in res.pods:
        title = pod['@title']
        iter_ += 1
        if pod.text is None:
            resp.append(title + '\n' + len(title) * '─' + '\n' + str(list(pod.subpod)[0]['img']['@src']))

        elif '| ' in pod.text:
            # Morph the table data into actual table visualization!
            text = []
            for i in pod.text.split('\n'):
                if ('|' in i) and i.replace('|', '').replace(' ', '') != '':
                    text.append(i.split('| '))

            resp.append(title + '\n' + len(title) * '─' + '\n' + tabulate(text))
            if iter_ == 2:
                speech = pod.text.replace('|', '')

        else:
            if iter_ == 2:
                speech = pod.text
            resp.append(title + '\n' + len(title) * '─' + '\n' + pod.text)

    return resp, speech


if "__main__" == __name__:
    print(get_wolfram_responses('integration of 2x+5 dx'))
    print(get_wolfram_responses('sap'))
