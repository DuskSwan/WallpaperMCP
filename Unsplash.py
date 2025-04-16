import requests
import json

# Unsplash API Access Key
ACCESS_KEY = 'A19NZq5pvBwCA2Ki-Xmn5wiRYlNdSYTGmBLPNQe_j4k'  # 替换为你的 Unsplash Access Key

# 获取随机壁纸的url
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
        image_url = data['urls']['regular']
        return image_url
    else:
        print(f"Error status code: {response.status_code}")
        return None

# 

if __name__ == "__main__":
    # 测试获取壁纸函数
    wallpaper_url = get_random_wallpaper()
    if wallpaper_url:
        print(f"壁纸 URL: {wallpaper_url}")
    else:
        print("无法获取壁纸")
