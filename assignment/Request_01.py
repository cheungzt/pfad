import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Set the target URL
url = "https://www.boxofficemojo.com/chart/top_lifetime_gross/?area=XWW"

# Set request headers to simulate a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# Send a request to the website
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.ok:
    print("Data is ready!")

    # Parse the HTML content using BeautifulSoup
    content = response.text
    soup = BeautifulSoup(content, "html.parser")

    # Initialize empty lists to store movie names and gross revenues
    movie_names = []
    grosses = []

    # Select elements containing movie names
    name_elements = soup.select('tr td a[href^="/title/"]')

    # Select elements containing gross revenues
    gross_elements = soup.select('tr td.a-text-right.mojo-field-type-money')

    # Check if movie names or gross revenue elements are found
    if not name_elements or not gross_elements:
        print("No movie names or gross income elements found. Please check the selectors.")

    # Extract movie names and their corresponding gross revenues
    for name, gross in zip(name_elements, gross_elements):
        try:
            # Get the text of the movie name and clean it
            movie_names.append(name.get_text().strip())

            # Convert the gross revenue to a float, removing "$" and commas
            gross_value = float(gross.get_text().strip().replace('$', '').replace(',', ''))
            grosses.append(gross_value)
        except ValueError:
            continue

    # Check if any data was extracted
    if len(grosses) == 0 or len(movie_names) == 0:
        print("No numeric data or movie names extracted. Please check the HTML structure and the parsing logic.")
    else:
        # Print the number of data points and display the first 10
        print(f"Number of data points: {len(grosses)}")
        print("First 10 movie names and grosses:")
        for name, gross in zip(movie_names[:10], grosses[:10]):
            print(f"{name}: ${gross:,.2f}")

        # Visualize the data with a bar chart
        plt.figure(figsize=(12, 6))
        plt.bar(movie_names[:10], grosses[:10], color='skyblue')
        plt.title("Top 10 Highest Grossing Movies - Box Office Mojo")
        plt.xlabel("Movie Name")
        plt.ylabel("Gross Revenue ($)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

else:
    print(f"Failed to retrieve data, status code: {response.status_code}")
