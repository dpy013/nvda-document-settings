# Developer notes

## Why this add-on exists

NVDA's built-in **Document formatting** settings panel exposes many related options in one long page. The page works, but it becomes harder to browse as more document formatting options are added. This add-on is a prototype for testing a more structured settings experience without changing NVDA core first.

The add-on replaces NVDA's built-in **Document formatting** category while it is installed. It keeps using NVDA's existing `documentFormatting` configuration keys, so testers can compare the new UI with the native behavior without migrating settings.

## Goals

- Keep the same setting names, groups, and configuration keys as NVDA where possible.
- Make the settings easier to browse with a category tree.
- Keep simple on/off options in a compact options list.
- Show detailed editors, such as combo boxes, spin controls, and multi-select lists, only when the user activates the related option.
- Make keyboard and screen reader behavior predictable for NVDA users.
- Keep the add-on small enough to be reviewed and possibly discussed upstream.

## Non-goals

- Do not create a new document formatting configuration system.
- Do not rename NVDA's native document formatting groups unless NVDA itself changes them.
- Do not duplicate settings that belong to other NVDA categories, such as Browse Mode settings.
- Do not add speculative customization that is not needed for testing this UI.

## Current UI model

The settings panel has two main areas:

1. A category tree on the left.
2. An options list on the right.

The category tree follows NVDA's native document formatting groups:

- Font
- Document information
- Pages and spacing
- Table information
- Elements

The options list contains the settings for the selected category. Boolean options can be toggled with Space. Options that need an editor can be activated with Space or Enter, then Tab moves to the editor.

## Implementation overview

Source files live under:

```text
addon/globalPlugins/documentFormattingTree/
```

Important files:

- `__init__.py`
  - Registers the global plugin.
  - Replaces NVDA's native `DocumentFormattingPanel` in `NVDASettingsDialog.categoryClasses` while the add-on is active.
  - Restores the native panel when the add-on is terminated.
- `options.py`
  - Defines the document formatting categories and options.
  - Keeps option labels and keys close to NVDA's native `DocumentFormattingPanel`.
- `panel.py`
  - Builds the tree/list settings UI.
  - Reads initial values from `config.conf["documentFormatting"]`.
  - Writes changed values back on Save.

## Build and checks

The project uses uv for the local development environment and SCons for packaging.

```powershell
uv sync --dev
uv run ruff check .
uv run ruff format --check .
uv run scons
```

The generated add-on package is:

```text
documentFormattingTree-0.1.0.nvda-addon
```

## Localization

Generate the translation template with:

```powershell
uv run scons locale/documentFormattingTree.pot
```

The template is generated from translatable `_()` strings in the add-on source.

## Testing notes

Manual testing should focus on NVDA speech and keyboard behavior:

- The add-on replaces the native Document formatting settings category.
- The category tree announces the current category clearly.
- The options list does not announce unrelated editor labels while browsing plain boolean items.
- Space toggles boolean options and reports the new state.
- Space or Enter activates options that have detailed editors.
- Tab moves into the active editor only after activation.
- OK saves values into NVDA's `documentFormatting` config section.
- Cancel discards changes.

## NVDA version support

The current target range is:

- Minimum tested NVDA version: 2026.1
- Last tested NVDA version: 2027.1

When NVDA changes the native `DocumentFormattingPanel`, update `options.py` and the grouping/order logic in `panel.py` to match NVDA first, then adjust the prototype UI only where needed.
