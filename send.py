import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class SendCSVFileUsingGmail:
    # email_user = 보내는 주소
    # email_password = email 앱 비밀번호
    # email_send = 받는사람 주소
    # email_subject = 이메일 제목
    # email_send_name = 고객님 이름
    def __init__(self, email_user, email_password, email_send, email_subject, email_send_name):
        self.email_user = email_user
        self.email_password = email_password
        self.email_send = email_send
        self.email_subject = email_subject
        self.email_send_name = email_send_name

    def send_email(self, file_name):
        msg = MIMEMultipart()
        msg['Subject'] = self.email_subject
        msg['From'] = self.email_user
        msg['To'] = self.email_send

        #이메일내용 붙이기
        email_body = '안녕하세요 {}고객님! 고객님이 요청하신 키워드를 추출하여 csv파일을 전달해드립니다!'.format(self.email_send_name)
        msg.attach(MIMEText(email_body, 'plain'))

        ##첨부파일 첨부하기
        #저장된 파일을 가지고 오기
        file_path = '/app/public/python/download/{}.csv'.format(file_name)
        attachment = open(file_path, 'rb')

        #파일을 첨부하는 과정
        mail_file = MIMEBase('application', 'csv')
        mail_file.set_payload((attachment).read())
        mail_file.add_header('Content-Disposition', 'attachment', filename='{}.csv'.format(file_name))
        encoders.encode_base64(mail_file)
        msg.attach(mail_file)

        text = msg.as_string()

        #smtp 프로토콜을 이용하여 메일 전송
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(self.email_user, self.email_password)
        server.sendmail(self.email_user, self.email_send,text)
        server.quit()


    def send_error_email(self):
        msg = MIMEMultipart()
        msg['Subject'] = self.email_subject
        msg['From'] = self.email_user
        msg['To'] = self.email_send

        #이메일내용 붙이기
        email_body = '죄송합니다 {}님. 금지된 키워드를 입력하셨거나, 오류가 발생하였습니다. 다시한번 사용해주세요!'.format(self.email_send_name)
        msg.attach(MIMEText(email_body, 'plain'))

        text = msg.as_string()

        #smtp 프로토콜을 이용하여 메일 전송
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(self.email_user, self.email_password)
        server.sendmail(self.email_user, self.email_send,text)
        server.quit()
