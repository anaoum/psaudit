#!/usr/bin/env python3

import os
import re
import sys
import asyncio
import subprocess

import psutil

MAX_PROCS = 100

whitelist = [
        re.compile('^Identifier=com\.apple\..*'),
        re.compile('^Identifier=com\.google\..*'),
        re.compile('^Identifier=com\.microsoft\..*'),
        re.compile('^Identifier=com\.adobe\..*'),
        re.compile('^Authority=.*JQ525L2MZD.*'), # Adobe
        re.compile('^Authority=.*EQHXZ8M8AV.*'), # Google
        re.compile('^Authority=.*UBF8T346G9.*'), # Microsoft
]

process_paths = {}
for p in psutil.process_iter(attrs={'pid', 'exe'}):
    if p.info['pid'] == 0:
        continue
    elif p.info['pid'] == os.getpid():
        continue
    process_paths[p.info['pid']] = p.info['exe']

process_audits = {}

async def audit_process(pid):
    path = process_paths[pid]
    if path is None:
        process_audits[pid] = None
        return
    p = await asyncio.create_subprocess_shell(f'codesign -dvv "{path}"', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await p.communicate()
    for line in stderr.decode('utf-8').split('\n'):
        for expr in whitelist:
            if expr.match(line):
                process_audits[pid] = True
                return
    process_audits[pid] = False

async def audit():
    remaining = list(process_paths.keys())
    while remaining:
        tasks = []
        while len(tasks) < MAX_PROCS and remaining:
            tasks.append(asyncio.create_task(audit_process(remaining.pop(0))))
        for task in tasks:
            await task

asyncio.run(audit())

failed = 0

for pid, audit_result in process_audits.items():
    if audit_result is None:
        print('could not determine executable for process', pid, file=sys.stderr)
        failed += 1
    elif audit_result is False:
        print(f'process {pid} ({process_paths[pid]}) not in whitelist', file=sys.stderr)
        failed += 1

sys.exit(failed)
