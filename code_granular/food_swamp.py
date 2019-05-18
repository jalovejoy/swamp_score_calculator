#################### Importing Libraries ####################
import googlemaps
import time
from datetime import datetime
import pandas as pd
import regex as re

#################### Defining Functions ####################

## Takes in a list of addresses and outputs the distnance matrix between each address and all the fast food, convenience
## and grocery stores nearby
## PARAMETERS: Search Radius, List of Nearby Businesses
def run_address_list(address_list):
    master_df = pd.DataFrame()
    for address in address_list:
        print("\nSearching for locations at: " + address)
        address_df = pd.DataFrame()
        state = (re.search('(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]'
                                '|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])', address).group(0))

        ## Google Geocode API to convert address into latitude and longitude coordinates
        address_geo = gmaps.geocode(address)
        address_lat_lng = [address_geo[0]['geometry']['location']['lat'], address_geo[0]['geometry']['location']['lng']]
        
        ## Running the search for nearby fast food locations
        print("\nSearching fast food locations...")
        fast_food_locations = find_nearby_businesses(address_lat_lng, search_radius, fast_food_restaurants, label="fast_food_rest")

        ## Running the search for nearby convenience stores
        print("\nSearching convenience store locations...")
        conv_store_locations = find_nearby_businesses(address_lat_lng, search_radius, conv_store_list, label="conv_store")

        ## Running the search for nearby grocery stores
        print("\nSearching grocery store locations...")
        groc_store_locations = find_nearby_businesses(address_lat_lng, search_radius, groc_store, label="groc_store")

        ## Combining Datasets
        address_df = pd.concat([fast_food_locations, conv_store_locations, groc_store_locations])

        ## Runs code to collect distance matrix from start address to each busness address
        print(f"\nProcessing distabce matrix for: " + address)
        address_df = google_distances(address, address_df['end_address'], address_df)

        master_df = pd.concat([master_df, address_df])
    
    return master_df

# Identifies places within a given radius of the latititude and longitude of a given address that match the name in a given list of places.
## Creates dataframe for all places that match the name of an input LIST with a given radius of a given lat/lng
def find_nearby_businesses(lat_long_string, radius, business_list, label):
    df = pd.DataFrame()
    for business in business_list:
        print(f"Finding {business} locations...")
        df = find_businesses(df, business, lat_long_string, radius, label)
    return df

## Finds all the places that match a SINGLE given name within a given radius of a given lat/lng
def find_businesses(df, business, lat_long_string, radius, label):
    data = pull_business_json(business, lat_long_string, radius, page_token=None) # Gets JSON data from Google Places API
    
    df = build_business_df(df, data, business, label) # Adds to dataframe
    page_token = data.get('next_page_token', None) # Sets page_token if there were more than 20 places
    time.sleep(2) # Rate limiting to keep API happy
    
    # Iterates over pages for a given location
    while page_token != None: 
        data = pull_business_json(business, lat_long_string, radius, page_token)
        df = build_business_df(df, data, business, label)
        page_token = data.get('next_page_token', None)
        time.sleep(2)
    return df

## Pulls json from Google Places API (limited to 20) for given place, lat/lng, radius
def pull_business_json(business, lat_long_string, radius, page_token=None):
    data = gmaps.places(query=business,
                     location=lat_long_string,
                     radius=radius,
                     page_token=page_token,
                     type=['restaurant','cafe', 'convenience_store', 'food', 'supermarket'])
    return data

## Adds places data to a dataframe
def build_business_df(df, data, business, label):
    for r in data['results']:
        index = df.shape[0]
        df.loc[index, 'business_name'] = r['name']
        df.loc[index, 'target_name'] = business
        df.loc[index, 'label'] = label
        df.loc[index, 'business_types'] = ", ".join(r['types'])
        df.loc[index, 'google_place_id'] = r['place_id']
        try:
            df.loc[index, 'rating'] = r['rating']
            df.loc[index, 'user_ratings_total'] = r['user_ratings_total']
        except:
            df.loc[index, 'rating'] = 'no_rating'
            df.loc[index, 'user_ratings_total'] = 'no_rating'
        df.loc[index, 'end_address'] = r['formatted_address']
        df.loc[index, 'latitude'] = r['geometry']['location']['lat']
        df.loc[index, 'longitude'] = r['geometry']['location']['lng']
        df.loc[index, 'pull_date'] = datetime.now().strftime('%Y-%m-%d')
    return df

