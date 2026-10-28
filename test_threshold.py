from app import app, get_suitability_assessment
import json

# Expected strings
low_expected = "Low Score — Further Medical Evaluation Required."
high_expected = "Higher Score — Further Medical Evaluation Required."

# 1. Exact boundary and threshold test cases
print("--- Running Boundary & Threshold Unit Tests ---")
# Score = 49%
assert get_suitability_assessment(49.0) == low_expected, f"Failed for 49.0: {get_suitability_assessment(49.0)}"
assert get_suitability_assessment(49) == low_expected, f"Failed for 49: {get_suitability_assessment(49)}"
assert get_suitability_assessment(49.9) == low_expected, f"Failed for 49.9: {get_suitability_assessment(49.9)}"
assert get_suitability_assessment(0.0) == low_expected, f"Failed for 0.0: {get_suitability_assessment(0.0)}"

# Score = 50%
assert get_suitability_assessment(50.0) == high_expected, f"Failed for 50.0: {get_suitability_assessment(50.0)}"
assert get_suitability_assessment(50) == high_expected, f"Failed for 50: {get_suitability_assessment(50)}"
assert get_suitability_assessment(50.1) == high_expected, f"Failed for 50.1: {get_suitability_assessment(50.1)}"
assert get_suitability_assessment(100.0) == high_expected, f"Failed for 100.0: {get_suitability_assessment(100.0)}"
print(" Boundary tests for 49% and 50% PASSED!")

# 2. Error handling tests
print("\n--- Running Error Handling Tests ---")
assert get_suitability_assessment(None) == "Assessment Unavailable"
assert get_suitability_assessment("invalid") == "Assessment Unavailable"
assert get_suitability_assessment(float('nan')) == "Assessment Unavailable"
print(" Error handling tests for None/invalid/NaN PASSED!")

# 3. Flask API endpoint tests
print("\n--- Running Flask Route Integration Tests ---")
client = app.test_client()

# GET /
res_get = client.get('/')
assert res_get.status_code == 200
html = res_get.data.decode('utf-8')
assert 'suitability-box' in html
assert 'suitability-message' in html
assert 'suitability-score-ref' in html
assert '50% Threshold Rule' in html
print(" GET / returned 200 with dynamic suitability DOM elements!")

# POST /predict with default values (score >= 50%)
payload_normal = {
    'r_age': 50, 'r_gender': 'Male', 'r_bmi': 25.0, 'r_meld_score': 15,
    'r_albumin_level': 40.0, 'r_na': 140.0, 'r_mg': 2.0, 'r_wbc': 7000,
    'r_lympochyte': 30.0, 'r_platelets': 200000, 'r_cold_ischemia_time': 360,
    'r_warm_ischemia_time': 30, 'r_rejection_episodes': 0, 'r_diabetes': 0,
    'r_hypertension': 0, 'r_alcohol_abuse': 0, 'r_smoking': 0,
    'r_hepatitis_b': 0, 'r_hepatitis_c': 0, 'r_alcoholic_cirrhosis': 0,
    'r_primary_biliary_cirrhosis': 0, 'r_blood_transfusion': 0
}
res1 = client.post('/predict', data=json.dumps(payload_normal), content_type='application/json')
assert res1.status_code == 200
data1 = res1.get_json()
print(f" Normal Case -> Health Score: {data1['health_score']}% | Assessment: {data1['suitability_assessment']}")
assert data1['health_score'] >= 50.0
assert data1['suitability_assessment'] == high_expected

# POST /predict with high-risk sample values (score < 50%)
payload_high_risk = {
    'r_age': 54, 'r_gender': 'Male', 'r_bmi': 27.4, 'r_meld_score': 22,
    'r_albumin_level': 32.0, 'r_na': 136.0, 'r_mg': 1.8, 'r_wbc': 8200,
    'r_lympochyte': 24.0, 'r_platelets': 160000, 'r_cold_ischemia_time': 420,
    'r_warm_ischemia_time': 35, 'r_rejection_episodes': 1, 'r_diabetes': 1,
    'r_hypertension': 1, 'r_alcohol_abuse': 0, 'r_smoking': 0,
    'r_hepatitis_b': 0, 'r_hepatitis_c': 1, 'r_alcoholic_cirrhosis': 0,
    'r_primary_biliary_cirrhosis': 0, 'r_blood_transfusion': 1
}
res2 = client.post('/predict', data=json.dumps(payload_high_risk), content_type='application/json')
assert res2.status_code == 200
data2 = res2.get_json()
print(f" High Risk Case -> Health Score: {data2['health_score']}% | Assessment: {data2['suitability_assessment']}")
assert data2['health_score'] < 50.0
assert data2['suitability_assessment'] == low_expected

print("\n=============================================")
print(" ALL TESTS PASSED SUCCESSFULLY! ")
print("=============================================")

