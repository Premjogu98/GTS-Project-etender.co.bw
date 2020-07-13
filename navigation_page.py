
from selenium import webdriver
import time
import global_var
import html
from Scraping_things import Scrap_data
from datetime import datetime
import sys
import os
import wx
import urllib.request
import urllib.parse
import requests
import html
import re
app = wx.App()


def ChromeDriver():
    browser = webdriver.Chrome(executable_path='C:\\chromedriver.exe')
    browser.maximize_window()
    url_list = ['https://etender.co.bw/opentenders','https://etender.co.bw/opentendersc']
    
    first_url(url_list[0],browser)
    second_url(url_list[1],browser)
    wx.MessageBox(f'Total: {str(global_var.Total)}\nDeadline Not given: {global_var.deadline_Not_given}\nduplicate: {global_var.duplicate}\ninserted: {global_var.inserted}\nexpired: {global_var.expired}\nQC Tenders: {global_var.QC_Tenders}','etender.co.bw', wx.OK | wx.ICON_INFORMATION)

def first_url(url,browser):
    browser.get(url)
    time.sleep(2)
    wx.MessageBox(' See IF Webpage Load Poperly Then Click on OK BUTTON ','etender.co.bw', wx.OK | wx.ICON_WARNING)
    time.sleep(2)
    for dropdown in browser.find_elements_by_xpath('//*[@id="DataTables_Table_0_length"]/label/select/option[3]'):
        dropdown.click()
        break
    time.sleep(5)

    tender_count = ''
    for tender_count in browser.find_elements_by_xpath('//*[@id="DataTables_Table_0_info"]'):
        tender_count = tender_count.get_attribute('innerText').strip()
        tender_count = tender_count.partition("of")[2].partition("entri")[0].strip()  # Showing 1 to 26 of 26 entries
        break
    for tr in range(1, int(tender_count) + 1, 1):
        main_loop = True
        while main_loop == True:
            try:
                company = ''
                category = ''
                Tender_number = ''
                Tender_title = ''
                Due_date = ''
                Open_tender_link = ''
                for company in browser.find_elements_by_xpath(f'//*[@id="DataTables_Table_0"]/tbody/tr[{str(tr)}]/td[2]'):
                    company = company.get_attribute('innerText').strip()
                    # print(company)
                    break
                for category in browser.find_elements_by_xpath(f'//*[@id="DataTables_Table_0"]/tbody/tr[{str(tr)}]/td[3]'):
                    category = category.get_attribute('innerText').strip()
                    # print(category)
                    break
                for Tender_number in browser.find_elements_by_xpath(f'//*[@id="DataTables_Table_0"]/tbody/tr[{str(tr)}]/td[4]'):
                    Tender_number = Tender_number.get_attribute('innerText').strip()
                    # print(Tender_number)
                    break
                for Tender_title in browser.find_elements_by_xpath(f'//*[@id="DataTables_Table_0"]/tbody/tr[{str(tr)}]/td[5]'):
                    Tender_title = Tender_title.get_attribute('innerText').strip()
                    # print(Tender_title)
                    break
                for Due_date in browser.find_elements_by_xpath(f'//*[@id="DataTables_Table_0"]/tbody/tr[{str(tr)}]/td[6]'):
                    Due_date = Due_date.get_attribute('outerHTML').strip()
                    Due_date = Due_date.partition('<td>')[2].partition('<br>')[0].strip()
                    try:
                        Due_date = datetime.strptime(Due_date, '%Y-%m-%d')
                        Due_date = Due_date.strftime("%Y-%m-%d")
                        # print(Due_date)
                    except:
                        wx.MessageBox(' Error On Date Formate Of Due_date -_- ', 'etender.co.bw', wx.OK | wx.ICON_ERROR)
                        print('Error On Date Formate Of Due_date')
                    break
                for Open_tender_link in browser.find_elements_by_xpath(f'//*[@id="DataTables_Table_0"]/tbody/tr[{str(tr)}]/td[7]/a'):
                    Open_tender_link = Open_tender_link.get_attribute('href').strip()
                    # print(Open_tender_link)
                    break
                loop = True
                while loop == True:
                    try:
                        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
                        headers = {'User-Agent': user_agent, }
                        request = urllib.request.Request(Open_tender_link, None, headers)  # The assembled request
                        response = urllib.request.urlopen(request)
                        time.sleep(2)
                        htmldata: str = response.read().decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
                        get_htmlsource = htmldata.partition('<div class="page">')[2].partition('<footer class="site-footer">')[0].strip()
                        get_htmlsource = html.unescape(str(get_htmlsource))
                        if get_htmlsource == '':
                            wx.MessageBox(' get_htmlsource variable null -_- ', 'etender.co.bw', wx.OK | wx.ICON_ERROR)
                        get_htmlsource = '<div class="page">' + get_htmlsource

                        Posted_date = get_htmlsource.partition('Date Posted:')[2].partition('<br>')[0].strip()

                        Scrap_data(get_htmlsource,company,category,Tender_number,Tender_title,Due_date,Open_tender_link,Posted_date)

                        print(f'Total: {str(tender_count)} Deadline Not given: {global_var.deadline_Not_given} duplicate: {global_var.duplicate} inserted: {global_var.inserted} expired: {global_var.expired} QC Tenders: {global_var.QC_Tenders}')
                        loop = False
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                            exc_tb.tb_lineno)
                        time.sleep(10)
                        loop = True
                        main_loop = False
                main_loop = False
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                    exc_tb.tb_lineno)
                time.sleep(10)
                main_loop = True


