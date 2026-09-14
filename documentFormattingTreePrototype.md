# NVDA文档设置插件开发文档

## 1. 目标

本插件用于验证一种新的 NVDA 文档格式设置界面：

- **分类**：tree view。
- **开关**：每个分类一个复选列表。
- **模式**：组合框。
- **数值**：spin control。
- **默认值**：沿用当前 NVDA 的 `documentFormatting` 默认配置。
- **配置存储**：直接读写 `config.conf["documentFormatting"]`。

原型插件不替换 NVDA 内置“文档格式设置”页面，只新增一个实验设置面板，方便和原界面对比。

---

## 2. 基于 AddonTemplate 创建插件

模板仓库：

```text
https://github.com/nvdaaddons/AddonTemplate
```

插件统一名称：

```text
NVDA文档设置
```

显示名称：

```text
NVDA文档设置
```

推荐核心代码位置：

```text
addon/globalPlugins/documentFormattingTree/__init__.py
```

推荐文档位置：

```text
docs/documentFormattingTreePrototype.md
```

---

## 3. 总体布局

建议设置面板布局：

```text
NVDA文档设置

分类：
  字体与文本
  文档信息
  页面与间距
  表格信息
  元素
  高级

当前分类设置：
  开关选项列表
  模式组合框
  数值输入框
```

左侧 tree view 只负责分类；右侧根据当前分类显示对应控件。

---

## 4. 控件规则

| 设置类型 | 控件 |
|---|---|
| 分类 | tree view |
| 二值开关 | 复选列表 |
| 多模式选项 | 组合框 |
| 数值 | spin control |

不要用多个复选框拼出一个多模式设置。例如“关闭 / 语音 / 盲文 / 语音和盲文”应使用组合框。

---

## 5. 分类与设置项

### 5.1 字体与文本

#### 开关项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 字体名称 | `reportFontName` | 关闭 |
| 字体大小 | `reportFontSize` | 关闭 |
| 上标和下标 | `reportSuperscriptsAndSubscripts` | 关闭 |
| 强调 | `reportEmphasis` | 关闭 |
| 高亮文本 | `reportHighlight` | 开启 |
| 样式 | `reportStyle` | 关闭 |
| 颜色 | `reportColor` | 关闭 |

#### 模式项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 字体属性报告 | `fontAttributeReporting` | 关闭 |

组合框值：

```text
0 = 关闭
1 = 语音
2 = 盲文
3 = 语音和盲文
```

---

### 5.2 文档信息

#### 开关项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 注释 | `reportComments` | 开启 |
| 书签 | `reportBookmarks` | 开启 |
| 编辑修订 | `reportRevisions` | 开启 |

#### 模式项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 拼写或语法错误 | `reportSpellingErrors2` | 语音 |

当前 NVDA 使用 bitmask：

```text
1 = 语音
2 = 声音
4 = 盲文
```

原型中可用组合框表示：

```text
0 = 关闭
1 = 语音
2 = 声音
4 = 盲文
3 = 语音和声音
5 = 语音和盲文
6 = 声音和盲文
7 = 语音、声音和盲文
```

---

### 5.3 页面与间距

#### 开关项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 页码 | `reportPage` | 开启 |
| 行号 | `reportLineNumber` | 关闭 |
| 忽略空白行的行缩进报告 | `ignoreBlankLinesForRLI` | 关闭 |
| 段落缩进 | `reportParagraphIndentation` | 关闭 |
| 行距 | `reportLineSpacing` | 关闭 |
| 对齐方式 | `reportAlignment` | 关闭 |

#### 模式项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 行缩进报告 | `reportLineIndentation` | 关闭 |

组合框值：

```text
0 = 关闭
1 = 语音
2 = 提示音
3 = 语音和提示音
```

#### 数值项

| 显示名称 | 配置键 | 当前默认 | 范围 |
|---|---|---|---|
| 缩进提示音长度，毫秒 | `indentToneDuration` | 40 | 10 到 2000 |

启用规则：

- `reportLineIndentation` 为 `2` 或 `3` 时启用。
- `reportLineIndentation` 为 `0` 或 `1` 时禁用。

---

### 5.4 表格信息

#### 开关项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 表格 | `reportTables` | 开启 |
| 布局表格 | `includeLayoutTables` | 关闭 |
| 单元格坐标 | `reportTableCellCoords` | 开启 |

#### 模式项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 表格标题 | `reportTableHeaders` | 行和列 |
| 单元格边框 | `reportCellBorders` | 关闭 |

表格标题值：

```text
0 = 关闭
1 = 行和列
2 = 行
3 = 列
```

单元格边框值：

```text
0 = 关闭
1 = 样式
2 = 颜色和样式
```

---

### 5.5 元素

