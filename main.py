import requests
import csv
import datetime



def extract_story_IDs(url):
    response = requests.get(url)                                                       
    if requests.status_codes != 200:
        stories_data = response.json()
        return stories_data
    else:
        print("error:" ,response.status_code)    
        
        
def add_a_line(row,status, name): 
    file_name = f'{name}'
    with open(file_name, status,newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)        
    return file_name    
  
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
            time = str(datetime.timedelta(seconds= ID_data['time'])) if 'time' in ID_data  else ''
            number_of_comments = len(ID_data['kids']) if 'kids' in ID_data  else ''
            row_to_write = [id,title, url, score, author, time, number_of_comments]
            
            stories_id.append(id)
            comments_id.append(ID_data['kids'])  if 'kids' in ID_data  else ''
            add_a_line(row_to_write,'a',file_name)
    return(stories_id, comments_id)   


def load_comments_data_to_file(comments,file_name,comments_number_to_analyse):
    for ID in range(comments_number_to_analyse):
        current_id = comments[ID]
        ID_data = try_data(current_id)
        if ID_data != 'error':
            row_to_write = []
            id = ID_data['id'] if 'id' in ID_data  else ''
            author = ID_data['by']  if 'by' in ID_data  else ''
            text = ID_data['text'] if 'text' in ID_data  else ''
            parent_story = ID_data['parent'] if 'parent' in ID_data  else ''
            time = str(datetime.timedelta(seconds= ID_data['time'])) if 'time' in ID_data  else ''
            row_to_write = [id,author,text, parent_story, time]
            add_a_line(row_to_write,'a',file_name)
        

def comments_data_to_csv(stories_id,comments_id,headlines_comments, comments_number):
    for story in stories_id:
        comments = try_data(story)
        comments = comments['kids'] if 'kids' in comments else 'error'
        if comments != 'error':    
            file_name = init_csv_data(headlines_comments,f'{story}_comments')
            comments_number = comments_number if len(comments) >= comments_number else len(comments)
            load_comments_data_to_file(comments,file_name,comments_number)


def  collection_and_analysis():
    headlines_stories = [ 'ID','title', 'URL', 'score', 'author', 'time', 'number of comments']
    headlines_comments = ['ID','author', 'text', 'time','parent_story']
    api_best_stories =  "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"       #url
    stories_data = extract_story_IDs(api_best_stories)
    stories_file_name = init_csv_data(headlines_stories,'stories')
    stories_id, comments_id = load_stories_data_to_file(stories_data,stories_file_name,5)
    comments_data_to_csv(stories_id, comments_id, headlines_comments, 5)

        

collection_and_analysis()