# NVDA Document Settings

[简体中文](readme.zh-CN.md)

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

## Developer notes

See [DEVELOPMENT.md](DEVELOPMENT.md) for the motivation, UI model, implementation overview, and testing notes.

## Development

Build commands configure and use the local uv virtual environment automatically. To configure it explicitly, run:

```powershell
.\scons.bat configure
```

Check formatting and linting:

```powershell
uv run ruff check .
uv run ruff format --check .
```

## Build

From this directory, run:

```powershell
.\scons.bat building
```

This configures `.venv` if needed and creates:

```text
documentFormattingTree-<version>.nvda-addon
```

## Version format

Builds use date-based versions:

- Stable release: `YY.MM`, for example `16.03` or `16.01`.
- Development build: `YYYY.MM.DD-dev`, for example `2026.07.09-dev`.
- Testing build: `YYYY.MM.DD-test`.
- Pull request build: `YYYY.MM.DD-pr<PR number>`.

GitHub Actions appends the workflow run number as `.build<run number>`.
## Localization template

Generate the translation template:

```powershell
.\scons.bat pot
```

This creates `locale/documentFormattingTree.pot` from translatable `_()` strings.

## User guide

Generate the user guide:

```powershell
.\scons.bat document
```

This creates:

```text
build/userGuide.md
```

## Clean

Clean build outputs and local build caches:

```powershell
.\scons.bat clear
```

This keeps `.venv` so the configured build environment can be reused.

<!-- download-links:start -->
## Download links

- Stable release: https://github.com/dpy013/nvda-document-settings/releases/latest
- Development builds: https://github.com/dpy013/nvda-document-settings/actions/workflows/build.yml?query=branch%3Adev
- Testing builds: https://github.com/dpy013/nvda-document-settings/actions/workflows/build.yml?query=branch%3Amain
- Pull request builds: https://github.com/dpy013/nvda-document-settings/pulls

GitHub Actions artifacts may require signing in to GitHub.
<!-- download-links:end -->

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

