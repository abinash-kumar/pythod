from email import mime
import smtplib
import poplib
import email


class AbMailUtils():
    """docstring for AbMailUtils"""
    def __init__(self, arg):
        super(AbMailUtils, self).__init__()
        self.arg = arg

    @staticmethod
    def send_email(to_email, otp):

        # Define to/from
        sender = 'noreply@addictionbazaar.com'
        recipient = to_email

        # Create message
        msg = mime.text.MIMEText("Your OTP is " + otp)
        msg['Subject'] = "Verify OTP - Seller registration - Addiction Bazaar"
        msg['From'] = sender
        msg['To'] = recipient

        # Create server object with SSL option
        server = smtplib.SMTP_SSL('smtp.zoho.com', 465)

        # Perform operations via server
        server.login(sender, 'amigoaddictionnoreply')
        server.sendmail(sender, [recipient], msg.as_string())
        server.quit()

    @staticmethod
    def send_email_of_order(user, products):

        # Define to/from
        sender = 'noreply@addictionbazaar.com'
        recipient = 'akmishra249@gmail.com,viplovpride07@gmail.com'

        # Create message
        msg = mime.text.MIMEText("""
        \n User      :  """ + str(user) + """
        \n Products  :  """ + str(products) + """
        """)
        msg['Subject'] = "Addiction Bazaar: Some one placed the Order"
        msg['From'] = sender
        msg['To'] = recipient

        # Create server object with SSL option
        server = smtplib.SMTP_SSL('smtp.zoho.com', 465)

        # Perform operations via server
        server.login(sender, 'amigoaddictionnoreply')
        server.sendmail(sender, [recipient], msg.as_string())
        server.quit()

    @staticmethod
    def read_email():
        server = poplib.POP3_SSL('poppro.zoho.com', 995)
        server.user('noreply@addictionbazaar.com')
        server.pass_('amigoaddictionnoreply')

        # get amount of new mails and get the emails for them
        messages = [server.retr(n + 1) for n in range(len(server.list()[1]))]

        # for every message get the second item (the message itself) and convert it to a string with \n; then create python email with the strings
        emails = [email.message_from_string('\n'.join(message[1])) for message in messages]

        for mail in emails:
            # check for attachment;
            for part in mail.walk():
                if not mail.is_multipart():
                    continue
                if mail.get('Content-Disposition'):
                    continue
                file_name = part.get_filename()
                # check if email park has filename --> attachment part
                if file_name:
                    file = open(file_name, 'w+')
                    file.write(part.get_payload(decode=True))
                    file.close()

    # send_mail(
    # 'Subject here',
    # 'your otp is '+otp,
    # 'aksoftbahraich@example.com',
    # [to_email],
    # fail_silently=False,
    # )
