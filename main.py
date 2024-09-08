from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Shop, Ewaste
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# Load the dataset
df = pd.read_csv('updated_e_waste_dataset.csv')
df_shops = pd.read_csv('shop.csv')
# Load the model
model = joblib.load('e_waste_pipeline.pkl')

# Pre-process data for dynamic dropdowns
device_types = df['Device Type'].unique()
brands = df['Brand Name'].unique()
models = df['Item Name'].unique()

@app.route('/')
def home():
    return render_template('home.html', device_types=device_types, brands=brands, models=models)
@app.route('/shops', methods=['GET', 'POST'])
def show_shops():
    if request.method == 'POST':
        selected_address = request.form.get('address')
        
        # Filter shops based on the selected address
        filtered_shops = df_shops[df_shops['address'] == selected_address]
        shops = filtered_shops.to_dict(orient='records')
    else:
        shops = []
    
    # List of sample addresses for the dropdown
    addresses = df_shops['address'].unique()
    
    return render_template('nearby_shop.html', shops=shops, addresses=addresses)

@app.route('/result', methods=['POST'])
def result():
    category = request.form['category']
    device_type = request.form['device_type']
    device_age= request.form['device_age']
    brand = request.form['brand']
    model_name = request.form['model']
    condition = request.form['condition']
    
    # Find the relevant row from the DataFrame
    filtered_df = df[(df['Item Name'] == model_name) & 
                     (df['Device Type'] == device_type) & 
                     (df['Brand Name'] == brand)]
    
    if not filtered_df.empty:
        item = filtered_df.iloc[0]
        
        # Create features DataFrame for prediction with required columns
        features = {
            'Item Name': item['Item Name'],
            'Category': item['Category'],
            'Brand Name': item['Brand Name'],
            'Device Age': item['Device Age'],
            'Device Condition': condition,
            'Material Recovery Rate': item['Material Recovery Rate'],
            'Device Type': item['Device Type'],
            'Year of Manufacture': item['Year of Manufacture'],
            'Market Value of Metals': item['Market Value of Metals'],
            'Cost of Recovery': item['Cost of Recovery'],
            'Gold (g)': item['Gold (g)'],
            'Aluminum (g)': item['Aluminum (g)'],
            'Silver (g)': item['Silver (g)'],
            'Carbon (g)': item['Carbon (g)'],
            'Platinum (g)': item['Platinum (g)'],
            'Rhodium (g)': item['Rhodium (g)'],
            'Nickel (g)': item['Nickel (g)'],
            'Tin (g)': item['Tin (g)'],
            'Lithium (g)': item['Lithium (g)'],
            'Current Metal Value ($)': item['Current Metal Value ($)'],
            'Recycling Score': item['Recycling Score']
        }
        
        # Ensure columns order matches the model's expected input
        columns = ['Item Name', 'Category', 'Brand Name', 'Device Age', 'Device Condition',
                   'Material Recovery Rate', 'Device Type', 'Year of Manufacture', 
                   'Market Value of Metals', 'Cost of Recovery', 'Gold (g)', 'Aluminum (g)', 
                   'Silver (g)', 'Carbon (g)', 'Platinum (g)', 'Rhodium (g)', 'Nickel (g)', 
                   'Tin (g)', 'Lithium (g)', 'Current Metal Value ($)', 'Recycling Score']
        
        features_df = pd.DataFrame([features], columns=columns)
        
        # Make prediction
        prediction = model.predict(features_df)[0]
        
        result_data = {
            'Item Name': item['Item Name'],
            'Category': item['Category'],
            'Brand Name': item['Brand Name'],
            'Device Age': device_age,
            'Device Condition': item['Device Condition'],
            'Material Recovery Rate': item['Material Recovery Rate'],
            'Device Type': item['Device Type'],
            'Year of Manufacture': item['Year of Manufacture'],
            'Market Value of Metals': item['Market Value of Metals'],
            'Cost of Recovery': item['Cost of Recovery'],
            'Gold (g)': item['Gold (g)'],
            'Aluminum (g)': item['Aluminum (g)'],
            'Silver (g)': item['Silver (g)'],
            'Carbon (g)': item['Carbon (g)'],
            'Platinum (g)': item['Platinum (g)'],
            'Rhodium (g)': item['Rhodium (g)'],
            'Nickel (g)': item['Nickel (g)'],
            'Tin (g)': item['Tin (g)'],
            'Lithium (g)': item['Lithium (g)'],
            'Current Metal Value ($)': item['Current Metal Value ($)'],
            'Recycling Score': item['Recycling Score'],
            'Predicted Price ($)': prediction
        }
    else:
        result_data = {'error': 'No data found for the selected criteria.'}
    
    return render_template('result.html', result_data=result_data)
@app.route('/book/<int:shop_id>', methods=['POST'])
def book(shop_id):
    # Here you would normally handle booking logic, e.g., saving the booking to a database
    shop = df_shops[df_shops['id'] == shop_id].iloc[0]
    
    # For demonstration purposes, just show a confirmation page
    return render_template('booking_confirmation.html', shop=shop)

if __name__ == '__main__':
    app.run(debug=True)
