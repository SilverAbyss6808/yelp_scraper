
import requests
import csv
import sys

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.5',
    'Alt-Used': 'www.yelp.com',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'www.yelp.com',
    'Priority': 'u=0, i',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0'
}

class Restaurant:
    def __init__(self, ranking, name, rating, reviewCount, priceRange, phone, categories, services):
        self.ranking = ranking
        self.name = name
        self.rating = rating
        self.reviewCount = reviewCount
        self.priceRange = priceRange
        self.phone = phone
        self.categories = categories
        self.services = services

    def __str__(self):
        return f'{self.ranking},{self.name},{self.rating},{self.reviewCount},{self.priceRange},{self.phone},{self.categories},{self.services}'

restaurants = []

prefix = 'https://www.yelp.com/search/snippet'
find_desc = 'Restaurants'
find_loc: str
if (len(sys.argv) == 2):
    if (sys.argv[1] != '' and len(sys.argv[1]) == 5 and sys.argv[1].isnumeric()):
        find_loc = str(sys.argv[1])
        print(f'Gathering data for restaurants near {find_loc}...')
    else:
        find_loc = '45810'
        print('Zip code error. Defaulting to 45810 (Ada, OH)...')
else:
    find_loc = '45810'
    print('Zip code not provided. Defaulting to 45810 (Ada, OH)...')
request_origin = 'request_origin-user'
url: str = prefix + '?find_desc=' + find_desc + '&find_loc=' + find_loc + '&' + request_origin
# print(url)

try:
    response = requests.get(url, headers=headers)
    json_check = response.headers["content-type"].strip().startswith("application/json")
except: print('HTTP response error.')

try:
    all_results = response.json()['searchPageProps']['mainContentComponentsListProps']
    for result in all_results:
        if result['searchResultLayoutType'] == "iaResult":

            try:
                ranking = result['searchResultBusiness']['ranking']
                if (ranking == ''): ranking = 'N/A'
                name = result['searchResultBusiness']['name']
                rating = result['searchResultBusiness']['rating']
                review_count = result['searchResultBusiness']['reviewCount']
                price_range = result['searchResultBusiness']['priceRange']
                if (price_range == ''): price_range = '-'
                phone = result['searchResultBusiness']['phone']
                categories = []
                services = []

                for cat in result['searchResultBusiness']['categories']: categories += [cat['title'] + ';']
                for service in result['serviceOfferings']: services += (service['label']['text'] + ';')

                categories_split = ''.join(categories).split(';')
                categories_split = [s.strip() for s in categories_split if s.strip()]

                services_split = ''.join(services).split(';')
                services_split = [s.strip() for s in services_split if s.strip()]

                restaurants.append(Restaurant(ranking, name, rating, review_count, price_range, phone, categories_split, services_split))
            except: print('List append error.')

        try:
            with open('restaurant_data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ranking', 'name', 'rating', 'review_count', 'price_range', 'phone', 'categories', 'services'])
                for rst in restaurants:
                    writer.writerow([
                        rst.ranking,
                        rst.name,
                        rst.rating,
                        rst.reviewCount,
                        rst.priceRange,
                        rst.phone,
                        ', '.join(rst.categories),
                        ', '.join(rst.services)
                    ])
        except:
            print('CSV error.')

    print('CSV successfully written to restaurant_data.csv.')

except FileNotFoundError:
    print('Status: ' + str(response))
    print('Is JSON: ' + str(json_check))
    print('File not found.')
except requests.exceptions.HTTPError as http_err:
    str = http_err.response.headers.get('X-RateLimit-Remaining')
    print(f'HTTP error: {http_err.response.status_code}')
    print(f'Rate limit: {str}')
except requests.exceptions.JSONDecodeError as json_err:
    print('JSON read error.')
    print('Is JSON: ' + str(json_check))
except:
    print('Unknown error. HTTP response: ' + str(response.status_code))