import requests
import seaborn as sns
import csv
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def add_a_line(row,status, name): 
    file_name = f'{name}'
    with open(file_name, status,newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row) 
        

def Creating_analysis_storage_files(head=[], name= str):
    head = ['types'] + head[:]
    csv_file = f'{name}_data_table.csv'
    add_a_line(head, 'w', csv_file) 
    return csv_file
    
    
def Correlate(data, subject_to_correlation, file):
    df = pd.read_csv(file)
    correlation_value = df[data].corr(df[subject_to_correlation])
    return correlation_value
    
    
def Update_data_in_the_table(array_of_rows,file):
    for row in array_of_rows:
            row_to_write = row
            add_a_line(row_to_write,'a',file)
    


def Create_rows_for_analysis_table(data_names, file):
    array_of_rows = []
    for data in data_names:
        row_values = [data]
        for subject_to_correlation in data_names:
            correlation = Correlate(data, subject_to_correlation, file) if data != subject_to_correlation else ""
            row_values.append(correlation)
        array_of_rows.append(row_values)
    return array_of_rows

def Visualize_correlation_matrix(data_names, file, whom):
    corr_matrix = pd.read_csv(file, index_col=0)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.xticks(range(len(data_names)), data_names, rotation=45)
    plt.yticks(range(len(data_names)), data_names, rotation=0)
    plt.title(f'Correlation Matrix of {whom}')
    plt.show()
    
 
def corelation2(parameters, data, about):
    data = pd.read_csv(data)
    parameters_data = data[parameters]
    colors = ['blue', 'green', 'orange']
    fig, ax = plt.subplots()
    ax.set_title(f'Influence on {about}')
    for var, color in zip(parameters_data.columns, colors):
        ax.scatter(parameters_data[var], data[about], color=color, label=var, alpha=0.6) 
    ax.legend()
    ax.set_xlabel('Parameter Value')
    ax.set_ylabel(about)
    plt.show()
 
 
def Analyze_data(data_names, file, whom):   
    Analyze_file = Creating_analysis_storage_files(data_names, f'correlations_{whom}')
    array_of_rows = Create_rows_for_analysis_table(data_names, file)
    Update_data_in_the_table(array_of_rows,Analyze_file)
    # variable = data_names[3]
    for variable in data_names:
        parameters = [item for item in data_names if item != variable]
        corelation2(parameters, file, variable)
    Visualize_correlation_matrix(data_names, Analyze_file, whom)






