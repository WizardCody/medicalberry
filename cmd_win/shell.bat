@ECHO OFF
CLS

ECHO.
ECHO  [92mMEDICAL[0m[94mBERRY[0m
ECHO.

cd /d %~dp0..

python manage.py shell %*

EXIT /B 0