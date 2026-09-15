import ast
import multiprocessing
import os
import shutil
import sys
import zipfile
from pathlib import Path

from SCons.Script import (
	AddOption,
	Alias,
	AlwaysBuild,
	BoolVariable,
	Clean,
	Default,
	Environment,
	Exit,
	GetOption,
	SetOption,
	Variables,
)

virtualEnv = os.getenv("VIRTUAL_ENV")
uv = os.getenv("uv")
if not virtualEnv or not uv or Path.cwd() != Path(virtualEnv).parent:
	print(
		"Error: SCons was started outside this project's uv Python virtual environment.\n"
		"Run SCons through scons.bat in the root of this repository.",
	)
	sys.exit(1)

ADDON_PACKAGE = "documentFormattingTree-0.1.0.nvda-addon"
ADDON_SOURCE_DIR = "addon"
BUILD_DIR = "build"
POT_FILE = "locale/documentFormattingTree.pot"
PROJECT_ID = "documentFormattingTree"
USER_GUIDE = f"{BUILD_DIR}/userGuide.md"

vars = Variables()
vars.Add(BoolVariable("release", "Whether this is a release build", False))
vars.Add("outputDir", "The directory where generated build outputs are placed", BUILD_DIR)

env = Environment(variables=vars, tools=["default"])
env.Decider("MD5-timestamp")

AddOption(
	"--all-cores",
	action="store_true",
	dest="all_cores",
	default=False,
	help="Use the maximum number of available processor cores",
)
numCores = multiprocessing.cpu_count()
if GetOption("all_cores"):
	SetOption("num_jobs", numCores)

unknown = vars.UnknownVariables().keys()
if unknown:
	print(f"Unknown command line variables: {unknown}")
	Exit(1)


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


def configureVenv(target, source, env):
	Path(str(target[0])).parent.mkdir(parents=True, exist_ok=True)
	Path(str(target[0])).write_text(f"{sys.executable}\n", encoding="utf-8")


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
		potFile.write('"POT-Creation-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n')
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


def buildDocument(target, source, env):
	Path(target[0].dir.abspath).mkdir(parents=True, exist_ok=True)
	with open(str(target[0]), "w", encoding="utf-8", newline="\n") as document:
		document.write(
			"# NVDA Document Settings user guide\n\n"
			"## What this add-on does\n\n"
			"NVDA Document Settings replaces NVDA's built-in Document formatting settings category "
			"while the add-on is installed. It keeps using NVDA's existing document formatting settings.\n\n"
			"## Open the settings\n\n"
			"1. Open the NVDA menu.\n"
			"2. Choose Preferences, then Settings.\n"
			"3. Select Document formatting.\n\n"
			"## Use the panel\n\n"
			"- Use the category tree to choose a document formatting group.\n"
			"- Tab to the options list for that group.\n"
			"- Press Space to toggle simple on/off options.\n"
			"- Press Space or Enter on options with more details, then Tab to the editor.\n"
			"- Press OK to save, or Cancel to discard changes.\n\n"
			"## Categories\n\n"
			"- Font\n"
			"- Document information\n"
			"- Pages and spacing\n"
			"- Table information\n"
			"- Elements\n"
		)


def cleanBuild(target, source, env):
	for path in [
		ADDON_PACKAGE,
		".sconsign.dblite",
		".ruff_cache",
		".uv-cache",
		"__pycache__",
		os.path.join("addon", "globalPlugins", "documentFormattingTree", "__pycache__"),
		BUILD_DIR,
	]:
		resolved = Path(path).resolve()
		root = Path.cwd().resolve()
		if not resolved.exists() or (resolved != root and root not in resolved.parents):
			continue
		if resolved.is_dir():
			shutil.rmtree(resolved)
		else:
			resolved.unlink()


configure = env.Command(".venv/.configured", ["pyproject.toml", "uv.lock", "uv.toml"], configureVenv)
addon = env.Command(ADDON_PACKAGE, getAddonSources(), buildAddon)
pot = env.Command(POT_FILE, getPythonSources(), buildPot)
document = env.Command(USER_GUIDE, ["readme.md"], buildDocument)
clear = env.Command("clear", [], cleanBuild)

Clean(addon, ADDON_PACKAGE)
Clean(document, BUILD_DIR)
Clean([addon, document, pot], [".ruff_cache", ".uv-cache"])

Alias("configure", configure)
Alias("building", [configure, addon])
Alias("pot", [configure, pot])
Alias("document", [configure, document])
AlwaysBuild(Alias("clear", clear))

Default("building")
