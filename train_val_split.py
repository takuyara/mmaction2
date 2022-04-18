import sys
def main():
	with open(f"ann_all_{sys.argv[1]}.txt") as f:
		rows = f.readlines()
	train_data = []
	val_data = []
	for row in rows:
		if row.startswith(sys.argv[2]):
			val_data.append(row)
		else:
			train_data.append(row)
	with open("train_annotation.txt", "w") as f:
		for row in train_data:
			f.write(row)
	with open("val_annotation.txt", "w") as f:
		for row in val_data:
			f.write(row)
if __name__ == '__main__':
	main()
