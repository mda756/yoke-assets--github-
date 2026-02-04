@echo off
echo ========================================
echo DOCX/PPTX to TXT Batch Converter
echo ========================================
echo.

echo Step 1: Installing required libraries...
pip install python-docx python-pptx

echo.
echo Step 2: Running converter...
python convert_docs_to_text.py

echo.
echo ========================================
echo DONE! Press any key to close...
pause
