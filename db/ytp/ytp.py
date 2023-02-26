import os
import streamlit as st
from pytube import Playlist
import base64

def download_video(stream, title):
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    with st.spinner(f'Downloading {title}...'):
        file_path = stream.download(output_path=download_folder)
    st.success(f'{title} downloaded successfully!')
    return file_path

def download_all_videos(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    file_paths = []
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                file_path = download_video(stream, video.title)
                file_paths.append(file_path)
    return file_paths

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
    file_paths = download_all_videos(playlist_url, resolution)
    st.success('All videos downloaded successfully!')

if file_paths:
    st.write('Downloaded videos:')
    video_bytes = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                video_bytes.append(f.read())
            st.video(video_bytes[-1])
            b64 = base64.b64encode(video_bytes[-1]).decode()
            href = f'<a href="data:file/mp4;base64,{b64}" download="{os.path.basename(file_path)}">Download {os.path.basename(file_path)}</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning(f'{file_path} does not exist.')
