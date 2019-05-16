# The Efficacy of Food Swamps as a Healthcare Outcomes Predictor

### Executive Summary

The goal of this project is to develop and test a food swamp feature that the [Staple Health](https://staplehealth.io/) platform can use to better predict patient risk, in turn allowing insurers and providers to optimize risk reduction initiatives. The project is broken into four stages. The first two stages operate at the FIPS County level while the latter two focus on food swamps at the address level.
1) Replicating findings from [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/) that identified that food swamps are an effective predictor of obesity rates at the FIPS County level.
2) Examine the effect of food swamps on other healthcare outcomes including: diabetes rates, rates of death from strokes, and life expectancy.
3) Develop a tool to determine a food swamp score at the street address level.
4) Examine the efficacy of the street address level food swamp score for predicting healthcare outcomes at the patient level.

For the FIPS County level study, data is collected from the USDA Food Atlas, USDA Economic Research Service, the Center for Disease Control and Prevention, the American Community Survey, and the 2010 US Census. The street address level data is collected using the [Google Places API](https://developers.google.com/places/web-service/intro).

This study does not attempt to optimize a prediction (r<sup>2</sup> score) for obesity but rather intends to identify the efficacy of food swamps as a predictor at a statistically significant (p < 0.001) level. Using the same controls applied in the [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/) study (Food Desert, Recreation Facilities, Natural Amenities, Milk/Soda Price Ratio, % Black, % Hispanic, Poverty Rate, County Size), significant relationships are found between food swamp scores and obesity, diabetes, deaths from strokes, and life expectancy. The findings from this stage emphasize the importance of food quality on health and support the idea that a food swamp metric is a valuable healthcare indicator. The notebooks for these results can be found under code/.

Additionally, this project successfully built a tool to calculate food swamp scores at the street address level. As of 2019-05-16 data on over 15,000 businesses (fast food restaurants, convenience stores, grocery stores) have been collected. [Staple Health](https://staplehealth.io/) is currently testing this tool on HIPAA protected patient data to determine its efficacy as an input in their machine learning models. Results are expected by June 10. The notebooks for these can be found under code/granular/.

### Data Dictionary
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
|  |  |  |  |  |  |