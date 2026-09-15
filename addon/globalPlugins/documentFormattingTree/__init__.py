import wx

import config
import globalPluginHandler
import ui
from gui import guiHelper, nvdaControls
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
import gui.settingsDialogs as settingsDialogs
from logHandler import log

try:
	import addonHandler
	addonHandler.initTranslation()
except Exception:
	_ = lambda text: text


class Option:
	def __init__(self, label, key, choices=None, values=None, minimum=None, maximum=None):
		self.label = label
		self.key = key
		self.choices = choices or []
		self.values = values or []
		self.minimum = minimum
		self.maximum = maximum


class Category:
	def __init__(self, label, boolOptions=(), choiceOptions=(), spinOptions=()):
		self.label = label
		self.boolOptions = list(boolOptions)
		self.choiceOptions = list(choiceOptions)
		self.spinOptions = list(spinOptions)


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


class DocumentFormattingTreePanel(SettingsPanel):
	title = _("Document formatting")

	def makeSettings(self, settingsSizer):
		docFormatting = config.conf["documentFormatting"]
		self._state = {key: docFormatting[key] for key in docFormatting}
		self._categories = self._buildCategories()
		self._boolOptions = []
		self._choiceOptions = []
		self._choiceControls = []
		self._spinControls = []
		self._currentCategoryIndex = None

		helper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		helper.addItem(mainSizer, flag=wx.EXPAND, proportion=1)

		self.categoryTree = wx.TreeCtrl(self, style=wx.TR_HIDE_ROOT | wx.TR_SINGLE | wx.TR_HAS_BUTTONS)
		self.categoryTree.SetName(_("Categories"))
		mainSizer.Add(self.categoryTree, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=10)

		self.categorySettingsPanel = wx.Panel(self)
		self.categorySettingsSizer = wx.BoxSizer(wx.VERTICAL)
		self.categorySettingsPanel.SetSizer(self.categorySettingsSizer)
		mainSizer.Add(self.categorySettingsPanel, proportion=2, flag=wx.EXPAND)

		root = self.categoryTree.AddRoot("root")
		for index, category in enumerate(self._categories):
			item = self.categoryTree.AppendItem(root, category.label)
			self.categoryTree.SetItemData(item, index)

		firstItem, _cookie = self.categoryTree.GetFirstChild(root)
		self.categoryTree.SelectItem(firstItem)
		self.categoryTree.Bind(wx.EVT_TREE_SEL_CHANGED, self._onCategoryChanged)
		self._showCategory(0)

	def _buildCategories(self):
		return [
			Category(_("Font and text"), [
				Option(_("Font name"), "reportFontName"), Option(_("Font size"), "reportFontSize"),
				Option(_("Superscripts and subscripts"), "reportSuperscriptsAndSubscripts"), Option(_("Emphasis"), "reportEmphasis"),
				Option(_("Highlighted text"), "reportHighlight"), Option(_("Style"), "reportStyle"), Option(_("Color"), "reportColor"),
			], [Option(_("Font attribute reporting"), "fontAttributeReporting", [_('Off'), _('Speech'), _('Braille'), _('Speech and braille')], [0, 1, 2, 3])]),
			Category(_("Document information"), [Option(_("Comments"), "reportComments"), Option(_("Bookmarks"), "reportBookmarks"), Option(_("Editor revisions"), "reportRevisions")], [
				Option(_("Spelling or grammar errors"), "reportSpellingErrors2", [_('Off'), _('Speech'), _('Sound'), _('Braille'), _('Speech and sound'), _('Speech and braille'), _('Sound and braille'), _('Speech, sound and braille')], [0, 1, 2, 4, 3, 5, 6, 7])
			]),
			Category(_("Pages and spacing"), [
				Option(_("Page numbers"), "reportPage"), Option(_("Line numbers"), "reportLineNumber"), Option(_("Ignore blank lines for line indentation reporting"), "ignoreBlankLinesForRLI"),
				Option(_("Paragraph indentation"), "reportParagraphIndentation"), Option(_("Line spacing"), "reportLineSpacing"), Option(_("Alignment"), "reportAlignment"),
			], [Option(_("Line indentation reporting"), "reportLineIndentation", [_('Off'), _('Speech'), _('Tones'), _('Speech and tones')], [0, 1, 2, 3])], [
				Option(_("Indentation tone duration, milliseconds"), "indentToneDuration", minimum=10, maximum=2000)
			]),
			Category(_("Table information"), [Option(_("Tables"), "reportTables"), Option(_("Layout tables"), "includeLayoutTables"), Option(_("Cell coordinates"), "reportTableCellCoords")], [
				Option(_("Table headers"), "reportTableHeaders", [_('Off'), _('Rows and columns'), _('Rows'), _('Columns')], [0, 1, 2, 3]),
				Option(_("Cell borders"), "reportCellBorders", [_('Off'), _('Style'), _('Color and style')], [0, 1, 2]),
			]),
			Category(_("Elements"), [
				Option(_("Headings"), "reportHeadings"), Option(_("Links"), "reportLinks"), Option(_("Link type"), "reportLinkType"), Option(_("Graphics"), "reportGraphics"),
				Option(_("Lists"), "reportLists"), Option(_("Block quotes"), "reportBlockQuotes"), Option(_("Groupings"), "reportGroupings"), Option(_("Landmarks and regions"), "reportLandmarks"),
				Option(_("Articles"), "reportArticles"), Option(_("Frames"), "reportFrames"), Option(_("Figures and captions"), "reportFigures"), Option(_("Clickable"), "reportClickable"),
				Option(_("Report formatting changes after the cursor, may cause lag"), "detectFormatAfterCursor"),
			]),
		]

	def _onCategoryChanged(self, event):
		try:
			index = self.categoryTree.GetItemData(event.GetItem())
		except RuntimeError:
			return
		event.Skip()
		if isinstance(index, int) and index != self._currentCategoryIndex:
			wx.CallAfter(self._showCategory, index)

	def _clearSettingsPanel(self):
		for child in self.categorySettingsPanel.GetChildren():
			child.Destroy()
		self.categorySettingsSizer.Clear()
		self._boolOptions = []
		self._choiceOptions = []
		self._choiceControls = []
		self._spinControls = []
		self.choiceList = None
		self.choiceEditorLabel = None
		self.choiceEditor = None
		self.boolList = None

	def _showCategory(self, index):
		try:
			if not self.categorySettingsPanel:
				return
		except RuntimeError:
			return
		try:
			self._showCategoryUnsafe(index)
		except RuntimeError:
			return
		except Exception:
			log.exception("Error showing NVDA Document Settings category")

	def _showCategoryUnsafe(self, index):
		if index == self._currentCategoryIndex:
			return
		self._currentCategoryIndex = index
		self.categorySettingsPanel.Freeze()
		try:
			self._clearSettingsPanel()
			category = self._categories[index]

			hasBoolOptions = bool(category.boolOptions)
			if hasBoolOptions:
				self._boolOptions = category.boolOptions
				self.boolList = nvdaControls.CustomCheckListBox(self.categorySettingsPanel, choices=[option.label for option in category.boolOptions])
				self.boolList.SetName(_("Options"))
				self.boolList.SetCheckedItems([i for i, option in enumerate(category.boolOptions) if bool(self._state.get(option.key))])
				self.boolList.SetSelection(0)
				self.boolList.SetMinSize((-1, min(240, 28 * len(category.boolOptions))))
				self.boolList.Bind(wx.EVT_CHECKLISTBOX, self._onBoolListChanged)
				self.categorySettingsSizer.Add(self.boolList, flag=wx.EXPAND | wx.BOTTOM, border=10)

			if category.choiceOptions:
				self._choiceOptions = category.choiceOptions
				self.choiceList = wx.ListBox(self.categorySettingsPanel, choices=[option.label for option in category.choiceOptions])
				self.choiceList.SetName(_("Mode options"))
				self.choiceList.SetSelection(0)
				self.choiceList.Bind(wx.EVT_LISTBOX, self._onChoiceListChanged)
				self.choiceList.Bind(wx.EVT_SET_FOCUS, self._onChoiceListFocus)
				self.categorySettingsSizer.Add(self.choiceList, flag=wx.EXPAND | wx.BOTTOM, border=10)

				self.choiceEditorLabel = wx.StaticText(self.categorySettingsPanel)
				self.choiceEditor = wx.Choice(self.categorySettingsPanel)
				self.choiceEditor.Bind(wx.EVT_CHOICE, self._onChoiceChanged)
				self.categorySettingsSizer.Add(self.choiceEditorLabel)
				self.categorySettingsSizer.Add(self.choiceEditor, flag=wx.EXPAND | wx.BOTTOM, border=10)
				self._choiceControls.append(self.choiceEditor)
				self._showChoiceEditor(0)

			for option in category.spinOptions:
				label = wx.StaticText(self.categorySettingsPanel, label=option.label)
				spin = wx.SpinCtrl(self.categorySettingsPanel, min=option.minimum, max=option.maximum, initial=int(self._state.get(option.key, option.minimum)))
				spin.SetName(option.label)
				spin.option = option
				spin.Bind(wx.EVT_SPINCTRL, self._onSpinChanged)
				spin.Bind(wx.EVT_TEXT, self._onSpinChanged)
				self.categorySettingsSizer.Add(label)
				self.categorySettingsSizer.Add(spin, flag=wx.EXPAND | wx.BOTTOM, border=10)
				self._spinControls.append(spin)

			self._updateDependentControls()
			self.categorySettingsPanel.Layout()
			self.Layout()
		finally:
			self.categorySettingsPanel.Thaw()

	def _onBoolListChanged(self, event):
		index = event.GetSelection()
		option = self._boolOptions[index]
		checked = self.boolList.IsChecked(index)
		self._state[option.key] = checked
		wx.CallAfter(ui.message, _("{label} checked" if checked else "{label} not checked").format(label=option.label))
		self._updateDependentControls()
		event.Skip()

	def _onChoiceListFocus(self, event):
		selection = self.choiceList.GetSelection()
		if selection != wx.NOT_FOUND:
			self._showChoiceEditor(selection)
		event.Skip()

	def _onChoiceListChanged(self, event):
		self._showChoiceEditor(event.GetSelection())
		event.Skip()

	def _showChoiceEditor(self, index):
		option = self._choiceOptions[index]
		self.choiceEditorLabel.SetLabel(option.label)
		self.choiceEditor.SetName(option.label)
		self.choiceEditor.Clear()
		for choice in option.choices:
			self.choiceEditor.Append(choice)
		try:
			selection = option.values.index(self._state.get(option.key))
		except ValueError:
			selection = 0
		self.choiceEditor.SetSelection(selection)
		self.choiceEditor.option = option

	def _onChoiceChanged(self, event):
		choice = event.GetEventObject()
		option = choice.option
		self._state[option.key] = option.values[choice.GetSelection()]
		self._updateDependentControls()

	def _onSpinChanged(self, event):
		spin = event.GetEventObject()
		option = spin.option
		self._state[option.key] = spin.GetValue()
		event.Skip()

	def _updateDependentControls(self):
		enableToneDuration = self._state.get("reportLineIndentation", 0) in (2, 3)
		for spin in self._spinControls:
			if spin.option.key == "indentToneDuration":
				spin.Enable(enableToneDuration)

	def onSave(self):
		docFormatting = config.conf["documentFormatting"]
		for key, value in self._state.items():
			if key in docFormatting:
				docFormatting[key] = value
