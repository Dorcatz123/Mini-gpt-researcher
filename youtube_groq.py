import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load the API key from the environment variables
YOUTUBE_API_KEY = 'AIzaSyDSgUdj73fSDu5ZIXICe9WfN8RmeIl2Hro'
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def youtube_search(query, max_results=5):
    """Search YouTube for videos based on the query."""
    if not YOUTUBE_API_KEY:
        raise ValueError("YouTube API key is missing. Please set it in the .env file.")

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch YouTube videos: {response.json()}")

    videos = response.json().get("items", [])
    results = []

    for video in videos:
        title = video["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
        description = video["snippet"]["description"]
        results.append(f"**Title:** {title}\n**URL:** {video_url}\n**Description:** {description}\n")

    with open("reports/research_youtube.txt", "w", encoding='utf-8') as file:
        file.write("\n".join(results))

    return "\n".join(results)
