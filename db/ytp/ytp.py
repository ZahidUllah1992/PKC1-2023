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
def download_file(stream, fmt):
    if fmt == 'audio':
        title = stream.title + '_audio.'+ stream.subtype
    else:
        title = stream.title + '.'+ stream.subtype

    stream.download(filename=title)
    
    if 'DESKTOP_SESSION' not in os.environ:
        with open(title, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/mp4;base64,{b64}" download=\'{title}\'>\
                Here is your link \
            </a>'
            st.markdown(href, unsafe_allow_html=True)

        os.remove(title)
def download_all_videos(playlist_url, resolution):
    playlist = Playlist(playlist_url)
    downloaded_videos = []
    with st.spinner(f'Downloading {playlist.title}...'):
        for video in playlist.videos:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                download_file(stream, 'video')
                downloaded_videos.append({'title': video.title, 'file_path': stream.default_filename})
    with ZipFile('videos.zip', 'w') as zip:
        for video in downloaded_videos:
            zip.write(video['file_path'])
            os.remove(video['file_path'])
    st.success('All videos downloaded successfully!')
    with open('videos.zip', 'rb') as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/zip;base64,{b64}" download="videos.zip">Download All Videos</a>'
        st.markdown(href, unsafe_allow_html=True)

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
    video_bytes = b''
    for video in downloaded_videos:
        if os.path.exists(video['file_path']):
            with open(video['file_path'], 'rb') as f:
                video_bytes += f.read()
            os.remove(video['file_path'])
        else:
            st.warning(f'{video["title"]} does not exist.')
    b64 = base64.b64encode(video_bytes).decode()
    href = f'<a href="data:file/mp4;base64,{b64}" download="videos.zip">Download All Videos</a>'
    st.markdown(href, unsafe_allow_html=True)
