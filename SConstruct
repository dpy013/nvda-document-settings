import ast
import os
import zipfile
from datetime import datetime, timezone

from SCons.Script import Command, Default

ADDON_PACKAGE = "documentFormattingTree-0.1.0.nvda-addon"
ADDON_SOURCE_DIR = "addon"
POT_FILE = "locale/documentFormattingTree.pot"
PROJECT_ID = "documentFormattingTree"


def getAddonSources():
	sources = []
	for root, dirs, files in os.walk(ADDON_SOURCE_DIR):
		dirs[:] = [d for d in dirs if d != "__pycache__"]
		for fileName in files:
			if fileName.endswith(".pyc"):
				continue
			sources.append(os.path.join(root, fileName))
	return sources


def getPythonSources():
	return [source for source in getAddonSources() if source.endswith(".py")]


def buildAddon(target, source, env):
	with zipfile.ZipFile(str(target[0]), "w", zipfile.ZIP_DEFLATED) as addonZip:
		for filePath in getAddonSources():
			archivePath = os.path.relpath(filePath, ADDON_SOURCE_DIR)
			addonZip.write(filePath, archivePath)


def escapePotString(text):
	return text.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t")


def writePotString(output, prefix, text):
	output.write(f'{prefix} "{escapePotString(text)}"\n')


def findMessages(filePath):
	with open(filePath, "r", encoding="utf-8") as sourceFile:
		tree = ast.parse(sourceFile.read(), filename=filePath)
	for node in ast.walk(tree):
		if not isinstance(node, ast.Call):
			continue
		if not isinstance(node.func, ast.Name) or node.func.id != "_":
			continue
		if not node.args or not isinstance(node.args[0], ast.Constant) or not isinstance(node.args[0].value, str):
			continue
		yield node.lineno, node.args[0].value


def buildPot(target, source, env):
	messages = {}
	for filePath in getPythonSources():
		for lineNumber, message in findMessages(filePath):
			messages.setdefault(message, []).append((filePath.replace(os.sep, "/"), lineNumber))

	os.makedirs(os.path.dirname(str(target[0])), exist_ok=True)
	created = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M+0000")
	with open(str(target[0]), "w", encoding="utf-8", newline="\n") as potFile:
		potFile.write("# Translations template for NVDA Document Settings.\n")
		potFile.write("# Copyright (C) 2026 NVDA Document Settings contributors\n")
		potFile.write("# This file is distributed under the same license as the NVDA Document Settings add-on.\n")
		potFile.write("# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.\n")
		potFile.write("#\n")
		writePotString(potFile, "msgid", "")
		potFile.write('msgstr ""\n')
		potFile.write(f'"Project-Id-Version: {PROJECT_ID} 0.1.0\\n"\n')
		potFile.write('"Report-Msgid-Bugs-To: \\n"\n')
		potFile.write(f'"POT-Creation-Date: {created}\\n"\n')
		potFile.write('"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n')
		potFile.write('"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n')
		potFile.write('"Language-Team: LANGUAGE <LL@li.org>\\n"\n')
		potFile.write('"MIME-Version: 1.0\\n"\n')
		potFile.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
		potFile.write('"Content-Transfer-Encoding: 8bit\\n"\n\n')

		for message in sorted(messages):
			for filePath, lineNumber in messages[message]:
				potFile.write(f"#: {filePath}:{lineNumber}\n")
			writePotString(potFile, "msgid", message)
			potFile.write('msgstr ""\n\n')


addon = Command(ADDON_PACKAGE, getAddonSources(), buildAddon)
pot = Command(POT_FILE, getPythonSources(), buildPot)
Default(addon)
