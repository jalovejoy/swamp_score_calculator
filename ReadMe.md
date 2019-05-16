# The Efficacy of Food Swamps as a Healthcare Outcomes Predictor

### Executive Summary
The goal of this project is to develop and test a food swamp feature that the [Staple Health](https://staplehealth.io/) platform can use to better predict patient risk, in turn allowing insurers and providers to optimize risk reduction initiatives. The project is broken into four stagesL
1) Replicating findings from [Cooksey-Stowers et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708005/) that identified that food swamps are an effective predictor of obesity rates at the FIPS County level.
2) Examine the effect of food swamps on other healthcare outcomes including: diabetes rates, rates of death from strokes, and life expectancy.
3) Develop a tool to determine a food swamp score at the street address level
4) Examine the efficacy of the street address level food swamp score for predicting healthcare outcomes at the patient level
Data was collected


### Data Dictionary
| Variable | Level | Definition | Format | Source | Year |
|-------------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------------|-------------------------|
| food_swamp_14 | FIPS County | Defined as (number of fast food restaurants + number of convenience stores / number of grocery stores) | Float | USDA Food Atlas | 2014 |
| food_desert_15 | FIPS County | Percent of population with low income (household income ≤ 200% of the federal poverty threshold) and low access (more than 1 mile from a supermarket/grocery store in an urban area or more than 10 miles in a rural area) | Float | USDA Food Atlas | 2015 |
| recreationFacilities_14 | FIPS County | Number of recreation & fitness facilities | Int | USDA Food Atlas | 2014 |
| povRate_15 | FIPS County | Poverty rate | Float | USDA Food Atlas | 2015 |
| milkSoda_price_ratio_10 | FIPS County | The ratio of (low fat milk price / national average) / (soda price / national average). Used as an indicator of prices for healthy foods / unhealthy options | Float | USDA Food Atlas | 2010 |
| natAmenityIndex | FIPS County | An index based on the physical characteristics of a county area that enhance the location as a place to live. Characteristics include: warm winter, winter sun, temperate summer, low summer humidity, topographic variation, and water area | Int | USDA Natural Amenities Scale | 1999 |
| pct_black | FIPS County | Percent of county population that is Black or African American | Float | American Community Survey | 2017  (5 year estimate) |
| pct_hispanicORlatino | FIPS County | Percent of county population that is Hispanic or Latino | Float | American Community Survey | 2017  (5 year estimate) |
| pct_over65 | FIPS County | Percent of county population that is over 65 years old | Float | American Community Survey | 2017 (5 year estimate) |
| totalArea | FIPS County | Total area of the county in square miles | Int | 2010 U.S. Census | 2010 |
|  |  |  |  |  |  |