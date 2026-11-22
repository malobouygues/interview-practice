def compute_size_on_disk(cluster_size: int, file_size: int) -> int:
    # division entière arrondie au supérieur
    clusters = (file_size + cluster_size - 1) // cluster_size
    return clusters * cluster_size
