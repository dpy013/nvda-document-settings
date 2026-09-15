import os
import zipfile

from SCons.Script import Command, Default

ADDON_PACKAGE = "documentFormattingTree-0.1.0.nvda-addon"
ADDON_SOURCE_DIR = "addon"


def getAddonSources():
	sources = []
	for root, dirs, files in os.walk(ADDON_SOURCE_DIR):
		dirs[:] = [d for d in dirs if d != "__pycache__"]
		for fileName in files:
			if fileName.endswith(".pyc"):
				continue
			sources.append(os.path.join(root, fileName))
	return sources


def buildAddon(target, source, env):
	with zipfile.ZipFile(str(target[0]), "w", zipfile.ZIP_DEFLATED) as addonZip:
		for filePath in getAddonSources():
			archivePath = os.path.relpath(filePath, ADDON_SOURCE_DIR)
			addonZip.write(filePath, archivePath)


addon = Command(ADDON_PACKAGE, getAddonSources(), buildAddon)
Default(addon)
