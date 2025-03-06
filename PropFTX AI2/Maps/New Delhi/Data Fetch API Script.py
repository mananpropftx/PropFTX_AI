import requests
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# List of locations (modify as needed)
locations =   [
  'Alaknanda',
  'Alaknanda Don Bosco Road',
  'Asaf Ali Road',
  'Chattarpur',
  'Chattarpur Enclave',
  'Dashrathpuri Metro Road',
  'Dilshad Garden',
  'Dwarka',
  'Dwarka Mor',
  'Dwarka Road',
  'Dwarka Sector 3',
  'Dwarka Sector 9',
  'GT Karnal Road',
  'Greater Kailash',
  'IP Extension',
  'Inder Mohan Bharadwaj Marg',
  'Indraprastha',
  'Jamia Nagar',
  'Janakpuri',
  'Jasola',
  'Jasola Vihar',
  'Kakrola',
  'Kalkaji',
  'Karol Bagh',
  'Kirti Nagar',
  'Loni Road',
  'Mahavir Enclave',
  'Main Chhatarpur Road',
  'Main Rajapuri Road',
  'Mandi Road',
  'Mayur Vihar',
  'Mayur Vihar 1',
  'Mehrauli',
  'Mehrauli Badarpur Road',
  'Moti Nagar',
  'Munirka',
  'Narwana Road',
  'Nawada',
  'New Rohtak Road',
  'Okhla',
  'Okhla Estate Marg',
  'Pandav Nagar',
  'Pankha Road',
  'Paschim Vihar',
  'Patel Road',
  'Patparganj',
  'Pitam Pura',
  'Rajpur Road',
  'Rohini',
  'Saharanpur Delhi Road',
  'Saket',
  'Sarita Vihar',
  'Sector 10 Dwarka',
  'Sector 11 Dwarka',
  'Sector 12 Dwarka',
  'Sector 13 Dwarka',
  'Sector 13 Rohini',
  'Sector 14 Rohini',
  'Sector 18 Dwarka',
  'Sector 19 Dwarka',
  'Sector 2 Dwarka',
  'Sector 22 Dwarka',
  'Sector 23 Dwarka',
  'Sector 4 Dwarka',
  'Sector 5 Dwarka',
  'Sector 6 Dwarka',
  'Sector 7 Dwarka',
  'Sector 9 Rohini',
  'Sector B Vasant Kunj',
  'Sector C Vasant Kunj',
  'Sector D Vasant Kunj',
  'Shahdara',
  'Sri Aurobindo Marg',
  'Uttam Nagar',
  'Uttam Nagar West',
  'Vasant Kunj',
  'Vasundhara Enclave',
  'Vikas Marg',
  'Vikaspuri',
  'Vipin Garden'
]
 # Add more locations as needed

# Define the quarters
quarters = ["Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"]

# Define the range of years (from Jan-Mar 2024 to Oct 2030)
years = list(range(2024, 2031))

# CSV file header
csv_header = ["location", "year", "quarter", "avg_price", "max_price", "min_price"]

with open('Delhi_price_predictions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    for location in locations:
        for year in years:
            predictions = [{"location": location, "quarter": quarter, "year": year} for quarter in quarters]
            
            payload = {
                "predictions": predictions,
                "city": "New Delhi",
                "priceType": "all"
            }

            try:
                logging.info(f"Fetching data for {location} - {year}")
                response = requests.post("https://ai-ml-propftx.letsphoenix.com/predict", json=payload)
                
                if response.status_code == 200:
                    data = response.json()

                    for entry in data:
                        row = [
                            entry["location"],
                            entry["year"],
                            entry["quarter"],
                            entry["avg_price"],
                            entry["max_price"],
                            entry["min_price"]
                        ]
                        writer.writerow(row) 
                        logging.info(f"Data saved for {location} - {year} - {entry['quarter']}")

                else:
                    logging.error(f"Failed to fetch data for {location} - {year}: {response.status_code}")
            
            except Exception as e:
                logging.error(f"Error occurred while fetching data for {location} - {year}: {str(e)}")
