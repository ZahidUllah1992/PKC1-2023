import os
import zipfile
import streamlit as st
from pytube import Playlist, Stream

def download_video(stream, title):
    with st.spinner(f'Downloading {title}...'):
        video_path = stream.download()
    st.success(f'{title} downloaded successfully!')
    return video_path

def download_all_videos(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    video_paths = []
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                video_path = download_video(stream, video.title)
                video_paths.append(video_path)
    return video_paths

st.title('YouTube Playlist Downloader')

playlist_url = st.text_input('Enter the URL of the YouTube playlist:')
if not playlist_url.startswith('https://www.youtube.com/playlist?'):
    st.warning('Please enter a valid YouTube playlist URL.')
    st.stop()

resolutions = [
    {'label': '720p', 'value': '720p'},
    {'label': '480p', 'value': '480p'},
    {'label': '360p', 'value': '360p'},
    {'label': '240p', 'value': '240p'},
    {'label': '144p', 'value': '144p'}
]

resolution = st.selectbox('Select video resolution:', [res['label'] for res in resolutions])

if st.button('Download All Videos'):
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    video_paths = download_all_videos(playlist_url, resolution)
    zip_file_path = os.path.join(download_folder, f'{playlist.title}.zip')
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for video_path in video_paths:
            zip_file.write(video_path, os.path.basename(video_path))
    st.success(f'All videos downloaded successfully and zipped at {zip_file_path}.')
    st.file_download(zip_file_path)
