@echo off

move .\src\dist\RepPal "C:\Program Files\"

icacls "C:\Program Files\RepPal" /grant Everyone:F /T
icacls "C:\Program Files\RepPal\cfg" /grant Everyone:F /T

echo "cleaning up"

cd /d "%temp%"

del /F /Q python-3.11.3-amd64.exe src.zip 

rmdir src /S /Q

echo "done"

echo "creating shortcut"

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "C:\Users\Public\Desktop\RepPal.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "C:\Program Files\RepPal\RepPal.exe" >> %SCRIPT%
echo oLink.WorkingDirectory = "C:\Program Files\RepPal" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

