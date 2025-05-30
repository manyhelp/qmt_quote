from qmt_quote.utils_trade import adjust_price_3, adjust_price_2, adjust_price_1

print(adjust_price_3(True, 20, 10, 11, 100))
print(adjust_price_3(True, 10.55, 10, 11, 5))
print(adjust_price_3(False, 10.55, 10, 11, 5))
print('=' * 60)
print(adjust_price_2(True, 20, 10, 11, 15, 10))
print(adjust_price_2(False, 0, 10, 11, 15, 10))
print(adjust_price_2(True, 20, 0, 0, 15, 10))
print(adjust_price_2(False, 0, 0, 0, 15, 10))
print(adjust_price_2(False, 0, 0, 0, 0, 10))
print(adjust_price_2(True, 6, 4, 5, 15, 10))
print('=' * 60)
print(adjust_price_1(True, 0, 0, 10, 11, 15, 12))
print(adjust_price_1(True, 1, 1, 10, 11, 15, 12))
print(adjust_price_1(False, 1, 1, 10, 11, 15, 12))
print(adjust_price_1(False, 1, 2, 0, 0, 0, 12))


print(adjust_price_3(False, 1.4600000000000001, ndigits=100))
