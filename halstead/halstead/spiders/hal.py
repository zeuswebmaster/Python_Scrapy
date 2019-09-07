# -*- coding: utf-8 -*-
import scrapy
import math
import csv
import win32api


class HalSpider(scrapy.Spider):
    name = 'hal'
    output = 'halstead.csv'
    header = ['AgentName', 'Office', 'Job Title', 'Email', 'Tel', 'Cell']
    with open(output, "a", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
        csv_writer.writeheader()

    def start_requests(self):
        default_url = "https://www.halstead.com/new-york-city-agents/page-{}/"

        for i in range(1, 37):
            url = default_url.format(i)

            yield scrapy.Request(url=url, callback=self.get_agent)
            # return

    def get_agent(self, response):
        print("_________________PARSE START_________________")

        agentUrls = response.xpath("//div[@class='agent-card']/a[1]/@href").extract()

        for agentUrl in agentUrls:
            agentUrl = "https://www.halstead.com" + agentUrl
            print("agentUrl------------> : ", agentUrl)

            yield scrapy.Request(url=agentUrl, callback=self.parse_page)
            # return

    def parse_page(self, response):
        with open(self.output, "a", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            tel = ""
            cell = ""

            agentName = response.xpath("//div[@class='agent-profile-info']/h2/text()").get()

            officeInfos = response.xpath("//p[@class='agent-title']/span//text()").extract()

            office = officeInfos[1].replace("\r", "")
            print(office)
            jobTitle = officeInfos[0]

            email = response.xpath("//p[@class='agent-detail']/a/text()").get()

            phone_infos = response.xpath("(//p[@class='agent-detail'])[2]/text()").extract()
            print(phone_infos)

            for phoneNumber in phone_infos:
                if 'Tel' in phoneNumber:
                    tel = phoneNumber.replace("Tel: ", "")
                elif 'Cell' in phoneNumber:
                    cell = (phoneNumber.replace("\r", "")).replace("Cell: ", "")

            print("---------------------    -------------------------")
            print("AgentNames--------------------> : ", agentName)
            print("office name-------------------> : ", office)
            print("JotTitle----------------------> : ", jobTitle)
            print("Email-------------------------> : ", email)
            print("Tel---------------------------> : ", tel)
            print("Cell--------------------------> : ", cell)

            writer.writerow([agentName, office, jobTitle, email, tel, cell])

