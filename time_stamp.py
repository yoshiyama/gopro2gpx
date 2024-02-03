import subprocess
import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import piexif

# 動画のメタデータから撮影開始時刻、長さ、フレームレートを取得
def get_video_metadata(video_path):
    # 撮影開始時刻を取得
    cmd_start_time = ['exiftool', '-CreateDate', '-s', '-s', '-s', video_path]
    result_start_time = subprocess.run(cmd_start_time, capture_output=True, text=True)
    start_time_str = result_start_time.stdout.strip()
    start_time = datetime.datetime.strptime(start_time_str, '%Y:%m:%d %H:%M:%S')

    # 動画の長さを取得
    cmd_duration = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    result_duration = subprocess.run(cmd_duration, capture_output=True, text=True)
    duration = float(result_duration.stdout.strip())

    # フレームレートを取得
    cmd_frame_rate = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=r_frame_rate',
                      '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    result_frame_rate = subprocess.run(cmd_frame_rate, capture_output=True, text=True)
    frame_rate_str = result_frame_rate.stdout.strip()
    frame_rate = eval(frame_rate_str)

    return start_time, duration, frame_rate

# EXIFデータに撮影時刻を追加する関数
def add_exif_datetime(image_path, datetime_obj):
    img = Image.open(image_path)
    exif_dict = {'0th': {}, 'Exif': {}, 'GPS': {}, '1st': {}, 'thumbnail': None}

    # EXIFのDateTimeオリジナルフィールドを設定
    exif_dict['0th'][piexif.ImageIFD.DateTime] = datetime_obj.strftime("%Y:%m:%d %H:%M:%S")
    exif_bytes = piexif.dump(exif_dict)
    img.save(image_path, exif=exif_bytes)
    img.close()



# 画像にタイムスタンプを描画し、EXIFデータにも撮影時刻を追加する
def add_timestamp_to_image(image_path, timestamp):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        text = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        draw.text((10, 10), text, (255, 255, 255), font=font)

        # EXIFデータにも撮影時刻を追加
        add_exif_datetime(image_path, timestamp)

# 動画から画像を抽出し、タイムスタンプを付ける
def extract_frames_with_timestamps(video_path, output_folder, start_time, duration, frame_rate, timestamp_file):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(timestamp_file, 'w') as f:
        total_frames = int(duration * frame_rate)
        for i in range(total_frames):
            offset_seconds = i / frame_rate
            timestamp = start_time + datetime.timedelta(seconds=offset_seconds)
            img_path = f'{output_folder}/img{i:03d}.jpg'

            # 動画の開始からのオフセット時間を秒単位で計算
            seek_time = offset_seconds

            cmd = [
                'ffmpeg', '-ss', str(seek_time), '-i', video_path, '-frames:v', '1', img_path
            ]
            subprocess.run(cmd, check=True)

            # 画像にEXIFとして撮影時刻を追加
            add_exif_datetime(img_path, timestamp)

            # タイムスタンプをテキストファイルに記録
            f.write(f'{img_path}: {timestamp}\n')

# 実行
video_file = '/mnt/f/GoPro-Seto_Danchi/20231006/Back/GH020239.MP4'
output_dir = '/mnt/f/GoPro-Seto_Danchi/20231006/Back/GH020239'
timestamp_file = '/mnt/f/GoPro-Seto_Danchi/20231006/Back/GH020239/timestamps.txt'

start_time, duration, frame_rate = get_video_metadata(video_file)
extract_frames_with_timestamps(video_file, output_dir, start_time, duration, frame_rate, timestamp_file)
