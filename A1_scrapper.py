import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

rest_names=[]
rest_urls=[]
my_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

for page in range (1,5):
  rest_page_url= 'https://www.swiggy.com/city/mumbai/top-rated-collection?page='
  response = requests.get(rest_page_url + str(page), headers=my_header)

  #check for response
  if response.status_code != 200:
    raise Exception('Failed to load page{}'.format(rest_urls))
  # parse using beautifulsoup
  doc = BeautifulSoup(response.text, 'html.parser')

 #getting name
  rest_name_tag= doc.find_all('div', {'class': 'nA6kb'})

  for tag in rest_name_tag:
    rest_names.append(tag.text)
  #getting url
  url_selection_class = "_1j_Yo"
  url_tags= doc.find_all('a', {'class': url_selection_class})
      
  base_url = 'https://swiggy.com'
  for tag in url_tags:
    rest_urls.append(base_url + tag['href'])

#creating dictionary    
rest_page_dict = {
    'name': rest_names,
    'url': rest_urls
    }
      
#puuting DataFrame      
rest_df = pd.DataFrame(rest_page_dict)
#creating csv file
rest_df.to_csv('A1_links.csv', index = None)
    

with open('A1_links.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile)

  urls = [row["url"] for row in reader]

combining = list()
my_list_of_details = list()
# Scraping the data from the urls
for url in urls:
    query = url
    page = requests.get(query, headers=my_header)
    output = list()
    soup = BeautifulSoup(page.text, 'html.parser')
    restuarant = soup.find('div', {'class':'_1637z'})
    res_name = restuarant.find('div', {'class':'OEfxz'}).text
    rest_cuisine_tag= restuarant.find('div', {'class':'_3Plw0 JMACF'}).text
    rest_location_tag= restuarant.find('div', {'class':'Gf2NS _2Y6HW'}).text
    rest_info_tag= restuarant.find_all('div', {'class':'_2l3H5'})
    rest_rating_tag = rest_info_tag[0].text.strip()
    price_two_tag = "Rs. "+rest_info_tag[2].text.strip()[2:]
    num_rating_tag= restuarant.find('div', {'class':'_1De48'}).text.strip()
    matches = soup.find('div', {'class':'_1hM1R znxoh'})
    heading = matches.find_all('div', {'class':'_2dS-v'})
    for j in heading:

        items = j.find_all('div', {'class':'_2wg_t'})
        try:
            types = j.find('h2', {'class':'M_o7R _27PKo'}).text
        except:
            types = j.find('h2', {'class':'M_o7R'}).text
        for k in items:
            name = k.find('h3', {'class':'styles_itemNameText__3ZmZZ'}).text
            try:
                price = k.find('span', {'class':'rupee'}).text
                price = float(price)
            except:
                print('price not found')
                price = 'NA'
            output.append([res_name, types, name, price, rest_cuisine_tag, rest_location_tag, rest_rating_tag, price_two_tag, num_rating_tag])
            
    my_list_of_details.append(output)
    
for i in my_list_of_details:
    for values in i:
        combining.append(values)
column_names = ['Restaurant name','Food types','Cuisine name', 'Price (in Rupees)', 'cuisine_tag', 'location', 'rating', 'price of two', 'num of rating']
df = pd.DataFrame(combining, columns=column_names)
# As we want the list of cheapest items sorting in ascending order
df=df.sort_values(by=["Price (in Rupees)"])
df.to_csv('A1_output.csv',index=False)