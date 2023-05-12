from bs4 import BeautifulSoup
from config import BRAND_NAMES, BRAND_NUMBERS, DESIRED_DISCOUNT
from requests_html import HTMLSession
import time
import difflib
import os
import shutil
import datetime

session = HTMLSession()

def find_items():
    # Clears listing text file if it exists
    file_to_delete = open("items.txt", "w")
    file_to_delete.close()

    found_item_count = 0
    all_found_items = []

    for brand_name, brand_num in zip(BRAND_NAMES, BRAND_NUMBERS):
        print(str(datetime.datetime.now()), "-", f"Searching {brand_name} items")

        for page_number in range(1, 100):
            url = f"https://www.yoox.com/us/men/shoponline/{brand_name}_md/{page_number}#/d={brand_num}&dept=men&gender=U&page={page_number}&season=X&sort=3"

            response = session.get(url, timeout=60)

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "lxml")

            # Ends loop when we reach a page that contains no items
            if soup.find("div", class_="itemData text-center") == None:
                break

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

                        # Want to sort items by price. Turn the current price into an int for sorting
                        sort_value = int(new_price.split(" ")[1].split(".")[0].replace(",",""))

                        # Put item data into a list containing all items so we can sort later
                        all_found_items.append([sort_value, brand, type, sale_percentage, old_price, new_price, url])

                        found_item_count += 1

    # Sort all items found from lowest price to highest price. Then we output onto text file
    all_found_items.sort()
    for item in all_found_items:
        with open("items.txt", "a") as f:
            f.write(f"Brand:       {item[1]} \n")
            f.write(f"Item Type:   {item[2]} \n")
            f.write(f"Sale:        {item[3]} \n")
            f.write(f"Old Price:   {item[4]} \n")
            f.write(f"New Price:   {item[5]} \n")
            f.write(f"URl:         {item[6]} \n\n")

    print(str(datetime.datetime.now()), "-", f"{found_item_count} total items found at {DESIRED_DISCOUNT}% off.")

def get_file_differences(file1, file2) -> bool:
    '''
    Get lines in file2 that are not in file1 as opposed to overall differences between the two txt files
    '''

    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    diff = difflib.ndiff(lines1, lines2)
    diff_lines = [line for line in diff if line.startswith('+ ')]
    if len(diff_lines) > 0:
        with open("new_sales.txt", "w") as f:
            f.write(str(datetime.datetime.now()) + f"\n")
            for line in diff_lines:
                f.write(line)
        shutil.copyfile('new_sales.txt', f"./logs/{str(datetime.datetime.now())}.txt")
        return True
    return False

def get_new_sale_items():
    # Specify the file paths
    file1 = "old_items.txt"  # Previous data
    file2 = "items.txt"  # Updated data

    # Call the function to get the differences between the two text files.
    new_sales = get_file_differences(file1, file2)

    if new_sales == True:
        os.system("open new_sales.txt")

    # Update the text file for old_items to our new list of items
    os.remove("old_items.txt")
    shutil.copyfile("items.txt", "old_items.txt")

if __name__ == "__main__":
    while True:
        find_items()
        get_new_sale_items()

        time_wait = 1
        print(str(datetime.datetime.now()), "-", f"Searching again in {time_wait} minute...")
        time.sleep(time_wait * 60)