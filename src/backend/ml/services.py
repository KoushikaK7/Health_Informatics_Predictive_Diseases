import logging
import os
import pandas as pd
import matplotlib
from pydantic import BaseModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

matplotlib.use('Agg')  # Use the non-GUI Agg backend
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Filter(BaseModel):
    state: str
    county: str
    disease: str


def predict(filter_input: Filter):
    try:
        # Load the dataset
        print(f"Predicting {filter_input.county} with {filter_input.state}")
        DATA_PATH = os.path.join(BASE_DIR, "../data/covid-19-usa.csv")
        data = pd.read_csv(DATA_PATH)
        data = data[data["state_name"] == filter_input.state]
        data = data[data["county_name"] == filter_input.county]
        # Take only the features with numerical values
        numerical_features = data.select_dtypes(include=['int64', 'float64']).columns
        X = data[numerical_features]

        print("Creating target variable")
        # Create the target variable
        y = data['covid_19_confirmed_cases']

        # Split the arch into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X[:1000], y[:1000], test_size=0.2, random_state=42)
        date_train, date_test = data.loc[X_train.index, 'date'], data.loc[
            X_test.index, 'date']  # Preserve dates for plotting

        print(f"Creating model")
        # Train the model
        model = RandomForestRegressor()

        print(f"Fitting model")
        model.fit(X_train, y_train)

        print(f"Predicting data")
        # Make predictions
        predictions = model.predict(X_test)
        print("Predicted COVID-19 Cases:")
        # for i, prediction in enumerate(predictions):
        #     print(f"Sample {i + 1}: {prediction}")

        # Evaluate the model
        mse = mean_squared_error(y_test, predictions)
        print("Mean Squared Error:", mse)

        print("Plotting data")
        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(data['date'], data['covid_19_confirmed_cases'], label='Original', alpha=0.75)
        plt.scatter(date_test, predictions, color='red', label='Predicted', alpha=0.6)
        plt.title(f'Random Forest Prediction of Confirmed Cases: {filter_input.state}-{filter_input.county}')
        plt.xlabel('Date')
        plt.ylabel('Cases')
        plt.legend()

        plt.tight_layout()
        # Define the base directory for figures
        figures_dir = f'{BASE_DIR}/../figures'

        # Check if the directory exists, and create it if it does not
        if not os.path.exists(figures_dir):
            os.makedirs(figures_dir)

        # Assuming state_name and county_name are defined earlier in your code
        file_name = f'{filter_input.state.lower().replace(" ", "-")}-{filter_input.county.lower().strip().replace(" ", "-")}-prediction.png'
        file_path = os.path.join(figures_dir, file_name)
        print("Saving plot")
        plt.savefig(file_path)
        plt.close()

        feature_list = ['covid_19_confirmed_cases', 'covid_19_deaths', 'precipitation', 'temperature']
        files_list = [file_name]
        for feature in feature_list:
            feature_file_name = plot_feature_over_time(feature, filter_input.state, filter_input.county)
            files_list.append(feature_file_name)

        return files_list
    except Exception as e:
        print(e)


def plot_feature_over_time(feature: str, state=None, county=None):
    DATA_PATH = os.path.join(BASE_DIR, "../data/covid-19-usa.csv")
    columns = ['date', f'{feature}', 'state_name', 'county_name']
    data = pd.read_csv(DATA_PATH, usecols=columns)
    data = data[data['state_name'] == state]
    data = data[data['county_name'] == county]
    # Ensure the date column is a datetime type for proper plotting
    data['date'] = pd.to_datetime(data['date'])

    # Sort the data by date to ensure correct line plotting
    data = data.sort_values('date')

    # Plotting
    plt.figure(figsize=(10, 5))  # Set the figure size for better readability
    plt.plot(data['date'], data[feature], linestyle='-', color='orange')
    plt.title(f'Time Series Plot for {feature}: {state} - {county}')
    plt.xlabel('Date')
    plt.ylabel(feature)
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate dates for better visibility
    plt.tight_layout()  # Adjust layout to fit elements

    file_name = f'{state.lower().replace(" ", "-")}-{county.lower().strip().replace(" ", "-")}-{feature}.png'
    figures_dir = f'{BASE_DIR}/../figures'
    file_path = os.path.join(figures_dir, file_name)
    print("Saving plot")
    plt.savefig(file_path)
    plt.close()
    return file_name


