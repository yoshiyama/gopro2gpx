import gpxpy
import piexif
from PIL import Image
from datetime import datetime
import os


def load_gpx_data(gpx_file):
    with open(gpx_file, 'r') as file:
        gpx = gpxpy.parse(file)
        return gpx


def find_closest_track_point(gpx_data, target_time):
    closest_point = None
    min_diff = None
    for track in gpx_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                # GPXのタイムスタンプをoffset-naiveに変換
                point_time_naive = point.time.replace(tzinfo=None)
                time_diff = abs((point_time_naive - target_time).total_seconds())
                if min_diff is None or time_diff < min_diff:
                    min_diff = time_diff
                    closest_point = point
    return closest_point



def get_image_timestamp(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if not exif_data:
            return None

        date_time_original = exif_data.get(36867)  # 36867 is the tag for DateTimeOriginal
        if date_time_original:
            return datetime.strptime(date_time_original, "%Y:%m:%d %H:%M:%S")
        return None


def write_exif_data(image_path, gpx_point):
    exif_dict = piexif.load(image_path)

    # GPS data format
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N' if gpx_point.latitude >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: convert_to_degrees(gpx_point.latitude),
        piexif.GPSIFD.GPSLongitudeRef: 'E' if gpx_point.longitude >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: convert_to_degrees(gpx_point.longitude),
        piexif.GPSIFD.GPSAltitude: (int(gpx_point.elevation), 1)  # 標高を分数形式に変換
    }

    exif_dict['GPS'] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)



def convert_to_degrees(value):
    deg = int(value)
    min = int((value - deg) * 60)
    sec = int(((value - deg) * 3600) % 60)
    return [(deg, 1), (min, 1), (sec, 1)]

# その他の関数は変更なし...


def get_exif_data(image_path):
    img = Image.open(image_path)
    exif_data = piexif.load(img.info['exif'])

    # EXIFデータから撮影日時を取得
    if piexif.ImageIFD.DateTime in exif_data['0th']:
        datetime_str = exif_data['0th'][piexif.ImageIFD.DateTime].decode('utf-8')
        datetime_original = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")
        return datetime_original
    else:
        return None

# 画像ファイルとGPXファイルのパス
image_path = '/mnt/f/GoPro-Seto_Danchi/20231006/Back/GH020239/img000.jpg'
gpx_file = '/mnt/f/GoPro-Seto_Danchi/20231006/Back/GH020239.gpx'

# データ読み込み
gpx_data = load_gpx_data(gpx_file)
image_timestamp = get_exif_data(image_path)

if image_timestamp is None:
    print("No valid timestamp found in image EXIF data.")
    exit()

# 最も近いGPXトラックポイントを見つける
closest_point = find_closest_track_point(gpx_data, image_timestamp)

# EXIFデータに書き込む
if closest_point:
    write_exif_data(image_path, closest_point)
else:
    print("No close track point found.")