#Convert Videos to mp3 

import os
import subprocess

videos=os.listdir("Videos")

for video in videos:
    video_number=video.split("#")[1].split(".")[0]
    video_name=video.split("Sigma")[0].strip()

    subprocess.run(['ffmpeg','-i', f'Videos/{video}', f'audios/{video_number}_{video_name}.mp3'])