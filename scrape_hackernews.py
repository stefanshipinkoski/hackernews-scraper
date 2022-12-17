import requests
from bs4 import BeautifulSoup
import pprint


# request for first page
res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
titles = soup.select('.titleline')
subtext = soup.select('.subtext')

#request for second page
next_res = requests.get('https://news.ycombinator.com/news?p=2')
next_page_soup = BeautifulSoup(next_res.text, 'html.parser')
titles_next = next_page_soup.select('.titleline')
subtext_next = next_page_soup.select('.subtext')


def create_custum(titles, subtext):
	'''This function will look for the titles links and,
	  scale the points for the posts that we looking for '''
	hn = []
	for idx, item in enumerate(titles):
		title = item.getText()
		href = item.find('a').get('href')
		vote = subtext[idx].select('.score')
		if len(vote):
			points = int(vote[0].getText().replace(' points', ''))
			if points > 99:
				hn.append({'title': title, 'link': href, 'votes': points})
	return hn

def next_page(titles_next, subtext_next):
	'''This function gets the posts from the next page'''
	next_content = create_custum(titles_next, subtext_next)
	return next_content

def sort_news(page1, page2):
	'''This function joins togheter the post from page1 and page2'''
	news = page1 + page2
	return sorted(news, key=lambda k: k['votes'], reverse=True)

hn = create_custum(titles, subtext)
np = next_page(titles_next, subtext_next) 
final_news =pprint.pformat(sort_news(hn, np))
 
with open('./news.txt', 'wt') as file:
	file.write(final_news)
	print('done')
