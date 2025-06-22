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

### For Testing/Development

1. Download the add-on files from this repository
2. Place them in your Anki add-ons directory
3. Restart Anki
4. Access via Tools → Sync Known Words to Migaku

#### Quick Setup via Git Clone

**Windows:**

```bash
cd "%APPDATA%\Anki2\addons21\"
git clone https://github.com/Seeido/anki-known-words-sync-to-migaku.git
```

**macOS:**

```bash
cd ~/Library/Application\ Support/Anki2/addons21/
git clone https://github.com/Seeido/anki-known-words-sync-to-migaku.git
```

**Linux:**

```bash
cd ~/.local/share/Anki2/addons21/
git clone https://github.com/Seeido/anki-known-words-sync-to-migaku.git
```

**After cloning, restart Anki to load the add-on.**

#### Removing After Testing

**Windows:**

```bash
cd "%APPDATA%\Anki2\addons21\"
rmdir /s anki-known-words-sync-to-migaku
```

**macOS:**

```bash
cd ~/Library/Application\ Support/Anki2/addons21/
rm -rf anki-known-words-sync-to-migaku
```

**Linux:**

```bash
cd ~/.local/share/Anki2/addons21/
rm -rf anki-known-words-sync-to-migaku
```

**After removal, restart Anki to unload the add-on.**

### For Regular Users (Coming Soon)

This add-on will be published on AnkiWeb with its own add-on ID for easy installation through Anki's add-on manager.

## Usage

1. Look for "Export Known Words to Clipboard" in the Tools menu
2. Select a deck to export from
3. Choose export type (words only or words with sentences)
4. Map your card fields (word field and sentence field if applicable)
5. The words will be copied to your clipboard with instructions for pasting (to Migaku)

## Use Cases

- **Migaku Integration**: Paste words into Migaku's Known Words section
- **Spreadsheet Analysis**: Export to Excel/Google Sheets for analysis
- **Text Processing**: Use in text editors for further processing
- **Language Learning**: Share word lists with tutors or study partners

## Requirements

- Anki 2.1.50 or later
