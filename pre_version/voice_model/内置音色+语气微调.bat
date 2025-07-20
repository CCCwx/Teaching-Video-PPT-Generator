@echo off
call conda activate cosyvoice
start http://127.0.0.1:50002
python webui.py --port 50002 --model_dir pretrained_models/CosyVoice-300M-Instruct
pause