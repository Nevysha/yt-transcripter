# Quick Readme

This python script downloads a YouTube video and creates its transcript using the Whisper python library.
It then summarizes the transcript using LMStudio. 

The video is downloaded as an mp4 file, and its audio is extracted as an mp3 file. 

To use this script, simply replace the YouTube video link in the `main()` function with the link of the video you want to download and process. 
The resulting transcript and summary will be saved in the same directory where the script is run from.
Note that LMStudio needs to be running locally for this script to work properly, as it makes API requests to LMStudio to generate the summaries. 

This is a simple example of how to use the Whisper and LMStudio libraries to process YouTube videos.

# Requirements
`choco install ffmpeg` # Windows

`pip install openai-whisper`

`pip install moviepy`

`pip install pytube`

`pip install openai`
