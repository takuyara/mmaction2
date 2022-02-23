import cv2
import os
import csv
base_path = "D:\\working-age-data\\frames"
new_path = "D:\\working-age-data\\videos"
label_path = "D:\\hope\\working-age\\CSV_ALL"
datasets = ["AUD", "BS", "RWTH", "UCAM"]
tasks = ["DB", "DE02", "DH02", "DS", "NBB", "NBE02", "NBH02", "NBS", "WEB", "WEP", "WEN"]
annotation_file = open("./total_annotation.txt", "w")
fourcc = cv2.VideoWriter_fourcc(*"XVID")
total_labels = []
def get_label(path, task):
	with open(path, newline = "") as f:
		reader = csv.DictReader(f)
		total_labels = []
		for row in reader:
			this_label = 0 if int(row[task]) <= 5 else 1
			total_labels.append(this_label)
			if len(total_labels) == 3:
				break
	x = total_labels
	label = x[0] * 4 + x[1] * 2 + x[2]
	assert 0 <= label and label <= 7
	return label
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
			frame_names = os.listdir(task_path)
			total_frames = []
			for frame_name in frame_names:
				frame = cv2.imread(os.path.join(task_path, frame_name))
				total_frames.append(frame)
			new_frame_path = os.path.join(new_path_subj, f"{task}.mp4")
			writer = cv2.VideoWriter(new_frame_path, fourcc, 24, (224, 224))
			for frame in total_frames:
				writer.write(frame)
			writer.release()
			video_label_path = os.path.join(os.path.join(os.path.join(label_path, dataset + "_csvs"), "SAM"), f"{subject}.csv")
			if not os.path.exists(video_label_path):
				continue
			label = get_label(video_label_path, task)
			annotation_file.write(f"{new_frame_path} {label}\n")
			total_labels.append(label)
annotation_file.close()
