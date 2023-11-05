@echo off
goto :DOES_PYTHON_EXIST


:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
goto :EOF

:PYTHON_DOES_NOT_EXIST
echo Python is not installed on your system.
echo Now opeing the download URL.
start "" "https://www.microsoft.com/store/productId/9PJPW5LDXLZ5"
PAUSE
goto :EOF

:PYTHON_DOES_EXIST
:: This will retrieve Python 3.8.0 for example.
for /f "delims=" %%V in ('python -V') do @set ver=%%V
echo Congrats, %ver% is installed...
python -m venv .\venv
venv\Scripts\pip install torch==1.13.1 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
venv\Scripts\pip install -U -r requirements.txt

PAUSE
goto :EOF


