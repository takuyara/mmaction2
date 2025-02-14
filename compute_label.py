import cv2
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
base_path = "D:\\working-age-data\\frames"
new_path = "D:\\working-age-data\\videos"
label_path = "D:\\working-age-data\\questionnaire"
datasets = ["AUD", "BS", "RWTH", "UCAM"]
tasks = ["DB", "DE02", "DH02", "DS", "NBB", "NBE02", "NBH02", "NBS", "WEB", "WEP", "WEN"]
annotation_file = open("./ann_all_a.txt", "w")
fourcc = cv2.VideoWriter_fourcc(*"XVID")
total_labels = []
def get_label(path, task):
	with open(path, newline = "") as f:
		reader = csv.DictReader(f)
		total_labels = []
		for row in reader:
			total_labels.append(int(row[task]))
			if len(total_labels) == 2:
				break
	label = 0
	"""
	if total_labels[0] <= 5:
		label += 2
	if total_labels[1] <= 5:
		label += 1
	assert 0 <= label and label <= 3
	"""
	t = total_labels[1]
	if t in [1, 2, 3]:
		return 0
	elif t in [4, 5, 6]:
		return 1
	elif t in [7, 8, 9]:
		return 2
	else:
		raise ValueError()
tvs = []
tas = []

total_labels = [0, 0, 0, 0]

for dataset in datasets:
	dataset_path = os.path.join(base_path, dataset)
	subjects = os.listdir(dataset_path)
	for subject in subjects:
		new_path_subj = os.path.join(os.path.join(new_path, dataset), subject)
		os.makedirs(new_path_subj, exist_ok = True)
		for task in tasks:
			task_path = os.path.join(os.path.join(dataset_path, subject), task)
			if not os.path.exists(task_path):
				continue
			video_label_path = os.path.join(os.path.join(os.path.join(label_path, dataset), "SAM"), f"{subject}.csv")
			if not os.path.exists(video_label_path):
				continue
			label = get_label(video_label_path, task)
			for i in range(50):
				new_frame_path = os.path.join(new_path_subj, f"{task}_{i}.mp4")
				if not os.path.exists(new_frame_path):
					break
				annotation_file.write(f"{dataset}/{subject}/{task}_{i}.mp4 {label}\n")
				total_labels[label] += 1
annotation_file.close()

print(total_labels)

# classes_count = [111, 163, 158, 108]
