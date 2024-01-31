import scrapy
import asyncio

class MoviesSpider(scrapy.Spider):
    name = 'movies_async'
    allowed_domains = ['ru.wikipedia.org']
    start_urls = ['https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83']

    async def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url=url, callback=self.parse_movie_by_year_page)

    async def parse_movie_by_year_page(self, response):
        year_pages = response.css('.mw-category a::attr(href)').extract()
        
        tasks = [self.pars_movie_page(response.urljoin(year_page)) for year_page in year_pages]
        await asyncio.gather(*tasks)

        next_page = response.xpath('//a[contains(text(), "Следующая страница")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_movie_by_year_page)
    
    async def parse_movie_page(self, url):
        
        def selector(self, response, paths):
            for path in paths:
                resp = response.xpath(path).extract()
                if resp:
                    return resp
            else:
                return []

        response = await self.async_request(url)

        if response:
            # get name
            name_paths = ('//*[@id="firstHeading"]/span/text()',
                        '//th[@colspan="2"]/text()')
            name = selector(response, name_paths)

            # get genre
            genre_paths = ('//span[@data-wikidata-property-id="P136"]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[4]/td/span/a/text()',
                        '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[4]/td/span/a/text()')
            genre = selector(response, genre_paths)

            # get director
            director_paths = ('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[5]/td/span/a/text()',)
            director = selector(response, director_paths)

            # get country
            country_paths = ('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[12]/td/span/span/a/span/text()',
                            '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[11]/td/span/span/a/span/text()',
                            '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[13]/td/span/span/a/span/text()')
            country = selector(response, country_paths)

            # get year
            year_paths = ('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[14]/td/a/span/text()',
                        '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[13]/td/a/span/text()',
                        '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[15]/td/a/span/text()')
            year = selector(response, year_paths)

            yield {
                'name' : name,
                'genre' : genre,
                'director' : director,
                'country' : country,
                'year' : year
            }

    async def async_request(self, url):
        try:
            response = await self.crawler.engine.downloader.fetch(scrapy.Request(url, callbacj=self.dummy_callback))
            return response
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
    
    def dummy_callback(self, response):
        return response
    
    def parse(self, response):
        pass