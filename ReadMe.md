# The Efficacy of Food Swamps as a Healthcare Outcomes Predictor

### Project Summary

The goal of this project is to develop and test a food swamp feature that the [Staple Health](https://staplehealth.io/) platform can use to better predict patient risk, in turn allowing insurers and providers to optimize risk reduction initiatives. The project is broken into four stages. The first two stages operate at the FIPS County level while the latter two focus on food swamps at the address level.
1) Replicating findings from [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/) that identified that food swamps are an effective predictor of obesity rates at the FIPS County level.
2) Examine the effect of food swamps on other healthcare outcomes including: diabetes rates, rates of death from strokes, and life expectancy.
3) Develop a tool to determine a food swamp score at the street address level.
4) Examine the efficacy of the street address level food swamp score for predicting healthcare outcomes at the patient level.

### Data Collection
For the FIPS County level study, data is collected from the USDA Food Atlas, USDA Economic Research Service, the Center for Disease Control and Prevention, the American Community Survey, and the 2010 US Census.

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

The street address level data is collected using the [Google Places API](https://developers.google.com/places/web-service/intro) with a search radius of 3000 meters. The distance from the input address to the grocery, fast food, or convenience store business is calculated using the [Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/start). The below diagram provides an effective overview of the current street level address data collection and processing methodology:

![alt text](https://raw.git.generalassemb.ly/JamesLovejoy-DEN/project_6/master/images/swamp-score-flow.png)

The collected data is stored in the following CSVs:
- Address Level Swamp Score: CSV of businesses gathered against starting address, their distance to the start address, & associated swamp score
- Business Locations: De-duplicated CSV of all Businesses by Type retrieved from all start addresses
- Address Master: Master CSV of all start addresses and their associated swamp scores

The data has been ommitted from this repository but can easily be collected by running the data_collection_location_based.ipynb notebook in /code_granular/.

### Findings & Results

This study does not attempt to optimize a prediction (r<sup>2</sup> score) for obesity but rather intends to identify the efficacy of food swamps as a predictor at a statistically significant (p < 0.001) level. Using the same controls applied in the [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/) study (Food Desert, Recreation Facilities, Natural Amenities, Milk/Soda Price Ratio, % Black, % Hispanic, Poverty Rate, County Size), significant relationships are found between food swamp scores and obesity, diabetes, deaths from strokes, and life expectancy. The findings from this stage emphasize the importance of food quality on health and support the idea that a food swamp metric is a valuable healthcare indicator. The notebooks for these results can be found under /code/.

Additionally, this project successfully built a tool to calculate food swamp scores at the street address level. As of 2019-05-16 data on over 15,000 businesses (fast food restaurants, convenience stores, grocery stores) have been collected and food swamp scores have been calculated for 18 addresses. [Staple Health](https://staplehealth.io/) is currently testing this tool on HIPAA protected patient data to determine its efficacy as an input in their machine learning models. Results are expected by June 10. The notebooks for these can be found under code/granular/.

### Limitations & Considerations

This project essentially acts as preliminary research and development into a feature for a larger model predicting a variety of healthcare outcomes. It's possible that while food swamps may be statistically significantly correlated with the healthcare outcomes researched in this project under the controls that [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/) used, the food swamp score may have multicollinearity or may be statistically insignificant when paired with the larger feature set in [Staple Health](https://staplehealth.io/) current platform.

A smaller considerations, as addressed in [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/), is that while obesity is the target for part of this project, there are issues with the way that obesity is calculated. Namely, there is debate over whether or not BMI is an accurate way of measuring obesity.