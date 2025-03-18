from geopy.geocoders import Nominatim
import csv

geolocator = Nominatim(user_agent="propftx")

locations = ["Alaknanda",
    "Chattarpur",
    "Chattarpur Enclave",
    "Dilshad Garden",
    "Dwarka Mor",
    "GT Karnal Road",
    "Indraprastha",
    "IP Extension",
    "Jamia Nagar",
    "Janakpuri",
    "Jasola",
    "Jasola Vihar",
    "Kakrola",
    "Kalkaji",
    "Loni Road",
    "Mahavir Enclave",
    "Mayur Vihar",
    "Mayur Vihar 1",
    "Mehrauli",
    "Mehrauli Badarpur Road",
    "Munirka",
    "Narwana Road",
    "Nawada",
    "New Rohtak Road",
    "Pandav Nagar",
    "Pankha Road",
    "Paschim Vihar",
    "Patel Road",
    "Patparganj",
    "Pitam Pura",
    "Rajpur Road",
    "Rohini",
    "Saket",
    "Sarita Vihar",
    "Sector 10 Dwarka",
    "Sector 11 Dwarka",
    "Sector 12 Dwarka",
    "Sector 13 Dwarka",
    "Sector 13 Rohini",
    "Sector 14 Rohini",
    "Sector 18 Dwarka",
    "Sector 2 Dwarka",
    "Sector 22 Dwarka",
    "Sector 23 Dwarka",
    "Sector 4 Dwarka",
    "Sector 9 Rohini",
    "Sector B Vasant Kunj",
    "Sector C Vasant Kunj",
    "Sector D Vasant Kunj",
    "Shahdara",
    "Uttam Nagar",
    "Uttam Nagar West",
    "Vasant Kunj",
    "Vasundhara Enclave",
    "Vikas Marg",
    "Vikaspuri",
    "Vipin Garden"]


location_data = []

with open('geocoded_locations.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Location', 'Latitude', 'Longitude'])
    
    for location in locations:
        print(f"Geocoding location: {location}...")
        location_info = geolocator.geocode(location)
        
        if location_info:
            print(f"Found coordinates for {location}: Latitude = {location_info.latitude}, Longitude = {location_info.longitude}")
            location_data.append((location, location_info.latitude, location_info.longitude))
            writer.writerow([location, location_info.latitude, location_info.longitude])
        else:
            print(f"Could not find coordinates for {location}")
            location_data.append((location, None, None))
            writer.writerow([location, None, None])

print("\nGeocoding completed. Data saved to 'delhi_geocoded_locations.csv'.")
