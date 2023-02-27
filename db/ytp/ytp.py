import os
import streamlit as st
from pytube import YouTube, Playlist
from typing import List, Optional

def download_video(yt: YouTube, resolution: Optional[str] = None) -> None:
    """
    Downloads a YouTube video.
    
    Args:
        yt (YouTube): A YouTube video object.
        resolution (Optional[str]): The resolution of the video to download (e.g. "720p", "480p", "360p").
    """
    try:
        if resolution:
            stream = yt.streams.filter(res=resolution).first()
        else:
            stream = yt.streams.get_highest_resolution()
        
        if not stream:
            st.warning(f"No stream found for {yt.title}")
            return
        
        stream.download(output_path="downloads/")
        st.success(f"Downloaded {yt.title}")
    except Exception as e:
        st.error(f"Error downloading {yt.title}: {e}")
    
def download_all_videos(playlist_url: str, resolution: Optional[str] = None) -> None:
    """
    Downloads all videos in a YouTube playlist.
    
    Args:
        playlist_url (str): The URL of the YouTube playlist.
        resolution (Optional[str]): The resolution of the videos to download (e.g. "720p", "480p", "360p").
    """
    playlist = Playlist(playlist_url)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    downloaded_videos = []
    
    for video_url in playlist.video_urls:
        try:
            video = YouTube(video_url)
            download_video(video, resolution)
            downloaded_videos.append(video.title)
        except Exception as e:
            st.error(f"Error downloading {video_url}: {e}")
    
    st.success(f"Downloaded {len(downloaded_videos)} videos: {', '.join(downloaded_videos)}")
    
def main():
    st.set_page_config(page_title="YouTube Playlist Downloader", page_icon=":arrow_down:")
    st.title("YouTube Playlist Downloader")
    
    playlist_url = st.text_input("Enter the URL of the YouTube playlist:")
    resolution = st.selectbox("Select the resolution of the videos to download:", ["", "720p", "480p", "360p"])
    
    if st.button("Download"):
        if not playlist_url:
            st.warning("Please enter a playlist URL.")
        else:
            download_all_videos(playlist_url, resolution)

if __name__ == "__main__":
    main()
