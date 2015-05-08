# done ~~todo: 671620616~~
echo Building Simple.exe..
pyinstaller Phantom\Run_this.py -F
echo Done, cleaning up...
move /Y dist\Run_this.exe Simple.exe
rd /S /Q dist
rd /S /Q build
DEL /Q Simple.spec
echo Complete!
