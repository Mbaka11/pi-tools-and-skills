[CmdletBinding()]
param(
    # Pass values > 0 to override. Zero means derive from installed RAM.
    [double]$WarnAEGB = 0,
    [double]$StopAEGB = 0,
    [double]$StopFreeGB = 0,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ae = @(Get-Process -Name AfterFX,AfterFX.com -ErrorAction SilentlyContinue)
$sumBytes = 0L
foreach ($process in $ae) { $sumBytes += $process.PrivateMemorySize64 }
$aeGB = if ($sumBytes) { [math]::Round($sumBytes / 1GB, 2) } else { 0 }
$os = Get-CimInstance Win32_OperatingSystem
$freeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)

$autoThresholds = $WarnAEGB -le 0 -or $StopAEGB -le 0 -or $StopFreeGB -le 0
if ($totalGB -ge 28 -and $totalGB -le 36) {
    $autoWarn = 18.0
    $autoStop = 20.0
    $autoFree = 6.0
} else {
    $autoWarn = [math]::Round($totalGB * 0.55, 1)
    $autoStop = [math]::Round($totalGB * 0.65, 1)
    $autoFree = [math]::Round($totalGB * 0.20, 1)
}
if ($WarnAEGB -le 0) { $WarnAEGB = $autoWarn }
if ($StopAEGB -le 0) { $StopAEGB = $autoStop }
if ($StopFreeGB -le 0) { $StopFreeGB = $autoFree }
if ($WarnAEGB -ge $StopAEGB) {
    throw 'WarnAEGB must be lower than StopAEGB.'
}

$status = if ($aeGB -ge $StopAEGB -or $freeGB -lt $StopFreeGB) {
    'pause'
} elseif ($aeGB -ge $WarnAEGB) {
    'warning'
} else {
    'safe'
}

$result = [ordered]@{
    localTimestamp = (Get-Date).ToString('o')
    timezone = [System.TimeZoneInfo]::Local.Id
    status = $status
    afterEffectsProcessCount = $ae.Count
    afterEffectsPrivateRamGB = $aeGB
    windowsAvailableRamGB = $freeGB
    windowsTotalRamGB = $totalGB
    thresholdMode = if ($autoThresholds) { 'auto-or-partial-override' } else { 'explicit' }
    thresholds = [ordered]@{
        warnAEGB = $WarnAEGB
        stopAEGB = $StopAEGB
        stopFreeGB = $StopFreeGB
    }
    processes = @($ae | ForEach-Object {
        [ordered]@{
            id = $_.Id
            title = $_.MainWindowTitle
            privateRamGB = [math]::Round($_.PrivateMemorySize64 / 1GB, 2)
            startTime = try { $_.StartTime.ToString('o') } catch { $null }
        }
    })
}

$json = $result | ConvertTo-Json -Depth 6
if ($OutputPath) {
    $dir = Split-Path -Parent $OutputPath
    if ($dir) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    if (Test-Path -LiteralPath $OutputPath) {
        throw "Refusing to overwrite existing RAM snapshot: $OutputPath"
    }
    $json | Set-Content -LiteralPath $OutputPath -Encoding UTF8
}
$json

if ($status -eq 'pause') { exit 2 }
if ($status -eq 'warning') { exit 1 }
exit 0
