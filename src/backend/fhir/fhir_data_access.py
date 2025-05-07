import matplotlib.pyplot as plt
import requests 
import datetime
from collections import defaultdict

def fetch_fhir_data(url):
    headers = {
        'Accept': 'application/fhir+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch arch: {response.status_code}")
        return None
    
def fetch_patient_data(base_url):
    # Construct the URL for fetching patient resources
    patient_url = f"{base_url}/Patient"

    # Fetch FHIR arch
    fhir_data = fetch_fhir_data(patient_url)

    if fhir_data is not None:
        # Parse patient resources from the response
        patients = fhir_data.get('entry', [])

        # Extract patient arch
        patient_data = []
        for patient in patients:
            resource = patient.get('resource', {})
            patient_id = resource.get('id')
            patient_name = resource.get('name', [{}])[0].get('given', [None])[0] if resource.get('name') else None
            patient_gender = resource.get('gender')
            patient_birthdate = resource.get('birthDate')
            
        # Extract address information
            address = resource.get('address', [])
            print(address)
            patient_address_parts = []
            for addr in address:
                if addr.get('line', []):
                    lines = addr.get('line', [])
                    #print("Line present")
                else:
                    lines = " "
                if addr.get('city'):
                    city = addr.get('city')
                    print(city)
                else:
                    city = " "
                if addr.get('state'):
                    state = addr.get('state')
                else:
                    state = " "
                if addr.get('postalCode'):
                    postal_code = addr.get('postalCode')
                else:
                    postal_code = " "
                if addr.get('country'):
                    country = addr.get('country')
                else:
                    country = " "
                
                # Construct address string
                #address_str = ' '.join(lines + [city, state, postal_code, country])
                address_str = ' '.join(lines) + ' ' + ' '.join([city, state, postal_code, country])
                if address_str:
                    patient_address_parts.append(address_str)

            # Join all address parts into a single string
            patient_address = ", ".join(patient_address_parts) if patient_address_parts else None



            # Store patient arch in a dictionary
            patient_info = {
                "id": patient_id,
                "name": patient_name,
                "gender": patient_gender,
                "birthdate": patient_birthdate,
                "address": patient_address
            }

            patient_data.append(patient_info)

        return patient_data
    else:
        return None

def fetch_condition_data(base_url):
    # Construct the URL for fetching condition resources
    condition_url = f"{base_url}/Condition?code=73211009"

    # Fetch FHIR arch
    fhir_data = fetch_fhir_data(condition_url)

    if fhir_data is not None:
        # Parse condition resources from the response
        conditions = fhir_data.get('entry', [])

        # Extract condition arch
        condition_data = []
        for condition in conditions:
            resource = condition.get('resource', {})
            condition_id = resource.get('id')
            condition_code = resource.get('code', {}).get('coding', [{}])[0].get('code')
            condition_code_display = resource.get('code', {}).get('coding', [{}])[0].get('display')
            condition_description = resource.get('code', {}).get('text')
            onset_date = resource.get('onsetDateTime')
            clinical_status = resource.get('clinicalStatus', {}).get('coding', [{}])[0].get('display')
            
            # Ensure onset_date is in a proper format
            if isinstance(onset_date, str):
                onset_date = onset_date.split('T')[0]  # Extract date part
                
            # Add condition arch to the list
            condition_data.append({
                #'id': condition_id,
                'code': condition_code,
                'code_name': condition_code_display,
                #'description': condition_description,
                'onset_date': onset_date,
                #'clinical_status': clinical_status  # Extracted clinical status
            })

        return condition_data
    else:
        return None

def fetch_location_data(base_url):
    # Construct the URL for fetching location resources
    location_url = f"{base_url}/Location"

    # Fetch FHIR arch using requests
    response = requests.get(location_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract location arch from the response JSON
        locations = response.json().get('entry', [])
        
        # Extract relevant information from each location resource
        location_data = []
        for location in locations:
            resource = location.get('resource', {})
            location_id = resource.get('id')
            location_name = resource.get('name')
            location_telecom = resource.get('telecom', [{}])[0].get('value')
            address = resource.get('address', {})
            location_address = ", ".join(address.get('line', []))
            location_city = address.get('city')
            location_state = address.get('state')
            location_postal_code = address.get('postalCode')
            
            # Add location arch to the list
            location_data.append({
                'id': location_id,
                'name': location_name,
                'telecom': location_telecom,
                'address': location_address,
                'city': location_city,
                'state': location_state,
                'postal_code': location_postal_code
            })

        return location_data
    else:
        print(f"Failed to fetch location arch: {response.status_code}")
        return None
    
def fetch_risk_assessment_data(base_url, patient_id):
    # Construct the URL for fetching Risk Assessment resources for the specific patient
    risk_assessment_url = f"{base_url}/RiskAssessment?subject={patient_id}"

    # Fetch FHIR arch using requests
    response = requests.get(risk_assessment_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract Risk Assessment arch from the response JSON
        risk_assessments = response.json().get('entry', [])
        
        # Extract relevant information from each Risk Assessment resource
        risk_assessment_data = []
        for entry in risk_assessments:
            resource = entry.get('resource', {})
            risk_assessment_id = resource.get('id')
            status = resource.get('status')
            method = resource.get('code', {}).get('coding', [{}])[0].get('display')
            performer = resource.get('performer', {}).get('reference')
            prediction = resource.get('prediction', [])

            # Extract predictions if available
            predictions_data = []
            for pred in prediction:
                outcome = pred.get('outcome', {}).get('text')
                probability_decimal = pred.get('probabilityDecimal')
                when_range = pred.get('whenRange', {})
                low_value = when_range.get('low', {}).get('value')
                low_unit = when_range.get('low', {}).get('unit')
                high_value = when_range.get('high', {}).get('value')
                high_unit = when_range.get('high', {}).get('unit')

                # Add prediction arch to the list
                predictions_data.append({
                    'outcome': outcome,
                    'probability_decimal': probability_decimal,
                    'low_value': low_value,
                    'low_unit': low_unit,
                    'high_value': high_value,
                    'high_unit': high_unit
                })

            # Add Risk Assessment arch to the list
            risk_assessment_data.append({
                'id': risk_assessment_id,
                'status': status,
                'method': method,
                'performer': performer,
                'predictions': predictions_data
            })

        return risk_assessment_data
    else:
        print(f"Failed to fetch Risk Assessment arch: {response.status_code}")
        return None
    
def create_time_series_analysis(base_url, disease_code, start_year, end_year):
    # Fetch condition arch for the specified disease
    condition_data = fetch_condition_data(base_url)

    if condition_data:
        # Filter condition arch based on the disease code and year range
        disease_data = [condition for condition in condition_data if condition['code'] == disease_code
                        and condition['onset_date'] is not None
                        and isinstance(condition['onset_date'], str)  # Check if onset date is a string
                        and start_year <= int(condition['onset_date'].split('-')[0]) <= end_year]  # Extract year from date string

        # Initialize defaultdict to aggregate arch based on time intervals
        time_series_data = defaultdict(int)

        # Aggregate arch based on onset date
        for condition in disease_data:
            onset_year = int(condition['onset_date'].split('-')[0])  # Extract year from date string
            time_series_data[onset_year] += 1
            print("\nOnset Year:", onset_year)
            print("\nCount:", time_series_data[onset_year])

        # Sort time series arch by year
        sorted_time_series_data = sorted(time_series_data.items())

        return sorted_time_series_data
    else:
        print("Failed to fetch condition arch.")
        return None
    
if __name__ == "__main__":
    base_url = "https://hapi.fhir.org/baseR4"
    #limit = 2000
    print("\nPatient Data")
    print(fetch_patient_data(base_url))
    print("\nCondition Data")
    print(fetch_condition_data(base_url))
    patient_id =  1202
    locations = fetch_location_data(base_url)
    if locations:
        print("Location Data:")
        for location in locations:
            print(location)
    else:
        print("Failed to fetch location arch.")

    risk_assessments = fetch_risk_assessment_data(base_url, patient_id)
    if risk_assessments:
        print("Risk Assessment Data:")
        for risk_assessment in risk_assessments:
            print(risk_assessment)
    else:
        print("Failed to fetch risk assessment arch.")

    limit = 1000  # Adjust the limit as needed
    disease_code = "73211009"  # Replace with the actual disease code
    disease_name = "Diabetes"  # Replace with the actual disease name
    start_year = 1950  # Start year of the selected range
    end_year = 2020  # End year of the selected range

    if disease_name:
        print(f"Disease Name: {disease_name}")

        time_series_analysis = create_time_series_analysis(base_url, disease_code, start_year, end_year)
        if time_series_analysis:
            years, counts = zip(*time_series_analysis)

            # Plotting the time series analysis
            plt.figure(figsize=(10, 6))
            plt.plot(years, counts, marker='o', linestyle='-')
            plt.title(f'Time Series Analysis of {disease_name} Occurrences')
            plt.xlabel('Year')
            plt.ylabel('Number of Occurrences')
            plt.grid(True)
            plt.xticks(years)
            plt.tight_layout()
            plt.show()
        else:
            print("No arch available for the specified disease code and year range.")
    else:
        print("Failed to fetch disease name.")
