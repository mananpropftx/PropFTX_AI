import requests
import csv
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

locations = [
    "100 Feet Ring Road",
    "Aga Abbas Ali Road",
    "Akshayanagar",
    "Amrutahalli",
    "Amruthahalli Main Road",
    "Anekal Main Road",
    "AnjanaPura",
    "Arekere",
    "Attibele",
    "Avalahalli",
    "Banashankari",
    "Banaswadi",
    "Bangalore University Road",
    "Bannerghatta Main Road",
    "Bannerughatta",
    "Basavanagudi",
    "Begur Koppa Road",
    "Begur Road",
    "Belathur Main Road",
    "Bellandur",
    "Bellary Road",
    "Benson Town",
    "Binny Pete",
    "Block 1st Koramangala",
    "Bommanahalli",
    "Bommasandra Jigani Link Road",
    "Borewell Road",
    "Brookefield",
    "BTM Layout",
    "Budigere",
    "Byatarayanapura",
    "Cambridge Road",
    "Carmelaram",
    "Chandapura",
    "Chandapura Anekal Road",
    "Channasandra",
    "Channasandra Main road",
    "Chokkanahalli",
    "Chunchgatta Main Road",
    "Church Street",
    "Coles Road",
    "Commissariat Road",
    "Cooke Town",
    "Cunningham Road",
    "CV Raman Nagar",
    "Devanahalli",
    "Doddaballapur Main Road",
    "Doddakannelli",
    "Doddakannelli Chikkanayakana Halli Road",
    "Dr Rajkumar Road",
    "ECC Road",
    "Electronic City",
    "Gear School Road",
    "GKVK Road",
    "Gottigere",
    "Gubbalala",
    "Gubbalala Main Road",
    "Gunjur",
    "Hadosiddapura",
    "Hagadur Main Road",
    "HAL Old Airport Road",
    "Halasuru",
    "Haralur Main Road",
    "Hebbal",
    "Hebbal Kempapura",
    "Hennur Gardens",
    "Hennur Main Road",
    "Hoodi",
    "Horamavu",
    "Horamavu Agara",
    "Hormavu Agara",
    "Hosa Road",
    "Hosabasavanapura",
    "Hoskote Chintamani Road",
    "Hosur Road",
    "HSR Layout",
    "Hulimavu",
    "Huskur Road",
    "Hutchins Road",
    "Indiranagar",
    "ITPL",
    "Jakkur",
    "Jakkur Road",
    "Jalahalli",
    "Jayanagar",
    "JCR Layout",
    "JP Nagar",
    "Kadubeesanahalli Road",
    "Kaggadasapura",
    "Kannamangala Main Road",
    "Kasavanahalli",
    "Kathriguppe Main Road",
    "Kempapura Main Road",
    "Kempegowda International Airport Road",
    "Kengeri",
    "Kengeri Satellite Town",
    "Kogilu",
    "Konanakunte",
    "Koramangala",
    "Kothanur",
    "Krishnarajapura",
    "Kudlu Gate",
    "Kumaraswamy Layout",
    "Kundalahalli",
    "Lalbagh Main Road",
    "Magadi Main Road",
    "Mahadevapura",
    "Malleshwaram",
    "Marathahalli",
    "Marathahalli Sarjapur Outer Ring Road",
    "Medahalli Kadugodi Road",
    "Medahalli Main Road",
    "MSR College Road",
    "Mysore Road",
    "Naagarabhaavi",
    "Nagavara",
    "Neotown Road",
    "Nice Ring Road",
    "NRI Layout Main Road",
    "Old Madras Road",
    "OMBR Layout",
    "Outer Ring Road",
    "Panathur",
    "Phase 1 Electronics City",
    "Phase 2 Electronic City",
    "Phase 6 JP nagar",
    "Phase 7 JP Nagar",
    "Phase 8th JP Nagar",
    "Pulikeshi Nagar",
    "Queens Road",
    "Rachenahalli",
    "Rajajinagar",
    "Ramagondanahalli Whitefield",
    "Ramamurthy Nagar",
    "Rashtriya Vidyalaya Road",
    "RK Hegde Nagar",
    "RR Nagar",
    "RT Nagar",
    "Sadarmangala Main Road",
    "Sahakar Nagar",
    "Sampige Road",
    "Sanjay Nagar Main Road",
    "Sanjayanagara",
    "Sankey Road",
    "Sarjapur Road",
    "Sarjapura",
    "Sarjapura Attibele Road",
    "Seegehalli Krishnarajapura",
    "Seegehalli Road",
    "Silver County Road",
    "Singasandra",
    "Somasundarapalya Main Road",
    "Spencer Road",
    "Stage 2 RMV",
    "Stage 3rd Banashankari",
    "State Highway 35",
    "Subramanyapura",
    "Thalaghattapura Main Road",
    "Thanisandra",
    "Thanisandra Main Road",
    "Thimmaiah Road",
    "Thurahalli",
    "Tumkur Road",
    "Uttarahalli Hobli",
    "Uttarahalli Main Road",
    "Vajarahalli",
    "Varthur",
    "Varthur Road",
    "Vidyaranyapura",
    "Vidyaranyapura Main Road",
    "Vijaynagar",
    "Vijaynagar Main Road",
    "Vittal Mallya Road",
    "Viviani Road",
    "Whitefield",
    "Whitefield Main Road",
    "Yelahanka",
    "Yelahanka Airforce Base",
    "Yelahanka New Town",
    "Yeswanthpur"
]
 
quarters = ["Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"]

years = list(range(2024, 2031))

csv_header = ["location", "year", "quarter", "avg_price", "max_price", "min_price"]

with open('Bangalore_recommedation_price_predictions1.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    for location in locations:
        for year in years:
            predictions = [{"location": location, "quarter": quarter, "year": year} for quarter in quarters]
            
            payload = {
                "predictions": predictions,
                "city": "Bangalore",
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
