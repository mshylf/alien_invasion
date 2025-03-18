import os
import sys
from PIL import Image

# 添加 settings.py 所在的目录到模块搜索路径（如果需要的话）
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from settings import Settings  # 如果以后需要使用设置，可保留

def convert_to_bmp(source_dir, target_dir):
    """将 source_dir 中的所有图片转换为 BMP 格式并保存到 target_dir"""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            source_path = os.path.join(source_dir, filename)
            try:
                with Image.open(source_path) as img:
                    base_name = os.path.splitext(filename)[0]
                    target_path = os.path.join(target_dir, f"{base_name}.bmp")
                    if os.path.exists(target_path):
                        print(f"文件已存在，覆盖: {target_path}")
                    img.save(target_path, format="BMP")
                    print(f"成功转换: {source_path} -> {target_path}")
            except Exception as e:
                print(f"转换失败: {source_path}，错误: {e}")

if __name__ == "__main__":
    cur_dir = os.path.dirname(__file__)
    convert_to_bmp(cur_dir, cur_dir)