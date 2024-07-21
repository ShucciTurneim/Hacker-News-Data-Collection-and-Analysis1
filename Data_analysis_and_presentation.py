import seaborn as sns
import csv
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def add_a_line(row, status, name): 
    """
    Add a row to a CSV file.
    
    Parameters:
    - row (list): The row data to be written to the CSV file.
    - status (str): The mode in which the file is opened ('w' for write, 'a' for append).
    - name (str): The name of the CSV file.
    """
    file_name = f'{name}'
    with open(file_name, status, newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row) 
        

def Creating_analysis_storage_files(head=[], name=str):
    """
    Create a new CSV file for storing analysis data.
    
    Parameters:
    - head (list): List of column headers for the CSV file.
    - name (str): Name of the file (without extension).
    
    Returns:
    - str: Name of the created CSV file.
    """
    head = ['types'] + head[:]
    csv_file = f'{name}_data_table.csv'
    add_a_line(head, 'w', csv_file) 
    return csv_file
    
    
def Correlate(data, subject_to_correlation, file):
    """
    Calculate correlation between two variables in a CSV file.
    
    Parameters:
    - data (str): Name of the first variable column.
    - subject_to_correlation (str): Name of the second variable column.
    - file (str): Name of the CSV file containing the data.
    
    Returns:
    - float: Correlation coefficient between the two variables.
    """
    df = pd.read_csv(file)
    correlation_value = df[data].corr(df[subject_to_correlation])
    return correlation_value
    
    
def Update_data_in_the_table(array_of_rows, file):
    """
    Update data in the analysis table.
    
    Parameters:
    - array_of_rows (list of lists): List of rows to add to the CSV file.
    - file (str): Name of the CSV file to update.
    """
    for row in array_of_rows:
        row_to_write = row
        add_a_line(row_to_write, 'a', file)
    


def Create_rows_for_analysis_table(data_names, file):
    """
    Create rows for an analysis table based on correlation calculations.
    
    Parameters:
    - data_names (list): List of variable names to analyze.
    - file (str): Name of the CSV file containing the data.
    
    Returns:
    - list of lists: List of rows with correlation values for each pair of variables.
    """
    array_of_rows = []
    for data in data_names:
        row_values = [data]
        for subject_to_correlation in data_names:
            correlation = Correlate(data, subject_to_correlation, file) if data != subject_to_correlation else ""
            row_values.append(correlation)
        array_of_rows.append(row_values)
    return array_of_rows


def Visualize_correlation_matrix(data_names, file, whom):
    """
    Visualize correlation matrix using a heatmap.
    
    Parameters:
    - data_names (list): List of variable names for the rows and columns of the matrix.
    - file (str): Name of the CSV file containing the correlation data.
    - whom (str): Name or description of the dataset being analyzed.
    """
    corr_matrix = pd.read_csv(file, index_col=0)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.xticks(range(len(data_names)), data_names, rotation=45)
    plt.yticks(range(len(data_names)), data_names, rotation=0)
    plt.title(f'Correlation Matrix of {whom}')
    plt.show()
    

def visualizeParameterImpact(parameters, data, about):
    """
    Visualize impact of parameters on a specific variable.
    
    Parameters:
    - parameters (list): List of parameter names to analyze.
    - data (str): Name of the CSV file containing the data.
    - about (str): Name of the variable to analyze the impact on.
    """
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


def Plot_correlations(data_names, file, whom):
    """
    Plot correlations between variables and visualize correlation matrix.
    
    Parameters:
    - data_names (list): List of variable names to analyze.
    - file (str): Name of the CSV file containing the data.
    - whom (str): Name or description of the dataset being analyzed.
    """
    Analyze_file = Creating_analysis_storage_files(data_names, f'correlations_{whom}')
    array_of_rows = Create_rows_for_analysis_table(data_names, file)
    Update_data_in_the_table(array_of_rows, Analyze_file)
    for variable in data_names:
        parameters = [item for item in data_names if item != variable]
        visualizeParameterImpact(parameters, file, variable)
    Visualize_correlation_matrix(data_names, Analyze_file, whom)
    

def Analyze_data(data_names, file, whom):   
    """
    Analyze data by plotting correlations.
    
    Parameters:
    - data_names (list): List of variable names to analyze.
    - file (str): Name of the CSV file containing the data.
    - whom (str): Name or description of the dataset being analyzed.
    """
    Plot_correlations(data_names, file, whom)






