import os
import streamlit as st
from pytube import Playlist, Stream
import base64
import rarfile

def download_video(stream, title):
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    with st.spinner(f'Downloading {title}...'):
        file_path = stream.download(output_path=download_folder)
    st.success(f'{title} downloaded successfully!')
    return file_path

def download_all_videos(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    downloaded_videos = []
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                file_path = download_video(stream, video.title)
                downloaded_videos.append({'title': video.title, 'file_path': file_path})
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

if st.button('Download All Videos'):
    downloaded_videos = download_all_videos(playlist_url, resolution)
    st.success('All videos downloaded successfully!')

if downloaded_videos:
    with rarfile.RarFile('videos.rar', 'w') as rar:
        for video in downloaded_videos:
            if os.path.exists(video['file_path']):
                rar.write(video['file_path'], arcname=video['title'])
                os.remove(video['file_path'])
            else:
                st.warning(f'{video["title"]} does not exist.')
    with open('videos.rar', 'rb') as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:application/x-rar-compressed;base64,{b64}" download=\'videos.rar\'>Download All Videos</a>'
        st.markdown(href, unsafe_allow_html=True)
