import requests
import csv
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Data_analysis_and_presentation import*

                
def add_a_line(row,status, name): 
    file_name = f'{name}'
    with open(file_name, status,newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)        
        
  
def init_csv_data(head=[],object= str):
    """Insert an array of your headers and get a csv file with your headers """
    csv_file = f'top_{object}_data_table.csv'
    add_a_line(head, 'w', csv_file) 
    return csv_file
    
    
def try_data(ID):
    url =  f'https://hacker-news.firebaseio.com/v0/item/{ID}.json?print=pretty'
    response = requests.get(url)                                                       
    if requests.status_codes != 200:
        data = response.json()
        return data   
    else:
        print(f'error:story {ID} data not exist')   
        return 'error'  
          
          
def Calculate_time(epoch_time):          
    now = time.time()      
    return str((now-epoch_time)/3600)
    # return str(datetime.timedelta(seconds= now-epoch_time))


def Calculate_date(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time)
    

        
def load_stories_data_to_file(data,file_name,stories_number_to_analyse):
    stories_id = []
    comments_id = []
    for ID in range(stories_number_to_analyse):
        current_id = data[ID]
        ID_data = try_data(current_id)
        if ID_data != 'error':
            row_to_write = []
            id = ID_data['id'] if 'id' in ID_data  else ''
            title = ID_data['title'] if 'title' in ID_data  else ''
            url = ID_data['url'] if 'url' in ID_data  else ''
            score = ID_data['score'] if 'score' in ID_data  else ''
            author = ID_data['by']  if 'by' in ID_data  else ''
            time_as_days = Calculate_time(ID_data['time']) if 'time' in ID_data  else ''
            date = Calculate_date(ID_data['time'])  if 'time' in ID_data  else 'Unknown'
            number_of_comments = len(ID_data['kids']) if 'kids' in ID_data  else ''
            descendants = ID_data['descendants'] if 'descendants' in ID_data  else 'Unknown'
            row_to_write = [id,title, url, score, author, time_as_days, date, number_of_comments, descendants]
            
            stories_id.append(id)
            comments_id.append(ID_data['kids'])  if 'kids' in ID_data  else None
            add_a_line(row_to_write,'a',file_name)
    return(stories_id, comments_id)   


def load_comments_data_to_file(comment,file_name,comments_number_to_analyse):
    # for ID in range(comments_number_to_analyse):
        # current_id = comments[ID]
        # ID_data = try_data(current_id)
        ID_data = try_data(comment)
        if ID_data != 'error':
            row_to_write = []
            id = ID_data['id'] if 'id' in ID_data  else ''
            author = ID_data['by']  if 'by' in ID_data  else ''
            text = ID_data['text'] if 'text' in ID_data  else ''
            parent_story = ID_data['parent'] if 'parent' in ID_data  else ''
            time_as_days = Calculate_time(ID_data['time']) if 'time' in ID_data  else ''
            date = Calculate_date(ID_data['time'])  if 'time' in ID_data  else 'Unknown'
            row_to_write = [id,author, parent_story, time_as_days, date, text]
            add_a_line(row_to_write,'a',file_name)
        

def comments_data_to_csv(stories_id,comments_id,headlines_comments, comments_number):
    file_name = init_csv_data(headlines_comments,'comments')
    for comments in comments_id:
        comments_number = comments_number if len(comments) >= comments_number else len(comments)
        for comment in range(comments_number):
           load_comments_data_to_file(comments[comment],file_name,comments_number) 
    return file_name
    
    
def extract_story_IDs(url):
    response = requests.get(url)                                                       
    if requests.status_codes != 200:
        stories_data = response.json()
        return stories_data
    else:
        print("error:" ,response.status_code)        


def Data_collection_and_storage():
    headlines_stories = [ 'ID','title', 'URL', 'score', 'author', 'time_as_days','date', 'number of comments', 'descendants']
    headlines_comments = ['ID','author', 'parent_story', 'time_as_days', 'date', 'text']
    api_best_stories =  "https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"       #url
    stories_data = extract_story_IDs(api_best_stories)
    stories_file_name = init_csv_data(headlines_stories,'stories')
    stories_id, comments_id = load_stories_data_to_file(stories_data,stories_file_name,5)
    comments_file_name = comments_data_to_csv(stories_id, comments_id, headlines_comments, 5)
    return stories_file_name, comments_file_name


def  collection_and_analysis():
    stories_file_name, comments_file_name = Data_collection_and_storage()
    # data_analyse(stories_file_name, comments_file_name)
    stories_data_to_analyse = ['score', 'time_as_days', 'number of comments', 'descendants']
    Analyze_data(stories_data_to_analyse, stories_file_name, 'stories')

        

collection_and_analysis()