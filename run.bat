@echo off

if not exist "src/generate_file/ui_main_window.py" (
    echo "\"ui_main_window.py\" not found"
    echo "Generate UI files"

    if not exist "src/generate_file/" (
        mkdir "src/generate_file"
    )

    pyuic5 src/main_window.ui -o src/generate_file/ui_main_window.py
)

if "%~1" == "debug" (
    echo "Running Debug build"

    python src/main.py
) else (
    echo "Running Release build"

    python -O src/main.py
)
