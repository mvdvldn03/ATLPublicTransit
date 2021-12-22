from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import random
import time

options = Options()
#options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")
userAgent = "____"
options.add_argument(f"user-agent={userAgent}")
driver = webdriver.Chrome(options=options, executable_path='./chromedriver')

def genAreas(csv):
    data = pd.read_csv(csv)
    areas = data['NEIGHBORHO'].tolist()
    return areas

def printTimes(list, reset_url):
    result = []
    index = 0
    for nsa in list:
        areas = nsa.split(",")
        average = 0.0
        counter = 0
        for area in areas:
            inttime = 0
            area = area.strip()

            try:
                time.sleep(2)
                inputElement = driver.find_element_by_xpath("//input[@class='tactile-searchbox-input']")
                inputElement.clear()
                inputElement.send_keys(f"{area} Atlanta, GA")
                time.sleep(3)
                driver.find_element_by_xpath("//div[@role='gridcell']").click()
                time.sleep(3)
                strtime = driver.find_element_by_xpath("//div[@id='section-directions-trip-0']").text
                strtime = ' '.join(' '.join(strtime.split(' ')).split('\n')).split()
                strtime = strtime[[i for i, n in enumerate(strtime) if n == 'AM'][1] - 1]
                strtime = strtime.split('—')[1].split(':')

                inttime += (int(strtime[0]) - 8) * 60
                inttime += int(strtime[1])

                average += inttime
                counter += 1
            except Exception as e:
                print(f"No route found for {area}")

                driver.get(reset_url)
            time.sleep(random.random() * 3)

        index += 1
        if(counter):
            result.append(average / counter)
            print(f"{index}, {average / counter}")
        else:
            result.append(0.0)
            print(f"{index},0.0")
    return result

def printDistance(list, reset_url):
    result = []
    index = 0
    for nsa in list:
        areas = nsa.split(",")
        average = 0.0
        counter = 0
        for area in areas:
            intdistance = 0.0
            area = area.strip()

            try:
                time.sleep(2)
                inputElement = driver.find_element_by_xpath("//input[@class='tactile-searchbox-input']")
                inputElement.send_keys(f"{area} Atlanta, GA")
                time.sleep(3)
                driver.find_element_by_xpath("//div[@role='gridcell']").click()
                time.sleep(3)
                strdistance = driver.find_element_by_xpath("//div[@id='section-directions-trip-0']").text
                strdistance = ' '.join(' '.join(strdistance.split(' ')).split('\n')).split()
                print(strdistance)

                if "mile" in strdistance:
                    intdistance += float(strdistance[strdistance.index("mile") - 1])
                if "miles" in strdistance:
                    intdistance += float(strdistance[strdistance.index("miles") - 1])

                average += intdistance
                counter += 1
            except Exception as e:
                print(f"No route found for {area}")

                driver.get(reset_url)
                inputElement = driver.find_element_by_xpath("//input[@class='tactile-searchbox-input']")

            time.sleep(2)
            inputElement.clear()

        index += 1
        try: new = round(average / counter, 4)
        except: new = 0.0

        print(f"{index},{new}")
    return result

if __name__ == '__main__':
    neighborhoods = genAreas("City_of_Atlanta_Neighborhood_Statistical_Areas.csv")

    reset_url = "https://www.google.com/maps/dir/Brookhaven,+GA/Downtown+Atlanta,+Atlanta,+GA/@33.8104311,-84.3980103,13z/data=!3m1!4b1!4m18!4m17!1m5!1m1!1s0x88f5089505f9f565:0x851a6587d0c37ec1!2m2!1d-84.3371266!2d33.8650186!1m5!1m1!1s0x88f5038740415b5d:0xa005d8181c4268d8!2m2!1d-84.3883717!2d33.755711!2m3!6e0!7e2!8j1639728000!3e3"
    driver.get(reset_url)

    #distance = printDistance(neighborhoods, reset_url)
    time = printTimes(neighborhoods, reset_url)
    #print(distance)
    print(time)
