import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector
import csv
import pandas as pd
import itertools

class MoviesSpider(scrapy.Spider):
    name = 'movies_spider'
    

    def start_requests(self):
        url = "https://www.moviemeter.com/movies/top-250-best-movies-of-all-time"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        titles = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr//h4/a/text()').extract()
        alt_titles = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[3]/div/div[1]/text()').extract()
        genres = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[3]/div/div[2]/text()').extract()
        release_year = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[3]/div/div[3]/text()').extract()
        movie_rank = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[1]/a/span/text()').extract()
        ratings = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[4]/div/div[1]/text()').extract()
        print(ratings)
        print(len(ratings))
        updated_alt_titles = []
        updated_genre = []
        updated_release_year = []

        i=0
        for alt_title,genre in zip(alt_titles,genres):
            if "Alternative title: " in alt_title:
                alt_title = alt_title.replace("Alternative title:",'')
                updated_alt_titles.append(alt_title)
                updated_genre.append(genre)
                updated_release_year.append(release_year[i])
                i+=1
                
            else:
                updated_alt_titles.append('')
                updated_genre.append(alt_title)
                updated_release_year.append(genre)
                
            
        dict = {'Title':titles, 'AlternativeTitle':updated_alt_titles, 'Genre':updated_genre, 'ReleaseYear':updated_release_year, 'MovieRank':movie_rank, 'Rating':ratings}
        df = pd.DataFrame(dict)
        df.to_csv('movie_data.csv',index=False)
         
        
        


process = CrawlerProcess()
process.crawl(MoviesSpider)
process.start()
