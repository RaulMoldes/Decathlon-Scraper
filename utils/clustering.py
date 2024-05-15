from utils.data_visualization import add_arrow, add_legend, CLUSTERS_CMAP
from sklearn.cluster import AgglomerativeClustering, KMeans, DBSCAN, Birch
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram

N_CLUSTERS = 7
EVALUATION_METHODS = {'silhouette_score': silhouette_score,
                      'calinski_harabasz_score': calinski_harabasz_score}


class MyKMeans(KMeans):

    def _transform(self, data):
        # Calculate the pairwise Mahalanobis distance
        cov_inv = np.linalg.inv(self.covariance_)
        diff = data - self.cluster_centers_[self.labels_]
        mahalanobis_dist = np.sqrt(
            np.sum(np.square(np.dot(diff, cov_inv)), axis=1))
        return mahalanobis_dist


CLUSTERING_METHODS = {'agglomerative': AgglomerativeClustering,
                      'kmeans': MyKMeans, 'dbscan': DBSCAN, 'birch': Birch, }


def cluster(data, method='agglomerative', n_clusters=N_CLUSTERS):
    if method == 'agglomerative':
        model = CLUSTERING_METHODS[method](
            linkage='ward', compute_distances=True, compute_full_tree=True, n_clusters=n_clusters)
        model.fit(data)
    elif method == 'dbscan':
        model = CLUSTERING_METHODS[method](
            eps=0.5, min_samples=10, metric='cosine')
        model.fit(data)
    elif method == 'birch':
        model = CLUSTERING_METHODS[method](
            threshold=0.5, n_clusters=n_clusters)
        model.fit(data)

    else:

        model = CLUSTERING_METHODS[method](
            n_clusters=N_CLUSTERS, init='k-means++', random_state=42)
        model.fit(data)
    if method == 'agglomerative':
        model.linkage_matrix_ = build_linkage_matrix(model)
    return model


def build_linkage_matrix(model):
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)
    return linkage_matrix


def plot_dendrogram(ax, model, **kwargs):
    # Plot the corresponding dendrogram
    dendrogram(model.linkage_matrix_, ax=ax, **kwargs)

    return ax


def evaluate_cluster(data, labels, method='silhouette_score'):

    print(
        f'{method.capitalize()} score: {EVALUATION_METHODS[method](data, labels)}')
    return EVALUATION_METHODS[method](data, labels)


def loading_plot(ax, df, loadings,  n_components=7):

    # Crear un DataFrame para visualizar los loadings
    loadings_df = pd.DataFrame(loadings.T, columns=[f'PC{i+1}' for i in range(n_components)],
                               index=df.columns[:-1])  # Excluye la columna 'cluster'

    # Graficar los loadings
    loadings_df['total'] = np.abs(loadings_df.sum(axis=1))

    ax.barh(loadings_df.index, np.sqrt(
        loadings_df['total']), color='b', label='Cargas sobre el espacio de componentes principales', alpha=0.5)

    # Repite para más componentes si es necesario

    ax.set_xlabel('Carga')
    ax.set_ylabel('Variable')
    ax.set_title(
        'Cargas sobre el espacio de componentes principales', fontsize=15)

    return ax


def pca_plot(ax, df, transformed, components, cluster_labels=None, columns=None, arrows=True):
    if columns is None:
        columns = df.columns
    if cluster_labels is not None:
        for i in range(len(transformed)):
            ax.scatter(transformed[i, 0], transformed[i, 1],
                       color=CLUSTERS_CMAP[cluster_labels[i]], label=f'Cluster {cluster_labels[i]}')

        ax = add_legend(ax=ax, legend_dict=CLUSTERS_CMAP,
                        loc='lower left', tipo=plt.Circle, fontsize=12)
    else:
        ax.scatter(transformed[:, 0], transformed[:, 1])

    if arrows:
        for i in range(len(components[0])):
            if np.sqrt(components[0, i]**2 + components[1, i]**2) > 0.3:
                ax = add_arrow(ax,  0, 0, components[0, i], components[1, i],
                               columns[i], color='black', text_color='black', text_adjust=1.1)
    ax.set_xticklabels(np.round(ax.get_xticks(), 2), fontsize=12)
    ax.set_yticklabels(np.round(ax.get_yticks(), 2), fontsize=12)
    return ax
