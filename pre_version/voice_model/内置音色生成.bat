@echo off
call conda activate cosyvoice
start http://127.0.0.1:50000
python webui.py --port 50000 --model_dir pretrained_models/CosyVoice-300M-SFT
pause