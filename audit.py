#!/usr/bin/env python3

import os
import re
import sys
import subprocess

import psutil

whitelist = [
        re.compile('^Identifier=com\.apple\..*'),
        re.compile('^Identifier=com\.google\..*'),
        re.compile('^Identifier=com\.microsoft\..*'),
        re.compile('^Identifier=com\.adobe\..*'),
        re.compile('^Authority=.*JQ525L2MZD.*'), # Adobe
        re.compile('^Authority=.*EQHXZ8M8AV.*'), # Google
        re.compile('^Authority=.*UBF8T346G9.*'), # Microsoft
]

def in_whitelist(process_path):
    p = subprocess.run(['codesign', '-dvv', process_path], capture_output=True)
    for line in p.stderr.decode('utf-8').split('\n'):
        for expr in whitelist:
            if expr.match(line):
                return True
    return False

failed = 0

for p in psutil.process_iter(attrs={'pid', 'exe'}):
    if p.info['pid'] == 0:
        continue
    elif p.info['pid'] == os.getpid():
        continue
    elif p.info['exe'] is None:
        print('could not determine executable for process', p.info['pid'], file=sys.stderr)
        failed += 1
    elif not in_whitelist(p.info['exe']):
        print(f'process {p.info["pid"]} ({p.info["exe"]}) not in whitelist', file=sys.stderr)
        failed += 1

sys.exit(failed)
