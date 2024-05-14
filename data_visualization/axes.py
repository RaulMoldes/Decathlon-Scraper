import seaborn as sns
import matplotlib.pyplot as plt

def box_plot(ax, x, y, data, title, fontsize = 12, **kwargs):
    ax = sns.boxplot(x=x, y=y, data=data, ax = ax, palette='Set2', **kwargs)
    ax.set_title(title, fontsize = fontsize*2)
    ax.set_xlabel(x.capitalize(), fontsize=fontsize)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize = fontsize*0.8)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize = fontsize*0.8)
    ax.set_ylabel(None, fontsize=fontsize)
    ax.grid(True, axis='x', linestyle='--', linewidth=0.5)
    return ax