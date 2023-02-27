import os
import streamlit as st
from pytube import Playlist, Stream
import base64

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

def download_file(stream, fmt):
    """  """
    if fmt == 'audio':
        title = stream.title + ' audio.'+ stream_final.subtype
    else:
        title = stream.title + '.'+ stream_final.subtype

    stream.download(filename=title)
    
    if 'DESKTOP_SESSION' not in os.environ:
        with open(title, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download=\'{title}\'>\
                Here is your link \
            </a>'
            st.markdown(href, unsafe_allow_html=True)

        os.remove(title)

st.title('YouTube Playlist Downloader by Codanins')
st.text('Videos will be downloaded in two steps')
st.text('downloding time will depends on Number of videos in playlist and Video resolution')

playlist_url = st.text_input('Enter the URL of the YouTube playlist:')
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

downloaded_videos = []
if st.button('Download All Videos to App Server'):
    downloaded_videos = download_all_videos(playlist_url, resolution)
    st.success('All videos downloaded successfully!')
    
if downloaded_videos:
    st.write('Downloaded videos:')
    for video in downloaded_videos:
        if os.path.exists(video['file_path']):
            with open(video['file_path'], 'rb') as f:
                video_bytes = f.read()
            b64 = base64.b64encode(video_bytes).decode()
            href = f'<a href="data:file/mp4;base64,{b64}" download="{video["title"]}.mp4">Download {video["title"]}</a>'
            st.markdown(href, unsafe_allow_html=True)
            os.remove(video['file_path'])

if st.button('Download Videos in One '):
    playlist = Playlist(playlist_url)
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                download_file(stream, video.title)
    st.success(f'{playlist.title} downloaded successfully! Check your Downloads folder for the files.')
