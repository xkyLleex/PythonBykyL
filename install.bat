@ECHO OFF
title 股市通知與分析
set /p var= 請輸入要用哪個身分安裝(admin=0,user=1,直接run=3):
If %var% == 0 goto Admin
If %var% == 1 goto User
If %var% == 3 goto runfile
echo 錯誤數值(請重新輸入！)
goto end

:Admin
echo 安裝套件中(admin)...
python -m pip install --upgrade pip
pip install selenium
pip install pandas_datareader
pip install matplotlib
goto runfile

:User
echo 安裝套件中(user)...
python -m install --user --upgrade pip
pip install --user selenium
pip install --user pandas_datareader
pip install --user matplotlib
goto runfile

:runfile
cls
echo 跑maingui中...
python maingui.py
echo 程式結束
goto end

:end
pause
