from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    """指定された画像ファイルからEXIFデータを取得する"""
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        return exif_data

def get_timestamp(exif_data):
    """EXIFデータからタイムスタンプを取得する"""
    if not exif_data:
        return None

    for tag_id in exif_data:
        # get the tag name
        tag = TAGS.get(tag_id, tag_id)
        if tag == "DateTime":
            return exif_data[tag_id]

    return None

# 画像ファイルのパスを指定
image_path = '/mnt/f/GoPro-Seto_Danchi/20231006/Back/GH020239/img000.jpg'

# EXIFデータを取得
exif_data = get_exif_data(image_path)

# タイムスタンプを取得し表示
timestamp = get_timestamp(exif_data)
if timestamp:
    print(f"Timestamp: {timestamp}")
else:
    print("Timestamp not found in EXIF data.")
