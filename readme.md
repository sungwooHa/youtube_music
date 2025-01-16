# YouTube Music Downloader

YouTube 영상의 음원을 MP3 형식으로 다운로드하는 프로그램입니다.

## 설치 및 실행 방법

1. Python 설치 (3.8 이상 권장)
   - [Python 다운로드 페이지](https://www.python.org/downloads/)에서 다운로드 및 설치

2. 가상 환경 생성 및 활성화
   ```bash
   # 가상환경 생성
   python -m venv myenv

   # 가상환경 활성화
   # Windows:
   myenv\Scripts\activate
   # macOS/Linux:
   source myenv/bin/activate
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

## 사용 방법

1. "FFmpeg 폴더 선택" 버튼을 클릭하여 `ffmpeg-master-latest-win64-gpl-shared/bin` 폴더 선택
2. "저장 위치 변경" 버튼을 클릭하여 원하는 저장 위치 선택 (선택사항)
3. 텍스트 영역에 YouTube URL을 입력 (여러 개의 URL을 한 줄에 하나씩 입력 가능)
4. "다운로드" 버튼 클릭
5. 진행 상태를 확인하며 다운로드 대기

## 폴더 구조
```
youtube_downloader/
│
├── ffmpeg-master-latest-win64-gpl-shared/  # FFmpeg 폴더
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

- 프로그램 실행 전 반드시 FFmpeg 폴더를 선택해야 합니다.
- 다운로드는 한 번에 여러 URL을 처리할 수 있습니다.
- 다운로드 중에는 "취소" 버튼으로 작업을 중단할 수 있습니다.
- 첫 실행 시 기본 저장 경로는 "Downloads/YouTube Music" 폴더입니다.

### PowerShell 실행 관련 주의사항

PowerShell에서 가상환경 활성화 시 보안 오류가 발생할 경우:

1. 관리자 권한으로 PowerShell을 실행
2. 다음 명령어 실행:
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```
3. 'Y' 입력하여 확인

또는 다음 방법으로 가상환경 활성화:
```powershell
myenv/Scripts/activate.ps1
```

Windows CMD(명령 프롬프트)에서는 위와 같은 문제 없이 실행 가능:
```cmd
myenv\Scripts\activate
```