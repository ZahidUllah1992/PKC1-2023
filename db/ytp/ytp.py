import os
import base64
import streamlit as st
from pytube import Playlist, Stream

def download_video(stream, title):
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    with st.spinner(f'Downloading {title}...'):
        stream.download(output_path=download_folder)
    st.success(f'{title} downloaded successfully!')
    return os.path.join(download_folder, title + '.mp4')

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
    st.write('Downloaded videos:')
    for video in downloaded_videos:
        st.write(video['title'])
        st.markdown(f'<a href="data:file/mp4;base64,{base64.b64encode(open(video["file_path"], "rb").read()).decode()}">Download</a>', unsafe_allow_html=True)
