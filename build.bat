@echo off
pyinstaller --noconsole --onefile --icon=assets\app.ico --add-data "assets\app.ico;." --add-data "assets\graphics.txt;assets" main.py
pause