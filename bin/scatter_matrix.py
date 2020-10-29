import pandas as pd
import matplotlib.pyplot as plt
from scrape import entorb

def scatter_matrix(de):
    de.drop(columns=[c for c in de.columns if "Doubling_Time" in c], inplace=True)
    ax = pd.plotting.scatter_matrix(de, figsize=(20,20))
    return ax.get_figure()

def correlation_table(de):
    corr = de.corr()
    corr.style.background_gradient(cmap='Blues')

def fit_deaths_to_cases(de):
    import numpy as np
    coefs = np.polyfit(x=de['Cases'], y=de['Deaths'], deg=4)
    de.plot(kind='line', x='Cases', y='Deaths', linestyle='', marker='o')
    poly = np.poly1d(coefs, variable='Cases')
    plt.plot(de['Cases'], poly(de['Cases']))
    return poly

def lagged_correlation(de):
    overlapping_days = int(0.5 * min([len(de['Cases_New']), len(de['Deaths_New'])]))
    lcor = lagged_correlation = pd.DataFrame.from_dict({ \
        'Cases_New VS Deaths_New': [de['Cases_New'].rolling('7D').mean().corr(de['Deaths_New'].rolling('7D').mean().shift(-t)) for t in range(overlapping_days)],
         'Delta_New': [-t for t in range(overlapping_days)]}).set_index('Delta_New')
    fig, axes = plt.subplots(nrows=2)

    poly = np.poly1d(np.polyfit(x=lcor.index, y=lcor['Cases_New VS Deaths_New'], deg=7), variable='r')
    lag = [x.real for x in poly.deriv().r if x.imag==0 and x.real<0][-1]
    return lag

def plot_lagged_correlation(de, lcor, lag):
    lcor.plot(ax=axes[0])
    axes[0].plot(lcor.index, poly(lcor.index), label="polyfit")
    axes[0].axvline(lag, linestyle=':')
    axes[0].legend()
    de['Cases_New'].rolling('7D').mean().plot(ax=axes[1])
    de['Deaths_New'].rolling('7D').mean().shift(int(lag)).plot(ax=axes[1], secondary_y=True)
    return fig

def main():
    area = 'DE-total'
    de = entorb.to_dataframe(area)
