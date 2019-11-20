if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Python build
pipenv run pyinstaller wooferbot_cli.spec --onefile --clean