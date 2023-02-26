import os
import streamlit as st
from pytube import Playlist, Stream
def download_video(stream, title, download_dir):
    with st.spinner(f'Downloading {title}...'):
        stream.download(output_path=download_dir)
    st.success(f'{title} downloaded successfully!')

def download_all_videos(playlist_url, resolution, download_dir):
    playlist = Playlist(playlist_url)
    downloaded_videos = []
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                download_video(stream, video.title, download_dir)
                downloaded_videos.append(video.title)
    return downloaded_videos

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

download_dir = st.text_input('Enter the download directory:')
if not os.path.exists(download_dir):
    st.warning('Please enter a valid directory path.')
    st.stop()

if st.button('Download All Videos'):
    downloaded_videos = download_all_videos(playlist_url, resolution, download_dir)
    st.success('All videos downloaded successfully!')

if downloaded_videos:
    st.write('Downloaded videos:')
    for video in downloaded_videos:
        st.write(video)
