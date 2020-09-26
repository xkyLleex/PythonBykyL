@echo off
set /p filename= input file name:
pyuic5 %filename%.ui > %filename%.py
pause