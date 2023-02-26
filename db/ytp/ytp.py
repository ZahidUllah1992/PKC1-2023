import streamlit as st
import requests
from pytube import YouTube, StreamQuery, Playlist
import base64
import os

def clear_text():
    st.session_state["url"] = ""
    st.session_state["mime"] = ""
    st.session_state["quality"] = ""

def download_file(stream, fmt):
    """  """
    if fmt == 'audio':
        title = stream.title + ' audio.'+ stream.subtype
    else:
        title = stream.title + '.'+ stream.subtype

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
            Playlist(url)
            access=True
        except:
            pass
    return access

def refine_format() -> (str, bool):
    """ """
    fmt = 'video'
    progressive = True

    return fmt, progressive


st.set_page_config(page_title="Youtube downloader", layout="wide")

# ====== SIDEBAR ======
with st.sidebar:

    st.title("Youtube download app")

    url = st.text_input("Insert your playlist link here", key="url")

    fmt, progressive = refine_format()

    if can_access(url):

        playlist = Playlist(url)
        playlist.populate_video_urls()

        mime_types = set([t.mime_type for t in playlist.videos[0].streams])
        mime_type = st.selectbox("Select a file type:", list(mime_types), key="mime")
        
        quality_values = [s.resolution for s in playlist.videos[0].streams if s.mime_type == mime_type]
        quality = st.selectbox("Select a quality:", quality_values, key="quality")
        
        selected_streams = [s for s in playlist.videos[0].streams if s.mime_type == mime_type and s.resolution == quality]
        
        if len(selected_streams) > 0:
            st.write("Selected video stream:", selected_streams[0])
            st.write("Download starts...")
            download_file(selected_streams[0], fmt)
            st.write("Download finished.")
        
        else:
            st.write("No video stream found for the selected quality.")
    
    else:
        st.write("Invalid URL.")
    
    if st.button("Clear"):
        clear_text()
