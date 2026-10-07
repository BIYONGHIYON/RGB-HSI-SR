param(
    [Parameter(Mandatory=$true)][string]$Checkpoint,
    [Parameter(Mandatory=$true)][string]$OutputDir,
    [string]$DataRoot = '',
    [string]$PreviousMetrics,
    [string]$Python = ''
)
$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not $Python) { $Python = Join-Path $root '.venv\Scripts\python.exe' }
if (-not $DataRoot) { $DataRoot = Join-Path $root 'SSA-MRN\data\dataset\RGB-HSI\LIB-HSI' }
$arguments = @((Join-Path $PSScriptRoot 'export_results.py'), '--checkpoint', $Checkpoint, '--output-dir', $OutputDir, '--data-root', $DataRoot)
if ($PreviousMetrics) { $arguments += @('--previous-metrics', $PreviousMetrics) }
& $Python @arguments
if ($LASTEXITCODE -ne 0) { throw 'Result export failed; report is incomplete' }
