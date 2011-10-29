#! /usr/bin/env python

import requests
import json
from xml.etree import ElementTree as etree

from secret import username, password

def post_task(question):
    r = requests.post(
        'https://sandbox.mobileworks.com/api/v1/tasks/',
        auth=(username, password),
        headers={'content-type': 'application/json'},
        data=json.dumps({ 
                'question': question,
                'answerType': 'm',
                'answerChoices': ['yes', 'no'],
                'computerOnly': True }))
    r.raise_for_status()
    if r.status_code == 201:
        return r.headers['location']
    else:
        raise Exception('Unexpected status code: %s' % r.status_code)

def extract_content(filename):
    xml = open(filename).read().replace('&nbsp;', u'\u00a0'.encode('utf8'))
    tree = etree.fromstring(xml)
    style = tree.find('head/style')
    diff, key = tree.findall('body/table')
    return '\n'.join([etree.tostring(x) for x in [style, diff, key]])

def main():
    import sys
    question = ('<p>Is the following change OK?</p>' 
                + extract_content(sys.argv[1]))
    print post_task(question)

if __name__ == '__main__':
    main()
