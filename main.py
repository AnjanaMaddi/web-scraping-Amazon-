from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import pandas as pd
import re

print("program started establishing connection..")
url = r'https://www.amazon.in/b/ref=s9_acss_bw_cg_INPCOF_2c1_w?node=21474843031&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-2&pf_rd_r=Y1MHHKXR4PG1SZCHA0ZG&pf_rd_t=101&pf_rd_p=abbc555d-7bf6-4aae-9be7-26499fda54f6&pf_rd_i=21102571031'
u = urlopen(url)
html_page = u.read()
print("connection..")
u.close()
page=soup(html_page,"html.parser")
print("html read....")
containers = page.findAll("div",{"class":"s-item-container"})
print("found the containers....")
names=[]
price=[]
actual_price=[]
discount=[]
stars=[]
images=[]
i=0
print("looping over elements..")
for v in containers:
    print(str(i+1)+"th element")
    x = v.findAll("a",{"class": "a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
    names.append(x[0].get('title'))
    x = v.findAll("span", {"class": "s-price"})
    p=x[0].text
    m = re.findall("[\d+]", p)
    m = ''.join(m)
    price.append(m)
    x = v.findAll("span", {"class": "a-text-strike"})
    p = x[0].text
    m = re.findall("[\d+]", p)
    m = ''.join(m)
    actual_price.append(m)
    x = v.findAll("span", {"class": "a-icon-alt"})
    stars.append(x[0].text.split(' ')[0])
    x = v.findAll("img", {"class": "s-access-image"})
    link = x[0].get('src')
    resource = urlopen(link)
    filename = "images/file"+str(i)+".jpg"
    images.append(filename)
    output = open(filename, "wb")
    output.write(resource.read())
    output.close()
    d=((int(actual_price[-1])-int(price[-1]))/int(actual_price[-1]))*100
    discount.append(d)
    i += 1
data = {'Product_name': names,
        'price':price,
        'actual_price':actual_price,
        'discount':discount,
        'rating_out_of_5': stars,
        'product_image':images
        }

df = pd.DataFrame(data,
    columns = [
        'Product_name', 'price','actual_price','discount','rating_out_of_5','product_image'
    ])
print(df)
df.to_json('HeadPhonesAndSpeakers.json')
