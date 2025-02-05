import requests
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# List of locations (modify as needed)
locations = ["Airport Road", "Akurdi", "Alandi", "Alandi Markal Road", "Alandi Road", 
    "Amanora Park Town", "Ambegaon", "Ambegaon BK", "Anand Nagar", "Apte Road", 
    "Ashok Nagar Tathawade", "Ashoka Nagar", "Aundh", "Aundh Baner Link Road", 
    "Aundh Ravet BRTS Road", "Aundh Road", "Aundh Wakad Road", "Awhalwadi Road", 
    "BMCC Road", "Balewadi", "Balewadi Gaon", "Balewadi Gaon Road", "Balewadi Phata", 
    "Baner", "Baner Aundh Road", "Baner Balewadi Road", "Baner Gaon", "Baner Mahalunge Road", 
    "Baner Pashan Link Road", "Baner Road", "Bavdhan", "Bhagwan Tatyasaheb Kawade Road", 
    "Bhandarkar Road", "Bharati Vidyapeeth Road", "Bhosari", "Bhosari Alandi Road", 
    "Bhugaon", "Bhukum", "Bhumkar Nagar Wakad", "Bhumkar Wasti Road", "Bibvewadi Road", 
    "Bibwewadi", "Bibwewadi Kondhwa Road", "Blue Ridge Town Pune", "Boat Club Road", 
    "Borhade Wadi", "Bund Garden", "Bund Garden Road", "Camp", "Chakan", "Chakan Alandi Road", 
    "Charholi BK", "Chhatrapati Shivaji Maharaj Road", "Chikhali Pimpri Chinchwad", "Chinchwad", 
    "Clover Village", "DP Road", "Dahanukar Colony", "Dange Chowk Road", "Datta Mandir Road", 
    "Deccan Gymkhana", "Dehu Moshi Road", "Dehu Road", "Dhankawadi", "Dhanori", 
    "Dhanori Lohegaon Road", "Dhanori Road", "Dhayari", "Dhayari Phata Road", "Dighi", 
    "Dighi Alandi Road", "Domkhel Road", "EON Free Zone", "Erandwane", "Fatima Nagar Wanowrie", 
    "Fursungi", "Gahunje", "Gahunje Road", "Ganeshkhind Road", "Ghole Road", "Ghorpadi", 
    "Ghorpadi Road", "Gultekadi", "Hadapsar", "Hadapsar Industrial Estate", "Hadapsar Road", 
    "Handewadi", "Handewadi Road", "Hills and Dales", "Hinjawadi", "Hinjawadi Wakad Road", 
    "Hinjwadi Rajiv Gandhi Infotech Park", "ITI Road", "Joggers Park", "Kad Nagar", "Kalyani Nagar", 
    "Karve Nagar", "Karve Road", "Kaspate Wasti", "Katraj", "Katraj Kondhwa Road", "Kavade Mala", 
    "Keshav Nagar Mundhwa", "Kesnanad Road", "Kharadi", "Kharadi Gaon", "Kirkatwadi", "Kiwale", 
    "Kondhwa", "Kondhwa BK", "Kondhwa Main Road", "Koregaon Park", "Koregaon Park Annexe", 
    "Koregaon Park Road", "Kothrud", "Law College Road", "Laxmi Nagar Balewadi", "Lohegaon", 
    "Lohegaon Wagholi Road", "Lokmanya Bal Gangadhar Tilak Road", "Loni Kalbhor", "Lullanagar", 
    "MG Road", "Maan", "Magarpatta", "Magarpatta Road", "Mahalunge", "Maharshi Nagar", "Mamurdi", 
    "Mangaldas Road", "Manjari BK", "Manjari Khurd", "Manjari Road", "Manjri", "Market Yard", 
    "Marunji", "Marunji Road", "Mayur Colony Kothrud", "Model Colony", "Mohamadwadi Settlement", 
    "Mohammed Wadi", "Mohan Nagar Co operative Society", "Moshi", "Moshi Alandi Road", 
    "Mumbai Pune Expressway", "Mundhwa", "NDA Road", "NIBM Annexe Area", "NIBM Road", "Nagar Road", 
    "Nanded", "Narhe", "New DP Road", "New Kalyani Nagar", "Nigdi", "Old Mumbai Pune Highway", 
    "Padmavati Sahakar Nagar Road", "Pan Card Club Road", "Park Street", "Parvati Paytha", "Pashan", 
    "Pashan Sus Road", "Patil Nagar Balewadi", "Patil Nagar Bavdhan", "Paud Road", 
    "Phase 1 Hinjewadi Rajiv Gandhi Infotech Park", "Phase 2 Hinjewadi Rajiv Gandhi Infotech Park", 
    "Phase 3 Hinjewadi Rajiv Gandhi Infotech Park", "Pimple Gurav", "Pimple Nilakh", "Pimple Saudagar", 
    "Pimpri", "Pimpri Chinchwad", "Pirangut", "Pisoli", "Pisoli Road", "Porwal Road", "Prabhat Road", 
    "Punawale", "Pune Bengaluru Highway", "Pune Nashik Highway", "Pune Solapur Highway", 
    "Pune University Road", "Punvale Bazar", "Rahatani", "Rambaug Colony", "Ravet", "Ravet Road", 
    "Sadashiv Peth", "Sadhu Vaswani Road", "Salisbury Park", "Salunkhe Vihar Society", "Sangamvadi", 
    "Saswad Road", "Satara Road", "Senapati Bapat Road", "Shankar Kalat Nagar", "Shankar Sheth Road", 
    "Shewalewadi", "Shirole Road", "Shivajinagar", "Shivane", "Sinhgad Road", "Solapur Road", 
    "Sopan Baug", "Sopan Baug Society", "Spine Road", "Sun City Road", "Sus", "Talegaon Dabhade", 
    "Tathawade Pimpri Chinchwad", "Tathawade Road", "Temghar Lavasa Road", "Thergaon", "Thite Nagar", 
    "Tingre Nagar", "Tulaja Bhawani Nagar", "Ubale Nagar", "Undri", "Vadgaon BK", "Viman Nagar", 
    "Vishal Nagar", "Vishrantwadi", "Wadgaon Sheri", "Wagholi", "Wagholi Road", "Wakad", "Wanowrie", 
    "Wanwadi", "Warje", "Yerawada","oshi Alandi Road"] # Add more locations as needed

