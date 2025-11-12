import base64
import hashlib
import hmac
import json
import time
import requests
from urllib.parse import urlencode
from app.core.config import settings


class SpeechService:
    """
    科大讯飞语音识别服务
    """
    
    def __init__(self):
        self.api_key = settings.SPEECH_API_KEY
        self.api_secret = settings.SPEECH_API_SECRET
        self.app_id = ""  # 需要从科大讯飞获取
        
    def _get_auth_url(self):
        """
        生成带有授权参数的URL
        """
        if not self.api_key or not self.api_secret:
            # 如果没有配置API密钥，返回模拟数据
            return None, None
        
        # 请求地址
        url = 'https://api.xfyun.cn/v1/service/v1/iat'
        
        # 时间戳
        cur_time = str(int(time.time()))
        
        # 构造参数
        param = {
            "engine_type": "sms16k",  # 引擎类型
            "aue": "raw",  # 音频格式
            "scene": "main",  # 场景
            "result_level": "complete"  # 结果级别
        }
        
        # 参数编码
        param_base64 = base64.b64encode(json.dumps(param).encode('utf-8')).decode('ascii')
        
        # 构造签名
        raw_str = self.api_key + cur_time + param_base64
        checksum = hmac.new(
            self.api_secret.encode('utf-8'),
            raw_str.encode('utf-8'),
            digestmod=hashlib.md5
        ).hexdigest()
        
        # 构造请求头
        headers = {
            'X-Appid': self.app_id,
            'X-CurTime': cur_time,
            'X-Param': param_base64,
            'X-CheckSum': checksum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        }
        
        return url, headers
    
    def recognize_speech(self, audio_data):
        """
        语音识别
        
        Args:
            audio_data: 音频数据
            
        Returns:
            识别结果
        """
        # 如果没有配置API密钥，返回模拟数据
        if not self.api_key or not self.api_secret:
            return {
                "success": True,
                "text": "我想去日本，5天，预算1万元，喜欢美食和动漫，带孩子",
                "raw_response": {"mock": True}
            }
        
        try:
            url, headers = self._get_auth_url()
            
            # 构造请求数据
            data = {
                'audio': base64.b64encode(audio_data).decode('ascii')
            }
            
            # 发送请求
            response = requests.post(url, headers=headers, data=data)
            result = response.json()
            
            if result['code'] == 0:
                return {
                    "success": True,
                    "text": result['data'],
                    "raw_response": result
                }
            else:
                return {
                    "success": False,
                    "error": f"语音识别失败: {result['desc']}",
                    "text": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"语音识别过程中发生错误: {str(e)}",
                "text": None
            }


# 创建全局实例
speech_service = SpeechService()