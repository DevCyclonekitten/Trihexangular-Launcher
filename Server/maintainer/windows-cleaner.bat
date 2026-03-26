@echo off
echo "Deleting paths: User\LocalLow\trihexangular-launcher, \User\.trihexangular-launcher"
rmdir %LOCALAPPDATA%\LocalLow\trihexangular-launcher
rmdir %USERPROFILE%\.trihexangular-launcher
pause