@echo off
python37\python.exe wooferbot.py
IF %ERRORLEVEL% NEQ 0 (
	pause
)