# The Efficacy of Food Swamps as a Healthcare Outcomes Predictor

![alt text](https://raw.githubusercontent.com/jalovejoy/swamp_score_calculator/master/images/burger.jpeg)

## Project Summary

The goal of this project is to develop and test a food swamp feature that the [Staple Health](https://staplehealth.io/) platform can use to better predict patient outcome risk, in turn allowing insurers and providers to optimize risk reduction initiatives. The project is broken into four stages. The first two stages operate at the FIPS County level while the latter two focus on food swamps at the address level.
1) Replicating findings from [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/) that identified that food swamps are an effective predictor of obesity rates at the FIPS County level.
2) Using the same control set as the previous study, examine the effect of food swamps on other healthcare outcomes including: diabetes rates, rates of death from strokes, and life expectancy.
3) Develop a tool to determine a food swamp score at the street address level.
4) Examine the efficacy of the street address level food swamp score for predicting healthcare outcomes at the patient level.

## Data Collection
#### County Level Data Collection
For the FIPS County level study (stages 1-2), data are collected from the USDA Food Atlas, USDA Economic Research Service, the Center for Disease Control and Prevention, the American Community Survey, and the 2010 US Census.

| Variable | Level | Definition | Format | Source | Year |
|-------------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------------|-------------------------|
| food_swamp_14 | FIPS County | Defined as (number of fast food restaurants + number of convenience stores / number of grocery stores) | Float | USDA Food Atlas | 2014 |
| food_desert_15 | FIPS County | Percent of population with low income (household income ≤ 200% of the federal poverty threshold) and low access (more than 1 mile from a supermarket/grocery store in an urban area or more than 10 miles in a rural area) | Float | USDA Food Atlas | 2015 |
| recreationFacilities_14 | FIPS County | Number of recreation & fitness facilities | Int | USDA Food Atlas | 2014 |
| povRate_15 | FIPS County | Poverty rate | Float | USDA Food Atlas | 2015 |
| milkSoda_price_ratio_10 | FIPS County | The ratio of (low fat milk price / national average) / (soda price / national average). Used as an indicator of prices for healthy foods / unhealthy options | Float | USDA Food Atlas | 2010 |
| natAmenityIndex | FIPS County | An index based on the physical characteristics of a county area that enhance the location as a place to live. Characteristics include: warm winter, winter sun, temperate summer, low summer humidity, topographic variation, and water area | Int | USDA Economic Research Service | 1999 |
| pct_black | FIPS County | Percent of county population that is Black or African American | Float | American Community Survey | 2017  (5 year estimate) |
| pct_hispanicORlatino | FIPS County | Percent of county population that is Hispanic or Latino | Float | American Community Survey | 2017  (5 year estimate) |
| pct_over65 | FIPS County | Percent of county population that is over 65 years old | Float | American Community Survey | 2017 (5 year estimate) |
| totalArea | FIPS County | Total area of the county in square miles | Int | 2010 U.S. Census | 2010 |
| obesityRate_13 | FIPS County | The rate of obesity rate as defined by percentage of residents with a Body Mass Index (BMI) > 30.0 | Float | USDA Food Atlas | 2013 |
| strokeDeath_rate | FIPS County | The rate of deaths from strokes within a county | Float | CDC | 2014 - 2016 |
| pct_diabetes_13 | FIPS County | Percent of the population with diabetes | Float | CDC | 2013 |
| avgLifeExpec | FIPS County | The average life expectancy of residents | Float | CDC | 2010 |
|  |  |  |  |  |  |

