# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Anki Add-on: Sync Known Words to Migaku

This add-on allows users to export known words from mature Anki cards to Migaku.
"""

import sys
import os
# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

import aqt
from aqt import mw
from aqt.utils import showInfo, tooltip
from aqt.qt import *
from anki.hooks import addHook

# Import UI components
from src.ui.selection_dialogs import deck_selection

MENU_ITEM_NAME = "Sync Known Words to Migaku"

def setup_menu():
    """Set up the add-on menu item, removing any existing one to prevent duplicates."""
    # Remove existing action to avoid creating duplicates when switching profiles
    for action in mw.form.menuTools.actions():
        if action.text() == MENU_ITEM_NAME:
            mw.form.menuTools.removeAction(action)
    
    # Create the new menu action
    action = QAction(MENU_ITEM_NAME, mw)
    action.triggered.connect(deck_selection)
    
    # Add it to the tools menu
    mw.form.menuTools.addAction(action)

# Set up the menu when Anki starts
addHook("profileLoaded", setup_menu)
