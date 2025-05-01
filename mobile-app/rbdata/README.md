# rbdata

This is a rebuilt dataset (Rebuilt-Data), with the source file being [SIPRI-Milex-data-1948-2023.xlsx](SIPRI-Milex-data-1948-2023.xlsx).

This large file is more like a report-type dataset. Using it directly for import would inevitably involve many errors, so I manually split the countries by continent and simplified the table data. Data from 1948-2023 will be placed in the rebuild folder and stored by continent (and even by region, as the source file specifically listed the Middle East as a separate section).

## Explanation

- The first column is the country name, and the remaining columns represent the military expenditure ($) of that country for each year from 1948-2023
- "..." means position, indicating that the military expenditure for this country in that year was not recorded, which is NULL. This can be processed by adding data, and in the future, it can be approximated by using the average of records from previous years
- "xx" means not recorded, which can be deleted and processed as NULL or recorded as 0. In future real-time change operations, maintain the data from previous columns without making changes or assignments

## To be continued

## Based on information released from White House with detailed information about the trade between US and the rest of countries.
- You will find the relevant information for each country, including Exports, Imports and Deficit (or surplus).

- Version 2 includes population (if data is available). Figures gathered from https://datahub.io/core/population