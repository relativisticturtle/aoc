@echo off
if exist .venv (
    call ".venv\Scripts\activate.bat"
) else (
    echo Creating AoC virtual environment...
    %LOCALAPPDATA%\Programs\Python\Python37\python -m venv .venv --prompt aoc
    call ".venv\Scripts\activate.bat"
    echo %CD% > .venv\Lib\site-packages\aoc.pth
    echo Installing requirements...
    pip install -r requirements.txt
    echo Done!
)
%COMSPEC% /k


