@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ===============================
echo   Cero-Core Launcher
echo ===============================

REM -------------------------------
REM Paths / Config
REM -------------------------------
set "PYTHON=python"
set "VENV_PY=.venv\Scripts\python.exe"

set "ARDUINO_DIR=src\python\Arduino"
set "ARDUINO_CLI=%ARDUINO_DIR%\arduino-cli.exe"

REM Firmware sketch
set "SKETCH=%ARDUINO_DIR%\ReadMHzkHz\ReadMHzkHz.ino"

REM Board (UNO default)
set "FQBN=arduino:avr:uno"
REM For Nano (uncomment if needed)
REM set "FQBN=arduino:avr:nano"

set "BUILD_DIR=%ARDUINO_DIR%\_build"

REM -------------------------------
REM [1/5] Check Python
REM -------------------------------
echo.
echo [1/5] Checking Python...
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Installing...

    where winget >nul 2>&1
    if not errorlevel 1 (
        winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    ) else (
        set "PY_VER=3.12.7"
        set "PY_URL=https://www.python.org/ftp/python/%PY_VER%/python-%PY_VER%-amd64.exe"
        set "PY_EXE=%TEMP%\python-%PY_VER%-amd64.exe"

        powershell -NoProfile -ExecutionPolicy Bypass -Command ^
          "Invoke-WebRequest '%PY_URL%' -OutFile '%PY_EXE%'"

        if not exist "%PY_EXE%" (
            echo ERROR: Python download failed.
            pause
            exit /b 1
        )

        "%PY_EXE%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        del /q "%PY_EXE%" >nul 2>&1
    )

    %PYTHON% --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python installed but not visible in PATH.
        echo Restart terminal and run again.
        pause
        exit /b 1
    )
)
echo Python OK.

REM -------------------------------
REM [2/5] Setup venv + deps
REM -------------------------------
echo.
echo [2/5] Setting up Python environment...
if not exist "%VENV_PY%" (
    %PYTHON% -m venv .venv || (
        echo ERROR: venv creation failed.
        pause
        exit /b 1
    )
)

"%VENV_PY%" -m pip install --upgrade pip
"%VENV_PY%" -m pip install -r requirements.txt

REM -------------------------------
REM [3/5] Install arduino-cli
REM -------------------------------
echo.
echo [3/5] Checking arduino-cli...
if not exist "%ARDUINO_CLI%" (
    echo Installing arduino-cli...

    if not exist "%ARDUINO_DIR%" mkdir "%ARDUINO_DIR%"

    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
      "Invoke-WebRequest https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip -OutFile arduino-cli.zip"

    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
      "Expand-Archive arduino-cli.zip -DestinationPath '%ARDUINO_DIR%' -Force"

    del /q arduino-cli.zip >nul 2>&1

    if not exist "%ARDUINO_CLI%" (
        echo ERROR: arduino-cli install failed.
        pause
        exit /b 1
    )
)
echo arduino-cli ready.

REM -------------------------------
REM [4/5] Compile + Upload firmware
REM -------------------------------
echo.
echo [4/5] Preparing Arduino core + compiling + uploading...

if not exist "%SKETCH%" (
    echo ERROR: Sketch not found:
    echo %SKETCH%
    pause
    exit /b 1
)

"%ARDUINO_CLI%" config init >nul 2>&1
"%ARDUINO_CLI%" core update-index
if errorlevel 1 (
    echo ERROR: Failed to update core index.
    pause
    exit /b 1
)

"%ARDUINO_CLI%" core install arduino:avr >nul 2>&1

REM ---- COM detection ----
set "PORT="
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ports = Get-CimInstance Win32_PnPEntity | Where-Object { $_.Name -match '\(COM\d+\)' }; $usb = $ports | Where-Object { $_.DeviceID -match 'VID_2341|VID_2A03|VID_1A86|VID_0403' } | Select-Object -First 1; if ($usb) { [regex]::Match($usb.Name,'COM\d+').Value }" > "%TEMP%\cero_port.txt"

set /p PORT=<"%TEMP%\cero_port.txt"
del "%TEMP%\cero_port.txt" >nul 2>&1

if "%PORT%"=="" (
    echo ERROR: Could not detect Arduino COM port.
    echo Plug the board and try again.
    pause
    exit /b 1
)

echo.
echo ===============================
echo   Detected Serial Port
echo ===============================
echo Detected Arduino port: %PORT%
echo.
echo Please update your ports manually in:
echo   src\python\Assets\Settings.json
echo.
echo Set:
echo   serial_ports.kHz = %PORT%
echo   serial_ports.MHz = %PORT%
echo.
echo After editing Settings.json, come back here.
echo ===============================
pause

REM ---- Continue with compile/upload after user confirms ----
if not exist "%BUILD_DIR%" mkdir "%BUILD_DIR%"

echo.
echo --- Compiling ---
"%ARDUINO_CLI%" compile --fqbn %FQBN% "%SKETCH%" --output-dir "%BUILD_DIR%"
if errorlevel 1 (
    echo ERROR: Compile failed.
    pause
    exit /b 1
)

echo.
echo --- Uploading ---
"%ARDUINO_CLI%" upload -p %PORT% --fqbn %FQBN% "%SKETCH%"
if errorlevel 1 (
    echo ERROR: Upload failed.
    echo If Nano clone, switch FQBN to arduino:avr:nano.
    pause
    exit /b 1
)

echo Firmware uploaded successfully.

REM -------------------------------
REM [5/5] Done (NO GUI launch)
REM -------------------------------
echo.
echo. 
echo [5/5] You can now open the app manually when you want: 
echo .src\python\main.py
pause
exit /b 0