[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,

    [Parameter(Mandatory = $true)]
    [string]$Label,

    [string]$BackupDir,
    [string]$ReceiptPath,

    [switch]$ConfirmedSaved
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $ConfirmedSaved) {
    throw 'Refusing to checkpoint: first verify the live After Effects project is saved, then pass -ConfirmedSaved.'
}

$project = Get-Item -LiteralPath $ProjectPath
if ($project.Extension -ne '.aep') {
    throw "Expected an .aep file, got: $($project.FullName)"
}

if (-not $BackupDir) {
    $BackupDir = Join-Path $project.Directory.FullName 'Backups'
}
New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$safeLabel = ($Label -replace '[^A-Za-z0-9_-]+', '_').Trim('_')
if (-not $safeLabel) { throw 'Label becomes empty after filename sanitization.' }

$baseName = [System.IO.Path]::GetFileNameWithoutExtension($project.Name)
$backupName = '{0}_{1}_{2}.aep' -f $baseName, $safeLabel, $stamp
$backupPath = Join-Path (Resolve-Path -LiteralPath $BackupDir).Path $backupName
if (Test-Path -LiteralPath $backupPath) {
    throw "Backup already exists: $backupPath"
}

if (-not $ReceiptPath) {
    $ReceiptPath = [System.IO.Path]::ChangeExtension($backupPath, '.checkpoint.json')
}
$ReceiptPath = [System.IO.Path]::GetFullPath($ReceiptPath)
if ([System.IO.Path]::GetExtension($ReceiptPath) -ine '.json') {
    throw "ReceiptPath must end in .json: $ReceiptPath"
}
if ($ReceiptPath.Equals($project.FullName, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'ReceiptPath must not be the canonical AEP path.'
}
if ($ReceiptPath.Equals([System.IO.Path]::GetFullPath($backupPath), [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'ReceiptPath must not be the backup AEP path.'
}
if (Test-Path -LiteralPath $ReceiptPath) {
    throw "Refusing to overwrite an existing receipt: $ReceiptPath"
}

$sourceHash = (Get-FileHash -LiteralPath $project.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Copy-Item -LiteralPath $project.FullName -Destination $backupPath
$backup = Get-Item -LiteralPath $backupPath
$backupHash = (Get-FileHash -LiteralPath $backup.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
if ($sourceHash -ne $backupHash -or $project.Length -ne $backup.Length) {
    throw 'Checkpoint verification failed: source and backup differ.'
}

$ae = @(Get-Process -Name AfterFX,AfterFX.com -ErrorAction SilentlyContinue)
$aePrivateBytes = 0L
foreach ($process in $ae) { $aePrivateBytes += $process.PrivateMemorySize64 }
$os = Get-CimInstance Win32_OperatingSystem

$receipt = [ordered]@{
    ok = $true
    localTimestamp = (Get-Date).ToString('o')
    timestampLabel = $stamp
    timezone = [System.TimeZoneInfo]::Local.Id
    source = $project.FullName
    sourceBytes = $project.Length
    sourceSha256 = $sourceHash
    backup = $backup.FullName
    backupBytes = $backup.Length
    backupSha256 = $backupHash
    label = $safeLabel
    afterEffectsProcessCount = $ae.Count
    afterEffectsPrivateRamGB = [math]::Round($aePrivateBytes / 1GB, 2)
    windowsAvailableRamGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
}

$receiptDir = Split-Path -Parent $ReceiptPath
if ($receiptDir) { New-Item -ItemType Directory -Path $receiptDir -Force | Out-Null }
$receipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ReceiptPath -Encoding UTF8
$receipt | ConvertTo-Json -Depth 5
