@echo off

cd /d "D:\IOT ポートフォリオ"

call ".venv\Scripts\activate.bat"

if not exist "logs" mkdir logs

echo ============================== >> "logs\task_log.txt"
echo 実行日時: %date% %time% >> "logs\task_log.txt"

python main.py >> "logs\task_log.txt" 2>&1

echo 終了日時: %date% %time% >> "logs\task_log.txt"