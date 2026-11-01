# PowerShell script to register auto-start task in Windows Task Scheduler
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VbsPath = Join-Path $ScriptDir "run_hidden.vbs"

$Action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$VbsPath`""
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask -TaskName "THLawDekaGateway" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Auto-start THLawDeka-mobile FastAPI Gateway" -Force
Write-Host "[SUCCESS] THLawDekaGateway scheduled task registered successfully." -ForegroundColor Green
Write-Host "Task will automatically start on user logon in hidden background mode." -ForegroundColor Cyan
