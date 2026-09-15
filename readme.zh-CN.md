# NVDA 文档设置

[English](readme.md)

这是一个实验性 NVDA 插件。安装后，它会替换 NVDA 内置的 **Document formatting** 设置分类。

这个插件用于验证一种新的文档格式设置界面：左侧使用分类树，右侧使用更紧凑的选项区域。

## 功能

- 安装插件后，替换 NVDA 内置的 **Document formatting** 设置分类。
- 使用树视图浏览文档格式设置分类。
- 使用列表显示布尔开关选项。
- 使用组合框显示多值报告模式。
- 使用数值调节控件显示数字选项。
- 继续读写 NVDA 现有的 `documentFormatting` 配置节。

## 要求

- 最低测试 NVDA 版本：2026.1
- 最新测试 NVDA 版本：2027.1

## 开发说明

开发者可以阅读 [DEVELOPMENT.md](DEVELOPMENT.md)，了解插件动机、界面模型、实现概览和测试重点。

## 开发环境

构建命令会自动配置并使用本地 uv 虚拟环境。如需显式配置，运行：

```powershell
.\scons.bat configure
```

检查格式和 lint：

```powershell
uv run ruff check .
uv run ruff format --check .
```

## 构建

在项目目录运行：

```powershell
.\scons.bat building
```

这会按需配置 `.venv`，并生成：

```text
documentFormattingTree-<version>.nvda-addon
```

## 版本格式

构建使用基于日期的版本号：

- 稳定版：`YY.MM`，例如 `16.03` 或 `16.01`。
- 开发版：`YYYY.MM.DD-dev`，例如 `2026.07.09-dev`。
- 测试版：`YYYY.MM.DD-test`。
- PR 构建：`YYYY.MM.DD-pr<PR 编号>`。

GitHub Actions 会在后面自动追加 workflow run number，格式为 `.build<run number>`。
## 本地化模板

生成翻译模板：

```powershell
.\scons.bat pot
```

这会从源码中的 `_()` 字符串生成：

```text
locale/documentFormattingTree.pot
```

## 用户指南

生成用户指南：

```powershell
.\scons.bat document
```

输出文件：

```text
build/userGuide.md
```

## 清理

清理构建产物和本地构建缓存：

```powershell
.\scons.bat clear
```

该命令会保留 `.venv`，方便后续复用已配置的构建环境。

<!-- download-links:start -->
## 下载链接

- 稳定版：https://github.com/dpy013/nvda-document-settings/releases/latest
- 开发版：https://github.com/dpy013/nvda-document-settings/actions/workflows/build.yml?query=branch%3Adev
- 测试版：https://github.com/dpy013/nvda-document-settings/actions/workflows/build.yml?query=branch%3Amain
- PR 构建：https://github.com/dpy013/nvda-document-settings/pulls

下载 GitHub Actions 构建产物可能需要登录 GitHub。
<!-- download-links:end -->

## 测试安装

1. 构建插件。
2. 打开生成的 `.nvda-addon` 文件。
3. 允许 NVDA 安装插件。
4. 按提示重启 NVDA。
5. 打开 **NVDA 菜单 > 选项 > 设置**。
6. 选择 **Document formatting**。

## 手动测试清单

- 设置分类可以在 NVDA 设置中显示。
- 分类树可以获得焦点，并正确朗读每个项目。
- 上下方向键可以切换分类。
- Tab 可以从分类树移动到当前分类的选项列表。
- 开关选项可以用空格切换。
- 组合框显示预期选项。
- 数值控件显示预期的值和范围。
- 按 OK 可以保存更改。
- 按 Cancel 可以放弃更改。
- 保存的值可以反映到 NVDA 的原生 Document Formatting 设置中。

## 已知限制

- 暂无设置搜索集成。
- 暂无自定义字体属性列表。

