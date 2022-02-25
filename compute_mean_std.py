import numpy as np
import cv2
import os

def load(x):
	img = cv2.imread(x)
	return np.array(img)

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


base_path = "D:\\working-age-data\\frames"
datasets = ["AUD", "BS", "RWTH", "UCAM"]
tasks = ["DB", "DE02", "DH02", "DS", "NBB", "NBE02", "NBH02", "NBS", "WEB", "WEP", "WEN"]
total_files = []

for dataset in datasets:
	dataset_path = os.path.join(base_path, dataset)
	subjects = os.listdir(dataset_path)
	for subject in subjects:
		for task in tasks:
			task_path = os.path.join(os.path.join(dataset_path, subject), task)
			if not os.path.exists(task_path):
				continue
			frame_names = np.random.choice(os.listdir(task_path), size = 20)
			total_files.extend([os.path.join(task_path, frame_name) for frame_name in frame_names])

print(compute_mean_std(total_files, 224, 3))