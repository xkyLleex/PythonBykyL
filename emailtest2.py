import smtplib
smtpserver = smtplib.SMTP_SSL("smtp.gmail.com",465)
smtpserver.ehlo()
smtpserver.login("ncutemail123@gmail.com","Email123")
smtpserver.sendmail("ncutemail123@gmail.com","leekwanyao710@gmail.com",
"Subject:")
smtpserver.quit()
print("send email success")
