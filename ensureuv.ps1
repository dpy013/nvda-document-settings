[CmdletBinding()]
param(
	[Parameter(ValueFromRemainingArguments = $true)]
	[string[]]$UvArgs
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$hasUv = [bool](Get-Command uv -ErrorAction SilentlyContinue)
if (-not $hasUv) {
	Write-Error 'uv is not installed. Install the latest stable uv first: https://docs.astral.sh/uv/getting-started/installation/'
}

& uv @UvArgs
exit $LASTEXITCODE
