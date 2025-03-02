# YouTube Music Downloader

YouTube 영상의 음원을 MP3 형식으로 다운로드하는 프로그램입니다.

## Windows 설치 및 실행 방법

1. Python 설치 (3.8 이상 권장)
   - [Python 다운로드 페이지](https://www.python.org/downloads/)에서 다운로드 및 설치
   - 설치 시 "Add Python to PATH" 옵션 체크 필수

2. 가상 환경 생성 및 활성화
   ```bash
   # 가상환경 생성
   python -m venv myenv

   # 가상환경 활성화 (Windows)
   myenv\Scripts\activate
   ```

3. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

4. FFmpeg 설정
   - 프로그램과 같은 폴더에 있는 `ffmpeg-master-latest-win64-gpl-shared` 폴더 안의 `bin` 폴더를 프로그램 실행 후 선택

5. 프로그램 실행
   ```bash
   python main.py
   ```

### Windows PowerShell 실행 관련 주의사항

PowerShell에서 가상환경 활성화 시 보안 오류가 발생할 경우:
```powershell
# PowerShell 관리자 권한으로 실행 후
Set-ExecutionPolicy RemoteSigned
# 'Y' 입력하여 확인

# 또는 다음 명령어로 활성화
.\myenv\Scripts\activate.ps1
```

Windows CMD(명령 프롬프트)에서는 다음과 같이 실행:
```cmd
myenv\Scripts\activate
```

## MacOS 설치 및 실행 방법

1. Homebrew 설치 (없는 경우)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Python 및 FFmpeg 설치
   ```bash
   # Python 설치
   brew install python

   # FFmpeg 설치
   brew install ffmpeg
   ```

3. 가상 환경 생성 및 활성화
   ```bash
   # 가상환경 생성
   python3 -m venv myenv

   # 가상환경 활성화 (MacOS)
   source myenv/bin/activate
   ```

4. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

5. 프로그램 실행
   ```bash
   python main.py
   ```

## 사용 방법

### Windows 사용자
1. "FFmpeg 폴더 선택" 버튼을 클릭하여 `ffmpeg-master-latest-win64-gpl-shared/bin` 폴더 선택
2. "저장 위치 변경" 버튼을 클릭하여 원하는 저장 위치 선택 (선택사항)
3. YouTube URL 입력 및 다운로드

### MacOS 사용자
1. "FFmpeg 폴더 선택" 버튼 클릭 시 자동으로 FFmpeg 경로 감지
   - 자동 감지 실패 시 수동으로 다음 경로 중 하나 선택:
     - Apple Silicon Mac: `/opt/homebrew/bin`
     - Intel Mac: `/usr/local/bin`
   - 정확한 경로는 터미널에서 `which ffmpeg` 명령어로 확인 가능
2. "저장 위치 변경" 버튼을 클릭하여 원하는 저장 위치 선택 (선택사항)
3. YouTube URL 입력 및 다운로드

## 폴더 구조
```
youtube_downloader/
│
├── ffmpeg-master-latest-win64-gpl-shared/  # FFmpeg 폴더 (Windows 전용)
│   └── bin/
│       ├── ffmpeg.exe
│       └── ffprobe.exe
│
├── myenv/                    # 가상환경 폴더
├── main.py                   # 프로그램 메인 파일
├── requirements.txt          # 필요한 패키지 목록
└── youtube_downloader_config.json  # 프로그램 설정 파일 (자동 생성)
```

## 주의사항

- 프로그램 실행 전 반드시 FFmpeg 설정이 필요합니다.
- 다운로드는 한 번에 여러 URL을 처리할 수 있습니다 (한 줄에 하나씩 입력).
- 다운로드 중에는 "취소" 버튼으로 작업을 중단할 수 있습니다.
- 첫 실행 시 기본 저장 경로는 "Downloads/YouTube Music" 폴더입니다.
- MacOS M1/M2 사용자의 경우 Rosetta 2가 필요할 수 있습니다 (자동으로 설치 요청됨).