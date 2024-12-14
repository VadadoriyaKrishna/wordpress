# this file use for load mails from mailbox , take response from LSTM model(.h5) , save data in database , attachments in local

from flask import Flask, jsonify, request
from flask_cors import CORS
import yaml
import os
import mysql.connector as M
from datetime import datetime, timedelta
from imap_tools import MailBox, AND
from mail_bifurcation import GetPredictionByModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app,origins=["http://localhost"])

# Database connection
conn = M.connect(host='localhost', username='phpmyadmin', password='root123', database='E-Insurance')
curr = conn.cursor()
conn.commit()

@app.route('/', methods=['GET'])
def fetch_emails():
    now = datetime.now()
    #delta = timedelta(minutes=10)          #change this according to duration  (untill 10 Minutes data)
    delta = timedelta(minutes=3000)

    start_time = now - delta
    end_time = now

    start_time_date = start_time.date()
    end_time_date = end_time.date()

    with open("credential.yml") as file:
        content = file.read()

    cred = yaml.load(content, Loader=yaml.FullLoader)
    my_mail_id, password = cred["user"], cred["pass"]
    login_platform = "imap.gmail.com"

    mailBox = MailBox(login_platform).login(my_mail_id, password)

    emails = []
    attachment_dir = "attachments"
    if not os.path.exists(attachment_dir):
        os.makedirs(attachment_dir)

    extension_tags = [".jpeg", ".png", ".py", ".php", ".txt", ".html", ".pdf",".h5"]
    #for i, msg in enumerate(mailBox.fetch(criteria=AND(date_gte=start_time_date, date_lt=end_time_date)), start=1):
    for i, msg in enumerate(mailBox.fetch(criteria=AND(date=now.date())), start=1):
        email_info = {
            "id": i,
            "Sender_id": msg.from_,
            "name": msg.from_values.name,
            "Reciever_id": msg.to,
            "subject": msg.subject,
            "date": msg.date_str,
            "body": msg.text,
            "attachments": []     #only save file path in this key
        }

        for att in msg.attachments:                             #attachment save in a local
            attachment_filename = att.filename
            print(attachment_filename)
            print('***********')


            filename_without_spaces_dashes = att.filename.replace(' ','_').replace('-','_')
            current_date = datetime.now().strftime('%d%m%y')
            attachment_filename = f"{os.path.splitext(filename_without_spaces_dashes)[0]}_{current_date}{os.path.splitext(filename_without_spaces_dashes)[1]}"

            print("new_filename")
            print(attachment_filename)
            print('***********')
 
            attachment_extension = os.path.splitext(attachment_filename)[1].lower()
            
            if attachment_extension in extension_tags:
                attachment_dir1 = os.path.join(attachment_dir, attachment_extension[1:])
            else:
                attachment_dir1 = attachment_dir
            
            if not os.path.exists(attachment_dir1):
                os.makedirs(attachment_dir1)
            
            file_path = os.path.join(attachment_dir1, attachment_filename)
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(att.payload)
                email_info["attachments"].append(file_path)
        emails.append(email_info)

    query1 = """CREATE TABLE IF NOT EXISTS mails (
      Id INT AUTO_INCREMENT PRIMARY KEY,
      sender_id VARCHAR(50),
      receiver_id VARCHAR(50), 
      subject varchar(200) DEFAULT NULL,
      mail_body longtext DEFAULT NULL,
      type VARCHAR(25),
      flag INT,
      attachment text(100),
      mail_time VARCHAR(100),
      storing_time DATETIME
    )"""
    curr.execute(query1)
    conn.commit()

    for email in emails:
        time = datetime.now()
        mail_text1 = f"{email['subject']} - {email['body']}"
        mail_text = mail_text1.replace('\n', ' ')
        #type_of_mail = GetPredictionByModel(mail_text)       # function fetch from mail_bifurcation.py
        type_of_mail = "Claim"
        query = """ INSERT INTO mails (
                sender_id, receiver_id,subject,mail_body, type,flag, attachment, mail_time, storing_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        flag = 1 if len(email["attachments"]) > 0 else 0   #use for attachments 0 means no and 1 means yes
        
        val = (email["Sender_id"], email["Reciever_id"][0],email['subject'],email['body'], type_of_mail, flag, ','.join(email["attachments"]), email["date"], time)# receiver id return one tuple like bc /bcc
        curr.execute(query, val)         #pass value in insert query
        conn.commit()
        delete_query = ''' DELETE t1 FROM mails t1        # multiline string
                        INNER JOIN mails t2
                        WHERE 
                        t1.Id > t2.Id AND 
                        t1.sender_id = t2.sender_id AND 
                        t1.receiver_id = t2.receiver_id AND 
                        t1.mail_time = t2.mail_time;
        '''
        curr.execute(delete_query)
        conn.commit()
        print()
        send_email(my_mail_id,password,email["Sender_id"],email["name"])
    mailBox.logout()
    return jsonify({"message": "Emails fetched and saved successfully"})

def send_email(from_email,password,to_email,user_name):
    try:
        subject = 'Response Related to Your Health Insurance Claim'
        body = f"""
        Dear {user_name},

        Thank you for reaching out to HealthGuard Insurance.

        We have received your email concerning your health insurance claim related to your policy. We have initiated the claim process and will keep you updated via email regarding the progress.

        If you have any questions or need further assistance, please do not hesitate to contact us.

        Best regards,

        John Doe
        Claims Department
        HealthGuard Insurance
        Phone: (123) 456-7890
        Email: support@fluvina.com
        """

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject

        # Attach the body with the msg instance
        message.attach(MIMEText(body, 'plain'))

        # Create SMTP session for sending the mail
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail's SMTP server
        server.starttls()  # Enable security

        # Login to the server
        server.login(from_email, password)

        # Send the email
        server.send_message(message)

        # Close the connection
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 4000 ,debug=True)
