import os
from moviepy.editor import *
import whisper
from openai import OpenAI


def main():
    from pytube import YouTube
    yt = YouTube('https://www.youtube.com/watch?v=m0FLBbdvThY')
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
        'video.mp4')

    video = VideoFileClip(os.path.join("video.mp4"))
    video.audio.write_audiofile(os.path.join("movie_sound.mp3"))

    model = whisper.load_model("medium")
    audio = whisper.load_audio("movie_sound.mp3")
    result = model.transcribe('movie_sound.mp3')
    print(f' The text in video: \n {result["text"]}')

    with open("result.txt", "w") as file:
        file.write(result["text"])

    # Server running locally on LMStudio
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant in charge of summarizing huge transcript of video. I will provide you with the text of the video. You will summarize it while keeping interesting informations. Keep the language as it is in the video."},
            {"role": "user", "content": "The text in video: \n" + result["text"]},
        ],
        temperature=0.7,
    )

    print(completion.choices[0].message)

    # store the result in a file
    with open("result_summary.txt", "w") as file:
        file.write(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
