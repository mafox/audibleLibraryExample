"""
Audible Library
This is a selenium application
The following dictionaries  will be created from the Audible library of interest
books, authors, narrators
these then form a pandas dataframe that is written to a csv filed.
Initially one book is obtained for testing and
various tests are included for which the code is subsequently  commented out.
The Audible site is obtained and I have chosen to input my credentials by hand. An  input command
allows the program to halt execution while these are inputted.

The code from Frank Andrade course as been used as required.

"""

from selenium import webdriver
import pandas as pd
import time

web = 'https://www.audible.com/library/titles'
path = 'D:/webScrappingAndrade/chromedriver/chromedriver.exe'

driver = webdriver.Chrome(path)
driver.get(web)
driver.maximize_window()

xxxx = input(':')  # halt the program

#  get and process the first book to test the Xpath
"""
book1 = driver.find_element_by_xpath('//span[contains(@class, "bc-size-headline3")]')
print(f'title: {book1.text}')
author1 = driver.find_element_by_xpath('.//li[contains(@class,"authorLabel")]')
print(f'author: {author1.text}')
narrator1 = driver.find_element_by_xpath('.//li[contains(@class,"narratorLabel")]')
print(f'narrator: {narrator1.text}\n')
"""

# Pagination
pagination = driver.find_element_by_xpath('//ul[contains(@class, "pagingElements")]')  # locating pagination bar
pages = pagination.find_elements_by_tag_name('li')  # locating each page displayed in the pagination bar
last_page = int(pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)

current_page = 1  # this is the page the bot starts scraping

booksDic = []
authorsDic = []
narratorsDic = []

#book title,  authors and narrators are each separently obtained using the driver as no container for the books
# was found and thus its members could not be used as book.find....
# The while loop below will work until the the bot reaches the last page of the website, then it will break
while current_page <= last_page:
	time.sleep(2)  # let the page render correctly
	books = driver.find_elements_by_xpath('//span[contains(@class, "bc-size-headline3")]')
	authors = driver.find_elements_by_xpath('.//li[contains(@class,"authorLabel")]')
	narrators = driver.find_elements_by_xpath('.//li[contains(@class,"narratorLabel")]')


	for book in books:
		booksDic.append(book.text)
		# print(f'title: {book.text}')
	for author in authors:
		authorsDic.append(author.text[4:])
		#(f'author: {author.text[4:]}')
	for narrator in narrators:
		narratorsDic.append(narrator.text[13:])
		#print(f'narrator: {narrator.text[13:]}')

	current_page = current_page + 1  # increment the current_page by 1 after the data is extracted
	# Locating the next_page button and clicking on it. If the element isn't on the website, pass to the next iteration
	try:
		next_page = driver.find_element_by_xpath('.//span[contains(@class , "nextButton")]')
		next_page.click()
	except:
		print("{an exception has been raised")
"""
This piece of code is here as one of my books is just sound and has no narrator. To ensure each dictionary is
 the same length, required for the data frame, I insedrted a dummy  narrator.
if narratorsDic[113] == 'Luis Moreno':
	narratorsDic.insert(114, "no narration")
	print(f'at 113: {narratorsDic[113]}\nat 114: {narratorsDic[114]}\nat 115: {narratorsDic[115]}')
else:
	print("incorrect position")
	print(f'at 113: {narratorsDic[113]}\nat 114: {narratorsDic[114]}\nat 115: {narratorsDic[115]}')
"""
# just chech each has same length
print(f'books:  {len(booksDic)}  authors: {len(authorsDic)} narrators: {len(narratorsDic)}')

df_books = pd.DataFrame({'title': booksDic})
df_authors = pd.DataFrame({'author': authorsDic})
df_narrators = pd.DataFrame({ 'narrator': narratorsDic})

df_books.to_csv("books.cvs", index  = True)
df_authors.to_csv("authors.cvs", index  = True)
df_narrators.to_csv("narrators.cvs", index  = True)

df_booksComposite = pd.DataFrame({'title': booksDic, 'author': authorsDic, 'narrator': narratorsDic})
df_booksComposite.to_csv('audio_library.csv', index=False)
