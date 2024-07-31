import numpy as np
import pandas as pd

# Load the CSV file
file_path = '/mnt/data/Costs & Profitability - Cookie Tracking.csv'
data = pd.read_csv(file_path)

# Replace dollar signs and commas and convert to float
data['Price'] = data['Price'].replace(r'[\$,]', '', regex=True).astype(float)

# Display the first few rows of the data to ensure it is loaded correctly
data.head()

# Initialize some variables
weeks = 52
weekly_menu = []
cookie_usage = pd.DataFrame(columns=['Week', 'Cookie Name'])

# Example initial setup (adapt to your needs)
top_15_cookies = data[data['Ranking'] <= 15]['Cookie Name'].tolist()
chilled_cookies = data[data['Temperature'] == 'Chilled']['Cookie Name'].tolist()

for week in range(1, weeks + 1):
    weekly_cookies = ['Crave (Milk) Chocolate Chip Cookie']
    
    # Ensure there is always one top 15 cookie other than 'Crave (Milk) Chocolate Chip Cookie'
    top_15_other = data[(data['Ranking'] <= 15) & (data['Cookie Name'] != 'Crave (Milk) Chocolate Chip Cookie')]

    if not top_15_other.empty:
        top_15_other_sample = top_15_other.sample(1)
        weekly_cookies.extend(top_15_other_sample['Cookie Name'].tolist())
    
    # Ensure at least one but not more than two chilled cookies
    chilled_sample = data[(data['Temperature'] == 'Chilled') & (~data['Cookie Name'].isin(weekly_cookies))]
    num_chilled = np.random.choice([1, 2], p=[0.8, 0.2])
    
    if len(chilled_sample) >= num_chilled:
        weekly_cookies.extend(chilled_sample.sample(num_chilled)['Cookie Name'].tolist())
    
    # Select remaining cookies ensuring average price and prep level constraints
    remaining_cookies_needed = 6 - len(weekly_cookies)
    filtered_data = data[
        (~data['Cookie Name'].isin(weekly_cookies)) &
        (~data['Cookie Name'].isin(cookie_usage[cookie_usage['Week'] >= week - 20]['Cookie Name'])) &
        (data['Price'] < 0.8)
    ]
    
    if len(filtered_data) >= remaining_cookies_needed:
        remaining_cookies = filtered_data.sample(remaining_cookies_needed)['Cookie Name'].tolist()
        weekly_cookies.extend(remaining_cookies)
    
    # Ensure the final list has 6 cookies
    if len(weekly_cookies) < 6:
        additional_cookies = data[
            (~data['Cookie Name'].isin(weekly_cookies))
        ].sample(6 - len(weekly_cookies))['Cookie Name'].tolist()
        weekly_cookies.extend(additional_cookies)
    
    # Store the week's menu
    weekly_menu.append({
        'Week': week,
        'Cookies': weekly_cookies
    })
    
    # Track cookie usage
    for cookie in weekly_cookies:
        cookie_usage = cookie_usage.append({'Week': week, 'Cookie Name': cookie}, ignore_index=True)

# Convert weekly menu to DataFrame for better visualization
weekly_menu_df = pd.DataFrame(weekly_menu)

# Print the first few weeks of the rotating menu
weekly_menu_df.head(), weekly_menu_df.tail()