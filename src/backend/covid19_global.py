import numpy as np
import pandas as pd
import os
#import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import plotly.express as px
import plotly.graph_objects as go

def country_wise_confirmed_cases(covid_data):
   try:
        df = covid_data.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered", "Active"]].sum()
        fig = px.choropleth(locations=df.index, locationmode='country names', 
                      color=df["Confirmed"], hover_name=df.index, title="Total Confirmed Cases", color_continuous_scale="Reds")
        #fig.show()
        file_path= os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures","country_wise_confirmed_cases.png")
        fig.write_image(file_path)
        print("Figure saved successfully at:", file_path)
   except Exception as e:
        print("Error:", e)
        
def country_wise_death_cases(covid_data):
   try:
        df = covid_data.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered", "Active"]].sum() 
        fig = px.choropleth(locations=df.index, locationmode='country names', 
                  color=df.values[:,1], hover_name=df.index, title="Total Death Cases", color_continuous_scale="Reds")
        #fig.show()
        file_path= os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures","country_wise_death_cases.png")
        fig.write_image(file_path)
        print("Figure saved successfully at:", file_path)
   except Exception as e:
        print("Error:", e)
        
def country_wise_recovered_cases(covid_data):
   try:
        df = covid_data.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered", "Active"]].sum()
        fig = px.choropleth(locations=df.index, locationmode='country names', 
                  color=df.values[:,2], hover_name=df.index, title="Total Recovered Cases", color_continuous_scale="blues")
        #fig.show()
        file_path= os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures","country_wise_recovered_cases.png")
        fig.write_image(file_path)
        print("Figure saved successfully at:", file_path)
   except Exception as e:
        print("Error:", e)
        
def country_wise_active_cases(covid_data):
   try:
        df = covid_data.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered", "Active"]].sum()
        fig = px.choropleth(locations=df.index, locationmode='country names', 
                  color=df.values[:,3], hover_name=df.index, title="Total Active Cases", color_continuous_scale="Reds")
        #fig.show()
        file_path= os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures","country_wise_active_cases.png")
        fig.write_image(file_path)
        print("Figure saved successfully at:", file_path)
   except Exception as e:
        print("Error:", e)
        
def daywise_count(day_wise_data):
    try:
        fig = px.bar(day_wise_data, x='Date', y=["Confirmed","Deaths",'Recovered',"Active"])
        fig.update_traces(marker=dict(line=dict(color='black', width=0.5)))
        #fig.show()
        file_path= os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures","country_wise_active_cases.png")
        fig.write_image(file_path)
        print("Figure saved successfully at:", file_path)
    except Exception as e:
        print("Error:", e)
        
def plot_country(y_value):
    df = country_data.sort_values(by=y_value, ascending=False).head(20)
    fig = px.bar(df, x="Country/Region", y=y_value,color="WHO Region", text=y_value, 
                 title=("Top 20 Countries with highest "+y_value+" Cases"))

    # Put bar total value above bars with 2 values of precision
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside',
                     marker=dict(line=dict(color='black', width=2)))
    
    fig.update_layout(xaxis_tickangle=-45)

    file_name = f'{y_value}.png'
    file_path = os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures", file_name)
    fig.write_image(file_path)
    #fig.show()
    
def plot_population(y_value):
    df = world_data.sort_values(by="Population", ascending=False).head(20)
    fig = px.bar(df, x="Country/Region", y="Population", color=y_value, text=y_value, 
                 title=("Population VS "+y_value))

    # Put bar total value above bars with 2 values of precision
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_traces(marker=dict(line=dict(color='black', width=2)))

    fig.update_layout(xaxis_tickangle=-45)
    file_name = f'{y_value}.png'
    file_path = os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures", file_name)
    fig.write_image(file_path)


    #fig.show()


if __name__ == "__main__":
    
    covid_data = pd.read_csv(r"C:\Users\koush\Downloads\covid_19_clean_complete_1.csv")
    day_wise_data = pd.read_csv(r"C:\Users\koush\Downloads\day_wise.csv")
    full_grouped_data = pd.read_csv(r"C:\Users\koush\Downloads\full_grouped_1.csv")
    usa_data = pd.read_csv(r"C:\Users\koush\Downloads\usa_county_wise_1.csv")
    country_data = pd.read_csv(r"C:\Users\koush\Downloads\country_wise_latest.csv")
    world_data = pd.read_csv(r"C:\Users\koush\Downloads\worldometer_data.csv")
    
    country_wise_confirmed_cases(covid_data)
    country_wise_death_cases(covid_data)
    country_wise_recovered_cases(covid_data)
    country_wise_active_cases(covid_data)
    daywise_count(day_wise_data)
    plot_country("Deaths")
    plot_country("Active")
    plot_population("TotalCases")