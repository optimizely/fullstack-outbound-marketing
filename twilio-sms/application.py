import os

from optimizely_config_manager import OptimizelyConfigManager
from twilio.rest import Client

from flask import Flask, request, render_template

TWILIO_ACCOUNT_SID = "<account_sid>"
TWILIO_AUTH_TOKEN = "<auth_token>"
FROM_NUMBER = '<from_number>'

OPTIMIZELY_PROJECT_ID = '<project_id>'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

application = Flask(__name__, static_folder='assets')
application.secret_key = os.urandom(24)

config_manager = OptimizelyConfigManager(OPTIMIZELY_PROJECT_ID)

@application.route('/')
def hello_world():
  return render_template('index.html')

# process inbound sms message
@application.route('/sms', methods=['GET', 'POST'])
def sms():
  # Twilio data
  from_number = request.form['From']
  message = request.form['Body'].lower()

  if message == 'hello':
    variation_key = config_manager.get_obj().activate('<experiment_key>', from_number)

    if variation_key == 'question':
      send_sms("Hello! Want to learn how to create this same experiment Optimizely Full Stack and Twilio? If so, respond with Yes", from_number)

    if variation_key == 'suggestion':
      send_sms("Hello! To learn more about Full Stack, we recommend checking out a sample app we built. Want to learn more? If so, respond with Yes", from_number)

    if variation_key == 'aggressive':
      send_sms("Hello, Did you know that avocados (persea americana), are not a vegetable, but a fruit. Technically avocados are classified as a large berry with a single seed. Additionally, in 2013 Mexico (the worlds largest producer of avocados) produced over 3 billion pounds of the fruit. If you want to learn more about this demo, respond with Yes.", from_number)

  elif message == 'no':
    send_sms('Thank you for your response. No Full Stack conversion event logged. We hope you enjoyed this demo!', from_number)

  elif message == 'yes':
    config_manager.get_obj().track('<track_event>', from_number)
    send_sms("Here's the GitHub repo. We hope you enjoyed this demo and are inspired to build your next app with Optimizely Full Stack. http://bit.ly/2o3CSoK", from_number)

  else:
    send_sms("Invalid command. Please respond with 'Hello' to start!", from_number)

def send_sms(msg, number):
  message = client.messages.create(to=number, from_=FROM_NUMBER, body=msg)
  return message


if __name__ == '__main__':
  application.debug = True
  application.run()
