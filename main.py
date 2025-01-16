import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import os
import json
from collections import deque
import threading

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Music Downloader")
        
        # 설정 파일 경로
        self.config_file = 'youtube_downloader_config.json'
        
        # 설정 불러오기
        self.load_config()
        
        # 작업 상태
        self.is_downloading = False
        
        # GUI 구성
        self.create_gui()
        
        # 프로그램 종료 시 설정 저장
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        """설정 파일 불러오기"""
        default_config = {
            'ffmpeg_path': '',
            'save_path': os.path.join(os.path.expanduser("~"), "Downloads", "YouTube Music")
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                    self.ffmpeg_path = config.get('ffmpeg_path', default_config['ffmpeg_path'])
                    self.save_path = config.get('save_path', default_config['save_path'])
            else:
                self.ffmpeg_path = default_config['ffmpeg_path']
                self.save_path = default_config['save_path']
                self.recent_urls = deque(maxlen=10)
        except:
            self.ffmpeg_path = default_config['ffmpeg_path']
            self.save_path = default_config['save_path']

    def save_config(self):
        """설정 파일 저장"""
        config = {
            'ffmpeg_path': self.ffmpeg_path,
            'save_path': self.save_path
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.update_status(f"설정 저장 중 오류 발생: {str(e)}")

    def on_closing(self):
        """프로그램 종료 시 처리"""
        if self.is_downloading:
            if messagebox.askokcancel("종료 확인", "다운로드가 진행 중입니다. 정말 종료하시겠습니까?"):
                self.is_downloading = False
                self.save_config()
                self.root.destroy()
        else:
            self.save_config()
            self.root.destroy()


    def update_status(self, message):
        """상태 메시지 업데이트"""
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')
        self.root.update_idletasks()

    def select_save_path(self):
        """저장 경로 선택"""
        new_path = filedialog.askdirectory(title="음악 파일을 저장할 폴더를 선택하세요",
                                         initialdir=self.save_path)
        if new_path:
            self.save_path = new_path
            self.save_path_label.config(text=f"현재 저장 경로:\n{self.save_path}")
            self.update_status(f"저장 경로가 변경되었습니다: {self.save_path}")
            self.save_config()

    def select_ffmpeg(self):
        """FFmpeg 폴더 선택"""
        ffmpeg_folder = filedialog.askdirectory(title="FFmpeg가 설치된 폴더를 선택하세요")
        if ffmpeg_folder:
            ffmpeg_path = os.path.join(ffmpeg_folder, 'ffmpeg.exe')
            ffprobe_path = os.path.join(ffmpeg_folder, 'ffprobe.exe')
            
            if os.path.exists(ffmpeg_path) and os.path.exists(ffprobe_path):
                self.ffmpeg_path = ffmpeg_folder
                self.ffmpeg_label.config(text=f"FFmpeg 경로: {ffmpeg_folder}")
                self.update_status("FFmpeg 설정이 완료되었습니다.")
                self.save_config()
            else:
                messagebox.showerror("오류", 
                    "선택한 폴더에서 FFmpeg를 찾을 수 없습니다.\n"
                    "ffmpeg.exe와 ffprobe.exe가 있는 폴더를 선택해주세요.")

    def progress_hook(self, d):
        """다운로드 진행 상황 업데이트"""
        if d['status'] == 'downloading':
            try:
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                
                if total:
                    progress = (downloaded / total) * 100
                    self.progress_bar['value'] = progress
                    self.update_status(f"다운로드 중... {progress:.1f}%")
            except Exception:
                self.update_status("다운로드 진행 중...")
        elif d['status'] == 'finished':
            self.update_status("다운로드 완료! 오디오 변환 중...")
            self.progress_bar['value'] = 100

    def start_download_thread(self):
        """다운로드 스레드 시작"""
        if not self.ffmpeg_path:
            messagebox.showerror("오류", "FFmpeg 폴더를 먼저 선택해주세요.")
            return
            
        urls = self.url_text.get("1.0", tk.END).strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()]  # 빈 줄 제거
        
        if not urls:
            messagebox.showerror("오류", "URL을 입력해주세요.")
            return
            
        if self.is_downloading:
            return
            
        self.is_downloading = True
        self.download_button.config(state='disabled')
        self.cancel_button.config(state='normal')
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state='disabled')
        
        thread = threading.Thread(target=self.download_multiple, args=(urls,))
        thread.daemon = True
        thread.start()

    def cancel_download(self):
        """다운로드 취소"""
        if self.is_downloading:
            self.is_downloading = False
            self.update_status("다운로드가 취소되었습니다.")
            self.download_button.config(state='normal')
            self.cancel_button.config(state='disabled')
            self.progress_bar['value'] = 0

    def download_multiple(self, urls):
        """여러 URL 다운로드 실행"""
        try:
            os.makedirs(self.save_path, exist_ok=True)
            
            def my_hook(d):
                if not self.is_downloading:
                    raise Exception("다운로드가 취소되었습니다.")
                self.root.after(0, self.progress_hook, d)
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [my_hook],
                'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
                'ffmpeg_location': self.ffmpeg_path,
            }
            
            total_urls = len(urls)
            for i, url in enumerate(urls, 1):
                if not self.is_downloading:
                    break
                    
                try:
                    self.root.after(0, self.update_status, f"\n[{i}/{total_urls}] {url} 다운로드 시작...")
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        error_code = ydl.download([url])
                        
                        if error_code != 0:
                            self.root.after(0, self.update_status, f"[{i}/{total_urls}] 다운로드 실패: {url}")
                            continue
                        
                    self.root.after(0, self.update_status, f"[{i}/{total_urls}] 다운로드 완료: {url}")
                    
                except Exception as e:
                    self.root.after(0, self.update_status, f"[{i}/{total_urls}] 오류 발생: {url}\n{str(e)}")
            
            if self.is_downloading:
                self.root.after(0, self.download_complete)
            
        except Exception as e:
            if self.is_downloading:
                error_msg = str(e)
                self.root.after(0, self.download_error, error_msg)
        
        finally:
            self.root.after(0, self.download_cleanup)

    def download_complete(self):
        """다운로드 완료 처리"""
        self.update_status("다운로드 및 변환 완료!")
        messagebox.showinfo("완료", f"다운로드가 완료되었습니다.\n저장 위치: {self.save_path}")

    def download_error(self, error_msg):
        """다운로드 오류 처리"""
        self.update_status(f"오류 발생: {error_msg}")
        messagebox.showerror("오류", f"다운로드 중 오류가 발생했습니다:\n{error_msg}")

    def download_cleanup(self):
        """다운로드 완료 후 정리"""
        self.is_downloading = False
        self.download_button.config(state='normal')
        self.cancel_button.config(state='disabled')
        self.progress_bar['value'] = 0
        
        try:
            for file in os.listdir(self.save_path):
                if file.endswith(".part"):
                    os.remove(os.path.join(self.save_path, file))
        except:
            pass

    def create_gui(self):
        """GUI 생성"""
        # FFmpeg 설정 프레임
        ffmpeg_frame = ttk.LabelFrame(self.root, text="FFmpeg 설정", padding="5")
        ffmpeg_frame.pack(fill="x", padx=10, pady=5)
        
        self.ffmpeg_label = ttk.Label(ffmpeg_frame, text=f"FFmpeg 경로: {self.ffmpeg_path or '설정되지 않음'}", wraplength=350)
        self.ffmpeg_label.pack(pady=5)
        
        self.ffmpeg_button = ttk.Button(ffmpeg_frame, text="FFmpeg 폴더 선택", command=self.select_ffmpeg)
        self.ffmpeg_button.pack(pady=5)
        
        # 저장 경로 설정 프레임
        save_frame = ttk.LabelFrame(self.root, text="저장 위치 설정", padding="5")
        save_frame.pack(fill="x", padx=10, pady=5)
        
        self.save_path_label = ttk.Label(save_frame, text=f"현재 저장 경로:\n{self.save_path}", wraplength=350)
        self.save_path_label.pack(pady=5)
        
        self.save_path_button = ttk.Button(save_frame, text="저장 위치 변경", command=self.select_save_path)
        self.save_path_button.pack(pady=5)
        
        # URL 입력 프레임
        url_frame = ttk.LabelFrame(self.root, text="URL 입력 (한 줄에 하나씩 입력)", padding="5")
        url_frame.pack(fill="x", padx=10, pady=5)
        
        # 스크롤바 추가
        scroll_frame = ttk.Frame(url_frame)
        scroll_frame.pack(fill="both", expand=True)
        
        self.url_scrollbar = ttk.Scrollbar(scroll_frame)
        self.url_scrollbar.pack(side="right", fill="y")
        
        self.url_text = tk.Text(scroll_frame, height=6, width=45, yscrollcommand=self.url_scrollbar.set)
        self.url_text.pack(side="left", fill="both", expand=True)
        
        self.url_scrollbar.config(command=self.url_text.yview)
        
        button_frame = ttk.Frame(url_frame)
        button_frame.pack(fill="x", pady=5)
        
        self.download_button = ttk.Button(button_frame, text="다운로드", command=self.start_download_thread)
        self.download_button.pack(side="left", padx=5, expand=True)
        
        self.cancel_button = ttk.Button(button_frame, text="취소", command=self.cancel_download, state='disabled')
        self.cancel_button.pack(side="right", padx=5, expand=True)
        
        # 상태 프레임
        status_frame = ttk.LabelFrame(self.root, text="진행 상태", padding="5")
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_text = tk.Text(status_frame, height=5, width=45)
        self.status_text.pack(padx=5, pady=5)
        self.status_text.config(state='disabled')
        
        self.progress_bar = ttk.Progressbar(status_frame, length=300, mode='determinate')
        self.progress_bar.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.geometry("400x650")
    root.mainloop()