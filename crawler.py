# coding=utf-8
from urllib.request import Request,urlopen
from lxml import etree
from mail import Email
from datetime import timedelta,datetime
import argparse

def crawl_tongqu(show_act=7):
    req = Request('https://tongqu.sjtu.edu.cn/act/type?type=-1', headers={'User-Agent': 'Mozilla/5.0'})
    html_doc = urlopen(req).read().decode()
    selector = etree.HTML(html_doc)
    act_script = selector.xpath("/html/body/script[2]")[0]
    act_all = act_script.text.replace("\/","/").strip().encode("utf-8").decode("unicode_escape")
    act_new_begin = act_all.find("g_init_type_acts")
    act_new_end = act_all.find(";var g_acts_recommend")
    act_new = act_all[act_new_begin+len("g_init_type_acts = "):act_new_end]
    null = None

    dict_all = eval(act_new)
    dict_act = dict_all["acts"]

    mail_context = "<h1>TONGQU ACTIVITY REMINDER</h1><br>\r\n\r\n"
    for i in range(min(show_act,10)):
        act = dict_act[i]
        act_id = act["actid"]
        act_url = "<b>[Link]</b>: https://tongqu.sjtu.edu.cn/act/" + act_id
        act_name = "<b>活动{}：".format(i+1) + act["name"] + "</b>"
        # act_time = "<b>[Time]</b>:" + act["start_time"] + " -> " + act["end_time"]
        act_member = "<b>[Member]</b>: " + act["member_count"] + "/" + act["max_member"]
        act_url_and_member = act_url+ " &nbsp;&nbsp; " +act_member
        
        act_all = [act_name,act_url_and_member,"<br>\r\n"]
        mail_context += "<br>\r\n".join(act_all)

    mail_context += "<br>"
    return mail_context

def crawl_scholarship(show_li=5):
    req = Request('http://xsb.seiee.sjtu.edu.cn/xsb/list/611-1-20.htm', headers={'User-Agent': 'Mozilla/5.0'})
    html_doc = urlopen(req).read().decode()
    selector = etree.HTML(html_doc)
    scholarship_ul = selector.xpath('//*[@id="layout11"]/div/div[2]/ul')[0]
    scholarship_lis = scholarship_ul.getchildren()[3:3+show_li]
    mail_context = "<h1>NEW SCHOLARSHIP REMINDER</h1><br>\r\n\r\n"
    new_term = False
    for scholarship_li in scholarship_lis:
        date,hyper = scholarship_li.getchildren()
        title = hyper.get("title")
        if(date.text == datetime.today().strftime("[%Y-%m-%d]") or date.text ==(datetime.today()+timedelta(-1)).strftime("[%Y-%m-%d]")):
            new_term = True
            title = "🆕" + title
            title = date.text + " " + title
            link = "http://xsb.seiee.sjtu.edu.cn" + hyper.get("href")
            mail_context += "<br>\r\n".join([title,link,'\r\n'])
    if not new_term:
        mail_context += "No new schoarship today & yesterday. <br>\r\n You may want visit http://xsb.seiee.sjtu.edu.cn/xsb/list/611-1-20.htm"

    mail_context += "<br>"
    return mail_context
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tongqu Crawler")
    parser.add_argument("-r","--recipient",type=str,default="yifan_lu@sjtu.edu.cn")
    args = parser.parse_args()

    msg1 = crawl_tongqu()
    msg2 = crawl_scholarship()
    email = Email(recipient=args.recipient,text=msg1+msg2)