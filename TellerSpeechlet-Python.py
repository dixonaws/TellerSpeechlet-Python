from __future__ import print_function

import urllib2
import json
import time


# TellerSpeechlet sample skill
# 1-8-2016, John Dixon
# dixonaws@amazon.com, www.github.com/dixonaws

# TellerSpeechlet-Python is a sample Alexa skill that demonstrates Lambda
# integration with RESTful APIs to get data about a customer's bank accounts.
# The PIN is hardcoded as "9876" in this skill in the verifyPIN() function

# We only support one customer in this version, "customer 1" in the mainMenu() function
# Customer 1 has many accounts
# Each account has many transactions
# Each transaction has a description, posting date. entity, and amount

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    print("event[session][user][userId]=" + str(event['session']['user']['userId']))

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


# ------------------------- on_session_started()

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


# ------------------------- on_launch()

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])

    # Dispatch to your skill's launch
    return get_welcome_response()


# ------------------------- on_intent()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    # intent_request is a Python dict object
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("*** on_intent: I received intent=" + str(intent));
    print("*** on_intent: I received intent_name=" + str(intent_name));

    # Dispatch to your skill's intent handlers
    if intent_name == "VerifyPIN":
        return verifyPIN(intent, session)
    elif intent_name == "MainMenu":
        return mainMenu(intent, session)
    elif intent_name == "GetAccountInfo":
        return getAccountInfo(intent, session)
    elif intent_name == "GetTransactions":
        return getTransactions(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


# ------------------------- start get_welcome_response()

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
   add those here
     """

    print("*** in get_welcome_response()")

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "<speak>Hi there! You're online with Co merica Bank. please tell me your 4 digit pin.</speak>"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "You created a 4 digit pin code the first time you enabled the" \
                    "Comerica skill. If you remember it, go ahead and say it now."

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text,
        should_end_session))  # ------------------------- end get_welcome_response()

# ------------------------- start verifyPIN()

def verifyPIN(intent, session):
    # We hardcode the PIN for POC purposes; in production, use account linking in the Alexa Skills Kit
    intCorrectPIN = 9876

    print("*** verifyPIN: I received intent " + str(intent));

    # Grab the PIN out of the intent and cast it to an integer
    PIN = intent['slots']['PIN']['value']
    intReceivedPIN = int(PIN)

    print("*** verifyPIN: I received PIN " + str(PIN))

    card_title = "Welcome"

    # Compare the PIN we received with the correct PIN
    if (intReceivedPIN == intCorrectPIN):
        return mainMenu()

    elif (intReceivedPIN != intCorrectPIN):
        speech_output = "<speak>Hmmm. That PIN code doesn't match my records</speak>";

    # Setting this to true ends the session and exits the skill.
    should_end_session = True

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# ------------------------- end verifyPIN()

# ------------------------- start mainMenu()

def mainMenu():
    print("*** in mainMenu()")
    session_attributes = {}
    card_title = "Welcome"

    # hit the API and get the customer details, like the first name, last name, and associated accounts
    # for now, we hardcode the customer number
    JSONcustomer = getCustomer(1)

    accountFirstName = JSONcustomer['firstName']
    accountLastName = JSONcustomer['lastName']

    JSONaccounts = JSONcustomer['accounts']
    intAccounts = len(JSONaccounts)

    sortedJSONccounts=sorted(JSONaccounts)

    speech_output = "<speak>"
    speech_output += "Great! Hello " + accountFirstName + " " + accountLastName + "! ... "
    speech_output += "I found " + str(intAccounts) + " accounts in your profile. Which account can I help you with?"

    # loop through the accounts associated with this customer and speak the service addresses
    for accounts in sortedJSONccounts:
        print(accounts['id'])

        account = getAccountById(accounts['id'])
        accountType = account['type']
        accountNumber = account['accountNumber']
        accountId=account['id']
        accountNumberLastFour = accountNumber[(len(accountNumber) - 4): len(accountNumber)]

        speech_output += "Account number " + str(accountId) + ", <break time='0.2s'/>" + accountType + ", ending in <say-as interpret-as='digits'>" + accountNumberLastFour + "</say-as>"
        speech_output += "<break time='1s'/>"
        # end for loop

    speech_output += "</speak>"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm here to help. You can ask me about your accounts, just say the number corresponding with the account."

    should_end_session = False

    print("*** done with mainMenu(), now the user should have selected an account...")

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# -------------- end mainMenu()

# -------------- start getCustomer()

def getCustomer(id):
    print("*** in getCustomer()")

    # we hardcode the base url for now
    baseCustomersUrl = "http://tellerapi.dixonaws.com:8080/api/customers/"
    accountUrl = baseCustomersUrl + str(id)

    startTime = int(round(time.time() * 1000))
    endTime = 0;
    print(accountUrl + ": GETting customer... ")

    opener = urllib2.build_opener()

    # ask the API to return JSON
    opener.addheaders = [('Accept', 'application/json')]

    response = ""

    try:
        # our response string should result in a JSON object
        response = opener.open(accountUrl).read()

        endTime = int(round(time.time() * 1000))
        print
        "done (" + str(endTime - startTime) + " ms)."

    except urllib2.HTTPError:
        print
        "Error in GET..."

    # decode the returned JSON response into JSONcustomer object (a Python dict object)
    JSONcustomer = json.loads(str(response))

    print("*** done with getCustomer, returning JSONcustomer...")
    return (JSONcustomer)


# --------------- end getCustomer()

# --------------- start getAccountById()

def getAccountById(accountId):
    print("*** in getAccountById(), getting account" + str(accountId))

    # we hardcode the base url for now
    baseAccountsUrl = "http://tellerapi.dixonaws.com:8080/api/accounts/"
    accountUrl = baseAccountsUrl + str(accountId)

    startTime = int(round(time.time() * 1000))
    endTime = 0;

    print(accountUrl + ": GETting account... ")

    opener = urllib2.build_opener()

    # ask the API to return JSON
    opener.addheaders = [('Accept', 'application/json')]

    response = ""

    try:
        # our response string should result in a JSON object
        response = opener.open(accountUrl).read()

        endTime = int(round(time.time() * 1000))
        print("done (" + str(endTime - startTime) + " ms).")

    except urllib2.HTTPError:
        print("Error in GET...")

    # decode the returned JSON response into JSONaccount (a Python dict object)
    JSONaccounts = json.loads(str(response))

    print("*** done with getAccountById(), returning JSONaccounts...")
    return (JSONaccounts)


# ------------------------- end getAccountById()

# ------------------------- start getAccountInfo()

def getAccountInfo(intent, session):
    print("*** getAccountInfo: I received intent" + str(intent));

    card_title = "Welcome"

    selectedAccount = intent['slots']['AccountNumber']['value']

    # we hardcode the URL to the API in this POC version
    url = "http://tellerapi.dixonaws.com:8080/api/accounts/" + str(selectedAccount)

    startTime = int(round(time.time() * 1000))
    endTime = 0;

    opener = urllib2.build_opener()
    opener.addheaders = [('Accept', 'application/json')]
    try:
        # our response string should result in a JSON object
        response = opener.open(url).read()

        endTime = int(round(time.time() * 1000))
        print("done (" + str(endTime - startTime) + " ms).")

    except urllib2.HTTPError:
        print("Error in GET...")

    # parse our JSON object into a Python Dict
    JSONaccount = json.loads(str(response))
    dictTransactions = JSONaccount['transactions']

    intNumberOfTransactions = len(dictTransactions)

    # get the values out of the JSON dict object (and cast them to strings)
    strBalance=str((JSONaccount['balance']))
    intBalanceLength=len(strBalance)

    strBalanceDollars=strBalance[0:(intBalanceLength-3)]
    strBalanceCents=strBalance[(intBalanceLength-2):intBalanceLength]

    speech_output = "<speak>"
    speech_output += "I found details for that account. The account balance is " + strBalanceDollars + " dollars and " + strBalanceCents + " cents. "
    speech_output += "There are " + str(intNumberOfTransactions) + " transactions that have posted within the last 30 days,"
    speech_output += "<break time='.5s'/>"

    if(intNumberOfTransactions>0):
        speech_output += " You can say, get transactions, if you want to hear them."
        speech_output += "</speak>"
        should_end_session = False
        session['transactions']=dictTransactions
        print("*** done with getAccount(), returning speech...")
        return build_response(session, build_speechlet_response(card_title, speech_output, None, should_end_session))
    else:
        speech_output += " What else can I help you with? Accounts, Financial Summary, Payments?"
        speech_output += "</speak>"
        should_end_session = True
        print("*** done with getAccount(), returning speech...")
        return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))


# ------------------------- end getAccountInfo()

# ------------------------- start getTransactions()

def getTransactions(intent, session):
    print("*** getTransactions: I received intent" + str(intent));
    print("*** getTransactions: I received a session variable with "+ str(len(session['attributes']['transactions'])) + " transactions included!")

    dictTransactions=session['attributes']['transactions']
    intNumberOfTransactions=len(dictTransactions)

    # we hardcode the URL to the API in this POC version
    baseUrl = "http://tellerapi.dixonaws.com:8080/api/transactions/"

    startTime = int(round(time.time() * 1000))
    endTime = 0;

    speech_output="<speak>Here are the most recent transactions. "
    card_title=""

    for transaction in dictTransactions:
        print(transaction['id'])

        transaction = getTransactionById(transaction['id'])
        strTransactionType = transaction['type']
        strAmount=str(transaction['amount'])

        # convert the amount to dollars ad cents so that we can speak it
        intAmountLength = len(strAmount)
        strAmountDollars = strAmount[0:(intAmountLength - 3)]
        strAmountCents = strAmount[(intAmountLength - 2):intAmountLength]

        strEntity=transaction['entity']
        datePosted=transaction['datePosted']

        speech_output += "A " + strTransactionType + " in the amount of " + strAmountDollars + " dollars and " + strAmountCents + " cents, at " + strEntity + " on " + datePosted +", "
        speech_output += "<break time='1s'/>"
    # end for loop

    speech_output += " What else can I help you with? Accounts, Financial Summary, Payments?"
    speech_output += "</speak>"
    should_end_session = False

    print("*** done with getTransactions(), returning speech...")

    return build_response(session, build_speechlet_response(card_title, speech_output, None, should_end_session))

# ------------------------- end getTransactions()

# --------------- start getTransactionById()

def getTransactionById(transactionId):
    print("*** in getTransactionById(), getting transaction " + str(transactionId))

    # we hardcode the base url for now
    baseTransactionsUrl = "http://tellerapi.dixonaws.com:8080/api/transactions/"
    transactionUrl = baseTransactionsUrl + str(transactionId)

    startTime = int(round(time.time() * 1000))
    endTime = 0;

    print(transactionUrl + ": GETting transaction... ")

    opener = urllib2.build_opener()

    # ask the API to return JSON
    opener.addheaders = [('Accept', 'application/json')]

    response = ""

    try:
        # our response string should result in a JSON object
        response = opener.open(transactionUrl).read()

        endTime = int(round(time.time() * 1000))
        print("done (" + str(endTime - startTime) + " ms).")

    except urllib2.HTTPError:
        print("Error in GET...")

    # decode the returned JSON response into JSONaccount (a Python dict object)
    JSONtransaction = json.loads(str(response))

    print("*** done with getTransactionById(), returning JSONtransaction...")
    return (JSONtransaction)


# ------------------------- end getTransactionById()


# ------------------------- start onSessionEnded()

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# ------------------------- end onSessionEnded()

# --------------- Functions that control the skill's behavior ------------------

# ------------------------- handle_session_end_request()

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for being a Power Company customer." \
                    "Have a nice day! "

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        #        'outputSpeech': {
        #            'type': 'PlainText',
        #            'text': output
        #        },
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def main():
    print("*** in main()")

