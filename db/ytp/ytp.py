import os
import streamlit as st
from zipfile import ZipFile
from pytube import Playlist

def download_all_videos(playlist_url, resolution='720p'):
    playlist = Playlist(playlist_url)
    playlist.populate_video_urls()
    zip_file_path = f'{playlist.title}.zip'

    with ZipFile(zip_file_path, 'w') as zip_file:
        for url in playlist.video_urls:
            try:
                video = YouTube(url)
                stream = video.streams.filter(res=resolution, file_extension='mp4').first()
                if stream is None:
                    st.warning(f"No '{resolution}' video available for {video.title} ({url})")
                    continue
                st.info(f"Downloading '{resolution}' video for {video.title} ({url})...")
                stream.download(output_path='./', filename_prefix='temp_')
                zip_file.write(f'temp_{stream.default_filename}')
                os.remove(f'temp_{stream.default_filename}')
            except Exception as e:
                st.warning(f"Error downloading {url}: {str(e)}")
                continue

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
