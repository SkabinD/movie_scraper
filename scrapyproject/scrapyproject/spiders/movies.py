import scrapy

class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['ru.wikipedia.org']
    start_urls = ['https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83']

    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url=url, callback=self.parse_movie_by_year_page)

    def parse_movie_by_year_page(self, response):
        year_pages = response.css('.mw-category a::attr(href)').extract()
        for year_page in year_pages:
            yield scrapy.Request(url=response.urljoin(year_page), callback=self.parse_movie_page)

        next_page = response.xpath('//a[contains(text(), "Следующая страница")]/@href').extract_first()

        if next_page:
            yield response.follow(next_page, callback=self.parse_movie_by_year_page)
    
    def parse_movie_page(self, response):
        # get name
        name_paths = ('//th[@colspan="2"]/text()',
                      '//*[@id="firstHeading"]/span/text()')
        name = self.selector(response, name_paths)

        # get genre
        genre_paths = ('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[3]/td/span/a[1]/text()',
                       '//span[@data-wikidata-property-id="P136"]/text()',
                       '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[4]/td/span/a/text()',
                       '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[4]/td/span/a/text()',
                       '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[3]/td/span/a/text()',
                       '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[3]/td/span/span/a/text()')
        genre = self.selector(response, genre_paths)

        # get director
        director_paths = ('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[5]/td/span/a/text()',
                          '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[5]/td/span/text()',
                          '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[4]/td/span/text()')
        director = self.selector(response, director_paths)

        # get country
        country_paths = ('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[12]/td/span/span/a/span/text()',
                         '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[11]/td/span/span/a/span/text()',
                         '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[13]/td/span/span/a/span/text()',
                         '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[16]/td/ul/li[1]/span/span[2]/span/a/text()',
                         '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[12]/td/div/p/span/a/span/text()',
                         '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[12]/td/ul/li/span/span[2]/span/a/text()')
        country = self.selector(response, country_paths)

        # get year
        year_paths = ('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[14]/td/a/span/text()',
                      '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[13]/td/a/span/text()',
                      '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[15]/td/a/span/text()',
                      '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[15]/td/span/span/span/a/text()',
                      '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[14]/td/span/span/span/a/text()',
                      '//*[@id="mw-content-text"]/div[1]/table/tbody/tr[13]/td/span/span/span/a/text()')
        year = self.selector(response, year_paths)

        yield {
            'name' : name,
            'genre' : genre,
            'director' : director,
            'country' : country,
            'year' : year
        }
    
    def selector(self, response, paths, name_flag=False):
        for path in paths:
            resp = response.xpath(path).extract()
            if resp:
                if name_flag and len(resp) > 1:
                    continue
                else:
                    return resp
        else:
            return []