#### Address Level Data Collection
The street address level data (stages 3-4) are collected using the [Google Places API](https://developers.google.com/places/web-service/intro) with a search radius of 3000 meters. The distance from the input address to the grocery, fast food, or convenience store business is calculated using the [Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/start). The below diagram provides an overview of the current street level address data collection and processing methodology:

![alt text](https://raw.githubusercontent.com/jalovejoy/swamp_score_calculator/master/images/swamp-score-flow.png)

The script currently searches for the below list of nearby businesses.

| Business Type | Business List |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fast Food Restaurants |  McDonald's, Burger King, Wendy's, Subway, Starbucks, Dunkin Donuts, Pizza Hut, KFC, Domino's, Baskin-Robbins, Hunt Brothers Pizza, Taco Bell, Hardee's, Papa John's Pizza, Dairy Queen, Little Caesars, Popeyes Louisiana Kitchen, Jimmy John's, Jack in the Box, Chick-fil-A, Chipotle, Panda Express, Denny's, IHOP, Carl's Jr., Five Guys, Waffle House, Krispy Kreme, Long John Silver's, Jersey Mike's Subs, Good Times Burgers & Frozen Custard, Culver's |
| Convenience Stores | 7-eleven, Kum & Go, Casey’s General Store, Cumberland Farms, Express Mart, Stripes Convenience, Twice Daily, Thorntons, Circle K |
| Grocery Stores | Trader Joe's, Safeway, Natural Grocers, King Soopers, Whole Foods, Hannaford, Stop & Shop, Sprouts Farmers Market, Shaw's Supermarket, Price Chopper, Wegmans, Pete’s Fresh Market, Kroger, Albertsons, Publix, Bojangles' Famous Chicken 'n Biscuit, Arby's, Krystal, Mother Earth Natural Foods, The Fresh Market |
| | |

Google's Places API also makes intuitive decisions about a user's needs: as an example, a search for "Taco Bell" may also retrieve other Mexican or taco restaurants. While this increases the probability of false positives, a survey of the data revealed that more often Google's intuition collected similar restaurants that could be deemed true positives (ie. it pulls non-mainstream fast food restaurants even when the search if "McDonald's"). Regardless, this meant a de-duplication process was essential to ensure that restaurants were not picked up twice (ie. a "Taco Bell" search picking up "Chipotle" locations and vice versa).

Recognizing that consumers are more likely to shop at a closer location than a further away location, a weighting system was applied to locations within an hour of the starting address (anything more than an hour was not counted). For each starting or input address, the weight of each business location is calculated in 3 ways:

![alt text](https://raw.githubusercontent.com/jalovejoy/swamp_score_calculator/master/images/score-weightings.png)

- Stepwise Points = (# places <10 minutes x 3) + (# places < 20 minutes x 2) + (# places < 60 minutes x 1)
- Linear Points = abs(time to business in seconds - 3600)
- Exponential Points = (abs(time to business in seconds - 3600) ** 3) / 1_000_000_000

The output of this script is a **Swamp Score Summary** CSV that includes the points for each establishment type (Fast Food, Grocery Store, Convenience Store) as well as the composite swamp score for each of the three scoring methodologies.

| Column | Description | Format |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|
| Address | The address input for swamp score calculation | String |
| State | The state in which the address exists | String (Two chars) |
| conv_store_points | The total points calculated for all convenience stores within an hour driving distance of the input location. This variable is provided in 3 formats: stepwise, linear, exponential decay | Float |
| fast_food_points | The total points calculated for all fast food restaurants within an hour driving distance of the input location. This variable is provided in 3 formats: stepwise, linear, exponential decay | Float |
| groc_store_points | The total points calculated for all grocery stores within an hour driving distance of the input location. This variable is provided in 3 formats: stepwise, linear, exponential decay | Float |
| swamp_score | Defined as: (conv_store_points + fast_food_points) / groc_store_points. Again this is provided with stepwise, linear, and exponential decay weightings | Float |
| | | |

The data has been ommitted from this repository but can easily be tested by running the data_collection_location_based.ipynb notebook in /code_granular/.

## Findings & Results

#### County Level Findings
This study does not attempt to optimize a prediction (r<sup>2</sup> score) for obesity but rather intends to identify the efficacy of food swamps as a predictor at a statistically significant (p < 0.001) level. Using the same controls applied in the [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/) study (Food Desert, Recreation Facilities, Natural Amenities, Milk/Soda Price Ratio, % Black, % Hispanic, Poverty Rate, County Size), significant relationships are found between food swamp scores and obesity, diabetes, deaths from strokes, and life expectancy.

The figure below showcases the predictions from this model against the actual obesity rates. The color represents the Natural Amenity Index for that county, a feature which had the second strongest effect on obesity rates.
![alt text](https://raw.githubusercontent.com/jalovejoy/swamp_score_calculator/master/images/predictionsVactual.png)

The absolute value of the standardized coefficients shows that the size of the effect of food swamps was larger than that of the milk / soda price ratio and the % of people over 65 – both of which also showed statistically significant relationships with obesity.

![alt text](https://raw.githubusercontent.com/jalovejoy/swamp_score_calculator/master/images/absCoefficients.png)

Even after controlling for obesity, food swamps maintained a statistically significant correlation to all three healthcare outcomes, albeit with a smaller coefficient. The findings from this stage emphasize the importance of food quality on health and support the idea that a food swamp metric is a valuable healthcare indicator, which has powerful policy and public health implications. The notebooks for these results can be found under /code/.

#### Address Level Findings

Additionally, this project successfully built a tool to calculate food swamp scores at the street address level. [Staple Health](https://staplehealth.io/) is currently testing this tool on HIPAA protected patient data to determine its efficacy as an input in their machine learning models. Results are expected by July 10. The notebooks for these can be found under /code_granular/.

## Limitations & Considerations

This project essentially acts as preliminary research and development into a feature for a larger model predicting a variety of healthcare outcomes. It's possible that while food swamps may be statistically significantly correlated with the healthcare outcomes researched in this project under the controls that [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/) used, the food swamp score may have multicollinearity or may be statistically insignificant when paired with the larger feature set in [Staple Health's](https://staplehealth.io/) current platform.

Another smaller consideration, as addressed in [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/), is that while obesity is the target for part of this project, there are issues with the way that obesity is calculated. Namely, there is debate over whether or not BMI is an accurate way of measuring obesity.