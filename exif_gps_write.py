"""
This program updates an image's EXIF data with GPS coordinates from a GPX file. It works by finding the closest GPS track point to the image's timestamp and then writing this location information, including latitude, longitude, and altitude, into the image's metadata using the gpxpy and piexif libraries. This enriches the image with accurate geographical tags based on the GPX data.

python exif_gps_write.py /path/to/images/directory /path/to/gpx/file.gpx

"""

import gpxpy
import piexif
from PIL import Image
from datetime import datetime
import os
import sys  # コマンドライン引数を扱うために追加


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

        # 複数のタグをチェック
        for tag in (36867,  # DateTimeOriginal
                    306,  # DateTime
                    36868):  # DateTimeDigitized
            date_time_original = exif_data.get(tag)
            if date_time_original:
                try:
                    return datetime.strptime(date_time_original, "%Y:%m:%d %H:%M:%S")
                except ValueError:
                    # フォーマットが一致しない場合は、次のタグを試す
                    continue
        return None


def write_exif_data(image_path, gpx_point):
    exif_dict = piexif.load(image_path)
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N' if gpx_point.latitude >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: convert_to_degrees(gpx_point.latitude),
        piexif.GPSIFD.GPSLongitudeRef: 'E' if gpx_point.longitude >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: convert_to_degrees(gpx_point.longitude),
        piexif.GPSIFD.GPSAltitude: (int(gpx_point.elevation), 1)
    }
    exif_dict['GPS'] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)


def convert_to_degrees(value):
    deg = int(value)
    min = int((value - deg) * 60)
    sec = int(((value - deg) * 3600) % 60)
    return [(deg, 1), (min, 1), (sec, 1)]


def process_images_in_directory(directory_path, gpx_file):
    gpx_data = load_gpx_data(gpx_file)
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image_timestamp = get_image_timestamp(image_path)
                if image_timestamp:
                    closest_point = find_closest_track_point(gpx_data, image_timestamp)
                    if closest_point:
                        write_exif_data(image_path, closest_point)
                        print(f"Updated {image_path}")
                    else:
                        print(f"No close track point found for {image_path}")
                else:
                    print(f"No valid timestamp found in {image_path}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <directory_path> <gpx_file>")
        sys.exit(1)

    directory_path = sys.argv[1]
    gpx_file = sys.argv[2]

    # ディレクトリ内の画像に対して処理を実行
    process_images_in_directory(directory_path, gpx_file)
