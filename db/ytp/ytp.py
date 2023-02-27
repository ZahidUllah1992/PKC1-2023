import os
import streamlit as st
from pytube import Playlist, Stream

def download_video(stream, title):
    with st.spinner(f'Downloading {title}...'):
        stream.download()
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
ok_button = st.button('OK')

if ok_button:
    if not playlist_url.startswith('https://www.youtube.com/playlist?'):
        st.warning('Please enter a valid YouTube playlist URL.')
        st.stop()

    resolutions = [
        {'label': '1080p', 'value': '1080p'},
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

    if st.button('Download Videos'):
        download_all_videos(playlist_url, resolution)
        download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        downloaded_videos = os.listdir(download_folder)
        st.write('Downloaded videos:')
        for video in downloaded_videos:
            if video.endswith('.mp4'):
                href = f'<a href="Downloads/{video}" download="{video}">Download {video}</a>'
                st.markdown(href, unsafe_allow_html=True)
