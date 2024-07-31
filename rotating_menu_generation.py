import numpy as np
import pandas as pd


#############
# LOAD DATA #
#############

file_path = "./Costs & Profitability - Cookie Tracking.csv"
data = pd.read_csv(file_path)


##############
# CLEAN DATA #
##############


def clean_price(price: str | float) -> float:
    "Replace dollar signs and commas and convert to float. Return 0 if invalid."

    if isinstance(price, str):
        price = price.replace("$", "").replace(",", "")

    try:
        return float(price)

    except ValueError:
        return 0


data["Price"] = data["Price"].apply(clean_price)


#############
# PREP DATA #
#############

# Initialize values to track weekly cookie menus through the year
weeks = 52
weekly_cookie_menus = []
cookie_usage = pd.DataFrame(data={"Week": [], "Cookie Name": []})

# Get the top 15 cookies (not including 'Crave (Milk) Chocolate Chip Cookie')
top_15_cookies = data[data["Top 15"] == "Yes"]["Cookie Name"].tolist()
top_15_cookies.remove("Crave (Milk) Chocolate Chip Cookie")

# Get the list of chilled cookies
chilled_cookies = data[data["Serve Temp"] == "Chilled"]["Cookie Name"].tolist()

for week in range(1, weeks + 1):
    "For each week, generate a menu with 6 cookies"

    ###################
    # COOKIES 1 and 2 #
    # Top 15          #
    ###################

    # Start with 'Crave (Milk) Chocolate Chip Cookie'
    weekly_cookie_menu = ["Crave (Milk) Chocolate Chip Cookie"]

    # Ensure there is always one top 15 cookie other than 'Crave (Milk) Chocolate Chip Cookie'
    weekly_cookie_menu.extend(
        np.random.choice(top_15_cookies, 1, replace=False).tolist()
    )

    ###########################
    # COOKIES 3 (and maybe 4) #
    # Chilled Cookies         #
    ###########################

    # Ensure at least one but not more than two chilled cookies
    chilled_sample = data[
        (data["Serve Temp"] == "Chilled")
        & (~data["Cookie Name"].isin(weekly_cookie_menu))
    ]

    num_chilled = np.random.choice([1, 2], p=[0.8, 0.2])

    if len(chilled_sample) >= num_chilled:
        weekly_cookie_menu.extend(
            chilled_sample.sample(num_chilled)["Cookie Name"].tolist()
        )

    ####################
    # COOKIES 4/5 to 6 #
    # Meet Constraints #
    ####################

    # Pick cookies not already picked for this week
    not_in_weekly_cookies = ~data["Cookie Name"].isin(weekly_cookie_menu)

    # Pick cookies not already picked in the past 20 weeks
    not_in_past_20_weeks = ~data["Cookie Name"].isin(
        cookie_usage[cookie_usage["Week"] >= week - 20]["Cookie Name"].tolist()
    )

    # Pick cookies below $0.80
    not_above_80_cents = data["Price"] < 0.8

    # Fill the weekly cookie menu with cookies that meet the constraints
    filtered_data = data[
        not_in_weekly_cookies & not_in_past_20_weeks & not_above_80_cents
    ]

    remaining_cookies_needed = 6 - len(weekly_cookie_menu)

    if len(filtered_data) >= remaining_cookies_needed:
        remaining_cookies = filtered_data.sample(remaining_cookies_needed)[
            "Cookie Name"
        ].tolist()

        weekly_cookie_menu.extend(remaining_cookies)

    # Ensure the final list has 6 cookies
    if len(weekly_cookie_menu) < 6:
        additional_cookies = (
            data[(~data["Cookie Name"].isin(weekly_cookie_menu))]
            .sample(6 - len(weekly_cookie_menu))["Cookie Name"]
            .tolist()
        )
        weekly_cookie_menu.extend(additional_cookies)

    ####################
    # SAVE COOKIE MENU #
    ####################

    weekly_cookie_menus.append({"Week": week, "Cookies": weekly_cookie_menu})

    # Track cookie usage
    for cookie in weekly_cookie_menu:
        cookie_usage = pd.concat(
            [cookie_usage, pd.DataFrame([{"Week": week, "Cookie Name": cookie}])],
            ignore_index=True,
        )


#############
# SAVE DATA #
#############

menus_df = pd.DataFrame(weekly_cookie_menus)
menus_df.to_csv("Weekly Cookie Menus.csv", index=False)
cookie_usage.to_csv("Cookie Usage.csv", index=False)
