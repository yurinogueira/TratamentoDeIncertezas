import json
import numpy as np
from statsmodels.tsa.stattools import adfuller

packets_retransmits_data = json.load(open("../dados/packets-retransmits_normalized.json"))

packets_retransmits_values = np.array([int(entry["val"]) for entry in packets_retransmits_data])

result = adfuller(packets_retransmits_values)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')

for key, value in result[4].items():
     print('\t%s: %.3f' % (key, value))
