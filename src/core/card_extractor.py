# -*- coding: utf-8 -*-

"""
Core functionality for extracting mature cards and their field values.
"""

from aqt import mw
from aqt.utils import showInfo


def extract_mature_cards(selected_deck_name, deck_id, card_count, sync_words_only, word_field, sentence_field):
    """Extract field values from mature cards (interval >= 21 days)."""
    
    NO_MATURE_CARDS_MESSAGE = "No mature cards found in the selected deck.\n\nMature cards are those with intervals of 21 days or more."
    EXTRACTION_ERROR_MESSAGE = "Error extracting card data. Please try again."
    
    try:
        # Search strategy: (1) collect all mature cards in the collection,
        # (2) collect all cards in the selected deck, (3) intersect the two
        # sets.  This avoids edge-cases where combining deck and property
        # filters in a single search query returns incorrect results on some
        # Anki installations.

        # Step 1 – every mature card in the collection.
        all_mature_card_ids = set(mw.col.find_cards("prop:ivl>=21"))

        if not all_mature_card_ids:
            showInfo(NO_MATURE_CARDS_MESSAGE)
            return None

        # Step 2 – every card that belongs to the chosen deck.
        deck_card_ids = set(mw.col.decks.cids(deck_id, children=True))

        # Step 3 – keep only cards that are in both sets.
        mature_ids_in_deck = list(all_mature_card_ids.intersection(deck_card_ids))

        if not mature_ids_in_deck:
            showInfo(NO_MATURE_CARDS_MESSAGE)
            return None
        
        mature_cards_data = []
        
        # Process the correctly filtered mature cards.
        for card_id in mature_ids_in_deck:
            card = mw.col.get_card(card_id)
            if not card:
                continue
            
            note = card.note()
            if not note:
                continue
            
            # Find field indices
            word_index = None
            sentence_index = None
            
            for i, field in enumerate(note.model()['flds']):
                if field['name'] == word_field:
                    word_index = i
                if not sync_words_only and sentence_field and field['name'] == sentence_field:
                    sentence_index = i
            
            # Extract values using indices
            word_value = note.fields[word_index] if word_index is not None else ""
            sentence_value = note.fields[sentence_index] if sentence_index is not None else ""
            
            # Store card data for sorting
            mature_cards_data.append({
                'word': word_value.strip(),
                'sentence': sentence_value.strip(),
                'review_date': getattr(card, 'review_time', 0) or getattr(card, 'due', 0) or 0,
                'interval': card.ivl,
                'card_id': card_id
            })
        
        # Sort by review date (most recently reviewed last - for Migaku auto-scroll compatibility)
        mature_cards_data.sort(key=lambda x: x['review_date'])
        
        # Validate that we have valid word data
        valid_cards = [card for card in mature_cards_data if card['word']]
        
        if not valid_cards:
            showInfo("No mature cards with valid word data found.\n\nPlease ensure the selected word field contains data.")
            return None
        
        # Return the extracted data for the next step
        return {
            'cards': valid_cards,
            'total_mature': len(mature_cards_data),
            'total_valid': len(valid_cards),
            'sync_words_only': sync_words_only,
            'word_field': word_field,
            'sentence_field': sentence_field
        }
        
    except Exception as e:
        showInfo(f"{EXTRACTION_ERROR_MESSAGE}\n\nError details: {str(e)}")
        return None 