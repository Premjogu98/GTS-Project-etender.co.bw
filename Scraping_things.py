import re
import time
import sys , os
import string
from datetime import datetime,timedelta
import global_var
import requests
import html
from Insert_On_Datbase import insert_in_Local
import wx
import html
app = wx.App()


def Scrap_data(get_htmlSource,company,category,Tender_number,Tender_title,Due_date,Open_tender_link,Posted_date):

    SegFeild = []
    for data in range(42):
        SegFeild.append('')
    
    a = True
    while a == True:
        try:
            Email_List = []
            Email_regex = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]+)", get_htmlSource)
            for Email in Email_regex:
                Extension = ['.jpeg', '.png', '.io', '.xls', 'xyz.com', '.doc', '.jpeg', '.pdf', '.gif', '.jpg',
                                'example', 'facebook', 'test@', 'test', 'amazon', 'naukri', 'wikipedia', 'tenders',
                                'tender']
                if not any(x in Email_regex for x in Extension):
                    if Email not in Email_List:
                        Email = Email.replace('%20', '').replace("%27", '').replace("mailto:%0", '').replace(
                            '<!--', '').replace('-->', '').replace('email:-', '').replace('mailto:', '').replace('mailto:%20', '').replace('mailto:%27', '').replace('--','')
                        Email_List.append(Email)
                        break
                break
            if Email_List != '':
                Email_List = str(Email_List).replace('[', '').replace(']', '').replace("'", "")
                SegFeild[1] = Email_List
            SegFeild[2] = 'Botswana<br>\n[Disclaimer : For Exact Organization/Tendering Authority details, please refer the tender notice.]'
            SegFeild[12] = company.upper()
            SegFeild[13] = Tender_number

            Tender_title = string.capwords(str(Tender_title))
            SegFeild[19] = Tender_title
            
            SegFeild[24] = Due_date
            
            Desc = f'{Tender_title}<br>\nTender Number:{Tender_number}<br>\nTender Category: {category}<br>\nComapny: {company}<br>\nPosted Date: {Posted_date}'
            Desc = string.capwords(str(Desc))
            SegFeild[18] = Desc
            SegFeild[7] = "BW"

            SegFeild[14] = "2"

            SegFeild[22] = "0"

            SegFeild[26] = "0.0"

            SegFeild[27] = "0" # Financier

            SegFeild[28] = Open_tender_link

            # Source Name
            SegFeild[31] = 'etender.co.bw'

            for SegIndex in range(len(SegFeild)):
                print(SegIndex, end=' ')
                print(SegFeild[SegIndex])
                SegFeild[SegIndex] = html.unescape(str(SegFeild[SegIndex]))
                SegFeild[SegIndex] = str(SegFeild[SegIndex]).replace("'", "''")

            if len(SegFeild[19]) >= 200:
                SegFeild[19] = str(SegFeild[19])[:200]+'...'

            if len(SegFeild[18]) >= 1500:
                SegFeild[18] = str(SegFeild[18])[:1500]+'...'
            check_date(get_htmlSource, SegFeild)
            a = False

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = True


def check_date(get_htmlSource, SegFeild):
    deadline = str(SegFeild[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                insert_in_Local(get_htmlSource, SegFeild)
            else:
                print("Expired Tender")
                global_var.expired += 1
        else:
            print("Deadline Not Given")
            global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)