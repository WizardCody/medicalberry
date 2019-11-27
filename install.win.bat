@ECHO OFF
CLS

ECHO.
ECHO  [92mMEDICAL[0m[94mBERRY[0m
ECHO.

cd /d %~dp0

pip install django
pip install django-jet
pip install libsass
pip install feedparser
pip install mysqlclient

ECHO.
ECHO in case of issues when installing mysqlclient install it from whl package
ECHO.
ECHO https://pypi.org/project/mysqlclient/#files
ECHO.
ECHO pip install <whlfile>
ECHO.

EXIT /B 0