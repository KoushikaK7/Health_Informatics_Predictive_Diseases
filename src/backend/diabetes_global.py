import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import ExtraTreesRegressor
#from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import os

def read_data(file_path):
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print("Error:", e)
        return None
    
def plot_line_chart_by_year(df, year, column):
    
    # Group the mean data by year
    mean_by_year = df.groupby(year)[column].mean()

    # Style
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))

    # Plot the line chart
    plt.plot(mean_by_year.index, mean_by_year.values, color='limegreen', linewidth=2)

    # Set up other visual elements
    plt.xlabel(year, fontsize = 14, color = 'white')
    plt.ylabel(column, fontsize = 14, color = 'white')
    plt.title(f'{column} by Year', fontsize = 16, color = 'white')

    # Set the colors of ticks and texts
    plt.tick_params(colors = 'white')
    plt.xticks(fontsize = 12, color = 'white')
    plt.yticks(fontsize = 12, color = 'white')
    #plt.show()
    file_name = f'{column}.png'
    file_path = os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures", file_name)
    plt.savefig(file_path)
    plt.close()
    
def plot_top_countries_diabetes_prevalence(df):
    """
    Plot the top 10 countries with the highest age-standardised diabetes prevalence.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
    """
    try:
        # Calculate mean prevalence by country and select top 10
        media_prevalence = df.groupby('Country/Region/World')['Age-standardised diabetes prevalence'].mean()
        media_prevalence = media_prevalence.sort_values(ascending=False).head(10)
        
        # Plotting
        plt.figure(figsize=(12, 10))
        plt.barh(media_prevalence.index, media_prevalence.values, color='green', alpha=0.8)
        plt.axvline(media_prevalence.mean(), color='red', linestyle='dashed', linewidth=2, label='Mean')
        plt.xlabel('Age-standardised diabetes prevalence', fontsize=12)
        plt.ylabel('Country/Region/World', fontsize=12) 
        plt.title('Top 10 Countries with Highest Age-standardised Diabetes Prevalence', fontsize=16)
        plt.legend()
        plt.tight_layout()
        #plt.show()
        file_path = os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures", 'plot_top_countries_diabetes_prevalence.png')
        plt.savefig(file_path)
        plt.close()
    except Exception as e:
        print("Error:", e)

def plot_top_countries_lower_interval(df):
    """
    Plot the top 10 countries with the highest lower 95% uncertainty interval.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
    """
    try:
        # Calculate mean lower interval by country and select top 10
        media_interval = df.groupby('Country/Region/World')['Lower 95% uncertainty interval'].mean()
        media_interval = media_interval.sort_values(ascending=False).head(10)
        
        # Plotting
        plt.figure(figsize=(12, 10))
        plt.barh(media_interval.index, media_interval.values, color='green', alpha=0.8)
        plt.axvline(media_interval.mean(), color='red', linestyle='dashed', linewidth=2, label='Mean')
        plt.xlabel('Lower 95% uncertainty interval', fontsize=12)
        plt.ylabel('Country/Region/World', fontsize=12) 
        plt.title('Top 10 Countries with Highest Lower 95% uncertainty interval', fontsize=16)
        plt.legend()
        plt.tight_layout()
        #plt.show()
        file_path = os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures", 'plot_top_countries_lower_interval.png')
        plt.savefig(file_path)
        plt.close()
    except Exception as e:
        print("Error:", e)
        
def plot_top_countries(df):
    media_prevalence = df.groupby('Country/Region/World')['Upper 95% uncertainty interval'].mean()
    media_prevalence = media_prevalence.sort_values(ascending=False).head(10)

    plt.figure(figsize=(12, 10))
    plt.barh(media_prevalence.index, media_prevalence.values, color='green', alpha=0.8)
    plt.axvline(media_prevalence.mean(), color='red', linestyle='dashed', linewidth=2, label='Mean')
    plt.xlabel('Upper 95% uncertainty interval', fontsize=12)
    plt.ylabel('Country/Region/World', fontsize=12)
    plt.title('Top 10 Countries with Upper 95% uncertainty interval', fontsize=16)
    plt.legend()
    plt.tight_layout()
    #plt.show()
    file_path = os.path.join(r"C:\wamp64\www\PredictiveDiseases_HealthInformatics-main\PredictiveDiseases_HealthInformatics-main\src\backend\figures", 'plot_top_countries.png')
    plt.savefig(file_path)
    plt.close()

if __name__ == "__main__":
    file_path = r"C:\Users\koush\Downloads\archive\Diabetes_Dataset _By_Age_Standardized_Countries.csv"
    df = read_data(file_path)
    plot_line_chart_by_year(df, 'Year', 'Age-standardised diabetes prevalence')
    plot_line_chart_by_year(df, 'Year', 'Lower 95% uncertainty interval')
    plot_line_chart_by_year(df, 'Year', 'Upper 95% uncertainty interval')
    plot_top_countries_diabetes_prevalence(df)
    plot_top_countries_lower_interval(df)
    plot_top_countries(df)
