param(
    [string]$TaskName = 'RGB-HSI-SR-Control',
    [string]$ControllerName = 'remote-training.py',
    [string]$PythonPath = ''
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$python = $PythonPath
if (-not $python) { $python = Join-Path $root '.venv\Scripts\pythonw.exe' }
if (-not (Test-Path -LiteralPath $python)) { throw "Python not found: $python" }
$controller = Join-Path $PSScriptRoot $ControllerName
$task = $TaskName
if (Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue) { throw "Task already exists: $task. Choose a new TaskName." }
$user = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$escape = { param($s) [System.Security.SecurityElement]::Escape($s) }
$xml = @"
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
<Triggers><LogonTrigger><Enabled>true</Enabled><UserId>$(& $escape $user)</UserId></LogonTrigger></Triggers>
<Principals><Principal id="Author"><UserId>$(& $escape $user)</UserId><LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
<Settings><MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy><DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries><StopIfGoingOnBatteries>false</StopIfGoingOnBatteries><ExecutionTimeLimit>PT0S</ExecutionTimeLimit><Enabled>true</Enabled></Settings>
<Actions Context="Author"><Exec><Command>$(& $escape $python)</Command><Arguments>-u &quot;$(& $escape $controller)&quot; worker</Arguments><WorkingDirectory>$(& $escape $root)</WorkingDirectory></Exec></Actions>
</Task>
"@
$path = Join-Path $env:TEMP ('rgb-hsi-controller-' + [guid]::NewGuid().ToString() + '.xml')
$xml | Set-Content -Path $path -Encoding Unicode
& schtasks.exe /Create /TN $task /XML $path
if ($LASTEXITCODE -ne 0) { throw 'Controller registration failed' }
& schtasks.exe /Run /TN $task
if ($LASTEXITCODE -ne 0) { throw 'Controller startup failed' }
Remove-Item $path
Write-Host 'Controller only started. Training was NOT started. Keep trainer signed in; locking is OK.'
