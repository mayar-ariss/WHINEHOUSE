from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import io

app = Flask(__name__)
CORS(app)

# Mock database
facilities = [
    {"id": 1, "name": "Rehab A", "location": "City X", "services": ["PT", "OT"],
     "accepted_insurance": ["Insurance A"], "available_capacity": 5},
    {"id": 2, "name": "Rehab B", "location": "City Y", "services": ["OT"],
     "accepted_insurance": ["Insurance B"], "available_capacity": 0},
    {"id": 3, "name": "Rehab C", "location": "City Z", "services": ["PT", "Wound Care"],
     "accepted_insurance": ["Insurance C"], "available_capacity": 3}
]


# Helper function to calculate match score
def calculate_distance(location1, location2):
    return 0 if location1 == location2 else 50

def calculate_match_score(patient, facilities):
    matches = []
    for facility in facilities:
        print(f"Checking facility: {facility['name']} - Capacity: {facility['available_capacity']}")  # Debugging

        if patient["insurance"] not in facility["accepted_insurance"]:
            print(f"Skipping {facility['name']} due to insurance mismatch.")  # Debugging
            continue
        
        # Calculate individual components of the score
        proximity_score = 100 - calculate_distance(patient["location"], facility["location"])  # Max: 100
        specialty_overlap = len(set(patient["needs"]).intersection(set(facility["services"]))) * 20  # Max: 20 per need
        availability_score = 50 if facility["available_capacity"] > 0 else 0  # Max: 50

        # Calculate total score
        total_score = proximity_score + specialty_overlap + availability_score

        # Calculate maximum possible score for normalization
        max_specialty_score = len(patient["needs"]) * 20
        max_score = 100 + max_specialty_score + 50  # Max proximity + max specialties + max availability

        # Normalize the score to a 0–100 range
        normalized_score = (total_score / max_score) * 100

        matches.append({
            "facility": facility,
            "score": round(normalized_score, 2)  # Round to 2 decimal places for clarity
        })
    
    # Sort matches by normalized score
    return sorted(matches, key=lambda x: x["score"], reverse=True)


@app.route('/api/match', methods=['POST'])
def match_facilities():
    patient = request.json
    print("Received patient data:", patient)  # Debugging input
    # Validate input
    if not patient.get("needs") or not patient.get("insurance") or not patient.get("location"):
        print("Invalid input received")
        return jsonify({"error": "Invalid input. All fields are required."}), 400
    matches = calculate_match_score(patient, facilities)
    print("Calculated matches:", matches)  # Debugging output
    return jsonify(matches)

@app.route('/api/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    stream = io.StringIO(file.stream.read().decode('UTF-8'))
    csv_input = csv.DictReader(stream)
    patients = [row for row in csv_input]
    print("Uploaded Patients:", patients)  # Debugging uploaded data

    # Calculate matches for each patient
    results = []
    for patient in patients:
        # Format patient data to match the expected structure
        formatted_patient = {
            "needs": [need.strip() for need in patient["Needs"].split(",")],
            "insurance": patient["Insurance"],
            "location": patient["Location"]
        }
        print(f"Processing patient: {patient['Name']} - {formatted_patient}")  # Debugging
        matches = calculate_match_score(formatted_patient, facilities)
        print(f"Matches for {patient['Name']}: {matches}")  # Debugging
        results.append({
            "patient": patient,
            "matches": matches
        })

    return jsonify({"message": "Upload successful", "results": results})

if __name__ == '__main__':
    print("Backend is running...")
    app.run(debug=True)
