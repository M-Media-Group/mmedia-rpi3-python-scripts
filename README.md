# M Media scripts

Scripts I use at my company. Included is a script to check space on SD and temperature and email data to admin on a Raspberry Pi, and a script to generate and email an Excel workbook from InstaPy logs.

## Install
Install with
`pip3 install git+https://github.com/mwargan/mmedia-rpi3-python-scripts.git`. Just add ` -U` to update.

The script will automatically install InstaPy and the correct chromedriver.

## Use
**Get a boot-report** by typing in `boot-checkin` in a CLI.

Add it to systemd with `ExecStartPre=/usr/bin/python3 /home/pi/.local/bin/boot-checkin`.

To **get an InstaPy report**, run `m-insta-report` in the CLI. The program will automatically use your default workspace path to get log data from the database.

## Config
On the first run of any of the above you'll be prompted with questions to fill in the following settings:
```
client:
  email: 
  instapy_id: 1
device:
  id: 
email:
  admin_email_address: 
  account: 
  password: 
  from_email_address: 
  smtp: email-smtp.eu-west-1.amazonaws.co
```
By deafult the SMTP is set to an AWS SES endpoint and the InstaPy ID is set to 1. Otherwise all other details must be filled in and you'll be asked for each. If you mess up, you can run `m-install` to restart.
- Client email is the clients email - they'll recieve reports and notifications here
- Client instapy_id is the ID in the InstaPy database (if only 1 account has ever run instapy on a given machine, its usually 1)
- Device ID, something like Pi_009
- Admin email address: admins email for reports and notifications
- Account: IAM SES account (or SMTP email address)
- Password IAM SES password (or SMTP password)
- From email address: which address the bot is sending emails from
- SMTP endpoint

## Contribute
Yes, please! :)