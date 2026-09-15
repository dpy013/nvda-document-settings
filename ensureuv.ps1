[CmdletBinding()]
param(
	[Parameter(ValueFromRemainingArguments = $true)]
	[string[]]$UvArgs
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
[Version]$UvVersion = '0.12.5'

$hasUv = [bool](Get-Command uv -ErrorAction SilentlyContinue)
if (-not $hasUv) {
	Write-Error 'uv is not installed. Install uv first: https://docs.astral.sh/uv/getting-started/installation/'
}

try {
	$json = uv self version --output-format json | ConvertFrom-Json
	[Version]$installedVersion = $json.Version
}
catch {
	[Version]$installedVersion = '0.0.0'
}

if ($installedVersion -lt $UvVersion) {
	Write-Error "uv $UvVersion or newer is required. Installed version: $installedVersion"
}

& uv @UvArgs
exit $LASTEXITCODE
