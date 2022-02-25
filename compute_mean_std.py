def load(x):
	x = x.split()[0]
def compute_mean_std(dataloader, size, n_channels):
	mean_values = [0 for __ in range(n_channels)]
	std_values = [0 for __ in range(n_channels)]
	n_samples = len(dataloader) * size * size
	for line in dataloader:
		x = load(line)
		for i in range(n_channels):
			mean_values[i] += np.sum(x[..., i]) / n_samples
	for line in dataloader:
		x = load(line)
		for i in range(n_channels):
			std_values[i] += np.sum((x[..., i] - mean_values[i]) ** 2) / n_samples
	for i in range(n_channels):
		std_values[i] = std_values[i] ** 0.5
	return mean_values, std_values
print(compute_mean_std("total_annotation.txt", 224, 3))