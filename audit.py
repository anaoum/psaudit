#!/usr/bin/env python3

import os
import re
import sys
import threading
import queue
import subprocess

import psutil

MAX_THREADS = 16

failed = 0

process_paths = {}
for p in psutil.process_iter(attrs={'pid', 'exe'}):
    pid, path = p.info['pid'], p.info['exe']
    if pid == 0:
        continue
    elif pid == os.getpid():
        continue
    elif path is None:
        print('could not determine executable for process', pid, file=sys.stderr)
        failed += 1
        continue
    process_paths[pid] = path
paths = set(process_paths.values())

whitelist = [
        re.compile('^Identifier=com\.apple\..*'),
        re.compile('^Identifier=com\.google\..*'),
        re.compile('^Identifier=com\.microsoft\..*'),
        re.compile('^Identifier=com\.adobe\..*'),
        re.compile('^Authority=.*JQ525L2MZD.*'), # Adobe
        re.compile('^Authority=.*EQHXZ8M8AV.*'), # Google
        re.compile('^Authority=.*UBF8T346G9.*'), # Microsoft
]

def audit_process(path):
    if path is None:
        return None
    p = subprocess.run(['codesign', '-dvv', path], capture_output=True)
    for line in p.stderr.decode('utf-8').split('\n'):
        for expr in whitelist:
            if expr.match(line):
                return True
    return False

def auditor(audit_queue, audit_results_queue):
    while True:
        path = audit_queue.get()
        if path is None:
            break
        result = audit_process(path)
        audit_results_queue.put((path, result))

audit_queue = queue.Queue()
audit_results_queue = queue.Queue()

for path in paths:
    audit_queue.put(path)

threads = []
for _ in range(MAX_THREADS):
    t = threading.Thread(target=auditor, args=(audit_queue, audit_results_queue))
    t.start()
    threads.append(t)

path_audits = {}
while len(path_audits) < len(paths):
    path, result = audit_results_queue.get()
    path_audits[path] = result
for _ in range(MAX_THREADS):
    audit_queue.put(None)
for t in threads:
    t.join()

for pid, path in process_paths.items():
    audit_result = path_audits[path]
    if audit_result is False:
        print(f'process {pid} ({process_paths[pid]}) not in whitelist', file=sys.stderr)
        failed += 1
sys.exit(failed)
