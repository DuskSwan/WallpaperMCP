import requests
import ctypes
from pathlib import Path

from PIL import Image
from io import BytesIO

import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件
ACCESS_KEY = os.getenv("UNSPLASH_API")


def analyze_response(response):
    """分析响应内容"""
    # 检查请求是否成功
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return
    
    # 获取响应的内容类型
    content_type = response.headers.get('Content-Type', '').lower()
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容类型: {content_type}")
    
    # 根据内容类型处理不同的数据
    if 'json' in content_type:
        # 如果响应内容是 JSON 格式
        try:
            json_data = response.json()  # 解析 JSON 数据
            print("响应内容（JSON 格式）：")
            print(json_data)
        except ValueError:
            print("响应内容不是有效的 JSON 格式")
    
    elif 'html' in content_type:
        # 如果响应内容是 HTML 格式
        print("响应内容（HTML 格式）：")
        print(response.text[:200] + "...")  # 打印 HTML 内容的前 200 个字符
    
    elif 'image' in content_type:
        # 如果响应内容是图片（二进制数据）
        print("响应内容是图片，保存为文件")
        # 使用 Pillow 显示图片
        image = Image.open(BytesIO(response.content))
        image.show()
        print("图片已显示")
    
    elif 'plain' in content_type:
        # 如果响应内容是纯文本
        print("响应内容（纯文本）：")
        print(response.text[:200] + "...")
    
    else:
        print("响应内容类型未知，原始内容：")
        print(response.text[:200] + "...")  # 打印内容的前 200 个字符

def get_random_wallpaper():
    """获取随机壁纸的url"""
    url = f"https://api.unsplash.com/photos/random?query=wallpaper&client_id={ACCESS_KEY}"
    # 发送请求
    response = requests.get(url)
    # 如果请求成功
    if response.status_code == 200:
        # 解析返回的 JSON 数据
        data = response.json()
        # 获取壁纸的图片URL
        image_url = data['urls']['raw']
        return image_url
    else:
        print(f"Error status code: {response.status_code}")
        return None

def download_one_image(image_url, save_dir='.', img_name=None):
    """下载图片到指定目录"""
    response = requests.get(image_url)

    # analyze_response(response)  # 分析响应内容
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 创建文件夹（如果不存在）
        save_path = Path(save_dir) / (img_name if img_name else "wallpaper.jpg")
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存图片到指定路径
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"图片已成功保存到 {save_path}")
        return save_path
    else:
        print("下载图片失败！")
        return None

def set_wallpaper(image_path: str):
    unicode_image_path = ctypes.c_wchar_p(image_path)
    result = ctypes.windll.user32.SystemParametersInfoW(20, 0, unicode_image_path, 3)
    if result:
        print(f"壁纸已成功设置为 {image_path}")
    else:
        print(f"设置壁纸失败！")

if __name__ == "__main__":
    wallpaper_url = get_random_wallpaper()
    img_path = download_one_image(wallpaper_url, ".")
    if img_path:
        set_wallpaper(str(img_path.resolve()))
