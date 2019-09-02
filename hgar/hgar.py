# import selenium
# from selenium import webdriver
# from selenium.webdriver import Chrome
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait as wait
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
import time
import os
import requests, json, csv



def main():

    open("hgar.csv", "w").close()

    header = ['FirstName', 'LastName', 'FullName', 'OfficeName', 'Address', 'County', 'State', 'Postal', 'Email', 'Fax', 'OfficePhone', 'PreferredPhone', 'OrigninatingSystemName', 'SourceSystemName', 'WebsiteUrl']

    with open("hgar.csv", "a", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames = header, lineterminator='\n')
        csv_writer.writeheader()

    headers1 = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'application-key': 'c0c73351-c4cf-4f32-9d49-8ad11c9d6b60',
        'application-org': 'HGAR',
        'Authorization': 'Bearer e1fe57d2-665f-11e7-907b-a6006ad3dba0',
        'Origin': 'https://www.hgar.com',
        'Referer': 'https://www.hgar.com/directory',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    headers2 = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'application-key': 'c0c73351-c4cf-4f32-9d49-8ad11c9d6b60',
        'application-org': 'HGAR',
        'cookie': 'PHPSESSID=t3lhaa6tljjt6cagv9vmahj63j; _ga=GA1.2.1454837322.1567379561; _gid=GA1.2.2126064532.1567379561; _fbp=fb.1.1567379568810.1145815588; _gat_aa=1; _gat=1',
        'referer': 'https://www.hgar.com/real-estate-office/187-realty-corp./187RTC',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    for i in range(0, 481):  #481

        
        url = 'https://mls-search.memb.io/v1/hgmls/offices?offset={}&limit=100&sortBy=OfficeName&order=asc&searchBy=office&OfficeStatus=Active'.format(i*100)
        
        second_f_url = "https://www.hgar.com/search/api/office/render/"
        response = requests.request("GET", url, headers=headers1)
        result = response.json()
        raw_data = result['bundle']
        # print(len(raw_data))

        for j in range(0, len(raw_data)):   #len(raw_data)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&------->", i)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$----->", j)
            officeAddress         = raw_data[j]['OfficeAddress1']
            officeName            = raw_data[i]['OfficeName']
            officeCountyOrParish  = raw_data[j]['OfficeCountyOrParish']
            officeStateOrProvince = raw_data[j]['OfficeStateOrProvince']
            officePostalCode      = raw_data[j]['OfficePostalCode']
            officeMlsId           = raw_data[j]['OfficeMlsId']

            # print("OfficeAddress1---------------------> : ", officeAddress)
            # print("OfficeName-------------------------> : ", officeName)
            # print("OfficeCountyOrParish---------------> : ", officeCountyOrParish)
            # print("OfficeStateOrProvince--------------> : ", officeStateOrProvince)
            # print("OfficePostalCode-------------------> : ", officePostalCode)
            # print("OfficeMlsId------------------------> : ", officeMlsId)

            data = {
                'address'      : officeAddress,
                'officeName'   : officeName,
                'officeCounty' : officeCountyOrParish,
                'officeState'  : officeStateOrProvince,
                'officePostal' : officePostalCode,
                'officeMlsId'  : officeMlsId
            }

            second_url = second_f_url + data['officeMlsId']
            
            response1 = requests.request("GET", second_url, headers=headers2)
            agent_result = response1.json()
            agent_data = agent_result['Agents']
            # print(len(agent_data))

            agent_scrapy(agent_data, data)

def agent_scrapy(agentData, data):
    print("##############################", len(agentData), data)
    with open("hgar.csv", 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for n in range(0, len(agentData)):
            
            # className = agentData[n]['MemberMlsSecurityClass']
            
            try:
                email          = agentData[n]['MemberEmail']
            except:
                email = ""
            try:
                firstName      = agentData[n]['MemberFirstName'] 
            except:
                firstName = "Non-Member"
            try:
                secondName     = agentData[n]['MemberLastName'] 
            except:
                secondName = "Non-Member"
            fullName       = agentData[n]['MemberFullName']
            fax            = agentData[n]['MemberFax']
            officePhone    = agentData[n]['MemberOfficePhone']
            preferredPhone = agentData[n]['MemberPreferredPhone']
            originatingSystemName = agentData[n]['OriginatingSystemName']
            sourceSystemName = agentData[n]['SourceSystemName']
            try:
                websiteUrl     = agentData[n]['SocialMediaOrWebsiteUrl']
            except:
                websiteUrl = ""
            print("---------------------------------------------------------")
            print("Email------------------------> : ", data['officeMlsId'])
            print("Email------------------------> : ", email)
            print("firstName--------------------> : ", firstName)
            print("secondName-------------------> : ", secondName)
            print("fullName---------------------> : ", fullName)
            print("fax--------------------------> : ", fax)
            print("officePhone------------------> : ", officePhone)
            print("preferredPhone---------------> : ", preferredPhone)
            print("originatingSystemName--------> : ", originatingSystemName)
            print("sourceSystemName-------------> : ", sourceSystemName)
            print("WebsiteUrl-------------------> : ", websiteUrl)

            writer.writerow([firstName, secondName, fullName, data['officeName'], data['address'], data['officeCounty'], data['officeState'], data['officePostal'], email, fax, officePhone, preferredPhone, originatingSystemName, sourceSystemName, websiteUrl])




if __name__ == "__main__":
    print("---------------scray start------------------")
    main()