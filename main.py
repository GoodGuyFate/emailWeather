import requests
import json
from email.message import EmailMessage
import smtplib
import ssl
import datetime

# Your email credentials (consider using a more secure method than environment variables)

with open('c.json') as file:
  data = json.load(file)

email_sender = 'email1@example.com'
email_key = data["EMAIL_PASSWORD"]
email_receiver = 'email2@example.com'

subject = 'Weekly Weather Summary'


def get_weather_data():
  with open('c.json') as file:
    data = json.load(file)
  api_key = data['API_KEY']

  url = f"https://api.openweathermap.org/data/2.5/forecast?lat={30.0626}&lon={31.2497}&appid={api_key}&units=metric"

  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    weather_summary = ""
    previous_date = None
    try:
      for forecast in data["list"]:  # Wrap in a try block
        temp = forecast["main"]["temp"]
        date_time = datetime.datetime.fromtimestamp(forecast["dt"])
        weather_desc = forecast["weather"][0]["description"]
        current_date = date_time.strftime("%Y-%m-%d")

        # Add a blank line between days
        if previous_date and current_date != previous_date:
          weather_summary += "\n"

        weather_summary += f"Date/Time: {date_time.strftime('%Y-%m-%d %H:%M')} - Temperature: {temp:.1f}°C - {weather_desc}\n"
        previous_date = current_date
    except KeyError:
      print("Error: 'list' key not found in API response data.")
      return ""  # Or handle the error differently (e.g., return a default message)
    return weather_summary
  else:
    return f"Error retrieving weather data: {response.status_code}"

def send_email():
  em = EmailMessage()
  em['From'] = email_sender
  em['To'] = email_receiver
  em['Subject'] = subject
  
  body = f"""
This is a weekly weather summary for Cairo, Egypt:

**Overall:**
{get_weather_data()}

**Note:** This report is based on data from OpenWeatherMap and provides a weekly high and low temperature summary.
"""
  
  em.set_content(body)

  context = ssl.create_default_context()

  with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    server.login(email_sender, email_key)
    server.sendmail(email_sender, email_receiver, em.as_string())

  print('Email sent')


send_email()


