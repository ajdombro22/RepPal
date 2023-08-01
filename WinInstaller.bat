@echo off

rem echo "making main folder"

rem if not exist "C:\Program Files\RepPal" mkdir "C:\Program Files\RepPal"

cd /d %temp%

del /F /Q python-3.11.3-amd64.exe src.zip 
rmdir src /S /Q

curl -O https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe

echo "installing python"

python-3.11.3-amd64.exe /passive 

py -m pip install --upgrade pip

echo "installing venv"

py -m pip install virtualenv

echo "downloading and unzipping src and utilities"

curl -O http://taxsite.tax.local/dev/reppalunziputil.py
curl -O http://taxsite.tax.local/dev/src.zip

py reppalunziputil.py "src.zip" "."

py -m venv src

cd src 

echo Building .exe, please hit the big blue button for defaults. I don't recommend otherwise unless you know what you are doing. This build is NOT portable.

py -m pip install cryptography
.\Scripts\python.exe -m pip install -r req.txt
.\Scripts\python.exe -m pip install cryptography
.\Scripts\python.exe -m pip install auto-py-to-exe

py reppalinstaller.py

pause
echo moving
pause
move "%temp%\src\dist\RepPal" "C:\Program Files\"
echo moved?
pause
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



pause