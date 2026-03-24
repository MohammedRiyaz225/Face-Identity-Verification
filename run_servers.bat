@echo off
echo Starting Face Identity Verification Projects...
echo.

echo [1/2] Starting Node.js Backend (Dashboard)...
start "Node.js Server" cmd /c "cd /d "%~dp0major project Josh and Aayush" && npm install && node app.js"

echo [2/2] Starting Python Flask Server (Face Recognition Camera)...
start "Flask Server" cmd /c "cd /d "%~dp0New folder" && py -m pip install -r requirements.txt && py wait.py"

echo.
echo Waiting 5 seconds for servers to initialize...
timeout /t 5 /nobreak >nul

echo Opening browser...
start http://localhost:3000/

echo Done! Both servers are now running in separate windows.
echo Keep those windows open to use the application.
