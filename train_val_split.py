import sys
def main():
	with open("total_annotation.txt") as f:
		rows = f.readlines()
	train_data = []
	val_data = []
	for row in rows:
		if row.find("DB") != -1 or row.find("DS") != -1 or row.find("DE02") != -1 or row.find("DH02") != -1:
			if len(sys.argv) > 2 and sys.argv[2] == "--no_d":
				continue
		if row.startswith(sys.argv[1]):
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
