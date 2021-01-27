from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


data = pd.DataFrame(columns=["Title","Year","Ratings","Genre","Description","Director","Cast","Image","Duration","Certificate","Votes"])
end = 9951
# end = 2
for i in range(1,end,50):
	# print(i,"/9951")

	print("\n\n")
	page = str(i)
	print(f'Scraping Page {i} / {end} ...')

	source = requests.get('https://www.imdb.com/search/title/?title_type=feature&release_date=2010-01-01,2019-12-31&sort=num_votes,desc&start='+page+'&ref_=adv_nxt').text
	
	soup = BeautifulSoup(source,'lxml')




	for movie in soup.find_all(class_ = 'lister-item mode-advanced'):

		flag = 1
		try:
			title = movie.h3.a.text.strip()
			link = 'https://www.imdb.com/'+ movie.h3.a['href']
		except Exception as e:
			title = None
			flag = 0
		print(title)

		
		try:
			votes = movie.find('p',class_ = 'sort-num_votes-visible').text.split()[1]
		except Exception as e:
			votes = None
		# print(votes)

		try:
			year = movie.find('span', class_ = 'lister-item-year text-muted unbold').text.strip()[-5:-1]
		except Exception as e:
			year = None
		
		try:
			Ratings = movie.find(class_ = 'ratings-bar').strong.text.strip()
		except Exception as e:
			Ratings = None
		try:
			Genre = movie.find('span', class_ = 'genre').text.strip()
		except Exception as e:
			Genre = None
		if flag:

			source = requests.get(link).text
			soup = BeautifulSoup(source,'lxml')
			try:
				desc = soup.find(class_ = 'summary_text').text.strip()
			except:
				desc = None
			try:
				direc = soup.find(class_ = 'credit_summary_item').a.text.strip()
			except:
				direc=None
			try:
				star = " ".join(soup.find_all(class_ = 'credit_summary_item')[2].text.split()[1:-7])
			except:
				star = None
			try:
				imag = soup.find(class_ = 'poster').img['src']
			except:
				imag = None
		else:
			desc = None
			direc= None
			star = None
			imag = None

		try:
			Duration = movie.find('span', class_ = 'runtime').text.strip()
		except Exception as e:
			Duration = None
		try:
			Certificate = movie.find('span', class_ = 'certificate').text.strip()
		except Exception as e:
			Certificate = None
 
		data = data.append({"Title":title, "Year":year, "Ratings":Ratings, "Genre":Genre,"Description":desc,"Director":direc,"Cast":star,"Image":imag, "Duration":Duration, "Certificate":Certificate,"Votes":votes}, ignore_index=True)
		data.to_csv('Final.csv',index = False) 
		
	time.sleep(2)
