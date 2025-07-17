import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import numpy as np

class VideoPlayer:
    def __init__(self, parent_frame, video_path, width=640, height=360):
        self.parent = parent_frame
        self.video_path = video_path
        self.width = width
        self.height = height

        # Try to use GPU decoding
        if hasattr(cv2, "cudacodec"):
            try:
                self.cap = cv2.cudacodec.createVideoReader(self.video_path)
                self.use_cuda = True
                self.fps = 25
                self.total_frames = 0  # cudacodec may not provide frame count
            except Exception as e:
                print("CUDA VideoReader not available, falling back to CPU:", e)
                self.cap = cv2.VideoCapture(self.video_path)
                self.use_cuda = False
                self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        else:
            self.cap = cv2.VideoCapture(self.video_path)
            self.use_cuda = False
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.speed = 1.0
        self.playing = False

        self.frame_label = ctk.CTkLabel(self.parent, text="")
        self.frame_label.pack()

        root = self.parent.winfo_toplevel()
        root.bind("<space>", self.toggle_play)
        root.bind("<Left>", lambda e: self.skip(-3))
        root.bind("<Right>", lambda e: self.skip(3))

    def play(self):
        self.playing = True
        self.update_frame()

    def pause(self):
        self.playing = False

    def toggle_play(self, event=None):
        if self.playing:
            self.pause()
        else:
            self.play()

    def skip(self, seconds):
        self.pause()
        current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        target_frame = current_frame + int(seconds * self.fps)
        target_frame = max(0, min(self.total_frames - 1, target_frame))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        self.show_frame()

    def set_speed(self, val):
        self.speed = val

    def update_frame(self):
        if not self.playing:
            return
        frame = self.read_frame()
        if frame is not None:
            self.show_frame(frame)
            delay = int(1000 / (self.fps * self.speed))
            self.parent.after(delay, self.update_frame)
        else:
            self.pause()

    def read_frame(self):
        if self.use_cuda:
            ret, gpu_frame = self.cap.nextFrame()
            if not ret:
                return None
            frame = gpu_frame.download()
        else:
            ret, frame = self.cap.read()
            if not ret:
                return None
        return frame

    def show_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((self.width, self.height))
        imgtk = ImageTk.PhotoImage(img)
        self.frame_label.configure(image=imgtk)
        self.frame_label.image = imgtk

    def release(self):
        if self.cap is not None:
            self.cap.release()
