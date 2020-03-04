import pkg_resources
import yaml
from crontab import CronTab
#from . import config


def install():
    #smtp = config.settings['email_password'] or "email-smtp.eu-west-1.amazonaws.com";

    # Define settings array
    data = dict(email=dict(
        admin_email_address=input('Admin email address: '),
        account=input('Email account: '),
        password=input('Email pass: '),
        smtp=input('SMTP server: ') or "email-smtp.eu-west-1.amazonaws.com",
    ),
                device=dict(id=input('Pi ID: '), ),
                client=dict(
                    email=input('Client email: '),
                    instapy_id=input('InstaPy ID: ') or 1,
                ))

    # Open or create settings file and write to file
    with open(pkg_resources.resource_filename(__name__, "settings.yml"),
              'w+') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    cron = CronTab(user=True)
    cron.remove_all(
        command=
        'pip3 install git+https://github.com/mwargan/mmedia-rpi3-python-scripts.git'
    )
    cron.remove_all(
        command=
        'pip3 install git+https://github.com/mwargan/mmedia-rpi3-python-scripts.git -U'
    )
    job = cron.new(
        command=
        '/usr/bin/pip3 install git+https://github.com/M-Media-Group/mmedia-rpi3-python-scripts.git -U',
        comment='update_mmedia')
    job.setall('11 0 * * *')

    testjob = cron.new(command='m-test', comment='test_instagram_bot')
    testjob.setall('10 0 * * *')

    cron.write()
