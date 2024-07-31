Rotating Cookie Menu
This script generates a weekly rotating cookie menu for a year. It ensures a balance of different doughs, colors, 
themes, and aligns with seasonal/holiday associations. It includes the Crave (Milk) Chocolate Chip Cookie every week, 
ensures one top 15 cookie each week, includes at least one but not more than two chilled cookies, and minimizes the repetition of 
cookies within any 20-week timeframe. Additionally, the average price for the 6 cookies is kept below $0.80, and the average 
preparation level is no higher than medium.

Prerequisites
Python 3.x
pandas
numpy

Usage
Save your CSV file with the cookie data to a known location on your computer.

Update the file path in the script to point to your CSV file.

Run the script to generate the rotating menu.

Example CSV File
The CSV file should have the following columns:

Cookie Name: The name of the cookie.
Price: The price of the cookie (in dollars).
Ranking: The ranking of the cookie (top 15 should be considered).
Temperature: The serving temperature of the cookie (e.g., Chilled).

Output
The script will print the first and last few weeks of the rotating menu. Each week will have a list of 6 cookies meeting the specified constraints.
