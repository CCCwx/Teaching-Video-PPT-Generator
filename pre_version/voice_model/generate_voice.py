from gradio_client import Client, file

# 创建客户端实例，指向你的Gradio应用
client = Client("http://127.0.0.1:50001/")

# 调用API并传入参数
result = client.predict(
    tts_text="我是通义实验室语音团队全新推出的生成式语音大模型，提供舒适自然的语音合成能力。",
    mode_checkbox_group="预训练音色",
    sft_dropdown="中文女",
    prompt_text="在那之后完全收购那家公司，因此保持管理层的一致性，利益即将加入家族的资产保持一致，这就是我们有时不买下全部的原因",
    prompt_wav_upload=file('cross_lingual_prompt.wav'),
    prompt_wav_record=file('cross_lingual_prompt.wav')
    seed=1,
    stream="false",
    speed=1,
    api_name="/generate_audio"
)

# 打印结果，结果是一个文件路径
print(result)