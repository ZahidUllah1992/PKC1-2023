import os
import streamlit as st
from pytube import Playlist, Stream
import tempfile

def download_video(stream, title):
    download_folder = os.path.join(tempfile.gettempdir(), 'youtube_playlist_downloader')
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    with st.spinner(f'Downloading {title}...'):
        stream.download(output_path=download_folder)
    st.success(f'{title} downloaded successfully!')

def download_all_videos(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                download_video(stream, video.title)

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
    download_all_videos(playlist_url, resolution)
    st.success('All videos downloaded successfully!')
