from xenolyte import Xenolyte
from _version import __version__
import utils
import os
import logging
from gui import gui

def main():
    gui.start_app()

if __name__ == "__main__":
    main()


# First Start of Application
#  if not os.path.exists("./data/vaults.csv"):
# Choose first vault dialog
# Or create Obsidian-like welcome window
# Vault Manager
# 