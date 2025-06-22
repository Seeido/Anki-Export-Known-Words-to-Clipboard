# -*- coding: utf-8 -*-

"""
Clipboard functionality for copying extracted words to clipboard.
"""

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *


def copy_words_to_clipboard(extracted_data):
    """
    Copy extracted words to clipboard and provide instructions.
    
    This exports the words to the user's clipboard for easy pasting into
    other applications like Migaku, spreadsheets, or text editors.
    
    Args:
        extracted_data: Data from the previous extraction step
        
    Returns:
        bool: True if successful, False otherwise
    """
    
    if not extracted_data or not extracted_data.get('cards'):
        showInfo("No words to copy to clipboard.")
        return False
    
    try:
        cards = extracted_data['cards']
        sync_words_only = extracted_data['sync_words_only']
        
        # Format the words for clipboard
        clipboard_text = ""
        
        for card in cards:
            word = card['word']
            sentence = card['sentence']
            
            if sync_words_only:
                # Words only format
                clipboard_text += f"{word}\n"
            else:
                # Words and sentences format (matching Migaku's expected format)
                if sentence:
                    clipboard_text += f"{word}\t{sentence}\n"
                else:
                    clipboard_text += f"{word}\n"
        
        # Copy to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(clipboard_text.strip())
        
        # Show success message with instructions
        word_count = len(cards)
        sync_type = "words only" if sync_words_only else "words and sentences"
        
        success_message = f"✅ Successfully copied {word_count} {sync_type} to clipboard!\n\n"
        success_message += "The words are now ready to paste anywhere!\n\n"
        success_message += "For Migaku users (most common use case):\n"
        success_message += "1. Open the Migaku window\n"
        success_message += "2. Go to the Settings tab\n"
        success_message += "3. Scroll down to the 'Known Words' section\n"
        success_message += "4. Click 'Add Words'\n"
        success_message += "5. Paste the copied words (Cmd+V / Ctrl+V)\n"
        success_message += "6. Click 'Add Words' again to confirm\n\n"
        success_message += "You can also paste into spreadsheets, text editors, or any other application."
        
        showInfo(success_message)
        return True
        
    except Exception as e:
        showInfo(f"Error copying words to clipboard: {str(e)}")
        return False 