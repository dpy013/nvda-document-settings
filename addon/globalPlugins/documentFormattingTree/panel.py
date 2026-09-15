import wx

import config
import ui
from gui import guiHelper, nvdaControls
from gui.settingsDialogs import SettingsPanel
from logHandler import log

try:
	import addonHandler
	addonHandler.initTranslation()
except Exception:
	_ = lambda text: text

try:
	from .options import buildCategories
except ImportError:
	from options import buildCategories


class DocumentFormattingTreePanel(SettingsPanel):
	title = _("Document formatting")

	def makeSettings(self, settingsSizer):
		docFormatting = config.conf["documentFormatting"]
		self._state = {key: docFormatting[key] for key in docFormatting}
		self._categories = buildCategories()
		self._optionItems = []
		self.optionList = None
		self.choiceEditorLabel = None
		self.choiceEditor = None
		self.spinEditorLabel = None
		self.spinEditor = None
		self.multiEditorLabel = None
		self.multiEditor = None
		self._activeEditorIndex = None
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
		self._optionItems = []
		self.optionList = None
		self.choiceEditorLabel = None
		self.choiceEditor = None
		self.spinEditorLabel = None
		self.spinEditor = None
		self.multiEditorLabel = None
		self.multiEditor = None
		self._activeEditorIndex = None

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

			self._optionItems = self._getCategoryItems(category)
			self.optionList = wx.ListBox(
				self.categorySettingsPanel,
				choices=self._getOptionListLabels(),
			)
			self.optionList.SetName(_("Options"))
			self.optionList.SetSelection(0)
			self.optionList.Bind(wx.EVT_LISTBOX, self._onOptionListChanged)
			self.optionList.Bind(wx.EVT_SET_FOCUS, self._onOptionListFocus)
			self.optionList.Bind(wx.EVT_KEY_DOWN, self._onOptionListKeyDown)
			self.categorySettingsSizer.Add(self.optionList, flag=wx.EXPAND | wx.BOTTOM, border=10)

			self.choiceEditorLabel = wx.StaticText(self.categorySettingsPanel)
			self.choiceEditor = wx.Choice(self.categorySettingsPanel)
			self.choiceEditor.Bind(wx.EVT_CHOICE, self._onChoiceChanged)
			self.categorySettingsSizer.Add(self.choiceEditorLabel)
			self.categorySettingsSizer.Add(self.choiceEditor, flag=wx.EXPAND | wx.BOTTOM, border=10)

			self.spinEditorLabel = wx.StaticText(self.categorySettingsPanel)
			self.spinEditor = wx.SpinCtrl(self.categorySettingsPanel)
			self.spinEditor.Bind(wx.EVT_SPINCTRL, self._onSpinChanged)
			self.spinEditor.Bind(wx.EVT_TEXT, self._onSpinChanged)
			self.categorySettingsSizer.Add(self.spinEditorLabel)
			self.categorySettingsSizer.Add(self.spinEditor, flag=wx.EXPAND | wx.BOTTOM, border=10)

			self.multiEditorLabel = wx.StaticText(self.categorySettingsPanel)
			self.multiEditor = nvdaControls.CustomCheckListBox(self.categorySettingsPanel)
			self.multiEditor.Bind(wx.EVT_CHECKLISTBOX, self._onMultiChanged)
			self.categorySettingsSizer.Add(self.multiEditorLabel)
			self.categorySettingsSizer.Add(self.multiEditor, flag=wx.EXPAND | wx.BOTTOM, border=10)

			self._setEditorVisible()

			self._updateDependentControls()
			self.categorySettingsPanel.Layout()
			self.Layout()
		finally:
			self.categorySettingsPanel.Thaw()

	def _getCategoryItems(self, category):
		boolByKey = {option.key: option for option in category.boolOptions}
		choiceByKey = {option.key: option for option in category.choiceOptions}
		spinByKey = {option.key: option for option in category.spinOptions}
		orders = {
			"Font": [
				("bool", "reportFontName"), ("bool", "reportFontSize"), ("choice", "fontAttributeReporting"),
				("bool", "reportSuperscriptsAndSubscripts"), ("bool", "reportEmphasis"), ("bool", "reportHighlight"),
				("bool", "reportStyle"), ("bool", "reportColor"),
			],
			"Document information": [
				("bool", "reportComments"), ("bool", "reportBookmarks"), ("bool", "reportRevisions"),
				("multi", "reportSpellingErrors2"),
			],
			"Pages and spacing": [
				("bool", "reportPage"), ("bool", "reportLineNumber"), ("choice", "reportLineIndentation"),
				("bool", "ignoreBlankLinesForRLI"), ("spin", "indentToneDuration"), ("bool", "reportParagraphIndentation"),
				("bool", "reportLineSpacing"), ("bool", "reportAlignment"),
			],
			"Table information": [
				("bool", "reportTables"), ("choice", "reportTableHeaders"), ("bool", "reportTableCellCoords"),
				("choice", "reportCellBorders"),
			],
			"Elements": [
				("bool", "reportHeadings"), ("bool", "reportLinks"), ("bool", "reportLinkType"), ("bool", "reportGraphics"),
				("bool", "reportLists"), ("bool", "reportBlockQuotes"), ("bool", "reportGroupings"), ("bool", "reportLandmarks"),
				("bool", "reportArticles"), ("bool", "reportFrames"), ("bool", "reportFigures"), ("bool", "reportClickable"),
				("bool", "detectFormatAfterCursor"),
			],
		}
		items = []
		for optionType, key in orders.get(category.label, []):
			option = {"bool": boolByKey, "choice": choiceByKey, "multi": choiceByKey, "spin": spinByKey}[optionType].get(key)
			if option is not None:
				items.append((optionType, option))
		return items

	def _isBoolOptionEnabled(self, option):
		if option.key == "ignoreBlankLinesForRLI":
			return self._state.get("reportLineIndentation", 0) != 0
		if option.key == "reportLinkType":
			return bool(self._state.get("reportLinks"))
		return True

	def _getOptionListLabels(self):
		labels = []
		for optionType, option in self._optionItems:
			label = option.label
			if optionType == "bool":
				state = _("checked") if bool(self._state.get(option.key)) else _("not checked")
				label = _("{label}, {state}").format(label=label, state=state)
				if not self._isBoolOptionEnabled(option):
					label = _("{label}, unavailable").format(label=label)
			labels.append(label)
		return labels

	def _refreshOptionList(self):
		if self.optionList is None:
			return
		selection = self.optionList.GetSelection()
		for index, label in enumerate(self._getOptionListLabels()):
			self.optionList.SetString(index, label)
		if selection != wx.NOT_FOUND and selection < len(self._optionItems):
			self.optionList.SetSelection(selection)

	def _setEditorVisible(self, choiceVisible=False, spinVisible=False, multiVisible=False):
		if self.choiceEditorLabel is not None:
			self.choiceEditorLabel.Show(choiceVisible)
		if self.choiceEditor is not None:
			self.choiceEditor.Show(choiceVisible)
		if self.spinEditorLabel is not None:
			self.spinEditorLabel.Show(spinVisible)
		if self.spinEditor is not None:
			self.spinEditor.Show(spinVisible)
		if self.multiEditorLabel is not None:
			self.multiEditorLabel.Show(multiVisible)
		if self.multiEditor is not None:
			self.multiEditor.Show(multiVisible)

	def _layoutCategorySettings(self):
		self.categorySettingsPanel.Layout()
		self.Layout()
		self._sendLayoutUpdatedEvent()

	def _getSelectedOptionItem(self):
		if self.optionList is None:
			return None, None
		selection = self.optionList.GetSelection()
		if selection == wx.NOT_FOUND or selection >= len(self._optionItems):
			return None, None
		return self._optionItems[selection]

	def _showEditorForSelectedOption(self):
		optionType, option = self._getSelectedOptionItem()
		if optionType == "choice":
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
			self._setEditorVisible(choiceVisible=True)
		elif optionType == "spin":
			self.spinEditorLabel.SetLabel(option.label)
			self.spinEditor.SetName(option.label)
			self.spinEditor.SetRange(option.minimum, option.maximum)
			self.spinEditor.SetValue(int(self._state.get(option.key, option.minimum)))
			self.spinEditor.option = option
			self._setEditorVisible(spinVisible=True)
		elif optionType == "multi":
			self.multiEditorLabel.SetLabel(option.label)
			self.multiEditor.SetName(option.label)
			self.multiEditor.Clear()
			for choice in option.choices:
				self.multiEditor.Append(choice)
			currentValue = self._state.get(option.key, 0)
			self.multiEditor.SetCheckedItems([
				index for index, value in enumerate(option.values)
				if currentValue & value
			])
			self.multiEditor.SetSelection(0)
			self.multiEditor.option = option
			self._setEditorVisible(multiVisible=True)
		else:
			self._setEditorVisible()
		self._layoutCategorySettings()

	def _onOptionListFocus(self, event):
		event.Skip()

	def _onOptionListChanged(self, event):
		self._activeEditorIndex = None
		self._setEditorVisible()
		self._layoutCategorySettings()
		event.Skip()

	def _onOptionListKeyDown(self, event):
		optionType, option = self._getSelectedOptionItem()
		key = event.GetKeyCode()
		if key == wx.WXK_SPACE and optionType == "bool":
			if not self._isBoolOptionEnabled(option):
				wx.CallAfter(ui.message, _("{label} unavailable").format(label=option.label))
				return
			checked = not bool(self._state.get(option.key))
			self._state[option.key] = checked
			self._refreshOptionList()
			self._updateDependentControls()
			wx.CallAfter(ui.message, _("{label} checked" if checked else "{label} not checked").format(label=option.label))
			return
		if key in (wx.WXK_SPACE, wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER) and optionType in ("choice", "spin", "multi"):
			self._activeEditorIndex = self.optionList.GetSelection()
			self._showEditorForSelectedOption()
			wx.CallAfter(ui.message, _("{label} selected").format(label=option.label))
			return
		if key == wx.WXK_TAB and not event.ShiftDown() and self._activeEditorIndex == self.optionList.GetSelection():
			if optionType == "choice":
				self.choiceEditor.SetFocus()
				return
			if optionType == "spin":
				self.spinEditor.SetFocus()
				return
			if optionType == "multi":
				self.multiEditor.SetFocus()
				return
		event.Skip()

	def _onMultiChanged(self, event):
		option = self.multiEditor.option
		value = 0
		for index, optionValue in enumerate(option.values):
			if self.multiEditor.IsChecked(index):
				value |= optionValue
		self._state[option.key] = value
		event.Skip()

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
		reportLineIndentation = self._state.get("reportLineIndentation", 0)
		self._refreshOptionList()
		if self.spinEditor is not None and getattr(self.spinEditor, "option", None):
			if self.spinEditor.option.key == "indentToneDuration":
				self.spinEditor.Enable(reportLineIndentation in (2, 3))

	def onSave(self):
		docFormatting = config.conf["documentFormatting"]
		for key, value in self._state.items():
			if key in docFormatting:
				docFormatting[key] = value
