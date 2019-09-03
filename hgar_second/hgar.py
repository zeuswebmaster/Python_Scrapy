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

    header = ['FirstName', 'LastName', 'FullName', 'OfficeName', 'OfficePhone', 'PreferredPhone']

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


    for i in range(0, 482): 
        url = 'https://mls-search.memb.io/v1/hgmls/agents?access_token=e1fe57d2-665f-11e7-907b-a6006ad3dba0&offset={}&limit=100&sortBy=MemberLastName&order=asc&searchBy=agent&MemberStatus=Active'.format(i*100)
        
        
        response = requests.request("GET", url, headers=headers1)
        result = response.json()
        raw_data = result['bundle']
        # print(len(raw_data))

        with open("hgar.csv", 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
        
            for j in range(0, len(raw_data)):   #len(raw_data)
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&------->", i)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$----->", j)
                try:
                    firstName      = raw_data[j]['MemberFirstName'] 
                except:
                    firstName = ""
                try:
                    secondName     = raw_data[j]['MemberLastName'] 
                except:
                    secondName = ""
                try:
                    officeName = raw_data[j]['OfficeName']
                except:
                    officeName = ""
                try:
                    fullName       = raw_data[j]['MemberFullName']
                except:
                    fullName = ""
                officePhone    = raw_data[j]['MemberOfficePhone']
                preferredPhone = raw_data[j]['MemberPreferredPhone']

                print("------------------------------------------------")
                
                print("firstName--------------------> : ", firstName)
                print("secondName-------------------> : ", secondName)
                print("fullName---------------------> : ", fullName)
                print("officePhone------------------> : ", officePhone)
                print("preferredPhone---------------> : ", preferredPhone)
                print("officeName-------------------> : ", officeName)
                
                writer.writerow([firstName, secondName, fullName, officeName, officePhone, preferredPhone])


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