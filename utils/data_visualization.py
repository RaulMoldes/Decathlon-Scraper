import matplotlib.pyplot as plt

CLUSTERS_CMAP = {
    0: 'r',
    1: 'g',
    2: 'b',
    3: 'y',
    4: 'c',
    5: 'm',
    6: 'k',
    7: 'brown',
    8: 'orange',
    - 1: 'gray'
}


def add_arrow(ax, x, y, dx, dy, label, color='r', alpha=0.5, text_color='g', text_adjust=1.05):

    ax.arrow(x, y, dx, dy, color=color, alpha=alpha,
             head_width=0.02, head_length=0.02)

    ax.text(dx*text_adjust, dy*text_adjust, label,
            color=text_color, ha='center', va='center', fontsize=12)
    return ax


def add_legend(ax, legend_dict: dict, loc: str = 'upper left', tipo=plt.Line2D, bbox_to_anchor=None, fontsize=12):

    labels = list(legend_dict.keys())

    handles = [tipo((0, 0), 0.1, color=value, label=key)
               for key, value in legend_dict.items()]

    ax.legend(handles=handles, labels=labels,
              loc=loc, bbox_to_anchor=bbox_to_anchor, fontsize=fontsize)
    return ax
