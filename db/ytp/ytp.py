import os
import base64
import streamlit as st
from pytube import YouTube

def download_file(stream, fmt):
    if fmt == 'audio':
        title = stream.title + ' audio.' + stream_final.subtype
    else:
        title = stream.title + '.' + stream_final.subtype

    stream.download(filename=title)
    
    return title

def serve_file(file_path):
    with open(file_path, 'rb') as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/zip;base64,{b64}" download=\'{os.path.basename(file_path)}\'>\
            Here is your link \
        </a>'
        st.markdown(href, unsafe_allow_html=True)

def download_and_serve_video(url, resolution):
    yt = YouTube(url)
    video = yt.streams.filter(res=resolution).first()
    if video:
        file_path = download_file(video, 'video')
        serve_file(file_path)
        st.success('Video downloaded successfully!')
    else:
        st.error('No video stream found for the selected resolution.')
