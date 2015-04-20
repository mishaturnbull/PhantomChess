#!/bin/sh
# required that you have done `pip install pyinstaller`
pyinstaller --onefile Phantom/Run_this.py -n Phantom_for_MacOSX_64bit
echo "Phantom_for_MacOSX_64bit has been built in Phantom/dist:"
ls -la Phantom/dist  # display file size, etc. of new app
open Phantom/dist    # show the new app in a Finder window
