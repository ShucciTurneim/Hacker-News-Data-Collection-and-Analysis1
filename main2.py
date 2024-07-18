import requests
import csv
import datetime

def extract_story_IDs(url):
    """
    Extracts story IDs from a given URL using the Hacker News API.

    Args:
    url (str): The URL of the Hacker News API endpoint.

    Returns:
    dict or None: JSON data containing story IDs if successful, None otherwise.
    """
    response = requests.get(url)
    if response.status_code == 200:
        stories_data = response.json()
        return stories_data
    else:
        print("error:", response.status_code)

def add_a_line(row, status): 
    """
    Appends a row of data to a CSV file.

    Args:
    row (list): List containing data to be written to the CSV file.
    status (str): File mode ('w' for write, 'a' for append).

    Returns:
    None
    """
    with open('top_stories_data_table.csv', status, newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)

def init_cvs_stories_data(head=[]):
    """
    Initializes a CSV file with headers.

    Args:
    head (list): List of header strings.

    Returns:
    str: Filename of the created CSV file.
    """
    csv_file = 'top_stories_data_table.csv'
    add_a_line(head, 'w')
    return csv_file

def try_story_data(data, ID):
    """
    Tries to fetch story data from Hacker News API based on story ID.

    Args:
    data (list): List of story IDs.
    ID (int): Index of the story ID to fetch.

    Returns:
    dict or str: JSON data of the story if successful, 'error' if unsuccessful.
    """
    url = f'https://hacker-news.firebaseio.com/v0/item/{data[ID]}.json?print=pretty'
    response = requests.get(url)
    if response.status_code == 200:
        story_data = response.json()
        return story_data
    else:
        print(f'error: story {ID} data not exist')
        return 'error'

def load_data_to_file(data, csv_file, stories_number_to_analyse):
    """
    Loads story data into a CSV file.

    Args:
    data (list): List of story IDs.
    csv_file (str): Filename of the CSV file to write data into.
    stories_number_to_analyse (int): Number of stories to analyze and load into the CSV file.

    Returns:
    None
    """
    for ID in range(stories_number_to_analyse):
        ID_data = try_story_data(data, ID)
        if ID_data != 'error':
            title = ID_data['title'] if 'title' in ID_data  else ''
            url = ID_data['url'] if 'url' in ID_data  else ''
            score = ID_data['score'] if 'score' in ID_data  else ''
            author = ID_data['by']  if 'by' in ID_data  else ''
            time = str(datetime.timedelta(seconds= ID_data['time']))
            number_of_comments = len(ID_data['kids'])
            row_to_write = [title, url, score, author, time, number_of_comments]
            add_a_line(row_to_write,'a')

def collection_and_analysis():
    """
    Main function to collect and analyze Hacker News best stories data.

    Fetches story IDs, initializes a CSV file with headers, and loads story data into the CSV file.

    Returns:
    None
    """
    api_best_stories = "https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"
    stories_data = extract_story_IDs(api_best_stories)
    stories_data_file = init_cvs_stories_data(['title', 'URL', 'score', 'author', 'time', 'number of comments'])
    load_data_to_file(stories_data, stories_data_file, 15)

collection_and_analysis()

