import os
from utils import (
    extract_text_by_file_type,
    generate_scripts,
    convert_text_to_speech,
    pdf_to_images,
    create_presentation_video,
)

# 设置测试文件夹和路径
test_dir = "test_files"
output_dir = "test_output"
os.makedirs(output_dir, exist_ok=True)

# 1. 测试 extract_text_by_file_type
def test_extract_text():
    print("Testing text extraction from PDF and PPTX files...")
    pdf_path = os.path.join(test_dir, "sample.pdf")
    pptx_path = os.path.join(test_dir, "sample.pptx")
    pdf_output_dir = os.path.join(output_dir, "pdf_text")
    pptx_output_dir = os.path.join(output_dir, "pptx_text")
    os.makedirs(pdf_output_dir, exist_ok=True)
    os.makedirs(pptx_output_dir, exist_ok=True)

    # 测试 PDF 文本提取
    extract_text_by_file_type(pdf_path, pdf_output_dir)
    print(f"PDF text extracted to {pdf_output_dir}")

    # 测试 PPTX 文本提取
    extract_text_by_file_type(pptx_path, pptx_output_dir)
    print(f"PPTX text extracted to {pptx_output_dir}")

# 2. 测试 generate_scripts
def test_generate_scripts():
    print("Testing script generation using GPT API...")
    input_directory = os.path.join(output_dir, "pdf_text")  # 使用上一步生成的PDF文本文件
    script_output_dir = os.path.join(output_dir, "generated_scripts")
    os.makedirs(script_output_dir, exist_ok=True)

    # 调用 generate_scripts 函数
    selected_style = "Standard"
    selected_token_limit = 800
    generate_scripts(input_directory, script_output_dir, selected_style, selected_token_limit)
    print(f"Scripts generated in {script_output_dir}")

# 3. 测试 convert_text_to_speech
def test_text_to_speech():
    print("Testing text-to-speech conversion...")
    script_output_dir = os.path.join(output_dir, "generated_scripts")  # 使用上一步生成的脚本
    speech_output_dir = os.path.join(output_dir, "speech")
    os.makedirs(speech_output_dir, exist_ok=True)

    # 调用 convert_text_to_speech 函数
    convert_text_to_speech(script_output_dir, speech_output_dir)
    print(f"Speech files generated in {speech_output_dir}")

# 4. 测试 pdf_to_images
def test_pdf_to_images():
    print("Testing PDF to image conversion...")
    pdf_path = os.path.join(test_dir, "sample.pdf")
    images_output_dir = os.path.join(output_dir, "pdf_images")
    os.makedirs(images_output_dir, exist_ok=True)

    # 调用 pdf_to_images 函数
    pdf_to_images(pdf_path, images_output_dir)
    print(f"Images generated in {images_output_dir}")

# 5. 测试 create_presentation_video
def test_create_presentation_video():
    print("Testing video creation from images and speech files...")
    images_dir = os.path.join(output_dir, "pdf_images")  # 使用上一步生成的图片文件
    speech_dir = os.path.join(output_dir, "speech")      # 使用上一步生成的语音文件
    output_video_path = os.path.join(output_dir, "final_presentation.mp4")

    # 调用 create_presentation_video 函数
    create_presentation_video(images_dir, speech_dir, output_video_path)
    print(f"Video generated at {output_video_path}")

# 运行所有测试函数
if __name__ == "__main__":
    test_extract_text()
    test_generate_scripts()
    test_text_to_speech()
    test_pdf_to_images()
    test_create_presentation_video()
