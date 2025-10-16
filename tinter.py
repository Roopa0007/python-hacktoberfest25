import tkinter as tk
from tkinter import filedialog
import pygame
from mutagen.mp3 import MP3

pygame.mixer.init()

current_song = None
paused = False
song_length = 0

def load_song():
    global current_song, song_length
    current_song = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if current_song:
        pygame.mixer.music.load(current_song)
        audio = MP3(current_song)
        song_length = audio.info.length
        pygame.mixer.music.play()
        label.config(text="🎵 Playing: " + current_song.split("/")[-1])
        update_progress()

def stop_song():
    pygame.mixer.music.stop()
    progress.set(0)
    label.config(text="⏹ Music Stopped")

def pause_resume_song():
    global paused
    if pygame.mixer.music.get_busy():
        if not paused:
            pygame.mixer.music.pause()
            label.config(text="⏸ Paused")
            paused = True
        else:
            pygame.mixer.music.unpause()
            label.config(text="🎶 Resumed: " + current_song.split("/")[-1])
            paused = False

def set_volume(val):
    volume = float(val)
    pygame.mixer.music.set_volume(volume)

def update_progress():
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000
        if song_length > 0:
            progress.set((current_time / song_length) * 100)
        root.after(500, update_progress)

root = tk.Tk()
root.title("🎵 Butterfly Music Player 🎶")
root.geometry("400x320")
root.resizable(False, False)
root.config(bg="#202020")

label = tk.Label(root, text="Load a song to play", fg="white", bg="#202020", font=("Arial", 12))
label.pack(pady=15)

tk.Button(root, text="🎶 Load & Play", width=20, command=load_song, bg="#3b82f6", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
tk.Button(root, text="⏸ Pause / Resume", width=20, command=pause_resume_song, bg="#f59e0b", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
tk.Button(root, text="⏹ Stop", width=20, command=stop_song, bg="#ef4444", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

tk.Label(root, text="🔊 Volume", bg="#202020", fg="white", font=("Arial", 10)).pack(pady=(15, 0))
volume_slider = tk.Scale(root, from_=0, to=1, resolution=0.1, orient="horizontal", length=200, command=set_volume, bg="#202020", fg="white")
volume_slider.set(0.7)
volume_slider.pack(pady=5)

progress = tk.DoubleVar()
progress_bar = tk.Scale(root, variable=progress, from_=0, to=100, orient="horizontal", length=300, bg="#202020", fg="white", state="disabled")
progress_bar.pack(pady=15)

root.mainloop()
