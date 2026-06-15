import os
import vlc
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class UniversalMusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Universal Music Player")
        self.geometry("750x400")
        self.resizable(False, False)
        
        try: self.iconbitmap('app_icon.ico')
        except: pass

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.playlist = []
        self.current_index = 0
        self.is_paused = False
        self.setup_ui()
        self.check_track_timer()

    def setup_ui(self):
        left_frame = ctk.CTkFrame(self, width=420, corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        self.song_label = ctk.CTkLabel(left_frame, text="No Media Loaded", font=("Arial", 15, "bold"), wraplength=380)
        self.song_label.pack(pady=20)
        self.load_btn = ctk.CTkButton(left_frame, text="📂 Load Any Audio/Video Files", command=self.load_files)
        self.load_btn.pack(pady=5)
        self.progress_slider = ctk.CTkSlider(left_frame, from_=0, to=1000, command=self.slide_seek)
        self.progress_slider.set(0)
        self.progress_slider.pack(fill="x", padx=30, pady=10)
        self.time_label = ctk.CTkLabel(left_frame, text="00:00 / 00:00", font=("Arial", 12))
        self.time_label.pack()
        controls_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        controls_frame.pack(pady=15)
        ctk.CTkButton(controls_frame, text="⏮", width=50, command=self.prev_song).pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="▶ Play", width=70, fg_color="#2ecc71", command=self.play_music).pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="⏸ Pause", width=70, fg_color="#f39c12", command=self.pause_music).pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="⏹ Stop", width=70, fg_color="#e74c3c", command=self.stop_music).pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="⏭", width=50, command=self.next_song).pack(side="left", padx=5)
        vol_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        vol_frame.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(vol_frame, text="🔊").pack(side="left", padx=5)
        self.volume_slider = ctk.CTkSlider(vol_frame, from_=0, to=100, command=self.set_volume)
        self.volume_slider.set(70)
        self.volume_slider.pack(side="left", fill="x", expand=True)
        self.player.audio_set_volume(70)
        right_frame = ctk.CTkFrame(self, width=280, corner_radius=10)
        right_frame.pack(side="right", fill="both", padx=(0, 15), pady=15)
        ctk.CTkLabel(right_frame, text="📋 Universal Queue", font=("Arial", 14, "bold")).pack(pady=10)
        self.playlist_box = ctk.CTkScrollableFrame(right_frame, width=250, height=300)
        self.playlist_box.pack(fill="both", expand=True, padx=5, pady=5)
        self.buttons_list = []

    def load_files(self):
        files = filedialog.askopenfilenames(title="Select Music & Video Files", filetypes=[("All Audio & Video", "*.mp3 *.mp4 *.m4a *.wav *.aac *.flac *.wma *.mkv *.avi")])
        if not files: return
        self.playlist = list(files)
        self.current_index = 0
        for btn in self.buttons_list: btn.destroy()
        self.buttons_list.clear()
        for idx, path in enumerate(self.playlist):
            filename = os.path.basename(path)
            btn = ctk.CTkButton(self.playlist_box, text=f"{idx+1}. {filename[:28]}", anchor="w", fg_color="transparent", text_color="white", command=lambda i=idx: self.jump_to_song(i))
            btn.pack(fill="x", pady=2)
            self.buttons_list.append(btn)
        self.highlight_current_track()
        self.prepare_track()

    def highlight_current_track(self):
        for idx, btn in enumerate(self.buttons_list):
            btn.configure(fg_color="#3498db" if idx == self.current_index else "transparent")

    def prepare_track(self):
        if not self.playlist: return
        track_path = self.playlist[self.current_index]
        self.song_label.configure(text=os.path.basename(track_path))
        media = self.instance.media_new(track_path)
        self.player.set_media(media)
        self.is_paused = False

    def play_music(self):
        if not self.playlist: return
        if self.is_paused:
            self.player.play()
            self.is_paused = False
        else:
            self.prepare_track()
            self.player.play()
        self.highlight_current_track()

    def pause_music(self):
        if self.player.is_playing():
            self.player.pause()
            self.is_paused = True

    def stop_music(self):
        self.player.stop()
        self.is_paused = False
        self.progress_slider.set(0)

    def next_song(self):
        if not self.playlist: return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_direct()

    def prev_song(self):
        if not self.playlist: return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_direct()

    def jump_to_song(self, index):
        self.current_index = index
        self.play_direct()

    def play_direct(self):
        self.player.stop()
        self.play_music()

    def set_volume(self, value):
        self.player.audio_set_volume(int(float(value)))

    def slide_seek(self, value):
        if self.playlist:
            self.player.set_position(float(value) / 1000.0)

    def check_track_timer(self):
        if self.playlist and self.player.is_playing():
            vlc_pos = self.player.get_position()
            if vlc_pos > 0:
                self.progress_slider.set(vlc_pos * 1000.0)
            cur_time = self.player.get_time() // 1000
            total_time = self.player.get_length() // 1000
            if cur_time >= 0 and total_time > 0:
                c_min, c_sec = divmod(cur_time, 60)
                t_min, t_sec = divmod(total_time, 60)
                self.time_label.configure(text=f"{c_min:02d}:{c_sec:02d} / {t_min:02d}:{t_sec:02d}")
                if cur_time >= total_time - 1 and total_time > 5:
                    self.next_song()
        self.after(500, self.check_track_timer)

if __name__ == "__main__":
    app = UniversalMusicPlayer()
    app.mainloop()
