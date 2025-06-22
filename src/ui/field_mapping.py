# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
UI dialogs for field mapping selection.
"""

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

# Import core functionality
from ..core.card_extractor import extract_mature_cards


def field_mapping(selected_deck_name, deck_id, card_count, sync_words_only):
    """Show a dialog to select field mappings for word and sentence extraction."""
    
    WINDOW_TITLE = "Select Field Mappings"
    FIELD_MAPPING_MESSAGE = "Select which fields contain the words and sentences:"
    WORD_FIELD_LABEL = "Word field:"
    SENTENCE_FIELD_LABEL = "Sentence field:"
    NO_FIELDS_MESSAGE = "No fields found in the selected deck."
    FIELD_NOT_FOUND_MESSAGE = "The selected field could not be found. Please try again."
    
    try:
        # Get the deck's note type to access its fields
        deck = mw.col.decks.get(deck_id)
        if not deck:
            showInfo("Error: Could not retrieve deck information.")
            return None
        
        # Get the note type ID from the deck
        if not isinstance(deck, dict):
            showInfo(f"Error: Unexpected deck data type: {type(deck)}")
            return None
            
        note_type_id = deck.get('mid')
        
        if not note_type_id:
            # Try to get note type from the deck's configuration
            conf = deck.get('conf', {})
            if isinstance(conf, dict):
                note_type_id = conf.get('mid')
            
        if not note_type_id:
            # If still no note type ID, try to get it from the first card in the deck
            try:
                card_ids = mw.col.decks.cids(deck_id, children=True)
                if card_ids:
                    first_card = mw.col.get_card(card_ids[0])
                    if first_card:
                        note_type_id = first_card.note().mid
            except Exception:
                pass
        
        if not note_type_id:
            showInfo("Error: Could not determine note type for the selected deck.")
            return None
        
        # Get the note type and its fields
        note_type = mw.col.models.get(note_type_id)
        if not note_type:
            showInfo("Error: Could not retrieve note type information.")
            return None
        
        # Get field names from the note type
        field_names = [field['name'] for field in note_type['flds']]
        
        if not field_names:
            showInfo(NO_FIELDS_MESSAGE)
            return None
        
        # Create the dialog
        dialog = QDialog(mw)
        dialog.setWindowTitle(WINDOW_TITLE)
        dialog.setModal(True)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add label
        label = QLabel(FIELD_MAPPING_MESSAGE)
        layout.addWidget(label)
        layout.addSpacing(10)
        
        # Create word field selection
        word_label = QLabel(WORD_FIELD_LABEL)
        layout.addWidget(word_label)
        
        word_combo = QComboBox()
        word_combo.addItems(field_names)
        layout.addWidget(word_combo)
        layout.addSpacing(10)
        
        # Create sentence field selection (only if not words-only)
        sentence_combo = None
        if not sync_words_only:
            sentence_label = QLabel(SENTENCE_FIELD_LABEL)
            layout.addWidget(sentence_label)
            
            sentence_combo = QComboBox()
            sentence_combo.addItems(field_names)
            layout.addWidget(sentence_combo)
            layout.addSpacing(10)
        
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
        
        # Add keyboard shortcuts
        ok_button.setShortcut("Return")
        cancel_button.setShortcut("Escape")
        
        dialog.setLayout(layout)
        
        # Show dialog and get result
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_word_field = word_combo.currentText()
            selected_sentence_field = sentence_combo.currentText() if sentence_combo else None
            
            # Validate selected fields
            if selected_word_field not in field_names:
                showInfo(FIELD_NOT_FOUND_MESSAGE)
                return None
            
            if not sync_words_only and selected_sentence_field not in field_names:
                showInfo(FIELD_NOT_FOUND_MESSAGE)
                return None
            
            # Proceed to extracting mature cards
            extract_mature_cards(selected_deck_name, deck_id, card_count, sync_words_only, selected_word_field, selected_sentence_field)
            
            return {
                'word_field': selected_word_field,
                'sentence_field': selected_sentence_field
            }
        else:
            return None
            
    except Exception as e:
        showInfo(f"Error during field mapping: {str(e)}")
        return None 