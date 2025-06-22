# Anki Add-on: Export Known Words to Clipboard

A simple add-on to export known words (and sentences) from mature Anki cards to your clipboard for easy pasting into other applications like Migaku, spreadsheets, or text editors.

## Note on Direction Change

This add-on was originally designed to sync directly to Migaku, but was changed to a clipboard export approach due to the complexity of browser automation and lack of a public Migaku API. This approach is more reliable, works with any application, and doesn't require external dependencies.

## Features

- **Export mature cards**: Only exports cards with intervals of 21+ days (mature cards)
- **Flexible export options**: Choose between words only or words with sentences
- **Custom field mapping**: Select which fields contain your words and sentences
- **Clipboard export**: Copies formatted text directly to your clipboard
- **Cross-platform**: Works on Windows, macOS, and Linux
- **No dependencies**: Uses only built-in Anki libraries

## Installation

### Method 1: Manual Installation

1. Download the add-on files
2. Extract to your Anki add-ons folder:
   - **Windows**: `%APPDATA%\Anki2\addons21\`
   - **macOS**: `~/Library/Application Support/Anki2/addons21/`
   - **Linux**: `~/.local/share/Anki2/addons21/`

### Method 2: Git Clone

```bash
# Navigate to your Anki add-ons folder
cd ~/Library/Application\ Support/Anki2/addons21/

# Clone the repository
git clone git@github.com:Seeido/Anki-Export-Known-Words-to-Clipboard.git

# Or using HTTPS
git clone https://github.com/Seeido/Anki-Export-Known-Words-to-Clipboard.git
```

### Method 3: Git Clone (Alternative Location)

```bash
# Clone to a different location
git clone git@github.com:Seeido/Anki-Export-Known-Words-to-Clipboard.git

# Then copy to Anki add-ons folder
cp -r Anki-Export-Known-Words-to-Clipboard ~/Library/Application\ Support/Anki2/addons21/
```

## Usage

1. Restart Anki
2. Look for "Export Known Words to Clipboard" in the Tools menu
3. Select a deck to export from
4. Choose export type (words only or words with sentences)
5. Map your card fields (word field and sentence field if applicable)
6. The words will be copied to your clipboard with instructions for pasting

## Use Cases

- **Migaku Integration**: Paste words into Migaku's Known Words section
- **Spreadsheet Analysis**: Export to Excel/Google Sheets for analysis
- **Text Processing**: Use in text editors for further processing
- **Language Learning**: Share word lists with tutors or study partners

## Requirements

- Anki 2.1.50 or later
- No additional dependencies required
