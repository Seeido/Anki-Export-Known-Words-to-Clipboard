# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Anki Add-on: Sync Known Words to Migaku

This add-on allows users to export known words from mature Anki cards to Migaku.
"""

import aqt
from aqt import mw
from aqt.utils import showInfo, tooltip
from aqt.qt import *
from anki.hooks import addHook

MENU_ITEM_NAME = "Sync Known Words to Migaku"

def deck_selection():
    """Show a dropdown menu of all available decks for selection and validate the choice."""
    
    NO_DECKS_MESSAGE = "No decks found in your collection."
    WINDOW_TITLE = "Select Deck"
    DECKS_SELECTION_MESSAGE = "Select a deck to sync known words from:"
    NO_CARDS_MESSAGE = "The selected deck has no cards. Please select a deck with cards."
    DECK_NOT_FOUND_MESSAGE = "The selected deck could not be found. Please try again."

    # Get all deck names
    deck_names = [d['name'] for d in mw.col.decks.all()]
    
    if not deck_names:
        showInfo(NO_DECKS_MESSAGE)
        return
    
    # Create the dialog
    dialog = QDialog(mw)
    dialog.setWindowTitle(WINDOW_TITLE)
    dialog.setModal(True)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add label
    label = QLabel(DECKS_SELECTION_MESSAGE)
    layout.addWidget(label)
    
    # Create dropdown
    combo = QComboBox()
    combo.addItems(deck_names)
    layout.addWidget(combo)
    
    # Add buttons
    button_layout = QHBoxLayout()
    ok_button = QPushButton("OK")
    cancel_button = QPushButton("Cancel")
    
    button_layout.addWidget(ok_button)
    button_layout.addWidget(cancel_button)
    layout.addLayout(button_layout)
    
    # Connect buttons
    ok_button.clicked.connect(dialog.accept)
    cancel_button.clicked.connect(dialog.reject)
    
    dialog.setLayout(layout)
    
    # Show dialog and get result
    if dialog.exec() == QDialog.DialogCode.Accepted:
        selected_deck_name = combo.currentText()
        
        # Validate the selected deck
        try:
            # Find the deck by name
            deck_id = None
            for deck in mw.col.decks.all():
                if deck['name'] == selected_deck_name:
                    deck_id = deck['id']
                    break
            
            if deck_id is None:
                showInfo(DECK_NOT_FOUND_MESSAGE)
                return
            
            # Check if the deck has any cards
            card_count = mw.col.decks.card_count(deck_id, include_subdecks=True)
            if card_count == 0:
                showInfo(NO_CARDS_MESSAGE)
                return
            
            showInfo(f"Selected deck: {selected_deck_name} (has {card_count} cards)\n(Deck validation complete - next step will be sync type selection)")
            
        except Exception as e:
            showInfo(f"Error validating deck: {str(e)}")
            return

def setup_menu():
    """Set up the add-on menu item."""
    # Create the menu action
    action = QAction(MENU_ITEM_NAME, mw)
    action.triggered.connect(deck_selection)
    
    # Add to the tools menu
    mw.form.menuTools.addAction(action)

# Set up the menu when Anki starts
addHook("profileLoaded", setup_menu)
