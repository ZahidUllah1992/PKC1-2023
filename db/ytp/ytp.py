import os
import requests
from zipfile import ZipFile
import streamlit as st

# Define function to download videos
def download_all_videos(playlist_url, resolution):
    # Set output path
    output_path = os.path.join(os.getcwd(), "downloads")
    os.makedirs(output_path, exist_ok=True)

    # Get playlist info
    playlist_info_url = f"{playlist_url}&pbj=1"
    playlist_info_response = requests.get(playlist_info_url)
    playlist_info_json = playlist_info_response.json()[1]["response"]["contents"]["twoColumnWatchNextResults"]["playlist"]["playlist"]["contents"]

    # Filter out unavailable videos and get video urls
    video_urls = []
    for video in playlist_info_json:
        if "unavailable" not in video["playlistPanelVideoRenderer"]["thumbnailOverlays"][0]["thumbnailOverlayResumePlaybackRenderer"]["style"]:
            video_id = video["playlistPanelVideoRenderer"]["videoId"]
            video_title = video["playlistPanelVideoRenderer"]["title"]["runs"][0]["text"]
            video_url = f"https://www.youtube.com/watch?v={video_id}&pbj=1"
            video_info_response = requests.get(video_url)
            video_info_json = video_info_response.json()[1]["response"]["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]
            video_formats = video_info_json["videoPlayer"]["streamingData"]["adaptiveFormats"]
            video_formats = [f for f in video_formats if "video/mp4" in f["mimeType"]]
            video_formats = sorted(video_formats, key=lambda f: int(f["qualityLabel"][:-1]))
            if resolution == "max":
                video_format = video_formats[-1]
            else:
                video_format = next((f for f in video_formats if resolution in f["qualityLabel"]), None)
            if video_format:
                video_url = video_format["url"]
                video_urls.append((video_title, video_url))

    # Download videos and add to zip file
    zip_file_path = os.path.join(output_path, "videos.zip")
    with ZipFile(zip_file_path, 'w') as zip_file:
        for video_title, video_url in video_urls:
            video_file_path = os.path.join(output_path, f"{video_title}.mp4")
            with open(video_file_path, 'wb') as video_file:
                video_response = requests.get(video_url, stream=True)
                total_length = video_response.headers.get('content-length')
                if total_length is None:  # no content length header
                    video_file.write(video_response.content)
                else:
                    downloaded = 0
                    total_length = int(total_length)
                    for data in video_response.iter_content(chunk_size=max(int(total_length / 1000), 1024 * 1024)):
                        downloaded += len(data)
                        video_file.write(data)
                        done = int(50 * downloaded / total_length)
                        st.progress(done/50)
            zip_file.write(video_file_path)

    return zip_file_path

# Set up Streamlit app
st.set_page_config(page_title="YouTube Playlist Downloader")
st.title("YouTube Playlist Downloader")

# Get user input
playlist_url = st.text_input("Enter YouTube playlist URL:")
resolution = st.selectbox("Select video resolution:", ["max", "1080", "720", "480", "360", "240"])

# Download videos and add to zip file

if st.button('Download All Videos'):
    playlist = Playlist(playlist_url)
    if playlist:
        download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        st.download_button(
            label='Click to download all videos',
            data=download_all_videos(playlist_url, resolution),
            file_name=f'{playlist.title}.zip',
            mime='application/zip',
            # suggest a default download location
            # this location is only a suggestion and the user can still choose a different location
            # depending on their browser settings
            folder=download_folder
        )
    else:
        st.warning('Could not load playlist. Please try again later.')
