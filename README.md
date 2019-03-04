# webscraper
Web scraper using Python, Scrapy and Scrapy-Splash

## How to run
1. Install Python [Scrapy](https://scrapy.org/) library  

```
$ pip install scrapy
```

2. Get [Docker for Desktop](https://www.docker.com/get-started) for your machine

3. Install Docker and proceed with [Splash](https://splash.readthedocs.io/en/stable/index.html) installation

```Docker
$ docker pull scrapinghub/splash
$ docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
```
4. Once the Docker container is running, enter this URL on your browser

```
http://localhost:8050/
```

5. You would be able to view Splash site, enter any URL to scrape and click Render Me

>Refer to this [link](https://splash.readthedocs.io/en/latest/install.html) for detailed installation guide

6. Install Python [Scrapy-Splash](https://splash.readthedocs.io/en/stable/index.html) library

```
$ pip install scrapy-splash
```

7. Setup MySQL instance and create a database named **stocksmarket**. Create **stocks** table by executing this query
```sql
CREATE TABLE `stocks` ( 
	`board` VarChar( 255 ) NULL,
	`stock_code` VarChar( 255 ) NOT NULL,
	`stock_name` VarChar( 255 ) NOT NULL,
	`logged_date` Date NOT NULL,
	`logged_time` Time NOT NULL,
	`open_price` Decimal( 10, 5 ) NULL,
	`high_price` Decimal( 10, 5 ) NULL,
	`low_price` Decimal( 10, 5 ) NULL,
	`last_price` Decimal( 10, 5 ) NULL,
	`counter` VarChar( 255 ) NOT NULL )
ENGINE = InnoDB;
```
8. Open **pipelines.py** and update the database settings as needed
```python
class BsklstockmarketPipeline(object):
    def open_spider(self, spider):
        print('open spider')
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="password",
          database="stocksmarket"
        )
```

9. Browse to *bsklstockmarket* folder and execute command below to run the spider

```
$ scrapy crawl thestar
```
## Relevant References
1. https://blog.scrapinghub.com/2015/03/02/handling-javascript-in-scrapy-with-splash
2. http://doc.scrapy.org/en/latest/topics/item-pipeline.html
3. http://mirkosecke.blogspot.com/2017/05/save-scraped-data-in-mysql-db.html
