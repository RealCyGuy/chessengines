@echo off
FOR /F "delims=" %%i IN ('poetry env info --path') DO set path=%%i
%path%\Scripts\python.exe engine.py