from geopy.geocoders import Nominatim
import csv

geolocator = Nominatim(user_agent="propftx")

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
    "Wanwadi", "Warje", "Yerawada","oshi Alandi Road"]


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

print("\nGeocoding completed. Data saved to 'pune_geocoded_locations.csv'.")
