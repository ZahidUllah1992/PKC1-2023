import os
import streamlit as st
from pytube import Playlist, Stream
import zipfile

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
    # zip all video files and return path to the zip file
    zip_file_path = os.path.join(os.path.expanduser('~'), f'{playlist.title}.zip')
    with ZipFile(zip_file_path, 'w') as zip_file:
        for path in video_paths:
            zip_file.write(path, os.path.basename(path))
    return zip_file_path

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
    playlist = Playlist(playlist_url)
    if playlist:
        download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        zip_path = download_all_videos(playlist_url, resolution)
        if zip_path:
            st.download_button(
                label='Click to download all videos',
                data=open(zip_path, 'rb').read(),
                file_name=os.path.basename(zip_path),
                mime='application/zip',
                # suggest a default download location
                # this location is only a suggestion and the user can still choose a different location
                # depending on their browser settings
                folder=download_folder
            )
    else:
        st.warning('Could not load playlist. Please try again later.')