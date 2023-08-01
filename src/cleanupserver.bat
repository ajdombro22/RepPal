@echo on

cd ..

set installdir=%~1
rem set installdir=%installdir:~0,-1%


echo %installdir%

echo move ".\src\dist\RepPal" "%installdir%\"
move .\src\dist\RepPal "%installdir%\"

echo icacls %installdir%\RepPal /grant Everyone:F /T
icacls "%installdir%\RepPal" /grant Everyone:F /T
icacls "%installdir%\RepPal\cfg" /grant Everyone:F /T

echo "cleaning up"

cd /d "%temp%"

rem del /F /Q src.zip src


echo bat done

pause