strMyString="0123456789"

intMyStringLength=len(strMyString)

print("myString: " + strMyString)
print("myStringLength is " + str(intMyStringLength))

print("Last four digits if myString is " + strMyString[(int(intMyStringLength)-4):intMyStringLength])

strBalance="9034.44"

intBalanceLength=len(strBalance)

strDollars=strBalance[0:(intBalanceLength-3)]
strCents=strBalance[(intBalanceLength-2):intBalanceLength]

print "balance: " + strBalance
print "dollars: " + strDollars
print "cents: " + strCents
