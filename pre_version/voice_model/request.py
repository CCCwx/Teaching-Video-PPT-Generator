import requests

data={
    "text":"今天我就是西部第一牛仔。",
    "reference_audio":"10.wav",
    "reference_text":"这是人工智能陈子豪，听起来还不错对吧，可以再合成一个陈五溪试试看。"
}
response=requests.post(f'http://127.0.0.1:9233/clone_eq',data=data,timeout=3600)


if response.status_code!=200:
    # 出错了
    print(response.json())
else:
    # 返回的wav数据流，可直接保存
    with open("./clone_output.wav",'wb') as f:
        f.write(response.content)




