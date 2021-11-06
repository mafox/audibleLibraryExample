import scrapy
from scrapy.selector import Selector
from selenium import webdriver
import pandas as pd
import time


class SeltoscrapySpider(scrapy.Spider):
	"""
	The purpose of this code is to scrape a personal Audible library.
	The first part uses selenium to control the pages.
	The initial page is accessed and the logon screen is chosen.
	There is an intentionally long  pause to allow the input of credentials.
	Thereafter the handover from selenium to scrapy occurs and the pages are scraped.
	The small piece of code required for pagination is done with selenium.

	"""

	name = 'selTOscrapy'
	allowed_domains = ['toscrape.com']
	start_urls = ['http://audible.com/']

	web = 'https://www.audible.com/library/titles'
	path = 'D:/webScrappingAndrade/chromedriver/chromedriver.exe'

	def combineAuthors(self,originaltext, authors, auth = True):
		"""
		:param originaltext: the text
		:param authors: author  for the result dictionary

		As books may have several authors and narrators this method
		combines them into a single string.
		"author" can be set to either authorDic or narratorDic, the dictionaries to store
		 the results.with auth beinmg True for author, the default, or False  for narrator.

		"""
		bytoken = 'By:'
		aORn = "Author"
		if not auth :
			bytoken = 'Narrated by:'
			aORn = "Narrator"

		#print(f'originaltext size: {len(originaltext)}')
		authorname = False
		author = ""
		for textitem in originaltext:
			textitem = textitem.strip()
			#print(f'*{textitem}*')
			if textitem == "" and author != "":
				#print(f'author name: {author}')
				authors.append(author)
				authorname = False
				author = ""

			if authorname:
				# print(f'author:  **{author}**')
				if textitem == ',':
					textitem = ', '
					authorname = True
				author = author + textitem
			if textitem == bytoken:
				authorname = True

		print(f'{aORn} size: {len(authors)}')

	# Using a dummy website to start scrapy requestGY9PEHih
	def start_requests(self):
		url = "http://quotes.toscrape.com"
		yield scrapy.Request(url=url, callback=self.parse_books)

	def parse_books(self, response):
		driver = webdriver.Chrome(self.path)
		#print(f'driver is * {driver} * \n')
		driver.get(self.web)
		driver.maximize_window()
		time.sleep(5 * 60)

		# Hand-off between Selenium and Scrapy happens here
		sel = Selector(text=driver.page_source)

		booksDic = []
		authorsDic = []
		narratorsDic = []

		# Pagination

		pagination = driver.find_element_by_xpath('//ul[contains(@class, "pagingElements")]')  # locating pagination bar
		pages = pagination.find_elements_by_tag_name('li')  # locating each page displayed in the pagination bar
		last_page = int(pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)
		print(f'pages: {pages} last page:{last_page}')
		current_page = 1  # this is the page the bot starts scraping

		while current_page <= last_page:

			books = sel.xpath('//span[contains(@class, "bc-size-headline3")]/text()').getall()
			for book in books:
				booksDic.append(book)
				#print(f'books: {books}')

			authors  = sel.xpath('.//li[contains(@class, "authorLabel")]//span/text()').getall()

			print(f'authors size: {len(authors)}')
			self.combineAuthors(authors, authorsDic)
			# for author in authorsDic:
			# 	print(f'author: {author}')
			print(f'authorsDic: length: {len(authorsDic)}')


			narrators = sel.xpath('.//li[contains(@class, "narratorLabel")]//span/text()').getall()

			# for narrator in narrators:
			#  print(f'narrator: *{narrator.strip()}*')
			self.combineAuthors(narrators, narratorsDic, False)

			current_page = current_page + 1  # increment the current_page by 1 after the data is extracted
			# Locating the next_page button and clicking on it. If the element isn't on the website, pass to the next iteration
			try:
				next_page = driver.find_element_by_xpath('//span[contains(@class , "nextButton")]')
				print(f'** next_page:(** {next_page} ')
				next_page.click()
			except:
				print("** an exception has been raised about next page **")

		driver.close()
		"""
		As a particular book has no narrator, it bis located and "no narrator" added
		this is to en sure that all dictionals have tghe same length.
		"""
		if last_page > 10:
			for index in range(118, 210):
				if narratorsDic[index] == 'Luis Moreno':
					bk = booksDic[index + 1]
					print(f'at  index {index + 1} {bk}: has no narrator')
					narratorsDic.insert(index + 1, "no narration")

					break
					
					
		# Storing the data into a DataFrame and exporting to a csv file
		print(f'books:  {len(booksDic)}  authors: {len(authorsDic)} narrators: {len(narratorsDic)}')
		df_books = pd.DataFrame({'title': booksDic})
		df_authors = pd.DataFrame({'author': authorsDic})
		df_narrators = pd.DataFrame({'narrator': narratorsDic})

		df_books = pd.DataFrame({'title': booksDic, 'author': authorsDic, 'narrator': narratorsDic})
		df_books.to_csv('books2.csv', index=False)
		df_books.to_json('books.json')