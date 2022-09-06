import imaplib
import configparser
import email
import os
import re

incoming_mail_server = ''
outgoing_mail_server = ''
mail_login = ''
mail_password = ''
white_list = []

def read_config():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config.ini")

    if not os.path.exists(config_path):
        print("Config not found! Exiting!")
        sys.exit(1)
    else:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('config.ini', encoding='utf-8-sig')
        global incoming_mail_server
        global outgoing_mail_server
        global mail_login
        global mail_password
        global white_list
        incoming_mail_server = config.get('mymail', 'in_mail')
        outgoing_mail_server = config.get('mymail', 'out_mail')
        mail_login = config.get('mymail', 'user')
        mail_password = config.get('mymail', 'password')
        raw_white_list = config.items('whitelist')
        for i in range(len(raw_white_list[0]) + 1):
            white_list.append(raw_white_list[i][0])
        print(white_list)

def allow_access(mail_address,ip_address):



def get_mail():

    mail = imaplib.IMAP4_SSL(incoming_mail_server)
    mail.login(mail_login, mail_password)
    mail.list()
    mail.select("inbox")

    (retcode, messages) = mail.search(None, '(UNSEEN)')
    if retcode == 'OK':

        for num in messages[0].split():
            typ, data = mail.fetch(num, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    raw_email = data[0][1]
                    raw_email_string = raw_email.decode('utf-8')
                    email_message = email.message_from_string(raw_email_string)
                    (real_name, mail_address) = email.utils.parseaddr(email_message['From'])
                    if mail_address in white_list:
                        email_message = email.message_from_string(raw_email_string)
                        if email_message.is_multipart():
                            for payload in email_message.get_payload():
                                body = payload.get_payload(decode=True).decode('utf-8')
#                                print(body)
                        else:
                            body = email_message.get_payload(decode=True).decode('utf-8')
#                            print(body)
                        ip_address = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', body).group()
                        print(ip_address)
                        allow_access(mail_address,ip_address)


    mail.close()
    mail.logout()


if __name__ == '__main__':
    read_config()
    get_mail()
