'''
# Django views and imports
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
from django.conf import settings
from django.http import HttpResponse
import logging
# Import the utility functions
from . import utils # Make sure to adjust the import path as needed

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'myapp/index.html')  # Updated path

@csrf_exempt
def process_presentation(request):
    if request.method == 'POST':
        # Check if file was uploaded successfully
        uploaded_file = request.FILES.get('file')
       
        if not uploaded_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        logger.info("File uploaded successfully.")

        # Get parameters from the request
        selected_style = request.POST.get('style', 'Standard')
        selected_token_limit = int(request.POST.get('token_limit', 800))
        voice_type = request.POST.get('voice_type') 

        # Generate a unique processing directory
        process_id = str(uuid.uuid4())
        process_dir = os.path.join(settings.MEDIA_ROOT, 'processes', process_id)
        os.makedirs(process_dir, exist_ok=True)

        # Save the uploaded file to the processing directory
        input_file_path = os.path.join(process_dir, uploaded_file.name)
        with open(input_file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        extracted_text_dir = os.path.join(process_dir, 'extracted_text')
        generated_script_dir = os.path.join(process_dir, 'generated_script')
        speech_dir = os.path.join(process_dir, 'speech')
        pdf_images_dir = os.path.join(process_dir, 'pdf_images')
        output_video_path = os.path.join(process_dir, 'final_presentation.mp4')

        # Create the necessary directories
        os.makedirs(extracted_text_dir, exist_ok=True)
        os.makedirs(generated_script_dir, exist_ok=True)
        os.makedirs(speech_dir, exist_ok=True)
        os.makedirs(pdf_images_dir, exist_ok=True)

        try:
            # Step 1: Extract text
            logger.info("Starting text extraction.")
            utils.extract_text_by_file_type(input_file_path, extracted_text_dir)
            logger.info("Text extraction completed.")

            # Step 2: Generate scripts
            logger.info("Starting script generation.")
            utils.generate_scripts(extracted_text_dir, generated_script_dir, selected_style, selected_token_limit)
            logger.info("Script generation completed.")

            # Step 3: Convert text to speech
            logger.info("Starting text-to-speech conversion.")
            utils.convert_text_to_speech(generated_script_dir, speech_dir,voice_type)
            print(voice_type)
            logger.info("Text-to-speech conversion completed.")

            # Step 4: Convert PDF to images
            logger.info("Starting PDF-to-image conversion.")
            utils.pdf_to_images(input_file_path, pdf_images_dir)
            logger.info("PDF-to-image conversion completed.")

            # Step 5: Create presentation video
            logger.info("Starting video creation.")
            utils.create_presentation_video(pdf_images_dir, speech_dir, output_video_path)
            logger.info("Video creation completed.")

        except Exception as e:
            logger.error(f"Error during processing: {e}")
            return JsonResponse({'error': str(e)}, status=500)

        # Return the video URL
        video_url = os.path.join(settings.MEDIA_URL, 'processes', process_id, 'final_presentation.mp4')
        return JsonResponse({'video_url': video_url})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
'''
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
from django.conf import settings
import logging
from django.utils.timezone import now
from django.urls import reverse
import json

from . import utils

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'myapp/index.html', {'timestamp': now().timestamp()})

def presentation_editor(request):
    return render(request, 'myapp/index_2.html', {'timestamp': now().timestamp()})

# 新增的两个API接口

def get_slides_data(request):
    process_id = request.GET.get('process_id')
    if not process_id:
        return JsonResponse({'error': 'Missing process_id'}, status=400)
    
    process_dir = os.path.join(settings.MEDIA_ROOT, 'processes', process_id)
    if not os.path.exists(process_dir):
        return JsonResponse({'error': 'Invalid process_id'}, status=404)
    
    # 获取 PDF 总页数
    pdf_images_dir = os.path.join(process_dir, 'pdf_images')
    num_pages = len([f for f in os.listdir(pdf_images_dir) if f.endswith('.png')])
    
    return JsonResponse({
        'num_pages': num_pages,
        'image_base_url': f'{settings.MEDIA_URL}processes/{process_id}/pdf_images/',
        'text_api_endpoint': reverse('get_script_text') + f'?process_id={process_id}'
    })

