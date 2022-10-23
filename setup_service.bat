:: Assumes nssm.exe is in PATH

set PROJET_ROOT=%~dp0
set SERVICE="heartbeat"
set PYTHON_EXEC="%PROJET_ROOT%env\Scripts\python.exe"
set ENTRYPOINT="%PROJECT_ROOT%heartbeat.py"

:: Remove any existing service
nssm remove %SERVICE% confirm

:: Install service
nssm install %SERVICE% %PYTHON_EXEC% ".\heartbeat.py" ".\gcloud-logger-key.json"
nssm set %SERVICE% AppDirectory %PROJET_ROOT%
nssm set %SERVICE% Description "Writes heartbeat log to Google Cloud Logging on a schedule"
nssm set %SERVICE% Start "SERVICE_DELAYED_AUTO_START"

:: Start service
nssm start %SERVICE%
