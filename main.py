from bs4 import BeautifulSoup
from config import BRAND_NAMES, BRAND_NUMBERS, DESIRED_DISCOUNT
from requests_html import HTMLSession
import time
import difflib
import os
import shutil

session = HTMLSession()

def find_items():
    # Clears listing text file if it exists
    file_to_delete = open("items.txt", "w")
    file_to_delete.close()

    found_item_count = 0

    for brand_name, brand_num in zip(BRAND_NAMES, BRAND_NUMBERS):
        for page_number in range(1, 100):
            url = f"https://www.yoox.com/us/men/shoponline/{brand_name}_md/{page_number}#/d={brand_num}&dept=men&gender=U&page={page_number}&season=X&sort=3"

            response = session.get(url, timeout=10)

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "lxml")

            # Ends loop when we reach a page that contains no items
            if soup.find("div", class_="itemData text-center") == None:
                break

            print(f"Searching {brand_name} page {page_number}")

            # Find all item listing
            items = soup.find_all("div", class_="col-8-24")
            for item in items:
                # Filters out non item elements
                if item.find("div", class_="itemData text-center") == None:
                    break

                # Filters out sold out items
                if "SOLD OUT" not in item.find("div", class_="price").text.strip():
                    sale_percentage = item.find("span", class_="element")

                    # Filters out items not on sale
                    if sale_percentage != None and int(sale_percentage.text.strip().split("%")[0]) >= DESIRED_DISCOUNT:
                        brand = item.find("div", class_="brand font-bold text-uppercase").text.strip()
                        type = item.find("div", class_="microcategory font-sans").text.strip()
                        sale_percentage = item.find("span", class_="element").text.strip()
                        old_price = item.find("span", class_="oldprice text-linethrough text-light").text.strip()
                        new_price = item.find( "div", class_="retail-newprice font-bold").text.strip()
                        url = "https://www.yoox.com" + item.find("a", class_="itemlink")["href"]

                        with open("items.txt", "a") as f:
                            f.write(f"\nBrand: \t\t{brand} \n")
                            f.write(f"Item Type: \t{type} \n")
                            f.write(f"Sale: \t\t{sale_percentage} \n")
                            f.write(f"Old Price: \t{old_price} \n")
                            f.write(f"New Price: \t{new_price} \n")
                            f.write(f"URl: \t\t{url} \n")

                        found_item_count += 1

    print(f"Finished. {found_item_count} items found.")

def get_file_differences(file1, file2):
    '''
    Get lines in file2 that are not in file1 as opposed to overall differences between the two txt files
    '''
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    diff = difflib.ndiff(lines1, lines2)
    diff_lines = [line for line in diff if line.startswith('+ ')]
    with open("new_sales.txt", "w") as f:
        for line in diff_lines:
            f.write(line)

def show_new_items():
    # Specify the file paths
    file1 = "old_items.txt"  # Previous data
    file2 = "items.txt"  # Updated data

    # Call the function to get the differences between the two text files.
    get_file_differences(file1, file2)

    # Update the text file for old_items to our new list of items
    os.remove("old_items.txt")
    shutil.copyfile("items.txt", "old_items.txt")

if __name__ == "__main__":
    while True:
        find_items()
        show_new_items()
        time_wait = 60*12
        print(f"Waiting {time_wait/60} hours...")
        time.sleep(time_wait * 60)