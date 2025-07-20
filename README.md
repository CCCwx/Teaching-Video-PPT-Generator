This project was developed by the Undergraduate in Chinese University of Hong Kong as his Final Year Project, aiming to developing an application which is able to help educators in teaching and learning. In this 
## Main Function
- Generate a teaching video according to the user input (Both PowerPoint Slides and PPT)
- Generate a descriptive PowerPoints accorfing to the user input (Both PowerPoint Slides and PPT)
## Technology stacks and APIs
This back-end application is developed based on Django Framework while we used JavaScript and Html to realized the front-end
### APIs Used
1. OpenAI 4o-mini API: Used for generate the script in the video
2. Alibaba CosyVoice API: Used for generate the voice in the video (Clone Voice avalable)
3. IFLY-Teck API: Used for generate the PowerPoints
## Environment Setup
This project support Python3.7 and above, please refer to https://www.python.org/ for further python environment installation. After installing the python, you have to do the following setup below:
### Third-party packages needed
Type the below command line into your terminal for Third-party packages installation:
<mark> pip install django==5.0.3 PyPDF2==3.0.1 python-pptx==0.6.23 gtts==2.4.0 pdf2image==1.17.0 moviepy==1.0.3 </mark>
d

   
   
