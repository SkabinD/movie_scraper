import scrapy
from scrapyproject.items import MovieItemExtended

class MoviesSpider(scrapy.Spider):
    name = 'movies_extended'
    allowed_domains = ['ru.wikipedia.org']
    start_urls = ['https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83']

    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url=url, callback=self.parse_movie_by_year_page)

    def parse_movie_by_year_page(self, response):
        year_pages = response.css('div#mw-pages li ::attr(href)').extract()
        for year_page in year_pages:
            yield scrapy.Request(url=response.urljoin(year_page), callback=self.parse_movie_page)

        next_page = response.xpath('//a[contains(text(), "Следующая страница")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_movie_by_year_page)
    
    def parse_movie_page(self, response):
        movie = MovieItemExtended()
        # get name
        name_paths = ('table.infobox tbody tr th.infobox-above::text',
                      'span.mw-page-title-main::text')
        movie['name'] = self.selector(response, name_paths)

        # get genre
        genre_paths = ('table.infobox tbody tr th:contains("Жанр") + td ::text',)
        movie['genre'] = self.selector(response, genre_paths)

        # get director
        director_paths = ('table.infobox tbody tr th:contains("Режисс") + td ::text',)
        movie['director'] = self.selector(response, director_paths)

        # get country
        country_paths = ('table.infobox tbody tr th:contains("Страна") + td ::text',)
        movie['country'] = self.selector(response, country_paths)

        # get year
        year_paths = ('table.infobox tbody tr th:contains("Год") + td ::text',)
        movie['year'] = self.selector(response, year_paths)

        imdb

        yield movie

    def selector(self, response, paths):
        ban = ['\\', '\n', '[1]', "[2]", "[3]", "[4]", "[d]", "[…]", ' / ', ' ', '  ', ', ', " (", " ", "(англ.)", "рус.", " и "]
        for path in paths:
            resp = set(filter(lambda x: x not in ban, response.css(path).extract()))
            if resp:
                return resp
        else:
            return []