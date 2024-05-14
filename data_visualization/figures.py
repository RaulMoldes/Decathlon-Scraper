from data_visualization.axes import box_plot
import matplotlib.pyplot as plt
FIGURES_PATH = 'images/*'
def plot_characteristics_rating(data, output_file: str = 'characteristics_rating.png'):
    
    fig,ax = plt.subplots(figsize = (30, 10))
    ax =  box_plot(ax, 'rating', 'title',data, title = 'Characteristics boxplot', fontsize = 20)
   
    fig.savefig(FIGURES_PATH.replace('*',output_file), format='png')
    return  fig, ax