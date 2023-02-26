import os
import streamlit as st
from pytube import Playlist, Stream

# Set the source directory to the downloaded videos directory
SRC_DIR = os.path.join(os.getcwd(), "videos")

def download_video(stream, title):
    download_folder = SRC_DIR
    with st.spinner(f'Downloading {title}...'):
        stream.download(output_path=download_folder)
    st.success(f'{title} downloaded successfully!')

def download_all_videos(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    downloaded_videos = []
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                download_folder = os.path.join(os.getcwd(), 'videos')
                video_file = stream.download(output_path=download_folder)
                downloaded_videos.append(video_file)
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
    
    # Serve the videos directory using streamlit.static
    st.markdown("### Downloaded Videos")
    for video in downloaded_videos:
        st.markdown(f"* [{video}]({streamlit.static(f'videos/{video}.mp4')})")

if downloaded_videos:
    st.write('Downloaded videos:')
    for video_file in downloaded_videos:
        filename = os.path.basename(video_file)
        st.write(f'{filename}')
        st.download_button(
            label='Download Video',
            data=open(video_file, 'rb').read(),
            file_name=filename,
            mime='video/mp4'
        )