#### 开关项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 标题 | `reportHeadings` | 开启 |
| 链接 | `reportLinks` | 开启 |
| 链接类型 | `reportLinkType` | 开启 |
| 图形 | `reportGraphics` | 开启 |
| 列表 | `reportLists` | 开启 |
| 引用块 | `reportBlockQuotes` | 开启 |
| 分组 | `reportGroupings` | 开启 |
| 地标和区域 | `reportLandmarks` | 开启 |
| 文章 | `reportArticles` | 关闭 |
| 框架 | `reportFrames` | 开启 |
| 图表和说明 | `reportFigures` | 开启 |
| 可点击 | `reportClickable` | 开启 |

依赖规则：

- 如果 `reportLinks` 关闭，`reportLinkType` 应禁用。
- 保留 `reportLinkType` 的值，不因禁用而自动改写。

---

### 5.6 高级

#### 开关项

| 显示名称 | 配置键 | 当前默认 |
|---|---|---|
| 报告光标后格式变化，可能导致延迟 | `detectFormatAfterCursor` | 关闭 |

---

## 6. 交互规则

### 6.1 Tree view

Tree view 只切换分类，不直接修改配置。

键盘行为：

- 上下箭头：切换分类。
- Tab：进入当前分类设置。
- 选择分类时重建右侧设置区域。
- 选择分类不保存配置。

### 6.2 复选列表

复选列表用于当前分类中的二值开关。

键盘行为：

- 上下箭头：移动项目。
- 空格：切换当前项目。
- Tab：离开列表。

期望朗读：

```text
报告以下元素，列表
标题，选中，1 / 12
链接，选中，2 / 12
文章，未选中，9 / 12
```

### 6.3 组合框

组合框用于多模式设置。

示例：

```text
字体属性报告: 关闭 / 语音 / 盲文 / 语音和盲文
行缩进报告: 关闭 / 语音 / 提示音 / 语音和提示音
```

### 6.4 Spin control

Spin control 用于数值设置。

示例：

```text
缩进提示音长度，毫秒: 40
```

---

## 7. 配置保存策略

遵循 NVDA 设置面板常规行为：

1. 打开面板时，从 `config.conf["documentFormatting"]` 读取当前值。
2. 用户修改界面时，只更新面板内临时状态。
3. 用户点击 OK 或 Apply 时，在 `onSave` 写入配置。
4. 用户取消时，不写入配置。

不要在以下行为中写配置：

- tree view 焦点变化。
- 分类选择变化。
- 控件获得焦点。
- 列表项目移动。

---

## 8. 插件注册设置面板

核心代码位置：

```text
addon/globalPlugins/documentFormattingTree/__init__.py
```

示例：

```python
import globalPluginHandler
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        NVDASettingsDialog.categoryClasses.append(DocumentFormattingTreePanel)

    def terminate(self):
        try:
            NVDASettingsDialog.categoryClasses.remove(DocumentFormattingTreePanel)
        except ValueError:
            pass
        super().terminate()
```

---

## 9. 数据模型草案

```python
from dataclasses import dataclass


@dataclass
class BoolOption:
    label: str
    key: str


@dataclass
class ChoiceOption:
    label: str
    key: str
    choices: list[str]
    values: list[int]


@dataclass
class SpinOption:
    label: str
    key: str
    minimum: int
    maximum: int


@dataclass
class Category:
    label: str
    boolOptions: list[BoolOption]
    choiceOptions: list[ChoiceOption]
    spinOptions: list[SpinOption]
```

如果需要兼容旧 Python，避免使用过新的类型语法。

---

## 10. 设置面板结构草案

```python
import wx
import config
import guiHelper
from gui import nvdaControls
from gui.settingsDialogs import SettingsPanel


class DocumentFormattingTreePanel(SettingsPanel):
    title = _("NVDA文档设置")

    def makeSettings(self, settingsSizer):
        self._state = dict(config.conf["documentFormatting"])
        self._categories = self._buildCategories()

        helper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        helper.addItem(mainSizer, flag=wx.EXPAND, proportion=1)

        self.categoryTree = wx.TreeCtrl(
            self,
            style=wx.TR_HIDE_ROOT | wx.TR_SINGLE | wx.TR_HAS_BUTTONS,
        )
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

        firstItem = self.categoryTree.GetFirstChild(root)[0]
        self.categoryTree.SelectItem(firstItem)
        self._showCategory(0)
```

---

## 11. 分类切换逻辑草案

