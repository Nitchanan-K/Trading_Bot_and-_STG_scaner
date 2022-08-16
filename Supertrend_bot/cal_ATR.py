one = {'time':21.15,'high':2148.50,'low':2131.88,'previous_close':2142.95,'max':16.62}
two = {'time':21.10,'high':2151.00,'low':2142.46,'previous_close':2146.55,'max':8.54}
three = {'time':21.05,'high':2147.70,'low':2135.40,'previous_close':2135.21,'max':8.54}

# TR
max_one = one['high'] - one['low']
print(max_one)

# because previous_close < low
# then  max = high - previous_close
max_three = three['high'] - three['previous_close']


# ATR
# add all TR (max) divided by numbers of TR

ATR = (one['max'] + two['max'] + three['max']) / 3
print(ATR)
