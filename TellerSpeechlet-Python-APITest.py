__author__ = 'dixonaws@amazon.com'

# import statements
from sys import argv
import urllib2
import urllib
import time
import sys
import json

def getInvoice(invoiceNumber):
    invoiceUrl="http://localhost:8080/RESTTest/api/invoices/" + str(invoiceNumber)

    startTime=int(round(time.time() * 1000))
    endTime=0;
    sys.stdout.write("GETting invoice... ")

    opener=urllib2.build_opener()

    # ask the API to return JSON
    opener.addheaders=[('Accept', 'application/json')]

    try:
        # our response string should result in a JSON object
        response = opener.open(invoiceUrl).read()

        endTime=int(round(time.time() * 1000))
        print "done (" + str(endTime-startTime) + " ms)."

    except urllib2.HTTPError:
        print "Error in GET..."

    # decode the returned JSON response into JSONIaccount (a Python dict object)
    JSONinvoice = json.loads(str(response))

    return(JSONinvoice)

### end getInvoice()

def getAccount(accountNumber):
    accountUrl="http://localhost:8080/RESTTest/api/accounts/"

    startTime=int(round(time.time() * 1000))
    endTime=0;
    sys.stdout.write(url + ": GETting account... ")

    opener=urllib2.build_opener()

    # ask the API to return JSON
    opener.addheaders=[('Accept', 'application/json')]

    response=""

    try:
        # our response string should result in a JSON object
        response=opener.open(url).read()

        endTime=int(round(time.time() * 1000))
        print "done (" + str(endTime-startTime) + " ms)."

    except urllib2.HTTPError:
        print "Error in GET..."

    # decode the returned JSON response into JSONIaccount (a Python dict object)
    JSONaccount = json.loads(str(response))

    return(JSONaccount)

### end getAccount()

## Main
script, args0 = argv

# take the fileName as the first argument, and the endpoint URL as the second argument
baseurl=args0

print "PowerCo API Test, v1.1"

url=baseurl

# retrieve account ID 1
JSONaccount=getAccount(1)

print JSONaccount

# decode the invoices from the account
JSONinvoices=JSONaccount['invoices']

# get the number of invoices associated with this account
intNumberOfInvoices=len(JSONinvoices)

# count the number of invoices in this account
print("I found " + str(intNumberOfInvoices) + " invoices associated with this account")

# loop through the invoices asspociated with this account and print out the amount due
for invoices in JSONinvoices:
    invoice=getInvoice(invoices['id'])
    print("Invoice id " + str(invoice['id']) + ": " + "$" + str(invoice['amountDollars']) + "." + str(invoice['amountCents']))


