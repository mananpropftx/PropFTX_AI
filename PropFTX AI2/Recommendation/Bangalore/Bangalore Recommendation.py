import pandas as pd

def calculate_roi_for_locality(amount_to_invest, current_year, time_period, csv_file_path, risk_level):
    locality_data = pd.read_csv(csv_file_path)
    locality_data['Risk'] = locality_data['Risk'].str.strip().str.lower()
    risk_level = risk_level.lower()
    filtered_data = locality_data[locality_data['Risk'] == risk_level]

    if filtered_data.empty:
        return None, None

    filtered_data['predicted_price'] = pd.to_numeric(filtered_data['predicted_price'], errors='coerce')
    filtered_data['year'] = pd.to_numeric(filtered_data['year'], errors='coerce')

    roi_results = []

    for locality in filtered_data['Locality'].unique():
        locality_data = filtered_data[filtered_data['Locality'] == locality]

        current_data = locality_data[locality_data['year'] == current_year]
        
        if current_data.empty:
            continue

        current_price = current_data['predicted_price'].mean()

        if pd.isna(current_price):
            continue

        area_to_buy = amount_to_invest / current_price

        future_year = current_year + time_period
        future_data = locality_data[locality_data['year'] == future_year]

        future_price = future_data['predicted_price'].mean()

        if pd.isna(future_price):
            continue

        future_value = area_to_buy * future_price

        roi = ((future_value - amount_to_invest) / amount_to_invest) * 100

        roi_results.append({
            'locality': locality,
            'current_year': current_year,
            'current_price': current_price,
            'area_to_buy': area_to_buy,
            'future_year': future_year,
            'future_price': future_price,
            'future_value': future_value,
            'roi': roi
        })

        print(f"\nCalculating ROI for Locality '{locality}' in {current_year} (current year) and {future_year} (future year):")
       

    roi_df = pd.DataFrame(roi_results)
    if roi_df.empty:
        return None, None

    # Find the best locality with the highest ROI
    best_locality = roi_df.loc[roi_df['roi'].idxmax()]

    return roi_df, best_locality


amount_to_invest = 100000  
current_year = 2025 
time_period = 5 
csv_file_path = "C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Recommendation\\Bangalore\\Bangalore Recommendation Data.csv"  # Path to the CSV file
risk_level = "Moderate" 
roi_df, best_locality = calculate_roi_for_locality(amount_to_invest, current_year, time_period, csv_file_path, risk_level)

if roi_df is not None:
    print(f"\nROI for all localities at risk level '{risk_level}':\n{roi_df}")
    print(f"Best locality for investment at risk level '{risk_level}': Locality '{best_locality['locality']}' in {best_locality['current_year']} with ROI of {best_locality['roi']:.2f}%")
else:
    print(f"No data found for the risk level '{risk_level}'.")
