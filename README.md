# Yoox-Sale-Scraper
Website scraper for the website of international retailer Yoox. Searches for any brands supported by Yoox and finds all items that are on sale. 

# Features
- Search the Yoox site for all items of any Yoox supported brands. 
- Find all items on sale based on the given desired discount. Users can change how much of a discount they want to search for, whether that's 50% off or 90% off.
- Scraper will continously run every few minutes. Default is every 5 minutes.
- Whenever new items are discovered to be on sale, it will open up a text file containing information about all these new items as well as the URL for easy access.
- Keeps a log of past sales that were found as the scraper runs. This is stored in the log folder. Remember to trash the logs every so often to avoid memory clog.
- Current only supports Men clothing, brands, and items

# Requirements 
- Python

Not using any headless browser Selenium.

# Usage 
Only two files you need to care about is `config.py` and `new_sales.txt`. 
- `new_sales.txt` will show you the new sales that come up
- `config.py` will be where you make changes to the script

# Adding More Brands
To add more brands for the scraper to search for, need two things, the brand name as listed by Yoox and the associated brand number.

These two things can be found on the URL. Each supported brand of Yoox has it's own specific url that will always be in a certain format. 

## Examples
The URL for Santoni is something like this:
https://www.yoox.com/us/men/shoponline/santoni_md#/d=615&dept=men&gender=U&page=1&season=X&ms=dr

Santoni brand name will be "santoni" and the brand number will be "615".

The URL for Brunello Cucinelli is something like this:
https://www.yoox.com/us/men/shoponline/brunello%20cucinelli_md#/Md=942&dept=men&gender=U&page=1&season=X&sort=3

The brand name would be "brunello%20cucinelli" and brand number would be "942".

You can add these two items for the brand into `config.py` and the scraper will search for it.
