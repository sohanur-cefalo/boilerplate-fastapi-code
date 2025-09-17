#!/usr/bin/env python3
"""
FastAPI Boilerplate Shell Launcher
==================================

Launches different interactive shells based on user preference.

Usage:
    python management/shell_launcher.py [shell_type]

Available shells:
    - bpython (recommended): Best autocompletion
    - ipython: Good balance of features
    - standard: Basic Python shell

Examples:
    python management/shell_launcher.py bpython
    python management/shell_launcher.py ipython
    python management/shell_launcher.py standard
"""

import sys
import os

def main():
    shell_type = sys.argv[1] if len(sys.argv) > 1 else "bpython"
    
    if shell_type == "bpython":
        os.system("python management/bpython_shell.py")
    elif shell_type == "ipython":
        os.system("python management/ipython_shell.py")
    elif shell_type == "standard":
        os.system("python management/shell.py")
    else:
        print(f"❌ Unknown shell type: {shell_type}")
        print("Available options: bpython, ipython, standard")
        sys.exit(1)

if __name__ == "__main__":
    main()
