from __future__ import annotations

import os
import re
from datetime import UTC, datetime
from pathlib import Path

VERSION_RE = re.compile(r'^version\s*=\s*".*"$', re.MULTILINE)


def get_build_date() -> datetime:
	value = os.environ.get("BUILD_DATE")
	if value:
		return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=UTC)
	return datetime.now(UTC)


def get_pr_number() -> str:
	for name in ("PR_NUMBER", "GITHUB_PR_NUMBER"):
		if os.environ.get(name):
			return os.environ[name]
	github_ref = os.environ.get("GITHUB_REF", "")
	match = re.match(r"refs/pull/(\d+)/", github_ref)
	return match.group(1) if match else "0"


def get_channel(default: str = "dev") -> str:
	return os.environ.get("ADDON_CHANNEL") or os.environ.get("VERSION_CHANNEL") or default


def get_version(channel: str | None = None) -> str:
	channel = channel or get_channel()
	date = get_build_date()
	if channel == "stable":
		version = date.strftime("%y.%m")
	elif channel in {"test", "beta"}:
		version = f"{date:%Y.%m.%d}-test"
	elif channel == "pr":
		version = f"{date:%Y.%m.%d}-pr{get_pr_number()}"
	else:
		version = f"{date:%Y.%m.%d}-dev"

	build_number = os.environ.get("GITHUB_RUN_NUMBER")
	if build_number:
		version = f"{version}.build{build_number}"
	return version


def update_version_in_file(path: str | Path, version: str) -> None:
	file_path = Path(path)
	content = file_path.read_text(encoding="utf-8")
	content = VERSION_RE.sub(f'version = "{version}"', content)
	file_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
	print(get_version())
