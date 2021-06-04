import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from pmdarima import auto_arima
import pickle
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("vaccination.csv",index_col='Updated On',parse_dates=True)
df.head()

first_dose = df["First Dose Administered"].values

plt.rcParams.update({'figure.figsize':(10,10), 'figure.dpi':100})
fig, axes = plt.subplots(3, 2, sharex=True)
axes[0, 0].plot(first_dose); axes[0, 0].set_title('Original Dataset')
plot_acf(first_dose, ax=axes[0, 1])

axes[1, 0].plot(np.diff(first_dose)); axes[1, 0].set_title('1st Order Differencing')
plot_acf(np.diff(first_dose), ax=axes[1, 1])
first_diff = np.diff(first_dose)

axes[2, 0].plot(np.diff(first_diff)); axes[2, 0].set_title('2nd Order Differencing')
plot_acf(np.diff(first_diff), ax=axes[2, 1])
plt.show()


fit = auto_arima(df["First Dose Administered"], trace = True, suppress_warnings = True)
fit.summary()

pickle.dump(fit,open('arimaModel.pkl','wb'))