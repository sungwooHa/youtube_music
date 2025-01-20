import PyInstaller.__main__
import os
import sys
import shutil
import glob

# 현재 작업 디렉토리 출력
print("Current working directory:", os.getcwd())

# 빌드 및 배포 폴더 설정
BUILD_DIR = 'build'
DIST_DIR = 'dist'
RELEASE_DIR = 'release'

# FFmpeg 파일들의 전체 경로 지정
FFMPEG_DIR = os.path.abspath('ffmpeg-master-latest-win64-gpl-shared/bin')
FFMPEG_EXE = os.path.join(FFMPEG_DIR, 'ffmpeg.exe')
FFPROBE_EXE = os.path.join(FFMPEG_DIR, 'ffprobe.exe')

# 경로 출력
print("FFMPEG path:", FFMPEG_EXE)
print("FFPROBE path:", FFPROBE_EXE)

# FFmpeg 파일들이 존재하는지 확인
if not os.path.exists(FFMPEG_EXE) or not os.path.exists(FFPROBE_EXE):
    raise FileNotFoundError(f"FFmpeg 파일을 찾을 수 없습니다.\n확인된 경로:\n{FFMPEG_EXE}\n{FFPROBE_EXE}")

# 기존 빌드 폴더들 정리
for dir_path in [BUILD_DIR, DIST_DIR, RELEASE_DIR]:
    if os.path.exists(dir_path):
        print(f"Cleaning {dir_path}/")
        shutil.rmtree(dir_path)

# 파일 복사를 위한 임시 디렉토리 생성
temp_dir = 'temp_ffmpeg'
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

# FFmpeg 실행 파일과 모든 DLL 파일들을 임시 디렉토리로 복사
print("\nCopying FFmpeg files...")
for file in glob.glob(os.path.join(FFMPEG_DIR, '*')):
    if file.endswith(('.exe', '.dll')):
        print(f"Copying: {os.path.basename(file)}")
        shutil.copy2(file, temp_dir)

# PyInstaller 명령어 생성
pyinstaller_args = [
    'main.py',
    '--onefile',
    '--windowed',
    '--name=YouTube Music Downloader',
]

# 모든 FFmpeg 관련 파일들을 add-binary로 추가
for file in os.listdir(temp_dir):
    pyinstaller_args.append(f'--add-binary={os.path.join(temp_dir, file)};.')

# 나머지 PyInstaller 옵션 추가
pyinstaller_args.extend([
    '--hidden-import=tkinter',
    '--hidden-import=yt_dlp',
    '--clean',
    f'--distpath={DIST_DIR}'
])

print("\nStarting build process...")
PyInstaller.__main__.run(pyinstaller_args)

# 임시 디렉토리 삭제
shutil.rmtree(temp_dir)

# Release 폴더 생성 및 파일 이동
os.makedirs(RELEASE_DIR, exist_ok=True)
shutil.move(
    os.path.join(DIST_DIR, 'YouTube Music Downloader.exe'),
    os.path.join(RELEASE_DIR, 'YouTube Music Downloader.exe')
)

print("\nBuild completed!")
print(f"Executable created at: {os.path.abspath(os.path.join(RELEASE_DIR, 'YouTube Music Downloader.exe'))}") 