# Define the quarters
quarters = ["Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"]

# Define the range of years (from Jan-Mar 2024 to Oct 2030)
years = list(range(2024, 2031))

# CSV file header
csv_header = ["location", "year", "quarter", "avg_price", "max_price", "min_price"]

# Initialize CSV file
with open('price_predictions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)  # Write header row

    # Iterate through locations
    for location in locations:
        # Iterate through years
        for year in years:
            # Build the payload to include all quarters for a specific location and year
            predictions = [{"location": location, "quarter": quarter, "year": year} for quarter in quarters]
            
            payload = {
                "predictions": predictions,
                "city": "Pune",
                "priceType": "all"
            }

            try:
                # Send request to the API
                logging.info(f"Fetching data for {location} - {year}")
                response = requests.post("https://ai-ml-propftx.letsphoenix.com/predict", json=payload)
                
                # Check for successful response
                if response.status_code == 200:
                    data = response.json()

                    # Extract and store prices for each quarter in the year
                    for entry in data:
                        row = [
                            entry["location"],
                            entry["year"],
                            entry["quarter"],
                            entry["avg_price"],
                            entry["max_price"],
                            entry["min_price"]
                        ]
                        writer.writerow(row)  # Write data to CSV
                        logging.info(f"Data saved for {location} - {year} - {entry['quarter']}")

                else:
                    logging.error(f"Failed to fetch data for {location} - {year}: {response.status_code}")
            
            except Exception as e:
                logging.error(f"Error occurred while fetching data for {location} - {year}: {str(e)}")
