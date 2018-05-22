# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.utils.project import get_project_settings
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import os

'''
class AitaotuimgPipeline(object):
    def __init__(self):
        self.filename = open('d:/imgs/beauty1.json','w',encoding='utf-8')

    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.filename.write(jsontext)
        return item


    def close(self,spider):
        self.filename.close()'''

class AitaotuimgPipeline(ImagesPipeline):
    # 获取setting文件中设置的变量值
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')
    def get_media_requests(self, item, info):
        image_url=item['img_url']
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_path =[x['path'] for ok,x in results if ok]
        img_path = "%s%s" % (self.IMAGES_STORE, item['title'])
        if os.path.exists(img_path) == False:
            os.mkdir(img_path)
        os.rename(self.IMAGES_STORE + image_path[0], img_path +'/'+item["name"] + '.jpg')

        item["path"] = self.IMAGES_STORE+ item["name"]
        return item