## Calculating Distance from Starting Address
def google_distances(start_address, end_addresses, df):
    
    ## Filling in rows using enumerate as the index, so it's important to reset index
    df.reset_index(inplace=True, drop=True)
    
    ## Iterating through each of the addresses
    for i, end_address in enumerate(end_addresses):
        try:
            distance_dict = gmaps.distance_matrix(origins=start_address, destinations = end_address)
            df.loc[i, 'duration'] = distance_dict['rows'][0]['elements'][0]['duration']['value']
            df.loc[i,'distance'] = distance_dict['rows'][0]['elements'][0]['distance']['value']
            df.loc[i,'start_address'] = start_address.replace(",","").replace(" ","-")
        
        ## Redundancy to reduce API errors... probably useless
        except:
            try:
                print(f"Distance retrieval failed for {end_address}. Trying again...")
                distance_dict = gmaps.distance_matrix(origins=start_address, destinations = end_address)
                df.loc[i, 'duration'] = distance_dict['rows'][0]['elements'][0]['duration']['value']
                df.loc[i,'distance'] = distance_dict['rows'][0]['elements'][0]['distance']['value']
                df.loc[i,'start_address'] = start_address.replace(",","").replace(" ","-")
            
            ## Creating alert in dataframe if distance failed
            except:
                print(f"Distance retrieval failed for {end_address}...")
                df.loc[i, 'duration'] = "Failed"
                df.loc[i, 'distance'] = "Failed"
                df.loc[i,'start_address'] = start_address.replace(",","").replace(" ","-")
          
        ## Signposting progress
        if i % 100 == 0:
            print(f"Completed distances for {i} of {len(end_addresses)}")
        time.sleep(0.5)

    return df

def organize_business_data(df):
    ## Renames addresses where the country is in its full name rather than the 3 letter code
    df['end_address'] = [address.replace('United States', 'USA') for address in df['end_address']]
    df['end_address'] = [address.replace('Canada', 'CAN') for address in df['end_address']]

    ## Creates a country column
    country = []
    for address in df['end_address']:
        if 'USA' in address:
            country.append('USA')
        elif 'CAN' in address:
            country.append('CAN')
        else:
            country.append('Unidentified')
    df['country'] = country

    ## Drops rows where the country isn't USA or CAN
    df.drop(df[((df['country'] != 'USA') & (df['country'] != 'CAN'))].index, inplace=True)

    ## Drops rows where there is no distance data
    df.drop(df[df['duration'] == 'Failed'].index, inplace=True)

    ## Reset Index
    df.reset_index(inplace=True, drop=True)

    ## Creates a state column
    state = []
    for address in df['end_address']:
        try:
             state.append(re.search('(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]'
                                    '|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])', address).group(0))
        except:
            state.append('Unidentified')
    df['state'] = state

    ## Resets duration and distance to floats
    df['duration'] = df['duration'].astype('float')
    df['distance'] = df['distance'].astype('float')

    ## Reset names as lower case
    df['business_name'] = [biz.lower() for biz in df['business_name']]
    df['target_name'] = [target.lower() for target in df['target_name']]

    return df

## Calculates points for the duration associated with each business address (row)
## There are three points types
## 1) points = a simple 10 minutes (3 points), 20 minute (2 points), 60 minutes (0 points) system
## 2) A linear gradient point systems spanning from 0 - 3600
## 3) An exponential points system spanning from 0 - 46.656
def calculate_points(df):
    for i, row in df.iterrows():
        if row['duration'] < 600:
            df.loc[i, 'proximity'] = 'close'
            df.loc[i, 'points'] = 3
        elif row['duration'] < 1200:
            df.loc[i, 'proximity'] = 'medium'
            df.loc[i, 'points'] = 2
        elif row['duration'] <= 3600:
            df.loc[i, 'proximity'] = 'far'
            df.loc[i, 'points'] = 1
            df.loc[i, 'gradient_points'] = abs(row['duration'] - 3600)
            df.loc[i, 'exp_points'] = (abs(row['duration'] - 3600) **3) / 1_000_000_000
        else:
            df.loc[i, 'proximity'] = 'over_hour'
            df.loc[i, 'points'] = 0
            df.loc[i, 'gradient_points'] = 0
            df.loc[i, 'exp_points'] = 0
    return df

