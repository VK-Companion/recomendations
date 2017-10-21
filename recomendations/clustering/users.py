from sklearn.cluster import KMeans

from recomendations.vectorizing.user import user_vector


def split_to_clusters(users, n_clusters):
    user_vectors = [user_vector(user) for user in users]

    clustering_algo = KMeans(n_clusters, n_jobs=-1)
    return clustering_algo.fit_predict(user_vectors)
