from __future__ import annotations

from pathlib import Path

REPOSITORY = "dpy013/nvda-document-settings"
BASE_URL = f"https://github.com/{REPOSITORY}"
WORKFLOW_URL = f"{BASE_URL}/actions/workflows/build.yml"
START = "<!-- download-links:start -->"
END = "<!-- download-links:end -->"

EN_BLOCK = f"""{START}
## Download links

- Stable release: {BASE_URL}/releases/latest
- Development builds: {WORKFLOW_URL}?query=branch%3Adev
- Testing builds: {WORKFLOW_URL}?query=branch%3Amain
- Pull request builds: {BASE_URL}/pulls

GitHub Actions artifacts may require signing in to GitHub.
{END}"""

ZH_BLOCK = f"""{START}
## 下载链接

- 稳定版：{BASE_URL}/releases/latest
- 开发版：{WORKFLOW_URL}?query=branch%3Adev
- 测试版：{WORKFLOW_URL}?query=branch%3Amain
- PR 构建：{BASE_URL}/pulls

下载 GitHub Actions 构建产物可能需要登录 GitHub。
{END}"""


def replace_block(content: str, block: str, before_heading: str) -> str:
	if START in content and END in content:
		start = content.index(START)
		end = content.index(END, start) + len(END)
		return f"{content[:start]}{block}{content[end:]}"
	marker = f"\n{before_heading}"
	if marker in content:
		return content.replace(marker, f"\n{block}\n{marker}", 1)
	return f"{content.rstrip()}\n\n{block}\n"


def update(path: str, block: str, before_heading: str) -> None:
	file_path = Path(path)
	content = file_path.read_text(encoding="utf-8")
	file_path.write_text(replace_block(content, block, before_heading).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
	update("readme.md", EN_BLOCK, "## Install for testing")
	update("readme.zh-CN.md", ZH_BLOCK, "## 测试安装")
