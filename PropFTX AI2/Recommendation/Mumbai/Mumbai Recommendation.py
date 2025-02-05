import pandas as pd

def calculate_roi_for_locality(amount_to_invest, time_period, csv_file_path, risk_level):
    locality_data = pd.read_csv(csv_file_path)

    print("Unique values in 'Risk' column:", locality_data['Risk'].unique())
    
    locality_data['Risk'] = locality_data['Risk'].str.strip().str.lower()

    risk_level = risk_level.lower()

    filtered_data = locality_data[locality_data['Risk'] == risk_level]

    if filtered_data.empty:
        return None, None

    filtered_data['predicted_price'] = pd.to_numeric(filtered_data['predicted_price'], errors='coerce')
    filtered_data['year'] = pd.to_numeric(filtered_data['year'], errors='coerce')

    roi_results = []

    for year in sorted(filtered_data['year'].dropna().unique()):
        current_data = filtered_data[filtered_data['year'] == year]
        current_price = current_data['predicted_price'].iloc[-1]

        if pd.isna(current_price):
            continue

        area_to_buy = amount_to_invest / current_price

        future_year = year + time_period
        future_data = filtered_data[filtered_data['year'] == future_year]

        if future_data.empty:
            continue

        future_price = future_data['predicted_price'].iloc[-1]

        if pd.isna(future_price):
            continue

        future_value = area_to_buy * future_price

        roi = ((future_value - amount_to_invest) / amount_to_invest) * 100

        roi_results.append({
            'year': year,
            'current_price': current_price,
            'area_to_buy': area_to_buy,
            'future_value': future_value,
            'roi': roi
        })

    roi_df = pd.DataFrame(roi_results)

    if roi_df.empty:
        return None, None

    best_locality = roi_df.loc[roi_df['roi'].idxmax()]

    return roi_df, best_locality


amount_to_invest = 100000  
time_period = 5
csv_file_path = "c:\\Users\\Administrator\\Downloads\\Mumbai Recommendation System Data.csv"  
risk_level = "Moderate"  
roi_df, best_locality = calculate_roi_for_locality(amount_to_invest, time_period, csv_file_path, risk_level)

if roi_df is not None:
    print(f"ROI for all quarters for risk level '{risk_level}':\n{roi_df}")
    print(f"Best locality for investment at risk level '{risk_level}': Year {best_locality['year']} with ROI of {best_locality['roi']}%")
else:
    print(f"No data found for the risk level '{risk_level}'.")
