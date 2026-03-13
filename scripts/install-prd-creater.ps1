param(
    [string]$TargetDir = "",
    [string]$RepoUrl = "https://github.com/aEboli/PRD-Creat.git",
    [string]$Branch = "main",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($TargetDir)) {
    if ($env:CODEX_HOME) {
        $TargetDir = Join-Path $env:CODEX_HOME "skills"
    } else {
        $TargetDir = Join-Path $HOME ".codex\\skills"
    }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git is required to install prd-creater."
}

$tempDir = Join-Path $env:TEMP ("prd-creater-install-" + [guid]::NewGuid().ToString("N"))
$sourceDir = Join-Path $tempDir "skills\\prd-creater"
$destDir = Join-Path $TargetDir "prd-creater"

try {
    git clone --depth 1 --branch $Branch $RepoUrl $tempDir | Out-Host
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null

    if (Test-Path $destDir) {
        if (-not $Force) {
            throw "Target already exists: $destDir`nRe-run with -Force to overwrite it."
        }
        Remove-Item -Path $destDir -Recurse -Force
    }

    Copy-Item -Path $sourceDir -Destination $destDir -Recurse -Force

    Write-Host ""
    Write-Host "[OK] Installed prd-creater to $destDir"
    Write-Host "[TIP] Example prompt: Use `$prd-creater to turn this feature brief into a PRD."
} finally {
    if (Test-Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force
    }
}