## Calculates a swamp score for each start address based on the points for all associated businesses
def calculate_swamp_score(df):
    iter_address = set(df['start_address'])
    swamp_df = pd.DataFrame()
    for i, i_address in enumerate(iter_address):
        swamp_df.loc[i,'start_address'] = i_address
        swamp_df.loc[i,'state'] = re.search('(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]'
            '|N[CDEHJMVY]|O[HKR]|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])', i_address).group(0)
        
        ## Simple points score
        conv_store_points = df[df['start_address'] == i_address].groupby('label').sum()['points']['conv_store']
        swamp_df.loc[i,'conv_store_points'] = conv_store_points
        
        fast_food_points = df[df['start_address'] == i_address].groupby('label').sum()['points']['fast_food_rest']
        swamp_df.loc[i,'fast_food_points'] = fast_food_points
        
        groc_store_points = df[df['start_address'] == i_address].groupby('label').sum()['points']['groc_store']
        swamp_df.loc[i,'groc_store_points'] = groc_store_points
        
        swamp_df.loc[i, 'swamp_score'] = (conv_store_points + fast_food_points) / groc_store_points
        
        ## Linear gradient score
        conv_store_grad_points = df[df['start_address'] == i_address].groupby('label').sum()['gradient_points']['conv_store']
        swamp_df.loc[i,'conv_store_grad_points'] = conv_store_grad_points
        
        fast_food_grad_points = df[df['start_address'] == i_address].groupby('label').sum()['gradient_points']['fast_food_rest']
        swamp_df.loc[i,'fast_food_grad_points'] = fast_food_grad_points
        
        groc_store_grad_points = df[df['start_address'] == i_address].groupby('label').sum()['gradient_points']['groc_store']
        swamp_df.loc[i,'groc_store_grad_points'] = groc_store_points
        
        swamp_df.loc[i, 'grad_swamp_score'] = (conv_store_grad_points + fast_food_grad_points) / groc_store_grad_points
        
        ## Exponential gradient score
        conv_store_exp_points = df[df['start_address'] == i_address].groupby('label').sum()['exp_points']['conv_store']
        swamp_df.loc[i,'conv_store_exp_points'] = conv_store_exp_points

        fast_food_exp_points = df[df['start_address'] == i_address].groupby('label').sum()['exp_points']['fast_food_rest']
        swamp_df.loc[i,'fast_food_exp_points'] = fast_food_exp_points

        groc_store_exp_points = df[df['start_address'] == i_address].groupby('label').sum()['exp_points']['groc_store']
        swamp_df.loc[i,'groc_store_exp_points'] = groc_store_points

        swamp_df.loc[i, 'exp_swamp_score'] = (conv_store_exp_points + fast_food_exp_points) / groc_store_exp_points
        
    return swamp_df

#################### User Input ####################
## API key input
# google_api_key = input("Google API Key: Needs access to Geolocate API, Places API, Distance Matrix API: ")
google_api_key = "AIzaSyARbUbY2ZBXJIWvEnz43fowdlGIuenqbuc "
gmaps = googlemaps.Client(key=google_api_key)


#################### EDIT THIS PART DEPENDING ON HOW YOU WANT TO INPUT ####################
## User input
address_list = input("ADDRESS LIST separate addresses with '//' ")
address_list =address_list.split("//")
#################### EDIT THIS PART DEPENDING ON HOW YOU WANT TO INPUT ####################

## Default search radius (as the crow flies) for locations
search_radius = input("SEARCH RADIUS (enter for default 3000): ") or 3000

## Default list of fast food restaurants to look for
fast_food_restaurants = ["McDonald's",'Burger King',"Wendy's","Subway","Starbucks","Dunkin Donuts", 
    "Pizza Hut", "KFC", "Domino's", "Baskin-Robbins", "Hunt Brothers Pizza", "Taco Bell", "Hardee's",
    "Papa John's Pizza", "Dairy Queen", "Little Caesars", "Popeyes Louisiana Kitchen", "Jimmy John's",
    "Jack in the Box", "Chick-fil-A", "Chipotle", "Panda Express", "Denny's", "IHOP", "Carl's Jr.",
    "Five Guys", "Waffle House", "Krispy Kreme" "Long John Silver's", "Jersey Mike's Subs",
    "Good Times Burgers & Frozen Custard", "Culver's"]

# fast_food_restaurants = ["McDonald's"] #### FOR TESTING: Set to a smaller search to save API credits

## Default list of convenience stores to look for
conv_store_list = ["7-eleven", "Kum & Go", "Casey’s General Store", "Cumberland Farms", "Express Mart",
    "Stripes Convenience", "Twice Daily", "Thorntons", "Circle K"]

# conv_store_list = ["7-eleven"] #### FOR TESTING: Set to a smaller search to save API credits

## Default list of grocery stores to look for
groc_store = ["Trader Joe's", "Safeway", "Natural Grocers", "King Soopers", "Whole Foods", "Hannaford",
    "Stop & Shop", "Sprouts Farmers Market", "Shaw's Grocery", "Price Chopper", "Wegmans", "Pete’s Fresh Market",
    "Kroger", "Albertsons", "Publix", "Bojangles' Famous Chicken 'n Biscuit", "Arby's", "Krystal",
    "Mother Earth Natural Foods", "The Fresh Market"]

# groc_store = ["Trader Joe's"] #### FOR TESTING: Set to a smaller search to save API credits

#################### Running Code ####################
master_df = run_address_list(address_list)

## Identifies country (USA or CAN) and drops non-USA or -CAN, drops rows without distance data
## Generally organizes dataframe
master_df = organize_business_data(master_df)

## Running the points for the travel duration of each starting location against each business end address
master_df = calculate_points(master_df)

## Calculating the swamp score for each start address
swamp_df = calculate_swamp_score(master_df)



## Exporting data to CSV
csv_name = f"../data/exports/granular/{datetime.now().strftime('%Y-%m-%d-%H%M%S_allData')}.csv"
master_df.to_csv(csv_name, index=False)

## Swamp score data
swamp_csv_name = f"../data/exports/swamp_summary/{datetime.now().strftime('%Y-%m-%d-%H%M%S_swamp')}.csv"
swamp_df.to_csv(swamp_csv_name, index=False)



