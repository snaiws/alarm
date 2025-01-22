import argparse
import time
import tkinter as tk
import winsound

def play_sound(sound_file):
    winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)


def stop_sound():
    """알람 소리 중지"""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()


def show_alert_window(message):
    """알람 메시지 창 표시"""
    def on_confirm():
        stop_sound()  # 소리 중지
        root.destroy()  # 창 닫기

    root = tk.Tk()
    root.title("알람")
    root.geometry("300x150")
    label = tk.Label(root, text=message, font=("Arial", 14))
    label.pack(pady=20)
    button = tk.Button(root, text="확인", command=on_confirm, font=("Arial", 12))
    button.pack(pady=10)
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="알람 실행 스크립트")
    parser.add_argument("--sound", required=True, help="알람 소리 파일 경로")
    parser.add_argument("--message", required=True, help="알람 메시지")
    args = parser.parse_args()

    # 알람 실행
    play_sound(args.sound)
    show_alert_window(args.message)
