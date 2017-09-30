import pymysql
import requests
from bs4 import BeautifulSoup
from down import download

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='stockexchange')
cur = conn.cursor()

def getUrl(dir):
	url=open(dir,"r").read()
	return url

def store(F,L):
	cur.execute("INSERT INTO `dsedayendsumm`(`DATE`, `TRADING CODE`, `LTP*`, `HIGH`, `LOW`, `OPENP*`, `CLOSEP*`, `YCP`, `TRADE`, `VALUE (mn)`, `VOLUME`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",L)
	conn.commit()
	print("Updated database ...")

def getStore(allData):
	L = []
	F = []
	head = allData.find('tr', attrs={ 'bgcolor':'#D6D6D6'})
	for val in head.find_all('font'):#attributes of table
		F.append(val.get_text())
	del F[0]
	print("Got all field ... ",F)
	for tr in allData.find_all('tr', attrs={ 'bgcolor':'#FFFFFF'}):#data of the table
		for val in tr.find_all('font'):
			L.append(val.get_text())
			# L.append(val.get_text())		
		del L[0]	
		print(L)
		store(F,L)
		L.clear()
	print("Got data 1 ...\n")
	for tr in allData.find_all('tr', attrs={ 'bgcolor':'#EFEFEF'}):#data of the table
		for val in tr.find_all('font'):
			L.append(val.get_text())
		del L[0]
		print(L)
		store(F,L)
		L.clear()
	print("Got data 2 ...\n")

def crawl():
	url = getUrl("dse1.txt")	
	html = requests.get(url)
	print("Downloaded ...\n")
	soup = BeautifulSoup(html.text, "lxml")
	# print(soup.prettify)
	allData = soup.find('table', attrs={ 'bgcolor':'#808000'})
	print("Soup ...\n")
	getStore(allData)

if __name__ == '__main__':
	crawl()
	cur.close()
	conn.close()
