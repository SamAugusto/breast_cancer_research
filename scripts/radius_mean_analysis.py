import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from statsmodels.stats.weightstats import ztest


def filter_by_diagnosis(df:pd.DataFrame, diag: str): # diag short for diagnosis like M for malign
    '''Takes a data frame and a diagnosis as an argument and returns a series mask with data only based on the diagnosis'''
    if type(df) is not pd.DataFrame:
        raise TypeError("The data is not a pandas data frame, please conver it to a pandas data frame")

    if type(diag) is not str:
        raise TypeError("Diag parameter should be a character or string")
    return df["diagnosis"].str.upper() == diag.upper()
def bar_plot_2_data(normal, affected) -> None: # Takes 2 data column
    '''Plots a bar graph to compare data from benign and malign cancers
    takes as input two np.float64'''

    data_to_plot = {"Normal":normal, "Affected": affected}
    fig, ax = plt.subplots()
    sns.barplot(data=data_to_plot, palette=["#43A35F", "#88413A"], ax=ax)
    ax.set(ylabel = "Average Radius Mean (Pixel Count)")
    fig.savefig(sys.stdout.buffer, format="png")
    return None
def distribution_analysis(radius_mean_data) -> tuple:
    '''Takes both normal and affected data to analyze if the radius mean have a significant difference'''
    # Creating and saving distribution histograms
    fig,ax = plt.subplots()
    sns.histplot(data=radius_mean_data,x="radius_mean",hue="diagnosis",palette=["#88413A","#43A35F"])
    fig.savefig(sys.stdout.buffer,format="png")
    
    # Filtering data to compare z-scores
    b_dist_data = radius_mean_data[filter_by_diagnosis(radius_mean_data,"B")]["radius_mean"]
    m_dist_data = radius_mean_data[filter_by_diagnosis(radius_mean_data,"M")]["radius_mean"]
    
    z_stat, p_value = ztest( x1 = b_dist_data,x2 = m_dist_data, value=0,alternative = 'two-sided')
    return (z_stat,p_value)
if __name__ == "__main__":
    cancer_data = pd.read_csv("../data/breast_cancer_dataset.csv.gz") # Takes the raw data as an input and returns a dataframe (pandas)
    avg_b_radius_mean_cancer_data = np.average(cancer_data[filter_by_diagnosis(cancer_data,"B")]["radius_mean"])
    avg_m_radius_mean_cancer_data = np.average(cancer_data[filter_by_diagnosis(cancer_data,"M")]["radius_mean"])
    
    ######## Analysis 1 understanding the average mean radius and comparing benging vs malign tumors averages########
    # Creates the figure saved in analysis for the "average radius mean comparisson"
    # bar_plot_2_data(avg_b_radius_mean_cancer_data,avg_m_radius_mean_cancer_data)

    
    ### Analysis 2 visualizing distributions and checking for significant differences ###############
    # choosing the entire distribution instead of just a single average number
    dist_radius_mean_cancer_data = cancer_data[["diagnosis","radius_mean"]]
   

    # Does a distribution analysis of the entire radius mean data of benign and malign tumors
    z,p = distribution_analysis(dist_radius_mean_cancer_data)
    # prints the values in radius distribution.txt file
    # print(f"Benign vs Malign data: Z-score {z:.2f}, p-value {p:.2f}")

