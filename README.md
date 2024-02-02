# Movies Data Parser

A simple parser for retrieving information about movies from Wikipedia, including their names, genres, directors, and more. There is also an extended version of the parser, which can retrive film rating from IMDb.com. The scraped data will be saved in the 'output.csv' file.

In order to use the parser, enter into the command line: "scrapy crawl movies" from the directory: "scrapyproject". Parsed data will be saved in "output.csv".

There is also an extended version of the parser that pulls ratings from the IMDb.com. In order to use it, enter into the command line: "scrapy crawl movies_extended".
