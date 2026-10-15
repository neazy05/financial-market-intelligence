@echo off
setlocal
cd /d "%~dp0"
echo ===============================================
echo Publish Financial Market Intelligence to GitHub
echo ===============================================
echo.
where git >nul 2>nul
if errorlevel 1 (
  echo ERROR: Git is not installed or not available in PATH.
  echo Install Git for Windows, then run this file again.
  pause
  exit /b 1
)
if exist .git (
  echo ERROR: This folder already has a .git directory.
  echo To avoid overwriting history, this script will stop here.
  pause
  exit /b 1
)
echo First create a NEW EMPTY repository on GitHub.
echo Do not add a README, .gitignore, or license on GitHub.
echo.
set /p REPO_URL=Paste the HTTPS URL of your empty GitHub repository: 
if "%REPO_URL%"=="" (
  echo ERROR: Repository URL is required.
  pause
  exit /b 1
)
git init
if errorlevel 1 goto fail
git branch -M main
git add .
if errorlevel 1 goto fail
git commit -m "Prepare graduation project portfolio"
if errorlevel 1 goto fail
git remote add origin "%REPO_URL%"
if errorlevel 1 goto fail
echo.
echo Pushing project to GitHub. A browser login may appear.
git push -u origin main
if errorlevel 1 goto fail
echo.
echo SUCCESS: Project pushed to GitHub.
echo Open the repository in your browser and check the README.
pause
exit /b 0
:fail
echo.
echo Publishing did not finish. Read the Git error above before trying again.
pause
exit /b 1
