# -*- coding: utf-8 -*-
import scrapy
import requests, json
import math
import csv
import win32api



class SiborSpider(scrapy.Spider):
    name = 'sibor'
    output = 'sibor.csv'
    open(output, 'w').close()
    header = ['AgentName', 'Office', 'OfficePhone', 'MobilePhone', 'Email', 'WebSite']
    with open(output, "a", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
        csv_writer.writeheader()
    def start_requests(self):

        default_url = "https://www.siborrealtors.com/agent/AgentSearch?page={0}&_keywordsAgentName=&_keywordsAll=&typeIn=Realtor%2CBroker%2COwner%2COffice%20Manager&searchMode=agent&sortOption=rndsrt&officeName=&officeLocation=&officeSortOption=name&_=156753251487{1}"

        for i in range(0, 118):  #118
            header = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Cookie': 'ASP.NET_SessionId=oexy1hdfqkbowtizmvqllc2g; BIGipServerPOOL-springweb-443=150999212.20480.0000; __utmc=67149331; __utmz=67149331.1567532462.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=9e50362ceb960952:T=1567532463:S=ALNI_MargSTWy6dxMytPgRXoTY3jb9d_8A; __utma=67149331.532846436.1567532462.1567538541.1567552497.4; __utmt=1; __utmb=67149331.1.10.1567552497',
                'Host': 'www.siborrealtors.com',
                'Referer': 'https://www.siborrealtors.com/agent/search?page={}'.format(i + 1),
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            url = default_url.format(i, i+1)
            response = requests.request("GET", url, headers=header)
            result = response.json()
            raw_data = result['data']

            for j in range(0, 20):
                first_url = "https://www.siborrealtors.com/profile/"
                agent_id = raw_data[j]['sysid']
                agentName = raw_data[j]['name']
                officeName = raw_data[j]['officename']

                # print("ID---------------------> : ", agent_id) 
                # print("AgentName--------------> : ", agentName) 
                # print("OfficeName-------------> : ", officeName) 
                
                data = {
                    "id"         : agent_id,
                    "agentName"  : agentName,
                    "officeName" : officeName 
                }
                agent_url = first_url + agent_id

                yield scrapy.Request(url=agent_url, callback=self.page_parse, meta=data)

                # return

    def page_parse(self, response):
        with open(self.output, "a", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            print("-------------Page Parse Start--------------")
            data = response.meta

            contact_labels = response.xpath("//dl[@class='dfn']//dt/text()")

            # contact_infos = response.xpath("//dl[@class='dfn]//dt/text()")
            officePhone = ""
            mobilePhone = ""
            email = ""
            webUrl = ""

            for i in range(0, len(contact_labels)):
                label = contact_labels[i].get().lower()
                if 'office' in label:
                    officePhone = response.xpath("//dl[@class='dfn']/dd[{}]/text()".format(i+1)).get()
                elif 'mobile' in label:
                    mobilePhone = response.xpath("//dl[@class='dfn']/dd[{}]/text()".format(i+1)).get()
                elif 'email' in label:
                    email = response.xpath("//dl[@class='dfn']/dd[{}]/a/@href".format(i+1)).get().replace("mailto:", "")
                elif 'web' in label:
                    webUrl = response.xpath("//dl[@class='dfn']/dd[{}]/a/@href".format(i+1)).get()
            print("------------------------------------------------")
            print("ID------------------------> : ", data['id'])
            print("AgentName-----------------> : ", data['agentName'])
            print("OfficeName----------------> : ", data['officeName'])
            print("OfficePhone---------------> : ", officePhone)
            print("MobilePhone---------------> : ", mobilePhone)
            print("Email---------------------> : ", email)
            print("WebSite-------------------> : ", webUrl)
            writer.writerow([data['agentName'], data['officeName'], officePhone, mobilePhone, email, webUrl])


        


    