```python
def _onCategoryChanged(self, event):
    item = event.GetItem()
    index = self.categoryTree.GetItemData(item)
    self._showCategory(index)


def _clearSettingsPanel(self):
    for child in self.settingsPanel.GetChildren():
        child.Destroy()
    self.settingsSizer.Clear()


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
        checked = [
            i for i, option in enumerate(category.boolOptions)
            if self._state.get(option.key)
        ]
        self.boolList.SetCheckedItems(checked)
        self.boolList.Bind(wx.EVT_CHECKLISTBOX, self._onBoolListChanged)
        self.settingsSizer.Add(self.boolList, flag=wx.EXPAND | wx.BOTTOM, border=10)

    self._choiceControls = []
    for option in category.choiceOptions:
        label = wx.StaticText(self.settingsPanel, label=option.label)
        choice = wx.Choice(self.settingsPanel, choices=list(option.choices))
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

    self._spinControls = []
    for option in category.spinOptions:
        label = wx.StaticText(self.settingsPanel, label=option.label)
        spin = wx.SpinCtrl(
            self.settingsPanel,
            min=option.minimum,
            max=option.maximum,
            initial=int(self._state.get(option.key)),
        )
        spin.option = option
        spin.Bind(wx.EVT_SPINCTRL, self._onSpinChanged)
        self.settingsSizer.Add(label)
        self.settingsSizer.Add(spin, flag=wx.EXPAND | wx.BOTTOM, border=10)
        self._spinControls.append(spin)

    self._updateDependentControls()
    self.settingsPanel.Layout()
```

---

## 12. 状态更新逻辑草案

```python
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
```

---

## 13. 依赖逻辑草案

```python
def _updateDependentControls(self):
    reportIndent = self._state.get("reportLineIndentation", 0)
    enableToneDuration = reportIndent in (2, 3)

    for spin in getattr(self, "_spinControls", []):
        if spin.option.key == "indentToneDuration":
            spin.Enable(enableToneDuration)
```

链接类型依赖链接：

- 最小原型可以先不禁用单项，只记录问题。
- 如果控件支持单项禁用，再实现 `reportLinks=False` 时禁用 `reportLinkType`。

---

## 14. 保存配置

```python
def onSave(self):
    docFormatting = config.conf["documentFormatting"]
    for key, value in self._state.items():
        if key in docFormatting:
            docFormatting[key] = value
```

---

## 15. 无障碍要求

- 每个控件必须有清楚标签。
- Tree view 只做分类，不因焦点移动保存设置。
- 复选列表中，上下箭头只移动，空格才切换。
- 组合框必须读出当前值。
- Spin control 必须读出标签和值。
- 禁用控件应能被感知。
- 不依赖颜色、布局位置或视觉缩进表达唯一含义。

---

## 16. 测试计划

### 基础测试

- 启用插件后，NVDA 设置对话框出现新分类。
- 进入新分类不报错。
- Tree view 可切换分类。
- 每个分类显示正确的复选列表、组合框和 spin control。

### 默认值测试

确认默认值与当前 NVDA 一致：

- 标题：开启。
- 链接：开启。
- 链接类型：开启。
- 图形：开启。
- 列表：开启。
- 表格：开启。
- 单元格坐标：开启。
- 表格标题：行和列。
- 页码：开启。
- 注释：开启。
- 书签：开启。
- 编辑修订：开启。
- 高亮文本：开启。
- 文章：关闭。
- 字体名称：关闭。
- 字体大小：关闭。
- 字体属性：关闭。
- 行缩进报告：关闭。
- 单元格边框：关闭。

### 保存测试

- 修改复选项后点击 OK，重新打开确认保留。
- 修改组合框后点击 OK，重新打开确认保留。
- 修改 spin control 后点击 OK，重新打开确认保留。
- 在 NVDA 原生“文档格式设置”中确认对应配置同步变化。

### 取消测试

- 修改设置后点击取消。
- 重新打开确认没有保存。

### 键盘测试

只用键盘完成：

- 打开 NVDA 设置。
- 进入原型面板。
- 切换分类。
- 切换复选项。
- 修改组合框。
- 修改 spin control。
- 保存和取消。

---

## 17. 原型阶段不做

- 不替换 NVDA 原生“文档格式设置”面板。
- 不新增设置搜索。
- 不新增自定义字体属性列表。
- 不改变 NVDA 默认提示策略。
- 不新增独立配置文件。
- 不修改 NVDA 核心代码。
- 不做复杂的父级三态选择。

---

## 18. 实现优先级

1. 注册新的设置面板。
2. 显示分类 tree view。
3. 切换分类时显示对应复选列表。
4. 保存二值开关。
5. 添加组合框模式项。
6. 添加 spin control。
7. 添加依赖逻辑。
8. 完成键盘和屏幕阅读测试。

---

## 19. 核心结论

本原型使用以下结构：

```text
分类：tree view
开关：每个分类一个复选列表
模式：组合框
数值：spin control
默认值：沿用 NVDA 当前 documentFormatting 默认配置
```

目标是减少 Tab 次数、保留清晰分类，并避免把多模式设置硬拆成多个复选框。


