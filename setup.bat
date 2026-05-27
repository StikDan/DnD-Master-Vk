@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Updating pip...
python -m pip install --upgrade pip

echo Installing requirements...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo Installing Ollama...
powershell -ExecutionPolicy Bypass -Command "irm https://ollama.com/install.ps1 | iex"

echo Setup LLM's
ollama pull ministral-3:14b-cloud
ollama pull deepseek-v3.2:cloud

echo Setup complete!
pause