from PIL import Image
import piexif

def get_exif_data(image_path):
    img = Image.open(image_path)
    exif_data = piexif.load(img.info['exif'])

    # EXIFデータから撮影日時を取得
    if piexif.ImageIFD.DateTime in exif_data['0th']:
        datetime_original = exif_data['0th'][piexif.ImageIFD.DateTime].decode('utf-8')
        print(f"撮影日時: {datetime_original}")
    else:
        print("撮影日時の情報はありません。")

# 使用例
image_file = '/mnt/f/GoPro-Seto_Danchi/20231006/Back/GH020239/img000.jpg'
get_exif_data(image_file)
