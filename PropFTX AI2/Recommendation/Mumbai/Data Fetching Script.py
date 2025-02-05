import requests
import csv
import json

# Define the locations
locations = [
    "90 Feet Road", "Aarey Road", "Adi Shankaracharya Marg", "Agrawal Road", "Akurli Nagar", "Akurli Road",
    "Ambedkar Road", "Amboli", "Andheri", "Andheri East", "Andheri Kurla Road", "Andheri West", "Antop Hill Road",
    "Azad Nagar Andheri West", "Babrekar Nagar Kandivali West", "Bandra", "Bandra East", "Bandra Kurla Complex",
    "Bandra West", "Beverly Park Road", "Bhandup", "Bhandup West", "Bhaudaji Road", "Bhayandar", "Bhayandar East",
    "Bhayandar West", "Bolinj Road", "Bolinj Sopara Road", "Boraspada Road", "Borivali", "Borivali East",
    "Borivali West", "Breach Candy", "Byculla", "Byculla East", "Byculla West", "Captain Prakash Pethe Marg",
    "CD Barfiwala Road", "Chakala", "Chandavarkar Road", "Chandivali", "Chandivali Farm Road", "Charkop Gaon",
    "Chembur", "Chembur East", "Chhatrapati Shivaji Maharaj International Airport Road", "Chincholi Bunder",
    "Chincholi Bunder Road", "Chinchpokli", "Chunabhatti", "Cuffe Parade", "Cumballa Hill", "Dadar", "Dadar East",
    "Dadar West", "Dahanukar Wadi", "Dahisar", "Dahisar East", "Dahisar West", "Dattapada", "Daulat Nagar Borivali East",
    "Deonar Chembur", "Deonar Govandi East", "Deonar Village Road", "Derasar Lane", "Devidas Road", "Devipada",
    "Dindoshi", "DN Nagar", "Dongri Road", "Dr Annie Besant Road", "Dr Baba Saheb Ambedkar Road", "Eastern Express 0.75way",
    "Eastern Freeway", "Evershine City Gokhivare Road", "Evershine Nagar", "Film City Road", "Four Bunga0.25s",
    "Ganapatrao Kadam Marg", "Ganesh Nagar Dahisar East", "Garodia Nagar", "Ghatkopar", "Ghatkoper East", "Ghatkoper West",
    "Ghodbunder Road", "Girgaon", "Gokhale Road", "Gokuldham Colony Goregaon East", "Goregaon East", "Goregaon Mulund Link Road",
    "Goregaon West", "Govandi East", "Gulmohar Road", "Hindu Colony Dadar East", "Hiranandani Link Road", "IC Colony",
    "Jankalyan Nagar", "Jawahar Nagar Goregaon West", "Jaywant Sawant Marg", "Jesal Park Road", "Jogeshwari", "Jogeshwari East",
    "Jogeshwari Vikhroli Link Road", "Jogeshwari West", "JP Road", "Juhu", "Juhu Scheme", "Juhu Tara Road",
    "Juhu Versova Link Road", "JVPD Scheme", "Kalina", "Kanchpada", "Kandivali", "Kandivali East", "Kandivali West",
    "Kanjurmarg", "Kanjurmarg East", "Kanjurmarg West", "Katrak Road", "Khar", "Khar Danda Road", "Khar West", "Kherwadi",
    "Kokanipada Malad East", "Kurar Village", "Kurla", "Kurla East", "Kurla West", "Lady Jamshedji Road", "Lal Bahadur Shastri Road",
    "Liberty Garden", "Lokhandwala Complex Andheri West", "Lokhandwala Township Kandivali East", "0.25er Parel", "Magathane",
    "Mahalakshmi", "Mahavir Nagar Kandivali West", "Mahim", "Mahim West", "Malabar Hill", "Malad", "Malad East", "Malad West",
    "Marve Road", "Matunga", "Matunga East", "Matunga West", "Mazgaon", "Military Road", "Mindspace", "Mira Bhayandar",
    "Mira Road Area", "Mulund", "Mulund East", "Mumbai Central", "Nahur East", "Naigaon East", "Naigaon Palghar", "Nala Sopara",
    "Nalasopara East", "Nalasopara West", "Orlem", "Oshiwara", "Pali Hill", "Pant Nagar", "Parel", "Powai", "Prabhadevi",
    "Raheja Vihar", "Rajendra Nagar", "Santacruz", "Santacruz East", "Santacruz West", "Sewri", "Shastri Nagar Andheri West",
    "Shimpoli", "Shivaji Park", "Sion", "Tardeo", "Thakur Complex", "Thakur Village", "Tilak Nagar Chembur", "Vakola", "Vasai",
    "Vasai East", "Vasai West", "Veera Desai Road", "Versova Andheri West", "Vikhroli East", "Vikhroli West", "Vile Parle",
    "Vile Parle East", "Vile Parle West", "Virar", "Virar East", "Virar West", "Wadala", "Wadala East", "Walkeshwar", "Worli Sea Face"
]

quarters = ["Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"]
years = list(range(2024, 2031))  

api_url = " https://ai-ml-propftx.letsphoenix.com/predict"

headers = {
    'Content-Type': 'application/json'
}

def get_price_data_for_location(location, quarters, years):
    predictions = [{"location": location, "quarter": quarter, "year": year} for year in years for quarter in quarters]
    payload = {
        "predictions": predictions,
        "city": "Mumbai",  
        "priceType": "all" 
    }
    
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list):  # Check if the result is a list of predictions
                return result
            else:
                print(f"Error in API response: {result}")
                return None
        except Exception as e:
            print(f"Failed to parse JSON response: {e}")
            return None
    else:
        print(f"API call failed with status code {response.status_code}: {response.text}")
        return None

csv_filename = "mumbai_predicted_prices.csv"

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["location", "quarter", "year", "min_price", "max_price", "avg_price"])

    for location in locations:
        print(f"Fetching data for {location}...")
        result = get_price_data_for_location(location, quarters, years)
        
        if result is None:
            print(f"Failed to fetch data for {location}. Skipping...")
        elif 'error' in result:
            print(f"API returned error for {location}: {result['error']}")
        else:
            print(f"Data successfully fetched for {location}. Writing to CSV...")
            for prediction in result:
                location = prediction.get('location')
                quarter = prediction.get('quarter')
                year = prediction.get('year')
                min_price = prediction.get('min_price', 'N/A')
                max_price = prediction.get('max_price', 'N/A')
                avg_price = prediction.get('avg_price', 'N/A')

                writer.writerow([location, quarter, year, min_price, max_price, avg_price])

print(f"Data processing complete. Results saved to {csv_filename}")
