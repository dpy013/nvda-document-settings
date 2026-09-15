import globalPluginHandler
from gui.settingsDialogs import NVDASettingsDialog
import gui.settingsDialogs as settingsDialogs

try:
	import addonHandler
	addonHandler.initTranslation()
except Exception:
	_ = lambda text: text

try:
	from .panel import DocumentFormattingTreePanel
except ImportError:
	from panel import DocumentFormattingTreePanel


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()
		self._replacedCategoryIndex = None
		self._replacedCategoryClass = None
		self._replaceNativeDocumentFormattingPanel()

	def _replaceNativeDocumentFormattingPanel(self):
		classes = NVDASettingsDialog.categoryClasses
		nativeClass = getattr(settingsDialogs, "DocumentFormattingPanel", None)
		for index, categoryClass in enumerate(classes):
			if categoryClass is DocumentFormattingTreePanel:
				return
			if categoryClass is nativeClass or categoryClass.__name__ == "DocumentFormattingPanel":
				self._replacedCategoryIndex = index
				self._replacedCategoryClass = categoryClass
				DocumentFormattingTreePanel.title = getattr(categoryClass, "title", DocumentFormattingTreePanel.title)
				classes[index] = DocumentFormattingTreePanel
				return
		classes.append(DocumentFormattingTreePanel)

	def terminate(self):
		classes = NVDASettingsDialog.categoryClasses
		if self._replacedCategoryIndex is not None and self._replacedCategoryClass is not None:
			try:
				if classes[self._replacedCategoryIndex] is DocumentFormattingTreePanel:
					classes[self._replacedCategoryIndex] = self._replacedCategoryClass
				else:
					classes.remove(DocumentFormattingTreePanel)
					classes.insert(self._replacedCategoryIndex, self._replacedCategoryClass)
			except (IndexError, ValueError):
				if self._replacedCategoryClass not in classes:
					classes.append(self._replacedCategoryClass)
		else:
			try:
				classes.remove(DocumentFormattingTreePanel)
			except ValueError:
				pass
		super().terminate()
