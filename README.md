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

If any processes fail the audit, they will be listed and the script will return a non-zero error code.
