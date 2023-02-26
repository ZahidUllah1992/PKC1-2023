import os
import streamlit as st
import base64
from pytube import Playlist

def clear_text():
    st.session_state["url"] = ""
    st.session_state["mime"] = ""
    st.session_state["quality"] = ""

def download_file(stream, fmt):
    """  """
    if fmt == 'audio':
        title = stream.title + ' audio.'+ stream_final.subtype
    else:
        title = stream.title + '.'+ stream_final.subtype

    stream.download(filename=title)
    
    if 'DESKTOP_SESSION' not in os.environ: #and os.environ('HOSTNAME')=='streamlit':
    
        with open(title, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download=\'{title}\'>\
                Here is your link \
            </a>'
            st.markdown(href, unsafe_allow_html=True)

        os.remove(title)


def can_access(url):
    """ check whether you can access the video """
    access = False
    if len(url) > 0:
        try:
            playlist = Playlist(url)
            playlist.populate_video_urls()
            access = True
        except:
            pass
    return access

def refine_format(fmt_type: str='video + audio') -> (str, bool):
    """ """
    fmt = 'video'
    progressive = True if fmt_type == 'video + audio' else False
    return fmt, progressive

st.set_page_config(page_title=" Youtube downloader", layout="wide")

# ====== SIDEBAR ======
with st.sidebar:

    st.title("Youtube download app")

    url = st.text_input("Insert your playlist link here", key="url")

    fmt_type = st.selectbox("Choose format:", ['video + audio'], key='fmt')

    fmt, progressive = refine_format(fmt_type)

    if can_access(url):

        playlist = Playlist(url)
        playlist.populate_video_urls()

        mime_types = set([t.mime_type for t in playlist.videos[0].streams])
        mime_type = st.selectbox("Mime types:", mime_types, key='mime')

        streams_mime = playlist.videos[0].streams.filter(mime_type=mime_type)

        # quality is average bitrate for audio and resolution for video
        if fmt=='audio':
            quality = set([t.abr for t in streams_mime])
            quality_type = st.selectbox('Choose average bitrate: ', quality, key='quality')
            stream_quality = streams_mime.filter(abr=quality_type)
        elif fmt=='video':
            quality = set([t.resolution for t in streams_mime])
            quality_type = st.selectbox('Choose resolution: ', quality, key='quality')
            stream_quality = streams_mime.filter(res=quality_type)

        # === Download block === #
        if stream_quality is not None:
            for i, video in enumerate(playlist.videos):
                st.write(f"Downloading video {i+1} of {len(playlist)}: {video.title}")
                stream_final = stream_quality.get_highest_resolution
