from utils.data_preparation import preprocess_characteristics_data
from utils.clustering import cluster, pca_plot
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

data = preprocess_characteristics_data()
model = cluster(data, method='kmeans')
pca = PCA(n_components=7)
pca = pca.fit(data)
transformed = pca.transform(data)
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
components = pca.components_

ax = pca_plot(ax, data, transformed, components, cluster_labels=model.labels_)
ax.grid(True)
plt.show()
