import requests
from bs4 import BeautifulSoup
import re
import mysql.connector

car_name = input('What is the name of the car you are looking for?\n')
end_list = []
page = 1
while page < 5:
    res = requests.get('https://bama.ir/car/'+car_name+'/all-models/all-trims?page='+str(page))
    soup = BeautifulSoup(res.text, 'html.parser')
    result = soup.find_all('div', attrs={'class':'listdata'})

    car_information = []
    for car in result:
        try:
            sample_car = []
            sample_car.append(car.find('p', attrs={'class': 'price hidden-xs'}).text)
            sample_car.append(car.find('span', attrs={'itemprop': 'price', 'style':False}).text)
            car_information.append(sample_car)
        except AttributeError:
            continue
    output_list = [subcar for subcar in car_information if subcar[1] !=  ' در توضیحات ' and subcar[1] != ' حواله ' and subcar[1] != ' توافقی ' and subcar[0] != '-']
    for j in output_list:
        end_list.append(j)
    page += 1

db = mysql.connector.connect(host='localhost',
                             user='root',
                             password='',
                             database="bama")

my_cursor = db.cursor()
drop_sql = 'DROP TABLE IF EXISTS car'
my_cursor.execute(drop_sql)
my_cursor.execute("CREATE TABLE car (operation VARCHAR(20), cost VARCHAR(20))")
my_cursor.execute('ALTER TABLE car CHARACTER SET utf8 COLLATE utf8_persian_ci')

sql = ('INSERT INTO car (operation, cost) VALUES (%s, %s)')

for i in range(0,20):
    val = (end_list[i][0], end_list[i][1])
    my_cursor.execute(sql, val)

