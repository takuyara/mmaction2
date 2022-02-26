import cv2
import os
import csv
base_path = "D:\\working-age-data\\frames"
new_path = "D:\\working-age-data\\videos"
label_path = "D:\\hope\\working-age\\CSV_ALL"
datasets = ["BS"]
tasks = ["DB", "DE02", "DH02", "DS", "NBB", "NBE02", "NBH02", "NBS", "WEB", "WEP", "WEN"]

TIME_WINDOW_SIZE = 32
RATE = 5

annotation_file = open("./total_annotation.txt", "w")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
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
	if total_labels[0] <= 5:
		label += 2
	if total_labels[1] <= 5:
		label += 1
	assert 0 <= label and label <= 3
	return label

sub_video_len = TIME_WINDOW_SIZE * RATE

for dataset in datasets:
	dataset_path = os.path.join(base_path, dataset)
	subjects = os.listdir(dataset_path)
	for subject in subjects:
		if subject in ["BN2NG500LF37LBV0001A", "DR2RS100RM34LBV0001A", "DV3NN700RM32LBV0001A", "GB4LS1000LF25LBV0001A"]:
			continue
		new_path_subj = os.path.join(os.path.join(new_path, dataset), subject)
		os.makedirs(new_path_subj, exist_ok = True)
		for task in tasks:
			task_path = os.path.join(os.path.join(dataset_path, subject), task)
			if not os.path.exists(task_path):
				continue
			video_label_path = os.path.join(os.path.join(os.path.join(label_path, dataset + "_csvs"), "SAM"), f"{subject}.csv")
			if not os.path.exists(video_label_path):
				continue
			# label = get_label(video_label_path, task)
			label = 0
			frame_names = os.listdir(task_path)
			total_frames = []
			for frame_name in frame_names:
				frame = cv2.imread(os.path.join(task_path, frame_name))
				total_frames.append(frame)
			n_subs = len(total_frames) // sub_video_len
			sub_video_sts = list(range(n_subs)) + [len(total_frames) - sub_video_len]
			for i, start in enumerate(sub_video_sts):
				new_frame_path = os.path.join(new_path_subj, f"{task}_{i}.mp4")
				writer = cv2.VideoWriter(new_frame_path, fourcc, 24, (224, 224))
				for frame in total_frames[start : start + sub_video_len]:
					writer.write(frame)
				writer.release()
				ann_path = f"{dataset}/{subject}/{task}_{i}.mp4"
				annotation_file.write(f"{ann_path} {label}\n")
				total_labels.append(label)
		print(f"Done: {dataset} {subject}")
annotation_file.close()
