import pandas
import smtplib
import random
import datetime as dt

FROM_EMAIL = "<email>"
APP_PASSWORD = "<password>"

today = (dt.datetime.now().month, dt.datetime.now().day)
bd_data = pandas.read_csv("./birthdays.csv")

bd_dict = {
    (data_row["month"], data_row["day"]): data_row for (index, data_row) in bd_data.iterrows()
}

if today in bd_dict:
    person = bd_dict[today]
    template_path = f"./letter_templates/letter_{random.randint(1,3)}.txt"
    with open(template_path) as template_file:
        template = template_file.read()
        template = template.replace("[NAME]", person["name"])

        email_subject = "Subject:Happy Birthday\n\n"

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=FROM_EMAIL, password=APP_PASSWORD)
            connection.sendmail(
                                from_addr=FROM_EMAIL,
                                to_addrs=person["email"],
                                msg=f"{email_subject}{template}"
            )
