import wx

import config
import globalPluginHandler
from gui import guiHelper, nvdaControls
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel

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
		if DocumentFormattingTreePanel not in NVDASettingsDialog.categoryClasses:
			NVDASettingsDialog.categoryClasses.append(DocumentFormattingTreePanel)

	def terminate(self):
		try:
			NVDASettingsDialog.categoryClasses.remove(DocumentFormattingTreePanel)
		except ValueError:
			pass
		super().terminate()


class DocumentFormattingTreePanel(SettingsPanel):
	title = _("NVDA文档设置")

	def makeSettings(self, settingsSizer):
		docFormatting = config.conf["documentFormatting"]
		self._state = {key: docFormatting[key] for key in docFormatting.keys()}
		self._categories = self._buildCategories()
		self._boolOptions = []
		self._choiceControls = []
		self._spinControls = []

		helper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		helper.addItem(mainSizer, flag=wx.EXPAND, proportion=1)

		self.categoryTree = wx.TreeCtrl(
			self,
			style=wx.TR_HIDE_ROOT | wx.TR_SINGLE | wx.TR_HAS_BUTTONS,
		)
		self.categoryTree.SetName(_("分类"))
		mainSizer.Add(self.categoryTree, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=10)

		self.settingsPanel = wx.Panel(self)
		self.settingsSizer = wx.BoxSizer(wx.VERTICAL)
		self.settingsPanel.SetSizer(self.settingsSizer)
		mainSizer.Add(self.settingsPanel, proportion=2, flag=wx.EXPAND)

		root = self.categoryTree.AddRoot("root")
		for index, category in enumerate(self._categories):
			item = self.categoryTree.AppendItem(root, category.label)
			self.categoryTree.SetItemData(item, index)

		self.categoryTree.Bind(wx.EVT_TREE_SEL_CHANGED, self._onCategoryChanged)
		firstItem, _cookie = self.categoryTree.GetFirstChild(root)
		self.categoryTree.SelectItem(firstItem)
		self._showCategory(0)

	def _buildCategories(self):
		return [
			Category(
				_("字体与文本"),
				boolOptions=[
					Option(_("字体名称"), "reportFontName"),
					Option(_("字体大小"), "reportFontSize"),
					Option(_("上标和下标"), "reportSuperscriptsAndSubscripts"),
					Option(_("强调"), "reportEmphasis"),
					Option(_("高亮文本"), "reportHighlight"),
					Option(_("样式"), "reportStyle"),
					Option(_("颜色"), "reportColor"),
				],
				choiceOptions=[
					Option(_("字体属性报告"), "fontAttributeReporting", [_("关闭"), _("语音"), _("盲文"), _("语音和盲文")], [0, 1, 2, 3]),
				],
			),
			Category(
				_("文档信息"),
				boolOptions=[
					Option(_("注释"), "reportComments"),
					Option(_("书签"), "reportBookmarks"),
					Option(_("编辑修订"), "reportRevisions"),
				],
				choiceOptions=[
					Option(_("拼写或语法错误"), "reportSpellingErrors2", [_("关闭"), _("语音"), _("声音"), _("盲文"), _("语音和声音"), _("语音和盲文"), _("声音和盲文"), _("语音、声音和盲文")], [0, 1, 2, 4, 3, 5, 6, 7]),
				],
			),
			Category(
				_("页面与间距"),
				boolOptions=[
					Option(_("页码"), "reportPage"),
					Option(_("行号"), "reportLineNumber"),
					Option(_("忽略空白行的行缩进报告"), "ignoreBlankLinesForRLI"),
					Option(_("段落缩进"), "reportParagraphIndentation"),
					Option(_("行距"), "reportLineSpacing"),
					Option(_("对齐方式"), "reportAlignment"),
				],
				choiceOptions=[
					Option(_("行缩进报告"), "reportLineIndentation", [_("关闭"), _("语音"), _("提示音"), _("语音和提示音")], [0, 1, 2, 3]),
				],
				spinOptions=[Option(_("缩进提示音长度，毫秒"), "indentToneDuration", minimum=10, maximum=2000)],
			),
			Category(
				_("表格信息"),
				boolOptions=[
					Option(_("表格"), "reportTables"),
					Option(_("布局表格"), "includeLayoutTables"),
					Option(_("单元格坐标"), "reportTableCellCoords"),
				],
				choiceOptions=[
					Option(_("表格标题"), "reportTableHeaders", [_("关闭"), _("行和列"), _("行"), _("列")], [0, 1, 2, 3]),
					Option(_("单元格边框"), "reportCellBorders", [_("关闭"), _("样式"), _("颜色和样式")], [0, 1, 2]),
				],
			),
			Category(
				_("元素"),
				boolOptions=[
					Option(_("标题"), "reportHeadings"),
					Option(_("链接"), "reportLinks"),
					Option(_("链接类型"), "reportLinkType"),
					Option(_("图形"), "reportGraphics"),
					Option(_("列表"), "reportLists"),
					Option(_("引用块"), "reportBlockQuotes"),
					Option(_("分组"), "reportGroupings"),
					Option(_("地标和区域"), "reportLandmarks"),
					Option(_("文章"), "reportArticles"),
					Option(_("框架"), "reportFrames"),
					Option(_("图表和说明"), "reportFigures"),
					Option(_("可点击"), "reportClickable"),
				],
			),
			Category(
				_("高级"),
				boolOptions=[Option(_("报告光标后格式变化，可能导致延迟"), "detectFormatAfterCursor")],
			),
		]

	def _onCategoryChanged(self, event):
		index = self.categoryTree.GetItemData(event.GetItem())
		if index is not None:
			self._showCategory(index)

	def _clearSettingsPanel(self):
		for child in self.settingsPanel.GetChildren():
			child.Destroy()
		self.settingsSizer.Clear()
		self._boolOptions = []
		self._choiceControls = []
		self._spinControls = []
		self.boolList = None

	def _showCategory(self, index):
		self._clearSettingsPanel()
		category = self._categories[index]

		title = wx.StaticText(self.settingsPanel, label=category.label)
		self.settingsSizer.Add(title, flag=wx.BOTTOM, border=8)

		if category.boolOptions:
			self._boolOptions = category.boolOptions
			self.boolList = nvdaControls.CustomCheckListBox(
				self.settingsPanel,
				choices=[option.label for option in category.boolOptions],
			)
			self.boolList.SetName(_("当前分类设置"))
			checked = [
				i for i, option in enumerate(category.boolOptions)
				if bool(self._state.get(option.key))
			]
			self.boolList.SetCheckedItems(checked)
			self.boolList.Bind(wx.EVT_CHECKLISTBOX, self._onBoolListChanged)
			self.settingsSizer.Add(self.boolList, flag=wx.EXPAND | wx.BOTTOM, border=10)

		for option in category.choiceOptions:
			label = wx.StaticText(self.settingsPanel, label=option.label)
			choice = wx.Choice(self.settingsPanel, choices=list(option.choices))
			choice.SetName(option.label)
			try:
				selection = option.values.index(self._state.get(option.key))
			except ValueError:
				selection = 0
			choice.SetSelection(selection)
			choice.option = option
			choice.Bind(wx.EVT_CHOICE, self._onChoiceChanged)
			self.settingsSizer.Add(label)
			self.settingsSizer.Add(choice, flag=wx.EXPAND | wx.BOTTOM, border=10)
			self._choiceControls.append(choice)

		for option in category.spinOptions:
			label = wx.StaticText(self.settingsPanel, label=option.label)
			spin = wx.SpinCtrl(
				self.settingsPanel,
				min=option.minimum,
				max=option.maximum,
				initial=int(self._state.get(option.key, option.minimum)),
			)
			spin.SetName(option.label)
			spin.option = option
			spin.Bind(wx.EVT_SPINCTRL, self._onSpinChanged)
			spin.Bind(wx.EVT_TEXT, self._onSpinChanged)
			self.settingsSizer.Add(label)
			self.settingsSizer.Add(spin, flag=wx.EXPAND | wx.BOTTOM, border=10)
			self._spinControls.append(spin)

		self._updateDependentControls()
		self.settingsPanel.Layout()
		self.Layout()

	def _onBoolListChanged(self, event):
		index = event.GetSelection()
		option = self._boolOptions[index]
		self._state[option.key] = self.boolList.IsChecked(index)
		self._updateDependentControls()

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




