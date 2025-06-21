# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
UI dialogs for deck and sync type selection.
"""

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *


def sync_type_selection(selected_deck_name, deck_id, card_count):
    """Show a dialog to select sync type (words only or words + sentences)."""
    
    WINDOW_TITLE = "Select Sync Type"
    SYNC_TYPE_MESSAGE = "Choose what to sync to Migaku from mature cards:"
    WORDS_ONLY_TEXT = "Words only"
    WORDS_AND_SENTENCES_TEXT = "Words and sentences (to match Migaku Memory's behavior)"
    
    # Create the dialog
    dialog = QDialog(mw)
    dialog.setWindowTitle(WINDOW_TITLE)
    dialog.setModal(True)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add label
    label = QLabel(SYNC_TYPE_MESSAGE)
    layout.addWidget(label)
    layout.addSpacing(10)  # Add some space
    
    # Add a small info label
    info_label = QLabel("Note: Only cards with intervals of 21+ days will be considered mature")
    info_label.setStyleSheet("color: gray; font-size: 10px;")
    layout.addWidget(info_label)
    
    # Create radio buttons for sync type selection
    words_only_radio = QRadioButton(WORDS_ONLY_TEXT)
    words_only_radio.setToolTip("Export only the target words from mature cards")
    
    words_and_sentences_radio = QRadioButton(WORDS_AND_SENTENCES_TEXT)
    words_and_sentences_radio.setToolTip("Export both words and example sentences, matching Migaku Memory's format")
    
    # Set words only as default
    words_only_radio.setChecked(True)
    
    layout.addWidget(words_only_radio)
    layout.addWidget(words_and_sentences_radio)
    layout.addSpacing(10)  # Add some space
    
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
    
    ok_button.setShortcut("Return")  # Enter key
    cancel_button.setShortcut("Escape")  # Escape key
    
    dialog.setLayout(layout)
    
    # Show dialog and get result
    if dialog.exec() == QDialog.DialogCode.Accepted:
        sync_words_only = words_only_radio.isChecked()
        sync_type = "words only" if sync_words_only else "words and sentences"
        
        showInfo(f"Selected sync type: {sync_type}\n(Deck: {selected_deck_name}, {card_count} cards)\n(Sync type selection complete - next step will be field mapping)")
        
        # TODO: Call the next step (field mapping) here
        # field_mapping(selected_deck_name, deck_id, card_count, sync_words_only)
    else:
        return None


def deck_selection():
    """Show a dropdown menu to select a deck and validate it."""
    
    NO_DECK_MESSAGE = "No decks found in your collection."
    WINDOW_TITLE = "Select Deck"
    DECK_SELECTION_MESSAGE = "Select a deck to sync known words from:"
    NO_CARDS_MESSAGE = "The selected deck has no cards. Please select a deck with cards."
    DECK_NOT_FOUND_MESSAGE = "The selected deck could not be found. Please try again."

    # Get all deck names
    deck_names = [d['name'] for d in mw.col.decks.all()]
    
    if not deck_names:
        showInfo(NO_DECK_MESSAGE)
        return
    
    # Create the dialog
    dialog = QDialog(mw)
    dialog.setWindowTitle(WINDOW_TITLE)
    dialog.setModal(True)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add label
    label = QLabel(DECK_SELECTION_MESSAGE)
    layout.addWidget(label)
    
    # Create dropdown for selecting deck
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
            
            # Proceed directly to sync type selection
            sync_type_selection(selected_deck_name, deck_id, card_count)
            
        except Exception as e:
            showInfo(f"Error validating deck: {str(e)}")
            return 