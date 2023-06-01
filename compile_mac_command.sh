#!/bin/bash

# Nuitka
# python -m nuitka --macos-create-app-bundle --follow-imports --macos-app-icon=icon.png --noinclude-unittest-mode=allow rsGUI.py

# Pyinstaller
# mac
pyinstaller rsGUI.py --windowed --onedir --icon Icons.icns --noconfirm