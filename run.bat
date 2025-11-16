@echo off
echo Installing required packages...
pip install -r requirements.txt

echo Starting Mutual Fund FAQ Assistant...
python app.py

pause