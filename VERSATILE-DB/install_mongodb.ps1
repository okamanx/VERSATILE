# MongoDB 4.4 Installation Script for Windows
# This script downloads and installs MongoDB 4.4 Community Edition

Write-Host "🚀 Installing MongoDB 4.4..." -ForegroundColor Green

# Create MongoDB directory
$mongodbDir = "C:\mongodb"
$dataDir = "C:\mongodb\data"
$logDir = "C:\mongodb\log"

if (!(Test-Path $mongodbDir)) {
    New-Item -ItemType Directory -Path $mongodbDir -Force
    Write-Host "✅ Created MongoDB directory: $mongodbDir" -ForegroundColor Green
}

if (!(Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force
    Write-Host "✅ Created data directory: $dataDir" -ForegroundColor Green
}

if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force
    Write-Host "✅ Created log directory: $logDir" -ForegroundColor Green
}

# Download MongoDB 4.4
$mongodbUrl = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.24.zip"
$zipPath = "$env:TEMP\mongodb-windows-x86_64-4.4.24.zip"
$extractPath = "$env:TEMP\mongodb"

Write-Host "📥 Downloading MongoDB 4.4..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri $mongodbUrl -OutFile $zipPath
    Write-Host "✅ Download completed" -ForegroundColor Green
} catch {
    Write-Host "❌ Download failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Extract MongoDB
Write-Host "📦 Extracting MongoDB..." -ForegroundColor Yellow
try {
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
    Write-Host "✅ Extraction completed" -ForegroundColor Green
} catch {
    Write-Host "❌ Extraction failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Copy MongoDB binaries
$mongodbBin = Get-ChildItem -Path $extractPath -Recurse -Name "mongod.exe" | Select-Object -First 1
$mongodbBinPath = Join-Path $extractPath $mongodbBin
$mongodbBinDir = Split-Path $mongodbBinPath

Write-Host "📋 Copying MongoDB binaries..." -ForegroundColor Yellow
try {
    Copy-Item -Path "$mongodbBinDir\*" -Destination $mongodbDir -Recurse -Force
    Write-Host "✅ Binaries copied to: $mongodbDir" -ForegroundColor Green
} catch {
    Write-Host "❌ Copy failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Add MongoDB to PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$mongodbDir*") {
    $newPath = "$currentPath;$mongodbDir"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "✅ Added MongoDB to PATH" -ForegroundColor Green
}

# Create MongoDB configuration
$configContent = "systemLog:`n   destination: file`n   path: $logDir\mongod.log`n   logAppend: true`nstorage:`n   dbPath: $dataDir`nnet:`n   bindIp: 127.0.0.1`n   port: 27017"

$configPath = "$mongodbDir\mongod.cfg"
$configContent | Out-File -FilePath $configPath -Encoding UTF8
Write-Host "✅ Created MongoDB config: $configPath" -ForegroundColor Green

# Create batch file to start MongoDB
$startScript = "@echo off`necho Starting MongoDB...`ncd /d $mongodbDir`nmongod --config mongod.cfg`npause"

$startScriptPath = "$mongodbDir\start_mongodb.bat"
$startScript | Out-File -FilePath $startScriptPath -Encoding ASCII
Write-Host "✅ Created start script: $startScriptPath" -ForegroundColor Green

# Clean up
Remove-Item -Path $zipPath -Force -ErrorAction SilentlyContinue
Remove-Item -Path $extractPath -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎉 MongoDB 4.4 Installation Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Start MongoDB: $startScriptPath" -ForegroundColor White
Write-Host "2. Or run: $mongodbDir\mongod.exe --config $configPath" -ForegroundColor White
Write-Host "3. Test connection: python test_mongodb.py" -ForegroundColor White
Write-Host ""
Write-Host "📁 MongoDB installed at: $mongodbDir" -ForegroundColor Cyan
Write-Host "📁 Data directory: $dataDir" -ForegroundColor Cyan
Write-Host "📁 Log file: $logDir\mongod.log" -ForegroundColor Cyan 