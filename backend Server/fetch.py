from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import numpy as np
import re


def lat_lon(city):
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://www.google.com/maps')
        driver.find_element_by_xpath(
            "//input[@id='searchboxinput']").send_keys(city)
        driver.find_element_by_xpath(
            "//button[@id='searchbox-searchbutton']").click()
        sleep(5)
        url = driver.current_url
        url = (re.findall(r'@.+/', url)[0])[1:-1].split(',')
        lat = url[0][:-2]
        lon = url[1][:-2]
        driver.close()
        return lat, lon
    except Exception as e:
        print(e)
        driver.close()
        return -1


def search_buses(a, b, date, seats):
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://bus.makemytrip.com/bus/search/'+a+'/'+b+'/'+date)
        sleep(1)
        try:
            Gbuses = driver.find_element_by_xpath(
                "//a[@class='bluePrimarybtn font12']")
            if Gbuses != None:
                Gbuses.click()
            sleep(1)
        except:
            pass
        d = dict()
        timing_start = driver.find_elements_by_xpath(
            "//span[@class='sc-gqjmRU izTLmu']")
        timing_duration = driver.find_elements_by_xpath(
            "//span[@class='sc-jzJRlG btSGRi']")
        timing_end = driver.find_elements_by_xpath(
            "//span[@class='sc-fjdhpX laKnSQ']")
        names = driver.find_elements_by_xpath(
            "//span[@class='sc-chPdSV glJpds']")
        types = driver.find_elements_by_xpath(
            "//span[@class='sc-kgoBCf cQRYis']")
        #d['rating'] = driver.find_elements_by_xpath("//span[@class='sc-hSdWYo eXbDWv']")
        cost = driver.find_elements_by_xpath(
            "//span[@class='sc-brqgnP bKUXLW']")
        seats = driver.find_elements_by_xpath("//ul[@class='sc-dxgOiQ BhRgU']")
        #n_state_bus = len(driver.find_elements_by_xpath("//div[@class='sc-kTUwUJ dmMRtR']")[0].find_elements_by_xpath(".//*"))
        #n_pri_bus = len(driver.find_elements_by_xpath("//div[@class='sc-kTUwUJ dmMRtR']")[1].find_elements_by_xpath(".//*"))
        c, dd = [], []
        for i in cost:
            c.append(i.text)
        least = np.argmin(c)
        for k in timing_duration:
            z = k.text.split(' ')
            print(z)
            if len(z) == 1:
                if z[0][-1] == 'h':
                    dd.append(int(z[0][:-1])*60)
                else:
                    dd.append(int(z[1][:-1]))
            else:
                dd.append(int(z[0][:-1])*60+int(z[1][:-1]))
        l_d = np.argmin(dd)
        print(dd)
        for i in range(len(timing_duration)):
            d[str(i)] = [timing_start[i].text, timing_duration[i].text,
                         timing_end[i].text, names[i].text+types[i].text, cost[i].text, seats[i].text]
        driver.close()
        if d == {}:
            return -1
        else:
            return d[str(least)], d[str(l_d)]
    except Exception as e:
        print(e)
        return -1


def search_flights(a, b, date, seats):
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://www.goibibo.com/flights/air-' +
                   a[0][3]+'-'+b[0][3]+'-'+date+'--'+str(seats)+'-0-0-E-D/')
        print('https://www.goibibo.com/flights/air-' +
              a[0][3]+'-'+b[0][3]+'-'+date+'--'+str(seats)+'-0-0-E-D/')
        d = dict()
        timing_start = driver.find_elements_by_xpath(
            "//span[@class='fb ico18 padT5 quicks']")
        timing_duration = driver.find_elements_by_xpath(
            "//div[@class='ico15 fb txtCenter quicks padT5']")
        timing_end = driver.find_elements_by_xpath(
            "//span[@data-cy='arrTime']")
        names = driver.find_elements_by_xpath(
            "//span[@class='greyLt ico13 padR10 padL5']")
        cost = driver.find_elements_by_xpath(
            "//span[@class='ico20 fb quicks']")
        c, dd = [], []
        for i in cost:
            c.append(i.text)
        least = np.argmin(c)
        for k in timing_duration:
            z = k.text.split(' ')
            dd.append(int(z[0][:-1])*60+int(z[1][:-1]))
        l_d = np.argmin(dd)
        for i in range(len(timing_duration)):
            d[str(i)] = [timing_start[i].text, timing_duration[i].text,
                         timing_end[i].text, names[i].text, cost[i].text]
        driver.close()
        if d == {}:
            return -1
        else:
            return d[str(least)], d[str(l_d)]
    except Exception as e:
        print(e)
        return -1