def get_script_text(request):
    process_id = request.GET.get('process_id')
    page_number = request.GET.get('page')
    
    text_path = os.path.join(
        settings.MEDIA_ROOT,
        'processes',
        process_id,
        'generated_script',
        f'generated_content_{page_number}.txt'
    )
    
    if not os.path.exists(text_path):
        return JsonResponse({'error': 'Text not found'}, status=404)
    
    with open(text_path, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    return JsonResponse({'text': text_content})

@csrf_exempt
def process_presentation(request):
    if request.method == 'POST':
        # 1. 获取上传的文件
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        # 2. 获取表单参数
        selected_style = request.POST.get('style', 'Standard')
        selected_token_limit = int(request.POST.get('token_limit', 800))
        voice_type = request.POST.get('voice_type')  # 这次也许用不上，但先保留

        # 3. 生成处理用的唯一目录
        process_id = str(uuid.uuid4())
        process_dir = os.path.join(settings.MEDIA_ROOT, 'processes', process_id)
        os.makedirs(process_dir, exist_ok=True)
        
        #让第一个界面传入的参数保留到第二个界面
        config_path = os.path.join(process_dir, 'config.json')
        with open(config_path, 'w') as f:
            json.dump({
                'voice_type': voice_type,
                'style': selected_style,
                'token_limit': selected_token_limit
            }, f)

        # 4. 保存上传文件到 process_dir 中
        input_file_path = os.path.join(process_dir, uploaded_file.name)
        with open(input_file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # 5. 准备子目录
        pdf_images_dir = os.path.join(process_dir, 'pdf_images')
        extracted_text_dir = os.path.join(process_dir, 'extracted_text')
        generated_script_dir = os.path.join(process_dir, 'generated_script')
        # speech_dir = os.path.join(process_dir, 'speech')  # 如果后续不需要，就不创建
        # output_video_path = os.path.join(process_dir, 'final_presentation.mp4')  # 如果后续不需要，就不创建

        os.makedirs(pdf_images_dir, exist_ok=True)
        os.makedirs(extracted_text_dir, exist_ok=True)
        os.makedirs(generated_script_dir, exist_ok=True)

        try:
            # ========== 第一步：PDF->Image，获取 PDF 页数 ==========
            logger.info("Starting PDF-to-image conversion (to count pages).")
            num_pdf_pages = utils.pdf_to_images(input_file_path, pdf_images_dir)
            logger.info(f"PDF-to-image completed. Total pages: {num_pdf_pages}")

           

            # ========== 第二步：提取文本 (extract_text_by_file_type) ==========
            logger.info("Starting text extraction.")
            utils.extract_text_by_file_type(input_file_path, extracted_text_dir)
            logger.info("Text extraction completed.")

            # ========== 第三步：生成脚本 (generate_scripts) ==========
            logger.info("Starting script generation.")
            utils.generate_scripts(
                extracted_text_dir,
                generated_script_dir,
                selected_style,
                selected_token_limit
            )
            logger.info("Script generation completed.")

          
            # ========== 验证脚本数与 PDF 页数是否一致 ==========
            num_scripts = utils.get_num_scripts_in_dir(generated_script_dir)
            logger.info(f"Found {num_scripts} script files generated.")

            if num_scripts == num_pdf_pages:
                logger.info("All scripts generated successfully.")
                redirect_url = reverse('presentation_editor') + f'?process_id={process_id}'  # 生成跳转 URL
                return JsonResponse({
                    'all_script_generated': True,
                    'redirect_url': redirect_url,  # 返回重定向地址
                    'message': f"All the scripts are generated, {num_scripts} scripts file are generated!"
                })
            else:
                logger.warning("Mismatch between PDF pages and script files.")
                return JsonResponse({
                    'all_script_generated': False,
                    'message': f"脚本未完全生成PDF {num_pdf_pages} 页，脚本数 {num_scripts}。"
                })

        except Exception as e:
            logger.error(f"Error during processing: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def save_script(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    process_id = request.POST.get('process_id')
    page = request.POST.get('page')
    content = request.POST.get('content')
    
    # 验证参数
    if not all([process_id, page, content]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    # 构建文件路径
    script_path = os.path.join(
        settings.MEDIA_ROOT,
        'processes',
        process_id,
        'generated_script',
        f'generated_content_{page}.txt'
    )
    
    # 检查文件是否存在
    if not os.path.exists(script_path):
        return JsonResponse({'error': 'File not found'}, status=404)
    
    # 写入内容
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Failed to save script: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
'''
@csrf_exempt
def generate_video(request):
    if request.method == 'POST':
        process_id = request.POST.get('process_id')
        if not process_id:
            return JsonResponse({'error': 'Missing process_id'}, status=400)
        
        process_dir = os.path.join(settings.MEDIA_ROOT, 'processes', process_id)
        if not os.path.exists(process_dir):
            return JsonResponse({'error': 'Invalid process_id'}, status=404)
        
        # 读取配置文件
        config_path = os.path.join(process_dir, 'config.json')
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                voice_type = config.get('voice_type')
                if not voice_type:
                    return JsonResponse({'error': 'Voice type not found in config'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Failed to load config: {str(e)}'}, status=500)
        
    # 设置参考音频文件路径
        ref_audio= "voice.wav"
        ref_text="My favorite hobby is reading books. It's like opening a door to different worlds. When I'm lost in a good story, time just flies by. Whether it's a thrilling mystery or a heartwarming romance, each book has its own charm."
        # 定义目录路径
        generated_script_dir = os.path.join(process_dir, 'generated_script')
        speech_dir = os.path.join(process_dir, 'speech')
        pdf_images_dir = os.path.join(process_dir, 'pdf_images')
        output_video_path = os.path.join(process_dir, 'final_presentation.mp4')
        
        os.makedirs(speech_dir, exist_ok=True)
        
        try:
            # 文字转语音
            logger.info("Starting text-to-speech conversion.")
            utils.convert_text_to_speech_with_clone(generated_script_dir, speech_dir,ref_audio, ref_text)
            logger.info("Text-to-speech conversion completed.")
            
            # 创建视频
            logger.info("Starting video creation.")
            utils.create_presentation_video(pdf_images_dir, speech_dir, output_video_path)
            logger.info("Video creation completed.")
            
            video_url = f'{settings.MEDIA_URL}processes/{process_id}/final_presentation.mp4'
            return JsonResponse({'video_url': video_url})
        
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
'''
# views.py 后端修改部分

@csrf_exempt
def generate_video(request):
    if request.method == 'POST':
        process_id = request.POST.get('process_id')
        if not process_id:
            return JsonResponse({'error': 'Missing process_id'}, status=400)
        
        process_dir = os.path.join(settings.MEDIA_ROOT, 'processes', process_id)
        if not os.path.exists(process_dir):
            return JsonResponse({'error': 'Invalid process_id'}, status=404)
        
        # 定义克隆音频路径
        target_dir = r"C:\Users\chen'zi'hao\Desktop\fyp\TTS\Cosyvoice\CosyVoice"
        target_file = os.path.join(target_dir, "voice.wav")
        use_clone = os.path.isfile(target_file)  # 核心检查逻辑
        ref_audio = "output.wav"
        
        # 定义参考文本（需与前端显示完全一致）
        ref_text = "My favorite hobby is reading books. It's like opening a door to different worlds. When I'm lost in a good story, time just flies by. Whether it's a thrilling mystery or a heartwarming romance, each book has its own charm."  # 根据你的需求修改
        
        # 读取配置文件
        config_path = os.path.join(process_dir, 'config.json')
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                voice_type = config.get('voice_type')
                
                # 关键逻辑：当不使用克隆时，必须提供语音类型
                if not use_clone and not voice_type:
                    return JsonResponse({'error': 'Voice type required when not using clone'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Failed to load config: {str(e)}'}, status=500)
        
        # 设置目录路径
        generated_script_dir = os.path.join(process_dir, 'generated_script')
        speech_dir = os.path.join(process_dir, 'speech')
        pdf_images_dir = os.path.join(process_dir, 'pdf_images')
        output_video_path = os.path.join(process_dir, 'final_presentation.mp4')
        
        os.makedirs(speech_dir, exist_ok=True)
        
        try:
            if use_clone:
                # 使用克隆语音生成
                logger.info("Starting voice clone.")
                utils.convert_text_to_speech_with_clone(
                    generated_script_dir, 
                    speech_dir,
                    ref_audio ,  # 传递完整路径
                    ref_text
                )
            else:
                # 使用普通TTS生成
                logger.info("Starting normal TTS.")
                utils.convert_text_to_speech_without_clone(
                    generated_script_dir,
                    speech_dir,
                    voice_type
                )
            
            # 创建视频
            logger.info("Starting video creation.")
            utils.create_presentation_video(pdf_images_dir, speech_dir, output_video_path)
            logger.info("Video creation completed.")
            
            video_url = f'{settings.MEDIA_URL}processes/{process_id}/final_presentation.mp4'
            return JsonResponse({'video_url': video_url})
        
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .utils import AIPPT

@csrf_exempt
@require_http_methods(["POST"])
def generate_ppt(request):
    # 从环境变量获取凭证（推荐）
    APP_ID = "f236f37d"  
    API_SECRET = "YTA5YmE1ZGU3NDhkMWYzMzk2YzMzZTA5"

    # 获取请求参数
    query = request.POST.get('query')
    template_id = request.POST.get('template_id','202407171E27C9D')
    file = request.FILES.get('file') # 获取上传的文件对象
    language = request.POST.get('language', 'cn')  # 默认为中文
    #file_url = request.POST.get('file_url') 暂时不需要

    # 参数验证
    # 修改后的参数验证逻辑
    input_sources = [source for source in [query, file] if source is not None]
    if not input_sources:  # 如果没有提供任何输入源
        return JsonResponse({'error': '必须至少提供query、file或file_url中的一个'}, status=400)
    
    #这个版本直接帮助我们上传filename，不用再手动写入了
    try:
        # 处理文件上传
        file_content, file_name = None, None
        if file:
            if not file.name:  # 确保文件名存在
                return JsonResponse({'error': '上传文件必须包含文件名'}, status=400)
                
            file_content = file.read()
            file_name = file.name

        # 初始化PPT生成器
        ppt_maker = AIPPT(
            app_id=APP_ID,
            api_secret=API_SECRET,
            text=query,
            template_id=template_id,
            file_name=file_name,
            file_content=file_content,
            #file_url=file_url,
            language=language  # 传递语言参数
        )
        
        task_id = ppt_maker.create_task()
        ppt_url = ppt_maker.get_result(task_id)
        
        return JsonResponse({'status': 'success', 
                             'ppt_url': ppt_url,
                             'language': language,
                             'template_id':template_id})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    

import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_voice(request):
    if request.method == 'POST' and request.FILES.get('voice'):
        voice_file = request.FILES['voice']
        
        # 指定保存路径（请确保路径存在且有写入权限）
        save_path = r"C:\Users\chen'zi'hao\Desktop\fyp\TTS\Cosyvoice\CosyVoice"
        file_path = os.path.join(save_path, 'voice.wav')
        output_path = os.path.join(save_path, 'output.wav')
        
        try:
            # 保存上传的文件
            with open(file_path, 'wb+') as destination:
                for chunk in voice_file.chunks():
                    destination.write(chunk)
            
            # 使用 ffmpeg 转码
            command = [
                'ffmpeg',
                '-i', file_path,  # 输入文件
                '-acodec', 'pcm_s16le',  # 音频编码
                '-ar', '48000',  # 采样率
                output_path  # 输出文件
            ]
            
            # 执行 ffmpeg 命令
            subprocess.run(command, check=True)
            
            return JsonResponse({'success': True, 'output_path': output_path})
        
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': f'ffmpeg 命令执行失败: {str(e)}'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': '无效请求'})
