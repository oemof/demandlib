import matplotlib.pyplot as plt
import pandas as pd


from demandlib import bdew

dt_index = pd.date_range(
    start="2020-01-01 00:00",
    end="2020-12-31 23:45",
    freq="15min",
)

h25 = bdew.H25(dt_index)
s25 = bdew.S25(dt_index)

print(h25.sum() / 4)
print(s25.sum() / 4)

plt.plot(h25, label="H")
plt.plot(s25, label="S")
plt.legend()

plt.show()
