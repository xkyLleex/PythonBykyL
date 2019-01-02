@ECHO OFF
python -m pip install --upgrade pip
pip install selenium
pip install pandas_datareader
pip install matplotlib
pause

::install全部maingui.py模組
::如果有"--user"的錯誤，請換成下面程式
::python -m install --user --upgrade pip
::pip install --user selenium
::pip install --user pandas_datareader
::pip install --user matplotlib