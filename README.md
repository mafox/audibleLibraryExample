# audibleLibraryExample
Audible Library
This is a selenium application
The following dictionaries  will be created from the Audible library of interest
books, authors, narrators
these then form a pandas dataframe that is written to a csv filed.
Initially one book is obtained for testing and
various tests are included for which the code is subsequently  commented out.
The Audible site is obtained and I have chosen to input my credentials by hand. An  input command
allows the program to halt execution while these are inputted.

The code from Frank Andrade course on Udemy  as been used as required.

The file selTOscrapy:
The purpose of this code is to scrape a personal Audible library.
	The first part uses selenium to control the pages.
	The initial page is accessed and the logon screen is chosen.
	There is an intentionally long  pause to allow the input of credentials.
	Thereafter the handover from selenium to scrapy occurs and the pages are scraped.
	The small piece of code required for pagination is done with selenium.