def predict_diabetes(filter_input: Filter):
    try:
        # Load the dataset
        # cols - Year,County_FIPS,County,State,Bivariate Tertile,Diagnosed Diabetes (Percentage) ,Obesity (Percentage)
        print(f"Predicting Diabetes: {filter_input.county} with {filter_input.state}")
        DATA_PATH = os.path.join(BASE_DIR, "../data/DiabetesAtlasData.csv")
        data = pd.read_csv(DATA_PATH)
        data = data.sort_values(by='Year')
        data = data[data["State"] == filter_input.state]
        data = data[data["County"] == filter_input.county]
        print(data.head())
        # Take only the features with numerical values
        numerical_features = data.select_dtypes(include=['int64', 'float64']).columns
        X = data[numerical_features]

        print("Creating target variable")
        # Create the target variable
        y = data['Diagnosed_Diabetes_Percentage']

        # Split the arch into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X[:1000], y[:1000], test_size=0.2, random_state=42)
        date_train, date_test = data.loc[X_train.index, 'Year'], data.loc[
            X_test.index, 'Year']  # Preserve dates for plotting

        print(f"Creating model")
        # Train the model
        model = RandomForestRegressor()

        print(f"Fitting model")
        model.fit(X_train, y_train)

        print(f"Predicting data")
        # Make predictions
        predictions = model.predict(X_test)
        print("Predicted Diabetes Cases:")
        # for i, prediction in enumerate(predictions):
        #     print(f"Sample {i + 1}: {prediction}")

        # Evaluate the model
        mse = mean_squared_error(y_test, predictions)
        print("Mean Squared Error:", mse)

        print("Plotting data")
        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(data['Year'], data['Diagnosed_Diabetes_Percentage'], label='Original', alpha=0.75)
        plt.scatter(date_test, predictions, color='red', label='Predicted', alpha=0.6)
        plt.title(f'Random Forest Prediction of Diabetes: {filter_input.state}-{filter_input.county}')
        plt.xlabel('Year')
        plt.ylabel('Case %')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        # Define the base directory for figures
        figures_dir = f'{BASE_DIR}/../figures'

        # Check if the directory exists, and create it if it does not
        if not os.path.exists(figures_dir):
            os.makedirs(figures_dir)

        # Assuming state_name and county_name are defined earlier in your code
        file_name = f'{filter_input.state.lower().replace(" ", "-")}-{filter_input.county.lower().strip().replace(" ", "-")}-prediction-diabetes.png'
        file_path = os.path.join(figures_dir, file_name)
        print("Saving plot")
        plt.savefig(file_path)
        # plt.show()
        files_list = [file_name]
        feature = 'Obesity_Percentage'

        # Plotting
        plt.figure(figsize=(10, 5))  # Set the figure size for better readability
        plt.plot(data['Year'], data[feature], linestyle='-', color='orange')
        plt.title(f'Time Series Plot for Obesity %: {filter_input.state}-{filter_input.county}')
        plt.xlabel('Date')
        plt.ylabel(feature)
        plt.grid(True)
        plt.xticks(rotation=45)  # Rotate dates for better visibility
        plt.tight_layout()  # Adjust layout to fit elements

        file_name_obesity = f'{filter_input.state.lower().replace(" ", "-")}-{filter_input.county.lower().strip().replace(" ", "-")}-obesity.png'
        file_path = os.path.join(figures_dir, file_name_obesity)
        print("Saving plot")
        plt.savefig(file_path)
        # plt.show()
        plt.close()
        files_list.append(file_name_obesity)

        return files_list
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # predict(state_name="Alabama", county_name="DeKalb County")

    # DATA_PATH = os.path.join(BASE_DIR, "../data/covid-19-usa.csv")
    # columns_to_load = ['county_name', 'state_name']
    # data = pd.read_csv(DATA_PATH, usecols=columns_to_load)
    # data['country_name'] = 'USA'
    # print(data.head())
    # # data = data[data['county_name'] == "DeKalb County"]
    # # plot_feature_over_time(data, 'temperature')
    # data = data.drop_duplicates(subset=['county_name'])
    # data.to_csv('./country-state-county.csv', index=False)
    # plot_feature_over_time('precipitation', 'Alabama', 'DeKalb County')
    filter_ = Filter(state="Alabama", county="DeKalb County", disease="Diabetes")
    # file_name = predict_diabetes(filter_)

    predict(filter_)
