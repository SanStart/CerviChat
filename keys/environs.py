import json

with open('keys/keys.json') as file:
    keys = json.load(file)


feature_names = {'NSI': 'Normal Superficial Intermediate',
        'AK': 'Abnormal Koilocytotic',
        'AD': 'Abnormal Dyskeratotic',
        'BM': 'Benign Metaplastic',
        'NP': 'Normal Parabasal',
        'NSD': 'Abnormal Severe Dysplastic',
        'ALD': 'Abnormal Light Dysplastic',
        'ACIS': 'Abnormal Carcinoma In Situ',
        'AMD': 'Abnormal Moderate Dysplastic',
        'NC': 'Normal Columnar', 
        'NS': 'Normal Superficiel',
        'NI': 'Normal Intermediate'}