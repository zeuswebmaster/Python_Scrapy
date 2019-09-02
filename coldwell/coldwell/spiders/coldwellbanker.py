# -*- coding: utf-8 -*-
import scrapy
import math
import csv
import win32api

base_url = "https://www.coldwellbankerhomes.com/sitemap/agents/"
nn = 0

class ColdwellbankerSpider(scrapy.Spider):
    name = 'coldwellbanker'
    # allowed_domains = ['coldwellbanker.com']
    # start_urls = base_url
    output = 'coldwellbankerhomes.csv'
    open(output, 'w').close()
    header = ['AgentName', 'Job Title', 'Office', 'Address', 'Email', 'MobilePhone', 'OfficePhone', 'DirectPhone', 'FaxPhone']
    with open(output, "a", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
        csv_writer.writeheader()

    def start_requests(self):
        print("-------------Start-------------")

        default_url = "https://www.coldwellbankerhomes.com/sitemap/new-york-agents/"

        yield scrapy.Request(url=default_url, callback=self.get_newyork)
    
    def get_newyork(self, response):
        item_urls = response.xpath("//tbody[@class='notranslate']//tr//a/@href").extract()
        agent_counts = response.xpath("//tbody[@class='notranslate']//tr//td[2]/text()").extract()
        print("----------------->", len(item_urls))

        first_url = "https://www.coldwellbankerhomes.com"
        
        for last_url, agent_count in zip(item_urls, agent_counts):
            url = first_url + last_url
            print("---", last_url, '----', agent_count)
            page_no = math.ceil(int(agent_count) / 26)

            for i in range(1, page_no + 1):
                default_url = url + "p_{}".format(i)
                # default_url = "https://www.coldwellbankerhomes.com/ny/astoria/agents/p_{}/".format(i)
                yield scrapy.Request(url=default_url, callback=self.get_agentUrl)
                # return
            # return
    def get_agentUrl(self, response):
        agent_urls = response.xpath("//div[contains(@class, 'agent-block') and contains(@class, 'col')]/a[1]/@href").extract()
        print("Agent------Counts------------->", len(agent_urls))
        for agent_url in agent_urls:
            default_url = "https://www.coldwellbankerhomes.com" + agent_url
            # print(default_url)
            
            yield scrapy.Request(url=default_url, callback=self.parse_agent)
            # return
    def parse_agent(self, response):
        global nn

        with open(self.output, "a", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            agentName = response.xpath("//h1[@id='main-content']/span/text()").get()
            jobTitle = response.xpath("//h2[@itemprop='jobTitle']/text()").get()
            raw_email = response.xpath("//div[@class='body']/text()").get()
            mobilePhone = response.xpath("//a[@data-phone-type='mobile']/text()").get()
            officePhone = response.xpath("//a[@data-phone-type='office']/text()").get()
            directPhone = response.xpath("//a[@data-phone-type='direct']/text()").get()
            faxPhone = response.xpath("//ul[@class='body']/li[4]//span/text()").get()

            office = response.xpath("//ul[contains(@class, 'body') and contains(@class, 'address-list')]/li/a/text()").get()
            raw_address = response.xpath("//ul[contains(@class, 'body') and contains(@class, 'address-list')]/li/span/text()").get().replace("\n", "")

            email = ''.join(raw_email).strip() if raw_email else ""
            address = ''.join(raw_address).strip() if raw_address else ""

            print("--------------------------------------------------", nn)
            print("Agent Name-------------------->  : ", agentName)
            print("Job Title--------------------->  : ", jobTitle)
            print("Email------------------------->  : ", email)
            print("Mobilephone------------------->  : ", mobilePhone)
            print("OfficePhone------------------->  : ", officePhone)
            print("DirectPhone------------------->  : ", directPhone)
            print("FaxPhone---------------------->  : ", faxPhone)
            print("Office------------------------>  : ", office)
            print("Address----------------------->  : ", address)

            nn = nn + 1

            writer.writerow([agentName, jobTitle, office, address, email, mobilePhone, officePhone, directPhone, faxPhone])
       








        
