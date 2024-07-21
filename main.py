import requests
import csv
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Data_analysis_and_presentation import *


def add_a_line(row, status, name):
    """
    Adds a row to a CSV file.

    Parameters:
    - row: List, the row of data to be written.
    - status: String, the file open mode ('w' for write, 'a' for append).
    - name: String, the name of the CSV file.

    Returns:
    None
    """
    file_name = f'{name}'
    with open(file_name, status, newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)


def init_csv_data(head=[], object=str):
    """
    Initialize a new CSV file with headers.

    Parameters:
    - head: List, headers for the CSV file.
    - object: String, identifier for the object related to the CSV file.

    Returns:
    String, the name of the created CSV file.
    """
    csv_file = f'top_{object}_data_table.csv'
    add_a_line(head, 'w', csv_file)
    return csv_file


def try_data(ID):
    """
    Attempts to fetch data from Hacker News API for a given story ID.

    Parameters:
    - ID: Integer, the ID of the story.

    Returns:
    Dict or String, JSON data of the story if successful, otherwise 'error'.
    """
    url = f'https://hacker-news.firebaseio.com/v0/item/{ID}.json?print=pretty'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'error: story {ID} data not exist')
        return 'error'


def Calculate_time(epoch_time):
    """
    Calculate the time difference from current time in hours given epoch time.

    Parameters:
    - epoch_time: Integer, time in epoch format.

    Returns:
    String, time difference in hours.
    """
    now = time.time()
    return str((now - epoch_time) / 3600)


def Calculate_date(epoch_time):
    """
    Convert epoch time to a datetime object.

    Parameters:
    - epoch_time: Integer, time in epoch format.

    Returns:
    datetime.datetime object.
    """
    return datetime.datetime.fromtimestamp(epoch_time)


def load_stories_data_to_file(data, file_name, stories_number_to_analyse):
    """
    Load stories data to a CSV file.

    Parameters:
    - data: List, list of story IDs.
    - file_name: String, name of the output CSV file.
    - stories_number_to_analyse: Integer, number of stories to analyze.

    Returns:
    Tuple, lists of story IDs and comments IDs.
    """
    stories_id = []
    comments_id = []
    for ID in range(stories_number_to_analyse):
        current_id = data[ID]
        ID_data = try_data(current_id)
        if ID_data != 'error':
            row_to_write = []
            id = ID_data['id'] if 'id' in ID_data else ''
            title = ID_data['title'] if 'title' in ID_data else ''
            url = ID_data['url'] if 'url' in ID_data else ''
            score = ID_data['score'] if 'score' in ID_data else ''
            author = ID_data['by'] if 'by' in ID_data else ''
            time_as_days = Calculate_time(ID_data['time']) if 'time' in ID_data else ''
            date = Calculate_date(ID_data['time']) if 'time' in ID_data else 'Unknown'
            number_of_comments = len(ID_data['kids']) if 'kids' in ID_data else ''
            descendants = ID_data['descendants'] if 'descendants' in ID_data else 'Unknown'
            row_to_write = [id, title, url, score, author, time_as_days, date, number_of_comments, descendants]
            stories_id.append(id)
            comments_id.append(ID_data['kids']) if 'kids' in ID_data else None
            add_a_line(row_to_write, 'a', file_name)
    return (stories_id, comments_id)


def load_comments_data_to_file(comment, file_name):
    """
    Load comments data to a CSV file.

    Parameters:
    - comment: Integer, comment ID.
    - file_name: String, name of the output CSV file.

    Returns:
    None
    """
    ID_data = try_data(comment)
    if ID_data != 'error':
        row_to_write = []
        id = ID_data['id'] if 'id' in ID_data else ''
        author = ID_data['by'] if 'by' in ID_data else ''
        text = ID_data['text'] if 'text' in ID_data else ''
        parent_story = ID_data['parent'] if 'parent' in ID_data else ''
        time_as_days = Calculate_time(ID_data['time']) if 'time' in ID_data else ''
        date = Calculate_date(ID_data['time']) if 'time' in ID_data else 'Unknown'
        row_to_write = [id, author, parent_story, time_as_days, date, text]
        add_a_line(row_to_write, 'a', file_name)


def comments_data_to_csv(stories_id, comments_id, headlines_comments, comments_number):
    """
    Create CSV file for comments data.

    Parameters:
    - stories_id: List, list of story IDs.
    - comments_id: List of Lists, list of lists of comment IDs.
    - headlines_comments: List, headers for comments data.
    - comments_number: Integer, number of comments to analyze per story.

    Returns:
    String, the name of the created CSV file.
    """
    file_name = init_csv_data(headlines_comments, 'comments')
    for comments in comments_id:
        comments_number = comments_number if len(comments) >= comments_number else len(comments)
        for comment in range(comments_number):
            load_comments_data_to_file(comments[comment], file_name)
    return file_name


def extract_story_IDs(url):
    """
    Extract story IDs from Hacker News API.

    Parameters:
    - url: String, API endpoint URL.

    Returns:
    Dict or None, JSON data of stories if successful, otherwise None.
    """
    response = requests.get(url)
    if response.status_code == 200:
        stories_data = response.json()
        return stories_data
    else:
        print("error:", response.status_code)


def Data_collection_and_storage():
    """
    Main function to collect and store data.

    Returns:
    Tuple, names of the created CSV files for stories and comments data.
    """
    headlines_stories = ['ID', 'title', 'URL', 'score', 'author', 'time_as_days', 'date', 'number of comments', 'descendants']
    headlines_comments = ['ID', 'author', 'parent_story', 'time_as_days', 'date', 'text']
    api_best_stories = "https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"
    stories_data = extract_story_IDs(api_best_stories)
    stories_file_name = init_csv_data(headlines_stories, 'stories')
    stories_id, comments_id = load_stories_data_to_file(stories_data, stories_file_name, 5)
    comments_file_name = comments_data_to_csv(stories_id, comments_id, headlines_comments, 5)
    return stories_file_name, comments_file_name


def collection_and_analysis():
    """
    Main function to collect and analyze data.
    """
    stories_file_name, comments_file_name = Data_collection_and_storage()
    stories_data_to_analyse = ['score', 'time_as_days', 'number of comments', 'descendants']
    Analyze_data(stories_data_to_analyse, stories_file_name, 'stories')


collection_and_analysis()