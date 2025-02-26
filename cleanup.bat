@echo off
:: filepath: /d:/program/Renaming System/cleanup.bat
echo Starting cleanup for Windows...

echo Removing test files...
del /s /q "D:\program\Renaming System\test_file_*.txt"
del /s /q "D:\program\Renaming System\renamed_*.txt"

echo Removing pytest cache directories...
for /d /r "D:\program\Renaming System" %%d in (.pytest_cache) do (
    if exist "%%d" (
        echo Removing %%d
        rd /s /q "%%d"
    )
)

echo Removing Python cache directories...
for /d /r "D:\program\Renaming System" %%d in (__pycache__) do (
    if exist "%%d" (
        echo Removing %%d
        rd /s /q "%%d"
    )
)

echo Cleanup completed! Now ready for GitHub.
pause