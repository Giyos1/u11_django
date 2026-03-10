from django.core.mail import send_mail, EmailMessage
from config.settings import BASE_DIR

def send_simple_email():
    send_mail(
        subject="Django email sinovi",
        message="Bu test email.",
        from_email="giyosoripov4@gmail.com",
        recipient_list=["a39307503@gmail.com", "gafurjonovdavronbek@gmail.com", "freddyfazber040@gmail.com",
                        "akmalovabu96@gmail.com", "av3066827@gmail.com"],
        fail_silently=False,
    )


import os


def send_email_with_attachment():
    file_path = os.path.join(BASE_DIR,'common/service/file.txt')

    if not os.path.exists(file_path):
        print("Fayl topilmadi!")
        return

    email = EmailMessage(
        subject="Fayl bilan email",
        body="Mana sizga biriktirilgan fayl.",
        from_email="giyosoripov4@gmail.com",
        to=["a39307503@gmail.com", "gafurjonovdavronbek@gmail.com", "freddyfazber040@gmail.com",
            "akmalovabu96@gmail.com", "av3066827@gmail.com"],
    )

    with open(file_path, "rb") as f:
        email.attach("file.txt", f.read(), "application/txt")

    email.send()


from django.core.mail import EmailMultiAlternatives


def send_html_email():
    subject = "HTML email sinovi"
    from_email = "giyosoripov4@gmail.com"
    to = ["a39307503@gmail.com", "gafurjonovdavronbek@gmail.com", "freddyfazber040@gmail.com",
            "akmalovabu96@gmail.com", "av3066827@gmail.com"]

    text_content = "Bu oddiy email matni."
    html_content = "<h1>Salom</h1><p>Bu <strong>HTML</strong> email.</p>"

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()


import threading
from django.core.mail import send_mail

def send_email_in_thread(subject, message, recipient):
    thread = threading.Thread(
        target=send_mail,
        args=(subject, message, "giyosoripov4@gmail.com", [recipient]),
        kwargs={"fail_silently": False},
    )
    thread.start()
