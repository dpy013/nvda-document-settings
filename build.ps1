$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$out = Join-Path $root "documentFormattingTree-0.1.0.nvda-addon"
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("nvdaAddon_" + [guid]::NewGuid().ToString("N"))

if (Test-Path -LiteralPath $out) {
	Remove-Item -LiteralPath $out -Force
}

New-Item -ItemType Directory -Path $tmp | Out-Null
Copy-Item -LiteralPath (Join-Path $root "addon\manifest.ini") -Destination $tmp
New-Item -ItemType Directory -Path (Join-Path $tmp "globalPlugins") | Out-Null
Copy-Item -LiteralPath (Join-Path $root "addon\globalPlugins\documentFormattingTree") -Destination (Join-Path $tmp "globalPlugins") -Recurse -Exclude "__pycache__"

Compress-Archive -Path (Join-Path $tmp "*") -DestinationPath ($out + ".zip") -Force
Move-Item -LiteralPath ($out + ".zip") -Destination $out -Force
Remove-Item -LiteralPath $tmp -Recurse -Force

Write-Host "Built $out"