def second_url(url,browser):
    browser.get(url)
    time.sleep(2)
    wx.MessageBox(' See IF Webpage Load Poperly Then Click on OK BUTTON ','etender.co.bw', wx.OK | wx.ICON_WARNING)
    time.sleep(2)
    for dropdown in browser.find_elements_by_xpath('//*[@id="DataTables_Table_0_length"]/label/select/option[4]'):
        dropdown.click()
        break
    time.sleep(5)
    
    tender_count = ''
    for tender_count in browser.find_elements_by_xpath('//*[@id="DataTables_Table_0_info"]'):
        tender_count = tender_count.get_attribute('innerText').strip()
        tender_count = tender_count.partition("of")[2].partition("entri")[0].strip()  # Showing 1 to 26 of 26 entries
        break

    for tr in range(1, int(tender_count)+1, 1):
        main_loop = True
        while main_loop == True:
            try:
                xpath = ''
                if tender_count == '1':
                    xpath = f'//*[@id="DataTables_Table_0"]/tbody/tr'
                else:
                    xpath = f'//*[@id="DataTables_Table_0"]/tbody/tr[{str(tr)}]'
                company = ''
                category = ''
                Tender_number = ''
                Tender_title = ''
                Due_date = ''
                Open_tender_link = ''
                for company in browser.find_elements_by_xpath(f'{xpath}/td[2]'):
                    company = company.get_attribute('innerText').strip()
                    # print(company)
                    break
                for category in browser.find_elements_by_xpath(f'{xpath}/td[3]'):
                    category = category.get_attribute('innerText').strip()
                    # print(category)
                    break
                for Tender_number in browser.find_elements_by_xpath(f'{xpath}/td[4]'):
                    Tender_number = Tender_number.get_attribute('innerText').strip()
                    # print(Tender_number)
                    break
                for Tender_title in browser.find_elements_by_xpath(f'{xpath}/td[5]'):
                    Tender_title = Tender_title.get_attribute('innerText').strip()
                    # print(Tender_title)
                    break
                for Due_date in browser.find_elements_by_xpath(f'{xpath}/td[6]'):
                    Due_date = Due_date.get_attribute('outerHTML').strip()
                    Due_date = Due_date.partition('<td>')[2].partition('<br>')[0].strip()
                    try:
                        Due_date = datetime.strptime(Due_date, '%Y-%m-%d')
                        Due_date = Due_date.strftime("%Y-%m-%d")
                        # print(Due_date)
                    except:
                        wx.MessageBox(' Error On Date Formate Of Due_date -_- ', 'etender.co.bw', wx.OK | wx.ICON_ERROR)
                        print('Error On Date Formate Of Due_date')
                    break
                for Open_tender_link in browser.find_elements_by_xpath(f'{xpath}/td[7]/a'):
                    Open_tender_link = Open_tender_link.get_attribute('href').strip()
                    # print(Open_tender_link)
                    break

                loop = True
                while loop == True:
                    try:
                        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
                        headers = {'User-Agent': user_agent, }
                        request = urllib.request.Request(Open_tender_link, None, headers)  # The assembled request
                        response = urllib.request.urlopen(request)
                        time.sleep(2)
                        htmldata: str = response.read().decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
                        get_htmlsource = htmldata.partition('<div class="page">')[2].partition('<footer class="site-footer">')[0].strip()
                        get_htmlsource = html.unescape(str(get_htmlsource))
                        if get_htmlsource == '':
                            wx.MessageBox(' get_htmlsource variable null -_- ', 'etender.co.bw', wx.OK | wx.ICON_ERROR)
                        get_htmlsource = '<div class="page">' + get_htmlsource

                        Posted_date = get_htmlsource.partition('Date Posted:')[2].partition('<br>')[0].strip()

                        Scrap_data(get_htmlsource,company,category,Tender_number,Tender_title,Due_date,Open_tender_link,Posted_date)
                        print(f'Total: {str(tender_count)} Deadline Not given: {global_var.deadline_Not_given} duplicate: {global_var.duplicate} inserted: {global_var.inserted} expired: {global_var.expired} QC Tenders: {global_var.QC_Tenders}')
                        loop = False
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                            exc_tb.tb_lineno)
                        time.sleep(10)
                        loop = True
                main_loop = False
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                    exc_tb.tb_lineno)
                time.sleep(10)
                main_loop = True
        


ChromeDriver()
