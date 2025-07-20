This project was developed by the Undergraduate in Chinese University of Hong Kong as his Final Year Project, aiming to developing an application which is able to help educators in teaching and learning. In this 
## Main Function
- Generate a teaching video according to the user input (Both PowerPoint Slides and PPT)
- Generate a descriptive PowerPoints accorfing to the user input (Both PowerPoint Slides and PPT)

## Project Screenshot
### Video Generation Part
<img width="1054" height="947" alt="Overall Layout" src="https://github.com/user-attachments/assets/ebabc261-0a04-4580-a192-8fa227ad2c72" />

<img width="699" height="504" alt="Voice Selection Part" src="https://github.com/user-attachments/assets/ed4991bb-af46-4493-b3fd-d5871361d83f" />
### PowerPoint Generation Part

###  Script Modification Part
<img width="1920" height="901" alt="Script Modification Part" src="https://github.com/user-attachments/assets/c03337d1-0117-412d-9a39-394c91b49891" />

### PowerPoint Generation Part
<img width="758" height="891" alt="PPT Generation Part" src="https://github.com/user-attachments/assets/83eaa4a0-75ff-4455-8fa2-5b10836ddd98" />

## Technology stacks and APIs
This back-end application is developed based on Django Framework while we used JavaScript and Html to realized the front-end
### APIs Used
1. OpenAI 4o-mini API: Used for generate the script in the video
2. Alibaba CosyVoice API: Used for generate the voice in the video (Clone Voice avalable)
3. IFLY-Teck API: Used for generate the PowerPoints
## Environment Setup
This project support Python3.7 and above, please refer to https://www.python.org/ for further python environment installation. After installing the python, you have to do the following setup below:
### Third-party packages needed
Type the below command line into your terminal for Third-party packages installation: <br>
```bash
pip install django==5.0.3 PyPDF2==3.0.1 python-pptx==0.6.23 gtts==2.4.0 pdf2image==1.17.0 moviepy==1.0.3 
```
### System level dependencies
| 依赖项     | macOS Installation Method                | Windows Installation Method                                     | Verification Command              |
|------------|-----------------------------------|---------------------------------------------------------------------------------|-----------------------|
| **Poppler** | `brew install poppler`            | 1. Download [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)<br>2. Add the `bin` directory to the system PATH.| `pdftoppm -v`         |
| **FFmpeg**  | `brew install ffmpeg`             | 1. Download [FFmpeg](https://ffmpeg.org/download.html)<br>2. Add the `bin` directory to the system PATH.       | `ffmpeg -version`     |
| **Ghostscript** | `brew install ghostscript`    | 1. Download [Ghostscript](https://www.ghostscript.com/releases/gsdnld.html)<br>2. Run the installation program | `gs --version`        |

### CosyVoice Setup
We strongly recommend downloading the following pretrained models and resources: <br>
1.CosyVoice2-0.5B - Base model (500M parameters) <br>
2.CosyVoice-300M - Lightweight model (300M parameters) <br>
3.CosyVoice-300M-SFT - Supervised Fine-Tuned version <br>
4.CosyVoice-300M-Instruct - Instruction-tuned version <br>
5.CosyVoice-ttsfrd - Text normalization resources <br>

### SDK one-click download (recommended)
```bash
pip install modelscope
```
```bash
from modelscope import snapshot_download

snapshot_download('iic/CosyVoice2-0.5B',        local_dir='pretrained_models/CosyVoice2-0.5B')
snapshot_download('iic/CosyVoice-300M',         local_dir='pretrained_models/CosyVoice-300M')
snapshot_download('iic/CosyVoice-300M-SFT',     local_dir='pretrained_models/CosyVoice-300M-SFT')
snapshot_download('iic/CosyVoice-300M-Instruct',local_dir='pretrained_models/CosyVoice-300M-Instruct')
snapshot_download('iic/CosyVoice-ttsfrd',       local_dir='pretrained_models/CosyVoice-ttsfrd')
```   
### Git Clone Manully
Ensure that Git LFS is installed and run it: <br>
```bash
mkdir -p pretrained_models
git lfs install               # Only need excute once

git clone https://www.modelscope.cn/iic/CosyVoice2-0.5B.git        pretrained_models/CosyVoice2-0.5B
git clone https://www.modelscope.cn/iic/CosyVoice-300M.git         pretrained_models/CosyVoice-300M
git clone https://www.modelscope.cn/iic/CosyVoice-300M-SFT.git     pretrained_models/CosyVoice-300M-SFT
git clone https://www.modelscope.cn/iic/CosyVoice-300M-Instruct.git pretrained_models/CosyVoice-300M-Instruct
git clone https://www.modelscope.cn/iic/CosyVoice-ttsfrd.git        pretrained_models/CosyVoice-ttsfrd
```

### Optional: ttsfrd Text Normalization Enhancement
For more accurate text normalization (numbers, symbols, dates, etc.), install the ttsfrd package:  <br>
```bash
cd pretrained_models/CosyVoice-ttsfrd/
unzip -o resource.zip -d .

pip install ttsfrd_dependency-0.1-py3-none-any.whl
pip install ttsfrd-0.4.2-cp310-cp310-linux_x86_64.whl
```

## How to Run the project?
This is a local-based and non-database project, hence we do not need to migrate database. 

### Application database migration
However, if you decide to add a database, please type the following command for each database update operation:
```bash
python manage.py migrate
```
### Start the server
```bash
# Default way (port 8000) 
python manage.py runserver

# Specify port (e.g. 8080) 
python manage.py runserver 8080

# Allow LAN access 
python manage.py runserver 0.0.0.0:8000
```

By following those step, our project should be deployed correctly on you devices and by clikcing the localhost, it will redirect to the generating teaching video & PPT pages as seen in the Project Screenshot part.





