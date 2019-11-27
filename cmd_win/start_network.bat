@ECHO OFF
CLS

ECHO.
ECHO  [92mMEDICAL[0m[94mBERRY[0m
ECHO.

cd /d %~dp0..

python manage.py runserver 0.0.0.0:8000 %*

EXIT /B 0