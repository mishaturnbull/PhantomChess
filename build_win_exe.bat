# done ~~todo: 671620616~~
echo Building Simple.exe..
pyinstaller Phantom\Run_this.py -F -n Simple
echo Done, cleaning up...
move /Y Phantom\Simple.exe Simple.exe
rd /S /Q dist
rd /S /Q build
echo Complete!
