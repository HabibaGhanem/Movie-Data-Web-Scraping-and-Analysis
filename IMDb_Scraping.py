import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import requests
import re

class IMDbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    def start_requests(self):
        url = "http://top250.info/charts/?2023/09/25"
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
        title_list = response.xpath('//td[3]/a/span/text()').extract()       
        
        release_year_list = []
        for title in title_list:
            substrings = re.search(r'(.+)\s\((\d{4})\)', title)
            title_list[title_list.index(title)] = substrings.group(1)
            release_year_list.append(substrings.group(2))
            
        movie_rank_list = response.xpath('//tr[contains(@class,"row")]/td[1][@align="center"]/text()').extract()
        rating_list = response.xpath('//td[4]/text()').extract()
        
        dict = {'Title':title_list,'ReleaseYear':release_year_list, 'IMDbRank':movie_rank_list, 'IMDbRating':rating_list}
        df = pd.DataFrame(dict)
        df.to_csv('IMDb_data.csv',index=False)



process = CrawlerProcess()
process.crawl(IMDbSpider)
process.start()