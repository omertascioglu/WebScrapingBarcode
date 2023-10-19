import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv


def search_google_barcode_name(barcode_number):

  url = f"https://www.google.com/search?q={barcode_number}"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")

  # Find the first search result that contains the barcode number.
  search_result = soup.find("h3",class_='zBAuLc l97dzf')
  if search_result is None:
    print("Empty search result")
    return None
  # Extract the barcode name from the search result title.
  product_name = search_result.find('div', class_='BNeawe vvjwJb AP7Wnd').text.split('-' and '|')[0].strip()

  return product_name

def is_barcode_in_number_format(barcode_number):

  try:
    int(barcode_number)
    return True
  except ValueError:
    return False

def main():
  """Iterates over a list of barcode numbers and checks their names."""
  df = pd.read_csv("barcode.csv")

  csv_file = "sample_data.csv"


  barcode_numbers = []

  for i in df["BARCODE"]:
      barcode_numbers.append(i)

  for barcode_number in barcode_numbers:
    # Check if the barcode is in number format.
    if is_barcode_in_number_format(barcode_number):
      # Search Google for the barcode name.
      barcode_name = search_google_barcode_name(barcode_number)

      # If the barcode name is found, print it.
      if barcode_name is not None:
        print(f"Barcode name for {barcode_number}: {barcode_name}")
        with open(csv_file, mode='a') as file:
          writer = csv.writer(file)
          writer.writerow([barcode_number, barcode_name])

  print(f"Data has been written to {csv_file}.")

if __name__ == "__main__":
  main()
