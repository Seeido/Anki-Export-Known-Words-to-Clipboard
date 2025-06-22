# -*- coding: utf-8 -*-

"""
Anki Add-on: Export Known Words to Clipboard

This add-on allows users to export known words from mature Anki cards to their clipboard
for easy pasting into other applications like Migaku, spreadsheets, or text editors.

Note: This add-on was originally designed to sync directly to Migaku, but was changed
to a clipboard export approach due to the complexity of browser automation and lack of
a public Migaku API. This approach is more reliable and works with any application.
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

# Import all the step functions
from src.ui.selection_dialogs import deck_selection, sync_type_selection
from src.ui.field_mapping import field_mapping
from src.core.card_extractor import extract_mature_cards
from src.core.clipboard_handler import copy_words_to_clipboard

MENU_ITEM_NAME = "Export Known Words to Clipboard"

def run_sync_workflow():
    """
    Main workflow function that orchestrates the entire export process.
    
    This function calls each step sequentially and passes results between them.
    If any step fails, the workflow terminates with an appropriate error message.
    """
    
    WORKFLOW_START_MESSAGE = "Starting Export Known Words to Clipboard workflow..."
    
    try:
        # Step 1: User Initiates Export (handled by menu item calling this function)
        
        # Step 2: Deck Selection
        deck_result = deck_selection()
        if not deck_result:
            return False
        
        selected_deck_name = deck_result['deck_name']
        deck_id = deck_result['deck_id']
        card_count = deck_result['card_count']
        
        # Step 3: Export Type Selection
        sync_type_result = sync_type_selection(selected_deck_name, deck_id, card_count)
        if not sync_type_result:
            return False
        
        sync_words_only = sync_type_result['sync_words_only']
        
        # Step 4: Field Mapping
        field_mapping_result = field_mapping(selected_deck_name, deck_id, card_count, sync_words_only)
        if not field_mapping_result:
            return False
        
        word_field = field_mapping_result['word_field']
        sentence_field = field_mapping_result['sentence_field']
        
        # Step 5: Extract Mature Cards
        extracted_data = extract_mature_cards(
            selected_deck_name, 
            deck_id, 
            card_count, 
            sync_words_only, 
            word_field, 
            sentence_field
        )
        if not extracted_data:
            showInfo("Card extraction failed. Workflow terminated.")
            return False
        
        # Step 6: Copy Words to Clipboard
        if not copy_words_to_clipboard(extracted_data):
            showInfo("Failed to copy words to clipboard. Workflow terminated.")
            return False
        
        # Workflow completed successfully!
        return True
        
    except Exception as e:
        showInfo(f"Unexpected error in export workflow: {str(e)}")
        return False

def setup_menu():
    """Set up the add-on menu item, removing any existing one to prevent duplicates."""
    # Remove existing action to avoid creating duplicates when switching profiles
    for action in mw.form.menuTools.actions():
        if action.text() == MENU_ITEM_NAME:
            mw.form.menuTools.removeAction(action)
    
    # Create the new menu action
    action = QAction(MENU_ITEM_NAME, mw)
    action.triggered.connect(run_sync_workflow)
    
    # Add it to the tools menu
    mw.form.menuTools.addAction(action)

# Set up the menu when Anki starts
addHook("profileLoaded", setup_menu)
