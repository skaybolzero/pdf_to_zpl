@echo off
call "%~dp0.venv\Scripts\activate.bat"
pdf-to-zpl "%1" --saida "%~dp0saida_zpl" --poppler-path "C:\poppler\Library\bin"
pause