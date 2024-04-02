from youtube_search import YoutubeSearch
from get_keywords import extract_keywords_from_title
import constants
import random

def time_to_seconds(time_str):
    """
    Convert time in the format "H:MM:SS" or "MM:SS" or "SS" to seconds.

    Parameters:
    - time_str (str): Time string in the format "H:MM:SS" or "MM:SS" or "SS".

    Returns:
    - int: Total time in seconds.
    """
    components = list(map(int, time_str.split(':')))
    
    if len(components) == 1:  # Only seconds provided
        total_seconds = components[0]
    elif len(components) == 2:  # Minutes and seconds provided
        total_seconds = components[0] * 60 + components[1]
    elif len(components) == 3:  # Hours, minutes, and seconds provided
        total_seconds = components[0] * 3600 + components[1] * 60 + components[2]
    else:
        raise ValueError("Invalid time format")

    return total_seconds

def get_youtube_link(post_title):
    search_query = extract_keywords_from_title(post_title)
    print("searching for "+ search_query + " video")
    results = YoutubeSearch(search_query, max_results=10).to_dict()
    for result in results:
        length_in_seconds = time_to_seconds(result["duration"])
        if length_in_seconds < 60 or length_in_seconds > 1200:
            print("video not right length")
            continue
        url = f"https://youtube.com{result['url_suffix']}"
        print("Getting: ", result["title"])
        return url
    return None

