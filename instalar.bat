@echo off
cd /d "%~dp0"
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -e .
echo Instalacao concluida! Agora arraste um PDF sobre executar.bat para gerar os ZPLs.
pause