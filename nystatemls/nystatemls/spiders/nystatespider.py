# -*- coding: utf-8 -*-
import scrapy
import requests
import csv
# import unicodecsv as csv
import win32api

data = []
base_url = "https://www.nystatemls.com/new_york_state_real_estate_agents.html"

class NystatespiderSpider(scrapy.Spider):
    name = 'nystatespider'
    output = 'nystate(601-677).csv'
    open(output, 'w').close()
    header = ['AgentName', 'Role', 'Company', 'Address', 'Area', 'PhoneNo1', 'PhoneNo2', 'PhoneNo3', 'PhoneNo4', 'Eamil', 'Website']
    with open(output, "a", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
        csv_writer.writeheader()

    def start_requests(self):

        default_url = "https://www.nystatemls.com/new_york_state_real_estate_agents.html?pn={}&rpp=50"
        for i in range(601, 677): # 677
            url = default_url.format(i)
            print (url)

            yield scrapy.Request(url=url, callback=self.get_urls)

    def get_urls(self, response):
        print("<---------------------Scraping Start------------------>")        
        item_urls = response.xpath("//a[contains(@class, 'ActionLink')]/@href").extract()
        
        first_url = "https://www.nystatemls.com/"

        # print("---------------->", len(item_urls))
        
        for second_url in item_urls:
            item_url = first_url + second_url
            
            yield scrapy.Request(url=item_url, callback=self.profile_parse)
            
    def profile_parse(self, response):
        print("<------------------Parsing item Page------------------->")
        with open(self.output, "a", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)

            phoneNo2 = ""
            phoneNo3 = ""
            phoneNo4 = ""
            email = ""
            website = ""

            agentName = response.xpath("//div[contains(@id, 'HomeMainContent')]//h1/strong/text()").get()

            agentJob = response.xpath("//div[contains(@id, 'HomeMainContent')]//h3/text()").get()
            
            comName = response.xpath("//a[@title='View Company Profile']/text()").get()

            address_infos = response.xpath("(//div[contains(@class, 'padding-20')])[2]//div/text()").extract()

            n = len(address_infos)
            # print("---------------------------------------", n)

            for address_info in address_infos:
                if '-' in address_info and ' ' not in address_info:
                    phoneNo = address_info
                    n = n - 1
                    if n == 2:
                        address = address_infos[0]
                        area = address_infos[1]
                        print("------------------------", n)
                    elif n == 3:
                        address = address_infos[0] + address_infos[1]
                        area = address_infos[2]
                else:
                    if n == 3:
                        address = address_infos[0] + address_infos[1]
                        area = address_infos[2]
                    elif n == 2:
                        address = address_infos[0]
                        area = address_infos[1]
                    phoneNo = ""
            
            con_classNames = response.xpath("(//div[contains(@class, 'padding-20')])[3]//tr/td[1]/i/@class").extract()
            
            counts = len(con_classNames)

            con_infos = response.xpath("(//div[contains(@class, 'padding-20')])[3]//tr/td[2]/text()").extract()
            
            for no in range(0, counts):
                if 'android-call' in con_classNames[no]:
                    phoneNo2 = con_infos[no]
                elif 'phone-portrait' in con_classNames[no]:
                    phoneNo3 = con_infos[no]
                elif 'ion-printer' in con_classNames[no]:
                    phoneNo4 = con_infos[no]
                elif 'email' in con_classNames[no]:
                    email = con_infos[no]
                elif '-world' in con_classNames[no]:
                    website = response.xpath("//a[@title='Website']/@href").extract()[0]
         
            print("----------------------------------------------------")
            print("----------", response.request.url)
            print("agentName----------------------->   : ", agentName)
            print("agentJob------------------------>   : ", agentJob)
            print("comName------------------------->   : ", comName)
            print("phoneNo------------------------->   : ", phoneNo)
            print("address------------------------->   : ", address)
            print("area---------------------------->   : ", area)
            print("phoneNo2------------------------>   : ", phoneNo2)
            print("phoneNo3------------------------>   : ", phoneNo3)
            print("phoneNo4------------------------>   : ", phoneNo4)
            print("email--------------------------->   : ", email)
            print("website------------------------->   : ", website)

            writer.writerow([agentName, agentJob, comName, address, area, phoneNo, phoneNo2, phoneNo3, phoneNo4, email, website])









