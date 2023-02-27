import os
import streamlit as st
from pytube import Playlist, Stream
import base64

st.title('YouTube Playlist Downloader by Codanics')

playlist_url = st.text_input('Enter the URL of the YouTube playlist:')
ok_button = st.button('OK')

resolutions = [
    {'label': '1080p', 'value': '1080p'},
    {'label': '720p', 'value': '720p'},
    {'label': '480p', 'value': '480p'},
    {'label': '360p', 'value': '360p'},
    {'label': '240p', 'value': '240p'},
    {'label': '144p', 'value': '144p'}
]

resolution = st.selectbox('Select video resolution:', [res['label'] for res in resolutions])

downloaded_videos = []

def download_video(stream, title):
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    with st.spinner(f'Downloading {title}...'):
        file_path = stream.download(output_path=download_folder)
    st.success(f'{title} downloaded successfully!')
    return file_path

def download_all_videos(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                file_path = download_video(stream, video.title)
                downloaded_videos.append({'title': video.title, 'file_path': file_path})
    return downloaded_videos

if ok_button:
    if not playlist_url.startswith('https://www.youtube.com/playlist?'):
        st.warning('Please enter a valid YouTube playlist URL.')
        st.stop()

if st.button('Download All Videos'):
    downloaded_videos = download_all_videos(playlist_url, resolution)
    if downloaded_videos:
        st.success('All videos downloaded successfully!')
    else:
        st.warning('No videos found in the playlist.')