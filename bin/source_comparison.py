import pandas as pd
import matplotlib.pyplot as plt

from scrape import entorb
from scrape import rki
from scrape import risklayer


if __name__ == "__main__":
    with plt.style.context('ggplot'):
        fig, axes = plt.subplots(nrows=6)

        da = entorb.to_dataframe(nation='DE')
        db = risklayer.to_dataframe(nation='DE')
        for ax,col in zip(axes.flat[:2], ['Cases', 'Cases_New']):
            (da[col]-db[col]).plot(kind='bar', label="%s, delta entorb - risklayer" % col,
                    sharex=True, ax=ax)
            ax.legend()

        dc = rki.to_dataframe(nation='DE')
        for ax,col in zip(axes.flat[2:4], ['Cases', 'Cases_New']):
            (da[col]-dc[col]).plot(kind='bar', label="%s, delta entorb - rki" % col,
                    sharex=True, ax=ax)
            ax.legend()

        for src in [entorb, rki, risklayer]:
            df = {entorb: da, rki: dc, risklayer: db}[src]
            for ax,col in zip(axes.flat[4:], ['Cases', 'Cases_New']):
                df[col].plot(label="%s, %s" % (col, src.__name__), sharex=True, ax=ax)
                ax.legend()


        fig = plt.gcf()
        fig.set_size_inches(16,9)
        fig.savefig('/var/www/html/peter/share/plot.png', bbox_inches='tight')
        fig.savefig('/var/www/html/peter/share/plot.svg', bbox_inches='tight')
