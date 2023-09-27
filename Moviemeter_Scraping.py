import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector
import csv
import pandas as pd
import itertools
import re
import numpy as np
import requests

class MoviemeterSpider(scrapy.Spider):
    name = 'moviemeter_spider'
    

    def start_requests(self):
        url = "https://www.moviemeter.com/movies/top-250-best-movies-of-all-time"
        try:
            # Make a request to the URL
            response = requests.get(url)
            yield scrapy.Request(url=url, callback=self.parse)
        except requests.exceptions.HTTPError as err:
            # Handle HTTP errors
            print(f'HTTP error occurred: {err}')
    
        except requests.exceptions.ConnectionError as err:
            # Handle connection errors
            print(f'Connection error occurred: {err}')
            
        except Exception as e:
            # Handle other parsing errors
            print(f'Error occurred while parsing HTML: {e}')
        
            

    def parse(self, response):
        
        title_list = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr//h4/a/text()').extract()
        alt_title_list = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[3]/div/div[1]/text()').extract()
        genre_list = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[3]/div/div[2]/text()').extract()
        duration_list = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[3]/div/div[3]/text()').extract()
        movie_rank_list = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[1]/a/span/text()').extract()
        rating_list = response.xpath('//*[@id="filter_system"]/div[2]/table/tbody/tr/td[4]/div/div[1]/text()').extract()
        release_year_list = []
        for title in title_list:
            substrings = re.search(r'(.+)\s\((\d{4})\)', title)
            title_list[title_list.index(title)] = substrings.group(1)
            release_year_list.append(substrings.group(2))
            

        updated_alt_title_list = []
        updated_genre_list = []
        updated_duration_list = []

        i = 0
        for alt_title,genre in zip(alt_title_list, genre_list):
            if "Alternative title: " in alt_title:
                alt_title = alt_title.replace("Alternative title:",'')
                updated_alt_title_list.append(alt_title.strip())
                updated_genre_list.append(genre)
                updated_duration_list.append(duration_list[i])
                i += 1
                
            else:
                updated_alt_title_list.append('')
                updated_genre_list.append(alt_title)
                updated_duration_list.append(genre)
                
            
        dict = {'Title':title_list, 'AlternativeTitle':updated_alt_title_list, 'Genre':updated_genre_list, 'MovieDuration':updated_duration_list, 'ReleaseYear':release_year_list, 'MovieRank':movie_rank_list, 'MoviemeterRating':rating_list}
        df = pd.DataFrame(dict)
        df.to_csv('moviemeter_data.csv',index=False)
         
        
process = CrawlerProcess()
process.crawl(MoviemeterSpider)
process.start()




