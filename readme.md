# NVDA Document Settings

Experimental NVDA add-on that replaces NVDA's built-in **Document formatting** settings panel while the add-on is installed.

The panel is a prototype for organizing NVDA document formatting options with a category tree and a compact settings area.

## Features

- Replaces NVDA's built-in **Document formatting** settings category while the add-on is installed.
- Uses a tree view for document formatting categories.
- Uses a check list for boolean options.
- Uses combo boxes for multi-value reporting modes.
- Uses spin controls for numeric options.
- Reads and writes NVDA's existing `documentFormatting` configuration section.

## Requirements

- Minimum NVDA version: 2026.1
- Last tested NVDA version: 2027.1

## Development

Create/update the local uv environment:

```powershell
uv sync --dev
```

Check formatting and linting:

```powershell
uv run ruff check .
uv run ruff format --check .
```

## Build

From this directory, run:

```powershell
uv run scons
```

This creates:

```text
documentFormattingTree-0.1.0.nvda-addon
```

## Install for testing

1. Build the add-on.
2. Open the generated `.nvda-addon` file.
3. Allow NVDA to install it.
4. Restart NVDA when prompted.
5. Open **NVDA menu > Preferences > Settings**.
6. Select **Document formatting**.

## Manual test checklist

- The settings category appears in NVDA Settings.
- The category tree receives focus and announces each item.
- Up and Down Arrow switch between categories.
- Tab moves from the tree to the current category options.
- Check list items can be toggled with Space.
- Combo boxes expose the expected choices.
- Spin controls expose the expected value and range.
- Pressing OK saves changes.
- Pressing Cancel discards changes.
- Saved values are reflected in NVDA's built-in Document Formatting settings.

## Known limitations

- There is no settings search integration.
- There is no custom font attributes list.

