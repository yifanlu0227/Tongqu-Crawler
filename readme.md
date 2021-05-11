# Tongqu & SEIEE Scholarship Crawler and Reminder

每天爬取最新同去网活动和电院学生办奖学金通知

# Update

[2021.5.11] 

1. 增加了对关键词的过滤。目前是“驾校”，可在crawler.py里自己增加
2. 运行到异常的时候也会发邮件。主要是同去网活动上标题若有英文双引号的时候会出问题orz。

# dependency

python 3

argparse 1.1

urllib 

lxml  4.5.2


# Usage 

1. Edit your SMTP server in mail.py, specfic your _username and _passwd.

2. use the crontab service of Linux/Unix

   `crontab -e`

   write command as crontab_config, for example, 

   `0 9 * * * /opt/anaconda3/bin/python /Users/luyifan/Code/Tongqu_Crawler/crawler.py -r "YOUR_EMAIL_ADDRESS"`

   It will send reminder email to "YOUR_EMAIL_ADDRESS" every 9 AM. 