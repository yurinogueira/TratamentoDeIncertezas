from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import json

packet_retransmits_data = json.load(open("../dados/packets-retransmits.json"))
for data in packet_retransmits_data:
    data["ts"] = datetime.fromtimestamp(data["ts"])

plt.grid(True)

df = pd.DataFrame(packet_retransmits_data)

fig, ax = plt.subplots()

fig.set_figheight(5)
fig.set_figwidth(15)

ax.plot(df["ts"], df["val"])
ax.xaxis_date()
fig.autofmt_xdate()

plt.ylabel("Tempo", fontsize=16)
plt.ylabel("Retransmissões", fontsize=16)

plt.show()
