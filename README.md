# psaudit
Process auditor for macOS. Verifies that all running processes have been signed by Apple.

# Installation
```
pip install psaudit
```

# Usage
```
psaudit
```

If any processes fail the audit, they will be listed and the script will return a non-zero error code indicating the number of failed processes. For example:
```
$ psaudit 
process 371 (/Applications/Utilities/Adobe Sync/CoreSync/Core Sync.app/Contents/PlugIns/ACCFinderSync.appex/Contents/MacOS/ACCFinderSync) not signed by Apple
process 14722 (/usr/local/Cellar/bash/5.0.11/bin/bash) not signed by Apple
process 75508 (/usr/local/Cellar/macvim/8.1-157/MacVim.app/Contents/MacOS/MacVim) not signed by Apple
process 75509 (/usr/local/Cellar/macvim/8.1-157/MacVim.app/Contents/MacOS/Vim) not signed by Apple
$ echo $?
4
```
