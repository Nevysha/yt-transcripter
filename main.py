import os


def main():
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe('movie_sound.mp3')
    print(f' The text in video: \n {result["text"]}')


if __name__ == "__main__":
    main()
