from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json


def reject_outliers(packet_reetransmits, m=2.):
    value_list = [int(entry["val"]) for entry in packet_reetransmits]

    value_array = np.array(value_list)
    d = np.abs(value_array - np.median(value_array))
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)

    result_data = []
    for i, value in enumerate(s < m):
        if value:
            result_data.append(packet_reetransmits[i])

    return result_data


packet_retransmits_data = json.load(open("../dados/packets-retransmits.json"))

normalizo = reject_outliers(packet_retransmits_data)
normalizo_backup = [{"ts": entry["ts"], "val": entry["val"]} for entry in normalizo]

for data in normalizo:
    data["ts"] = datetime.fromtimestamp(data["ts"])

plt.grid(True)

df = pd.DataFrame(normalizo)

fig, ax = plt.subplots()

fig.set_figheight(5)
fig.set_figwidth(15)

ax.plot(df["ts"], df["val"])
ax.xaxis_date()
fig.autofmt_xdate()

plt.ylim(0, 60000)
plt.ylabel("Tempo", fontsize=16)
plt.ylabel("Retransmissões", fontsize=16)

plt.show()

json_object = json.dumps(normalizo_backup, indent=4)
with open("../dados/packets-retransmits_normalized.json", "w") as outfile:
    outfile.write(json_object)
