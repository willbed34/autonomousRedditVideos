from youtube_search import YoutubeSearch
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

def get_youtube_link():
    query = random.choice(constants.gameplay_options)
    results = YoutubeSearch(query, max_results=10).to_dict()
    for result in results:
        length_in_seconds = time_to_seconds(result["duration"])
        if length_in_seconds < 60 or length_in_seconds > 600:
            print("video not right length")
            continue
        url = f"https://youtube.com{result['url_suffix']}"
        print("Getting: ", result["title"])
        return url
    return None

