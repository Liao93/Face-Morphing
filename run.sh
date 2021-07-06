#!/bin/sh

if [ ! -f src/generate_file/ui_main_window.py ]; then
    echo "\"ui_main_window.py\" not found"
    echo "Generate UI files"

    mkdir -p "src/generate_file"

    pyuic5 src/main_window.ui -o src/generate_file/ui_main_window.py
fi

if [ "${1}" = "debug" ]; then
    echo "Running Debug build"

    python3 src/main.py
else
    echo "Running Release build"

    python3 -O src/main.py
fi
