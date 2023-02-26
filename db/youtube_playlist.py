import streamlit as st
from pytube import Playlist, Stream

def download_video(stream, title):
    with st.spinner(f'Downloading {title}...'):
        stream.download()
    st.success(f'{title} downloaded successfully!')

def download_selected_videos(videos):
    selected_videos = st.multiselect('Select videos to download:', videos)
    if selected_videos:
        with st.spinner('Preparing downloads...'):
            for video in selected_videos:
                stream = video.streams.get_highest_resolution()
                download_video(stream, video.title)

def download_all_videos(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                download_video(stream, video.title)

st.title('YouTube Playlist Downloader bu UB')

playlist_url = st.selectbox('Select a playlist to download:', [
    'https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH',
    'https://www.youtube.com/playlist?list=PLP8GkvaEuropX5pDd5_--G6KvpSshwRQ5'
])

playlist = Playlist(playlist_url)
videos = playlist.videos

resolution = st.selectbox('Select video resolution:', ['720p', '480p', '360p', '240p', '144p'])

if st.button('Download All Videos'):
    download_all_videos(playlist_url, resolution)
    st.success('All videos downloaded successfully!')

if st.button('Download Selected Videos'):
    download_selected_videos(videos)
    st.success('Selected videos downloaded successfully!')
