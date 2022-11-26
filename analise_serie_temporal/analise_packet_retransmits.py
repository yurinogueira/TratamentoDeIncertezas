import json
from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

import warnings


packets_retransmits_data = json.load(open("../dados/packets-retransmits_normalized.json"))
for entry in packets_retransmits_data:
    entry["ts"] = datetime.fromtimestamp(entry["ts"])

data_ranges = [entry["ts"] for entry in packets_retransmits_data]
values = [entry["val"] for entry in packets_retransmits_data]

df = pd.DataFrame(values, index=data_ranges)

df.columns = ["val"]
daily = df.resample("d").sum()

mediana = daily.median()["val"]

for index, row in daily.iterrows():
    if 0.2 > row["val"] > -0.2:
        row["val"] = mediana

# ETS Decomposition
result_add = seasonal_decompose(daily["val"], model="additive", extrapolate_trend="freq")
result_mul = seasonal_decompose(daily["val"], model="multiplicative", extrapolate_trend="freq")

plt.rcParams.update({"figure.figsize": (15, 10)})
result_add.plot().suptitle("Aditivo", x=0.2, fontweight="bold")
plt.show()

result_mul.plot().suptitle("Multiplicativo", x=0.2, fontweight="bold")
plt.show()

plot_acf(df["val"])
plot_pacf(df["val"])
plt.show()

warnings.filterwarnings("ignore")

stepwise_fit = auto_arima(
    daily["val"],
    start_p=1,
    start_q=1,
    max_p=1,
    max_q=1,
    m=12,
    start_P=0,
    seasonal=True,
    d=None,
    D=1,
    trace=True,
    error_action="ignore",
    suppress_warnings=True,
    stepwise=True
)


stepwise_fit.summary()

train = daily.iloc[:len(daily) - 12]
test = daily.iloc[len(daily) - 12:]

# Após a execução do treino foi verificado
# que a melhor order a se usar para essa quantidade de tempo treinada
# é (0, 0, 0) e o seasonal order de ) (0, 1, 2)

model = SARIMAX(
    train["val"],
    order=(0, 0, 0),
    seasonal_order=(0, 1, 2, 12)
)

result = model.fit()
result.summary()

start = len(train)
end = len(train) + len(test) - 1

predictions = result.predict(start, end, typ="levels").rename("Predictions")

test["val"].plot(legend=True)
predictions.plot(legend=True)

plt.show()

model = SARIMAX(
    daily["val"],
    order=(0, 0, 0),
    seasonal_order=(1, 1, 0, 12)
)

result = model.fit()

forecast = result.predict(
    start=len(daily),
    end=(len(daily) - 1) + 12,
    typ="levels",
).rename("Forecast")

daily["val"].plot(figsize=(12, 5), legend=True)
forecast.plot(legend=True)

plt.show()
