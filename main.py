import os
from pytube import YouTube
from moviepy.editor import *
import whisper
from openai import OpenAI
import argparse


def main(video_url):

    yt = YouTube(video_url)
    video_id = yt.vid_info['videoDetails']['videoId']
    video_filename = f'{video_id}.mp4'
    audio_filename = f'{video_id}.mp3'
    transcription_filename = f'{video_id}-transcription.txt'
    summary_filename = f'{video_id}-summary.txt'

    yt.streams.filter(progressive=True, file_extension='mp4')\
        .order_by('resolution').desc().first()\
        .download(filename=video_filename)

    video = VideoFileClip(video_filename)
    video.audio.write_audiofile(audio_filename)

    model = whisper.load_model('medium')
    result = model.transcribe(audio_filename)
    transcription = result['text']
    print(f' The text in video: \n {transcription}')

    with open(transcription_filename, 'w') as file:
        file.write(transcription + '\n')

    # Point to a local LMStudio server.
    client = OpenAI(base_url='http://localhost:1234/v1', api_key='not-needed')

    completion = client.chat.completions.create(
        model='local-model',  # This field is currently unused.
        messages=[
            {'role': 'system',
             'content': 'You are a helpful assistant in charge of summarizing huge transcript of video. I will provide you with the text of the video. You will summarize it while keeping interesting informations. Keep the language as it is in the video.'},
            {'role': 'user', 'content': 'The text in video: \n' + transcription},
        ],
        temperature=0.7,
    )

    print(completion.choices[0].message)

    # Store the summary in a file.
    with open(summary_filename, 'w') as file:
        file.write(completion.choices[0].message.content + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download a YouTube video, extract its audio, transcribe it, and summarize it.')
    parser.add_argument('video_url')
    args = parser.parse_args()

    main(args.video_url)
