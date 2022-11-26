import json
import numpy as np
from statsmodels.tsa.stattools import adfuller

throughput_data = json.load(open("../dados/throughputs_normalized.json"))

throughput_values = np.array([int(entry["val"]) for entry in throughput_data])

result = adfuller(throughput_values)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')

for key, value in result[4].items():
     print('\t%s: %.3f' % (key, value))
