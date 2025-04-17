import requests
import ctypes
from pathlib import Path
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 加载 .env 文件
load_dotenv()  
Unsplash_KEY = os.getenv("UNSPLASH_API")

# 初始化 MCP 服务器
mcp = FastMCP("wallpaper-server")

def analyze_response(response):
    """分析响应内容"""
    if response.status_code != 200:
        return f"请求失败，状态码: {response.status_code}"
    
    content_type = response.headers.get('Content-Type', '').lower()
    
    response_info = f"响应状态码: {response.status_code}\n响应内容类型: {content_type}\n"
    
    if 'json' in content_type:
        try:
            json_data = response.json()  # 解析 JSON 数据
            response_info += "响应内容（JSON 格式）：\n" + str(json_data)
        except ValueError:
            response_info += "响应内容不是有效的 JSON 格式"
    
    elif 'html' in content_type:
        response_info += "响应内容（HTML 格式）：\n" + response.text[:200] + "..."
    
    elif 'image' in content_type:
        image = Image.open(BytesIO(response.content))
        image.show()
        response_info += "图片已显示"
    
    elif 'plain' in content_type:
        response_info += "响应内容（纯文本）：\n" + response.text[:200] + "..."
    
    else:
        response_info += "响应内容类型未知，原始内容：\n" + response.text[:200] + "..."
    
    return response_info

@mcp.tool()
def get_random_wallpaper() -> str:
    """获取随机壁纸的URL"""
    url = f"https://api.unsplash.com/photos/random?query=wallpaper&client_id={Unsplash_KEY}"
    response = requests.get(url)
    try:
        if response.status_code == 200:
            data = response.json()
            return data['urls']['raw']
        else:
            return f"Error status code: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def download_one_image(image_url: str, save_dir: str = '.', img_name: str = None) -> str:
    """下载图片到指定目录"""
    response = requests.get(image_url)
    if response.status_code == 200:
        save_path = Path(save_dir) / (img_name if img_name else "wallpaper.jpg")
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return f"图片已成功保存到 {save_path.resolve()}"
    else:
        return "下载图片失败！"

@mcp.tool()
def set_wallpaper(image_path: str) -> str:
    """设置壁纸"""
    unicode_image_path = ctypes.c_wchar_p(image_path)
    result = ctypes.windll.user32.SystemParametersInfoW(20, 0, unicode_image_path, 3)
    if result:
        return f"壁纸已成功设置为 {image_path}"
    else:
        return "设置壁纸失败！"

if __name__ == "__main__":
    mcp.run(transport='stdio')
