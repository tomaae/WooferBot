@echo off
python37\python wooferbot.py
IF %ERRORLEVEL% NEQ 0 (
	pause
)