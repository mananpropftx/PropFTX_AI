import matplotlib.pyplot as plt
import pandas as pd

data = [
    {"avg_price": 6028.399999999995, "location": "Bandlaguda Jagir", "max_price": 7394.087170405021, "min_price": 4853.845471544242, "quarter": "Jan-Mar", "year": 2024},
    {"avg_price": 5997.109999999996, "location": "Bandlaguda Jagir", "max_price": 7355.7086640746575, "min_price": 4828.651916902113, "quarter": "Apr-Jun", "year": 2024},
    {"avg_price": 6020.549999999998, "location": "Bandlaguda Jagir", "max_price": 7384.45881391115, "min_price": 4847.5249408973705, "quarter": "Jul-Sep", "year": 2024},
    {"avg_price": 6101.490000000008, "location": "Bandlaguda Jagir", "max_price": 7483.735141887504, "min_price": 4912.694845427069, "quarter": "Oct-Dec", "year": 2024},
    {"avg_price": 3218.4999999999977, "location": "Bandlaguda Jagir", "max_price": 3947.6261624889794, "min_price": 2591.417565218822, "quarter": "Jan-Mar", "year": 2025},
    {"avg_price": 3166.9999999999973, "location": "Bandlaguda Jagir", "max_price": 3884.459237720241, "min_price": 2549.9516635227615, "quarter": "Apr-Jun", "year": 2025},
    {"avg_price": 3250.499999999997, "location": "Bandlaguda Jagir", "max_price": 3986.875513801592, "min_price": 2617.1827856901596, "quarter": "Jul-Sep", "year": 2025},
    {"avg_price": 3439.099999999997, "location": "Bandlaguda Jagir", "max_price": 4218.20137810031, "min_price": 2769.03655384311, "quarter": "Oct-Dec", "year": 2025},
    {"avg_price": 6028.399999999995, "location": "Bandlaguda Jagir", "max_price": 7394.087170405021, "min_price": 4853.845471544242, "quarter": "Jan-Mar", "year": 2026},
    {"avg_price": 5997.109999999996, "location": "Bandlaguda Jagir", "max_price": 7355.7086640746575, "min_price": 4828.651916902113, "quarter": "Apr-Jun", "year": 2026},
    {"avg_price": 6020.549999999998, "location": "Bandlaguda Jagir", "max_price": 7384.45881391115, "min_price": 4847.5249408973705, "quarter": "Jul-Sep", "year": 2026},
    {"avg_price": 6101.490000000008, "location": "Bandlaguda Jagir", "max_price": 7483.735141887504, "min_price": 4912.694845427069, "quarter": "Oct-Dec", "year": 2026},
    {"avg_price": 6028.399999999995, "location": "Bandlaguda Jagir", "max_price": 7394.087170405021, "min_price": 4853.845471544242, "quarter": "Jan-Mar", "year": 2027},
    {"avg_price": 5997.109999999996, "location": "Bandlaguda Jagir", "max_price": 7355.7086640746575, "min_price": 4828.651916902113, "quarter": "Apr-Jun", "year": 2027},
    {"avg_price": 6020.549999999998, "location": "Bandlaguda Jagir", "max_price": 7384.45881391115, "min_price": 4847.5249408973705, "quarter": "Jul-Sep", "year": 2027},
    {"avg_price": 6101.490000000008, "location": "Bandlaguda Jagir", "max_price": 7483.735141887504, "min_price": 4912.694845427069, "quarter": "Oct-Dec", "year": 2027},
    {"avg_price": 3218.4999999999977, "location": "Bandlaguda Jagir", "max_price": 3947.6261624889794, "min_price": 2591.417565218822, "quarter": "Jan-Mar", "year": 2028},
    {"avg_price": 3166.9999999999973, "location": "Bandlaguda Jagir", "max_price": 3884.459237720241, "min_price": 2549.9516635227615, "quarter": "Apr-Jun", "year": 2028},
    {"avg_price": 3250.499999999997, "location": "Bandlaguda Jagir", "max_price": 3986.875513801592, "min_price": 2617.1827856901596, "quarter": "Jul-Sep", "year": 2028},
    {"avg_price": 3439.099999999997, "location": "Bandlaguda Jagir", "max_price": 4218.20137810031, "min_price": 2769.03655384311, "quarter": "Oct-Dec", "year": 2028},
    {"avg_price": 6028.399999999995, "location": "Bandlaguda Jagir", "max_price": 7394.087170405021, "min_price": 4853.845471544242, "quarter": "Jan-Mar", "year": 2029},
    {"avg_price": 5997.109999999996, "location": "Bandlaguda Jagir", "max_price": 7355.7086640746575, "min_price": 4828.651916902113, "quarter": "Apr-Jun", "year": 2029},
    {"avg_price": 6020.549999999998, "location": "Bandlaguda Jagir", "max_price": 7384.45881391115, "min_price": 4847.5249408973705, "quarter": "Jul-Sep", "year": 2029},
    {"avg_price": 6101.490000000008, "location": "Bandlaguda Jagir", "max_price": 7483.735141887504, "min_price": 4912.694845427069, "quarter": "Oct-Dec", "year": 2029},
    {"avg_price": 6028.399999999995, "location": "Bandlaguda Jagir", "max_price": 7394.087170405021, "min_price": 4853.845471544242, "quarter": "Jan-Mar", "year": 2030},
    {"avg_price": 5997.109999999996, "location": "Bandlaguda Jagir", "max_price": 7355.7086640746575, "min_price": 4828.651916902113, "quarter": "Apr-Jun", "year": 2030},
    {"avg_price": 6020.549999999998, "location": "Bandlaguda Jagir", "max_price": 7384.45881391115, "min_price": 4847.5249408973705, "quarter": "Jul-Sep", "year": 2030},
    {"avg_price": 6101.490000000008, "location": "Bandlaguda Jagir", "max_price": 7483.735141887504, "min_price": 4912.694845427069, "quarter": "Oct-Dec", "year": 2030}
]

quarters = [f"{entry['quarter']} {entry['year']}" for entry in data]
avg_prices = [entry['avg_price'] for entry in data]

df = pd.DataFrame({
    'Quarter': quarters,
    'Avg Price': avg_prices
})

plt.figure(figsize=(12, 6))
plt.plot(df['Quarter'], df['Avg Price'], marker='o', linestyle='-', color='b', label='Avg Price')
plt.xticks(rotation=90)
plt.xlabel('Quarter')
plt.ylabel('Price')
plt.title('Average Price Over Quarters (2024 - 2030)')
plt.grid(True)
plt.tight_layout()
plt.show()
