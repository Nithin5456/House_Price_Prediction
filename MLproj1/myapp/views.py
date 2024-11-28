from django.shortcuts import render
import pickle
import json
import numpy as np

def predict_home_price(request):
    prediction = ""
    total_sqft = bhk = bathroom = location = ""

    if request.method == 'POST':
        # Check if the "Clear" button was clicked
        if request.POST.get('clear') == 'True':
            # Reset all fields and prediction
            return render(request, 'index.html', {'prediction': "", 'total_sqft': '', 'bhk': '', 'bathroom': '', 'location': ''})
        
        # Extract values from the form
        total_sqft = request.POST.get('total_sqft', '')
        bhk = request.POST.get('bhk', '')
        bathroom = request.POST.get('bathroom', '')
        location = request.POST.get('location', '').lower()

        # Check for valid inputs
        if not total_sqft or not bhk or not bathroom or not location:
            return render(request, 'index.html', {'prediction': "Please fill all the fields.", 'total_sqft': total_sqft, 'bhk': bhk, 'bathroom': bathroom, 'location': location})

        try:
            # Ensure valid numeric inputs
            total_sqft = float(total_sqft)
            bhk = int(bhk)
            bathroom = int(bathroom)
        except ValueError:
            return render(request, 'index.html', {'prediction': "Invalid input. Please enter correct values.", 'total_sqft': total_sqft, 'bhk': bhk, 'bathroom': bathroom, 'location': location})

        # Load model and columns
        model = pickle.load(open('banglore_home_prices_model.pickle', 'rb'))
        columns = json.load(open('columns.json', 'r'))['data_columns']

        # Initialize input data with zeros for all columns
        input_data = np.zeros(len(columns))

        # One-hot encode the location
        if location in columns:
            input_data[columns.index(location)] = 1
        else:
            print(f"Warning: location '{location}' not found in columns")

        # Set values for total_sqft, bath, and bhk
        input_data[columns.index('total_sqft')] = total_sqft
        input_data[columns.index('bath')] = bathroom
        input_data[columns.index('bhk')] = bhk

        # Make prediction
        prediction = model.predict([input_data])[0]

        # Multiply prediction by 100000 (1 lakh)
        result = round(prediction * 100000, 2)

        return render(request, 'index.html', {
            'prediction': result,
            'total_sqft': total_sqft,
            'bhk': bhk,
            'bathroom': bathroom,
            'location': location
        })
    
    return render(request, 'index.html', {'prediction': prediction})
