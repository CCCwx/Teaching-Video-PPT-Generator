@echo off
call conda activate cosyvoice
start http://127.0.0.1:50001
python webui.py --port 50001 --model_dir pretrained_models/CosyVoice-300M
pause