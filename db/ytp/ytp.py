import os
import streamlit as st
from zipfile import ZipFile
from pytube import Playlist

def download_all_videos(playlist_url, resolution):
    # create playlist object
    playlist = Playlist(playlist_url)

    # extract video urls from playlist
    video_urls = playlist.video_urls

    # create a temporary directory to store downloaded videos
    temp_dir = "./temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # download videos and save to temporary directory
    for url in video_urls:
        video = YouTube(url)
        streams = video.streams.filter(res=resolution).first()
        streams.download(temp_dir)

    # create zip file of downloaded videos
    zip_file_path = os.path.join(temp_dir, "videos.zip")
    with ZipFile(zip_file_path, 'w') as zip_file:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                zip_file.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file),
                                               os.path.join(temp_dir, '..')))

    # delete temporary directory
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(temp_dir)

    return zip_file_path

# Set up the Streamlit app
st.set_page_config(page_title="YouTube Playlist Downloader")

# Set the title of the app
st.title("YouTube Playlist Downloader")

# Get the YouTube playlist URL from the user
playlist_url = st.text_input("Enter the YouTube playlist URL")

# Get the desired resolution from the user
resolution = st.selectbox("Select the desired resolution",
                          ["360p", "720p", "1080p"])

# Add a download button to download the videos
if st.button("Download"):
    zip_file_path = download_all_videos(playlist_url, resolution)
    with open(zip_file_path, "rb") as f:
        bytes_data = f.read()
        st.download_button(label="Download videos", data=bytes_data, 
                           file_name="videos.zip", mime="application/zip")
