# Tongqu & SEIEE Scholarship Crawler and Reminder

每天爬取最新同去网活动和电院学生办奖学金通知

# dependency

python 3.+

argparse

urllib

lxml


# Usage 

1. Edit your SMTP server in mail.py, specfic your _username and _passwd.

2. use the crontab service of Linux/Unix

   `crontab -e`

   write command as crontab_config, for example, 

   `0 9 * * * /opt/anaconda3/bin/python /Users/luyifan/Code/Tongqu_Crawler/crawler.py -r "YOUR_EMAIL_ADDRESS"`

   It will send reminder email to "YOUR_EMAIL_ADDRESS" every 9 AM. 




