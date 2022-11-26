from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import json

throughput_data = json.load(open("../dados/throughputs.json"))
for data in throughput_data:
    data["ts"] = datetime.fromtimestamp(data["ts"])

plt.grid(True)

df = pd.DataFrame(throughput_data)

fig, ax = plt.subplots()

fig.set_figheight(5)
fig.set_figwidth(15)

ax.plot(df["ts"], df["val"] / 1000000000)
ax.xaxis_date()
fig.autofmt_xdate()

plt.ylabel("Tempo", fontsize=16)
plt.ylabel("Gbits/s", fontsize=16)

plt.show()
