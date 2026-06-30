@echo off
REM Active le venv
call venv\Scripts\activate.bat

REM Définir PYTHONPATH pour que les imports fonctionnent
set PYTHONPATH=%CD%

REM Lancer pytest
python -m pytest -v

REM Fin
pause