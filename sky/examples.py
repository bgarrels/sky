from sky.configs import DEFAULT_CRAWL_CONFIG

########## 1. Setup ##################################################
        
PROJECT_NAME = 'testproj'

default_config = DEFAULT_CRAWL_CONFIG

bbc_config = {
    'seed_urls' : ['http://www.bbc.com/news/world/europe'],
    'crawl_required_strings' : 'europe',
    'index_required_strings' : 'news/world-europe-',
}

######### 2a. File      ##############################################

from sky.crawler_services import CrawlFileService
from sky.crawler_plugins import CrawlFilePluginNews

storage_object = {'path' : '/Users/pascal/sky_collections/'}

cs = CrawlFileService(PROJECT_NAME, storage_object, CrawlFilePluginNews)

######### 2b. Cloudant  ##############################################

import cloudant
from sky.crawler_services import CrawlCloudantService
from sky.crawler_plugins import CrawlCloudantPluginNews

with open('cloudant.username') as f:
    USERNAME = f.read()    
with open('cloudant.password') as f:
    PASSWORD = f.read() 
account = cloudant.Account(USERNAME)
account.login(USERNAME, PASSWORD)

cs = CrawlCloudantService(PROJECT_NAME, account, CrawlCloudantPluginNews)

######### 2c. ElasticSearch ##########################################

import elasticsearch

from sky.crawler_services import CrawlElasticSearchService
from sky.crawler_plugins import CrawlElasticSearchPluginNews

es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])

cs = CrawlElasticSearchService(PROJECT_NAME, es, CrawlElasticSearchPluginNews)

######### 2d. ZODB ###################################################

import ZODB.FileStorage
from sky.crawler_services import CrawlZODBService
from sky.crawler_plugins import CrawlZODBPluginNews

fname = '/Users/pascal/sky_collections/zodb/{}.fs'.format(PROJECT_NAME)
storage = ZODB.FileStorage.FileStorage(fname)

cs = CrawlZODBService(PROJECT_NAME, storage, CrawlZODBPluginNews)

######### 3. Add config files to the database ########################

default = cs.get_crawl_plugin('default')
default.save_config(default_config)

bbc = cs.get_crawl_plugin('bbc.com')
bbc.save_config(bbc_config)

######## 4. Start crawling ###########################################
cs.run('bbc.com')
