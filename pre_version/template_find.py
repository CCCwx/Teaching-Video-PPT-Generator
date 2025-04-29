import hashlib
import hmac
import base64
import json
import time
import requests

class AIPPT():
    def __init__(self, APPId, APISecret):
        self.APPid = APPId
        self.APISecret = APISecret
        self.header = {}

    def get_signature(self, ts):
        try:
            auth = self.md5(self.APPid + str(ts))
            return self.hmac_sha1_encrypt(auth, self.APISecret)
        except Exception as e:
            print(e)
            return None

    def hmac_sha1_encrypt(self, encrypt_text, encrypt_key):
        return base64.b64encode(hmac.new(encrypt_key.encode('utf-8'), 
                                  encrypt_text.encode('utf-8'), 
                                  hashlib.sha1).digest()).decode('utf-8')

    def md5(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def getHeaders(self):
        timestamp = int(time.time())
        signature = self.get_signature(timestamp)
        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": "application/json; charset=utf-8"
        }
        return headers

    def getTheme(self, style=None, color=None, industry=None, pageNum=1, pageSize=10):
        url = "https://zwapi.xfyun.cn/api/ppt/v2/template/list"
        self.header = self.getHeaders()
        
        params = {
            "payType": "not_free",
            "pageNum": pageNum,
            "pageSize": pageSize
        }
        
        if style:
            params["style"] = style
        if color:
            params["color"] = color
        if industry:
            params["industry"] = industry
        
        response = requests.get(url, headers=self.header, params=params)
        return response.text

if __name__ == '__main__':
    # 替换为你的实际APPId和APISecret
    APPId = "f236f37d"
    APISecret = "YTA5YmE1ZGU3NDhkMWYzMzk2YzMzZTA5"
    
    # 创建实例
    demo = AIPPT(APPId, APISecret)
    
    try:
        # 示例1：查询教育培训行业的红色简约模板
        print("查询教育培训行业的红色简约模板:")
        result = demo.getTheme(style="简约", industry="教育培训")
        
        # 解析结果
        result_json = json.loads(result)
        if result_json['code'] == 0:
            templates = result_json['data']['records']
            for template in templates:
                print(f"模板ID: {template['templateIndexId']}")
                print(f"风格: {template['style']}")
                print(f"颜色: {template['color']}")
                print(f"行业: {template['industry']}")
                print(f"页数: {template['pageCount']}")
                print("-" * 50)
        else:
            print("查询失败:", result_json['desc'])
            
        # 示例2：查询所有商务风格的模板（第一页）
        print("\n查询所有商务风格的模板:")
        result = demo.getTheme(style="商务")
        result_json = json.loads(result)
        # ...同样方式解析结果
        
    except Exception as e:
        print("发生错误:", str(e))