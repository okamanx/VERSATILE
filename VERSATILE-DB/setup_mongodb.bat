@echo off
echo 🚀 Setting up MongoDB 4.4...

REM Create directories
if not exist "C:\mongodb" mkdir "C:\mongodb"
if not exist "C:\mongodb\data" mkdir "C:\mongodb\data"
if not exist "C:\mongodb\log" mkdir "C:\mongodb\log"

echo ✅ Created directories

REM Download MongoDB
echo 📥 Downloading MongoDB...
powershell -Command "Invoke-WebRequest -Uri 'https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.24.zip' -OutFile '%TEMP%\mongodb.zip'"

REM Extract
echo 📦 Extracting...
powershell -Command "Expand-Archive -Path '%TEMP%\mongodb.zip' -DestinationPath '%TEMP%\mongodb-extract' -Force"

REM Find and copy mongod.exe
for /r "%TEMP%\mongodb-extract" %%i in (mongod.exe) do (
    echo 📋 Copying files from %%~dpi
    xcopy "%%~dpi*" "C:\mongodb\" /E /Y
    goto :found
)
:found

REM Create config file
echo Creating config file...
(
echo systemLog:
echo    destination: file
echo    path: C:\mongodb\log\mongod.log
echo    logAppend: true
echo storage:
echo    dbPath: C:\mongodb\data
echo net:
echo    bindIp: 127.0.0.1
echo    port: 27017
) > "C:\mongodb\mongod.cfg"

REM Create start script
echo Creating start script...
(
echo @echo off
echo echo Starting MongoDB...
echo cd /d C:\mongodb
echo mongod.exe --config mongod.cfg
echo pause
) > "C:\mongodb\start_mongodb.bat"

REM Cleanup
del "%TEMP%\mongodb.zip" 2>nul
rmdir /s /q "%TEMP%\mongodb-extract" 2>nul

echo.
echo 🎉 MongoDB 4.4 Setup Complete!
echo.
echo 📋 To start MongoDB:
echo 1. Open Command Prompt as Administrator
echo 2. Run: C:\mongodb\start_mongodb.bat
echo 3. Or manually: cd C:\mongodb ^&^& mongod.exe --config mongod.cfg
echo.
echo 📁 MongoDB location: C:\mongodb
echo 📁 Data directory: C:\mongodb\data
echo 📁 Log file: C:\mongodb\log\mongod.log
echo.
pause 