# Simple MongoDB 4.4 Download Script
Write-Host "🚀 Downloading MongoDB 4.4..." -ForegroundColor Green

# Create directories
$mongodbDir = "C:\mongodb"
$dataDir = "C:\mongodb\data"
$logDir = "C:\mongodb\log"

New-Item -ItemType Directory -Path $mongodbDir -Force | Out-Null
New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

Write-Host "✅ Created directories" -ForegroundColor Green

# Download MongoDB
$url = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.24.zip"
$zipPath = "$env:TEMP\mongodb.zip"
$extractPath = "$env:TEMP\mongodb-extract"

Write-Host "📥 Downloading MongoDB..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $url -OutFile $zipPath

Write-Host "📦 Extracting..." -ForegroundColor Yellow
Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force

# Find and copy mongod.exe
$mongodPath = Get-ChildItem -Path $extractPath -Recurse -Name "mongod.exe" | Select-Object -First 1
$mongodDir = Split-Path (Join-Path $extractPath $mongodPath)

Write-Host "📋 Copying files..." -ForegroundColor Yellow
Copy-Item -Path "$mongodDir\*" -Destination $mongodbDir -Recurse -Force

# Create config file
$config = @"
systemLog:
   destination: file
   path: C:\mongodb\log\mongod.log
   logAppend: true
storage:
   dbPath: C:\mongodb\data
net:
   bindIp: 127.0.0.1
   port: 27017
"@

$config | Out-File -FilePath "$mongodbDir\mongod.cfg" -Encoding UTF8

# Create start script
$startScript = @"
@echo off
echo Starting MongoDB...
cd /d C:\mongodb
mongod.exe --config mongod.cfg
pause
"@

$startScript | Out-File -FilePath "$mongodbDir\start_mongodb.bat" -Encoding ASCII

# Cleanup
Remove-Item -Path $zipPath -Force -ErrorAction SilentlyContinue
Remove-Item -Path $extractPath -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎉 MongoDB 4.4 Downloaded Successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 To start MongoDB:" -ForegroundColor Yellow
Write-Host "1. Open Command Prompt as Administrator" -ForegroundColor White
Write-Host "2. Run: C:\mongodb\start_mongodb.bat" -ForegroundColor White
Write-Host "3. Or manually: cd C:\mongodb && mongod.exe --config mongod.cfg" -ForegroundColor White
Write-Host ""
Write-Host "📁 MongoDB location: C:\mongodb" -ForegroundColor Cyan
Write-Host "📁 Data directory: C:\mongodb\data" -ForegroundColor Cyan
Write-Host "📁 Log file: C:\mongodb\log\mongod.log" -ForegroundColor Cyan 