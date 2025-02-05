from geopy.geocoders import Nominatim
import csv

geolocator = Nominatim(user_agent="propftx")

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



# Prepare a list to store the geocoded information
location_data = []

# Open a CSV file to write the data
with open('geocoded_locations.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Location', 'Latitude', 'Longitude'])
    
    # Loop through the array and geocode each location
    for location in locations:
        print(f"Geocoding location: {location}...")
        location_info = geolocator.geocode(location)
        
        if location_info:
            print(f"Found coordinates for {location}: Latitude = {location_info.latitude}, Longitude = {location_info.longitude}")
            # Save the geocoded data in the location_data list
            location_data.append((location, location_info.latitude, location_info.longitude))
            # Write the data to the CSV
            writer.writerow([location, location_info.latitude, location_info.longitude])
        else:
            print(f"Could not find coordinates for {location}")
            # Save a None value for unavailable coordinates
            location_data.append((location, None, None))
            # Write the data with None values to the CSV
            writer.writerow([location, None, None])

print("\nGeocoding completed. Data saved to 'geocoded_locations.csv'.")
