import requests


def fetch_fhir_data(url):
    headers = {
        'Accept': 'application/fhir+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None


def print_patient_data(patient_record):
    print(f"Fetched {len(patient_record['entry'])} Patient records.")
    for entry in patient_record['entry']:
        patient = entry['resource']

        # Handle potentially multiple names, choosing the first as primary
        name = patient.get('name', [{}])[0]  # Assume first name as primary if exists
        full_name = "N/A"
        if name:
            parts = [name.get('family', '')] + name.get('given', [])  # Family name + given names
            full_name = ' '.join(filter(None, parts))

        # Handle potential complexity in address (assume first address as primary)
        address = patient.get('address', [{}])[0]
        address_text = "N/A"
        if address:
            # Convert 'line' list to a single string
            line = ' '.join(address.get('line', []))
            parts = [line] + [
                address.get(part, '')
                for part in ['city', 'state', 'postalCode', 'country']
            ]
            address_text = ', '.join(filter(None, parts))  # Construct full address

        gender = patient.get('gender', 'N/A')

        print(f"Patient ID: {patient['id']}, Full Name: {full_name}, Gender: {gender}, Address: {address_text}")


def print_condition_data(condition_data):
    print(f"Fetched {len(condition_data['entry'])} Condition records.")
    for entry in condition_data['entry']:
        condition = entry['resource']
        clinical_status = condition.get('clinicalStatus', {}).get('coding', [{}])[0].get('display', 'N/A')
        onset = condition.get('onsetDateTime', 'N/A')
        abatement = condition.get('abatementDateTime', 'N/A')
        recorded_date = condition.get('recordedDate', 'N/A')
        print(f"Condition ID: {condition['id']}, Clinical Status: {clinical_status}, Onset: {onset}, Abatement: {abatement}, Recorded Date: {recorded_date}")


def print_risk_assessment_data(risk_assessment_data):
    print(f"Fetched {len(risk_assessment_data['entry'])} Risk Assessment records.")
    for entry in risk_assessment_data['entry']:
        risk_assessment = entry['resource']
        predictions = risk_assessment.get('prediction', [])
        prediction_text = 'N/A'
        if predictions and 'outcome' in predictions[0]:
            prediction_text = predictions[0]['outcome'].get('text', 'N/A')
        print(f"Risk Assessment ID: {risk_assessment['id']}, Prediction: {prediction_text}")


def print_observation_data(observation_data):
    print(f"Fetched {len(observation_data['entry'])} Observation records.")
    for entry in observation_data['entry']:
        observation = entry['resource']
        code_display = observation.get('code', {}).get('coding', [{}])[0].get('display', 'N/A')
        value = observation.get('valueQuantity', {}).get('value', 'N/A')
        unit = observation.get('valueQuantity', {}).get('unit', 'N/A')
        print(f"Observation ID: {observation['id']}, Code: {code_display}, Value: {value} {unit}")


if __name__ == "__main__":
    base_url = "https://hapi.fhir.org/baseR4/"
    resource_function_map = {
        "Patient?_count=5": print_patient_data,
        "Condition?_count=5": print_condition_data,
        "RiskAssessment?_count=5": print_risk_assessment_data,
        "Observation?_count=5": print_observation_data,
    }

    for resource, function in resource_function_map.items():
        fhir_url = f"{base_url}{resource}"
        data = fetch_fhir_data(fhir_url)
        # print(arch)
        if data and 'entry' in data:
            function(data)
        else:
            print(f"No data fetched for {resource.split('?')[0]}.")
