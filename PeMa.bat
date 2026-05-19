@echo off
chcp 65001 > nul
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   PeMa Launcher
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$repo = 'dreysed/PeMa'; " ^
"$dataDir = \"$env:LOCALAPPDATA\PeMa\"; " ^
"$versionFile = \"$dataDir\.version\"; " ^
"$installer = \"$dataDir\PeMa-Setup.exe\"; " ^
"$appExe = \"$env:LOCALAPPDATA\Programs\PeMa\PeMa.exe\"; " ^
"if (-not (Test-Path $appExe)) { $appExe = \"$env:ProgramFiles\PeMa\PeMa.exe\" }; " ^
"if (-not (Test-Path $dataDir)) { New-Item -ItemType Directory -Path $dataDir | Out-Null }; " ^
"Write-Host 'Проверка обновлений...'; " ^
"try { " ^
"  $release = Invoke-RestMethod \"https://api.github.com/repos/$repo/releases/latest\"; " ^
"  $latest = $release.tag_name; " ^
"  $current = if (Test-Path $versionFile) { Get-Content $versionFile } else { 'none' }; " ^
"  if ($latest -ne $current) { " ^
"    Write-Host \"Скачиваем PeMa $latest...\"; " ^
"    $url = \"https://github.com/$repo/releases/download/$latest/PeMa-Setup.exe\"; " ^
"    Invoke-WebRequest $url -OutFile $installer -UseBasicParsing; " ^
"    Write-Host 'Устанавливаем...'; " ^
"    Start-Process $installer -ArgumentList '/VERYSILENT /NORESTART' -Wait; " ^
"    Set-Content $versionFile $latest; " ^
"    Write-Host \"Обновлено до $latest\" " ^
"  } else { Write-Host \"Актуальная версия ($current)\" } " ^
"} catch { Write-Host 'Нет интернета — запускаем текущую версию' }; " ^
"Write-Host ''; Write-Host 'Запуск PeMa...'; " ^
"if (Test-Path $appExe) { Start-Process $appExe } else { Write-Host 'Приложение не найдено. Запустите PeMa.bat ещё раз для установки.' }"
