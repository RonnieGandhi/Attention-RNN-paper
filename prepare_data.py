# -*- coding: utf-8 -*-
import numpy as np 
import pandas as pd
import nltk
import re


def load_data_and_labels(path):
	data = []
	lines = [line.strip() for line in open(path)]
	for idx in range(0, len(lines), 4):
		id = lines[idx].split("\t")[0]
		relation = lines[idx + 1]

		sentence = lines[idx].split("\t")[1][1:-1]
		# sentence = sentence.replace("<e1>", " _e1_ ").replace("</e1>", " _/e1_ ")
		# sentence = sentence.replace("<e2>", " _e2_ ").replace("</e2>", " _/e2_ ")
		sentence = sentence.replace("<e1>", "<e1> ").replace("</e1>", " </e11>")
		sentence = sentence.replace("<e2>", "<e2> ").replace("</e2>", " </e22>")

		# tokens = nltk.word_tokenize(sentence)
		#
		# tokens.remove('_/e1_')
		# tokens.remove('_/e2_')
		#
		# e1 = tokens.index("_e1_")
		# del tokens[e1]
		# e2 = tokens.index("_e2_")
		# del tokens[e2]
		#
		# sentence = " ".join(tokens)

		sentence = clean_str(sentence)

		# data.append([id, sentence, e1, e2, relation])
		data.append([id, sentence, relation])

	# df = pd.DataFrame(data=data, columns=["id", "sentence", "e1_pos", "e2_pos", "relation"])
	df = pd.DataFrame(data=data, columns=["id", "sentence", "relation"])
	labelsMapping = {'Other': 0,
					 'Message-Topic(e1,e2)': 1, 'Message-Topic(e2,e1)': 2,
					 'Product-Producer(e1,e2)': 3, 'Product-Producer(e2,e1)': 4,
					 'Instrument-Agency(e1,e2)': 5, 'Instrument-Agency(e2,e1)': 6,
					 'Entity-Destination(e1,e2)': 7, 'Entity-Destination(e2,e1)': 8,
					 'Cause-Effect(e1,e2)': 9, 'Cause-Effect(e2,e1)': 10,
					 'Component-Whole(e1,e2)': 11, 'Component-Whole(e2,e1)': 12,
					 'Entity-Origin(e1,e2)': 13, 'Entity-Origin(e2,e1)': 14,
					 'Member-Collection(e1,e2)': 15, 'Member-Collection(e2,e1)': 16,
					 'Content-Container(e1,e2)': 17, 'Content-Container(e2,e1)': 18}
	df['label'] = [labelsMapping[r] for r in df['relation']]

	x_text = df['sentence'].tolist()

	# pos1, pos2 = get_relative_position(df)

	# Label Data
	y = df['label']
	labels_flat = y.values.ravel()

	labels_count = np.unique(labels_flat).shape[0]

	# convert class labels from scalars to one-hot vectors
	# 0  => [1 0 0 0 0 ... 0 0 0 0 0]
	# 1  => [0 1 0 0 0 ... 0 0 0 0 0]
	# ...
	# 18 => [0 0 0 0 0 ... 0 0 0 0 1]
	def dense_to_one_hot(labels_dense, num_classes):
		num_labels = labels_dense.shape[0]
		index_offset = np.arange(num_labels) * num_classes
		labels_one_hot = np.zeros((num_labels, num_classes))
		labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
		return labels_one_hot

	labels = dense_to_one_hot(labels_flat, labels_count)
	labels = labels.astype(np.uint8)

	# return x_text, pos1, pos2, labels
	return x_text, labels


def batch_iter(data, batch_size, num_epochs, shuffle=True):
	"""
	Generates a batch iterator for a dataset.
	"""
	data = np.array(data)
	data_size = len(data)
	num_batches_per_epoch = int((len(data) - 1) / batch_size) + 1
	for epoch in range(num_epochs):
		# Shuffle the data at each epoch
		# if shuffle:
		# 	shuffle_indices = np.random.permutation(np.arange(data_size))
		# 	shuffled_data = data[shuffle_indices]
		# else:
		# 	shuffled_data = data
		for batch_num in range(num_batches_per_epoch):
			start_index = batch_num * batch_size
			end_index = min((batch_num + 1) * batch_size, data_size)
			# yield shuffled_data[start_index:end_index]
			yield data[start_index:end_index]
            
def clean_str(string):
	"""
	Tokenization/string cleaning for all datasets except for SST.
	Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
	"""
	string = re.sub(r"[^A-Za-z0-9()<>/,!?\'\`]", " ", string)
	string = re.sub(r"\'s", " \'s", string)
	string = re.sub(r"\'ve", " \'ve", string)
	string = re.sub(r"n\'t", " n\'t", string)
	string = re.sub(r"\'re", " \'re", string)
	string = re.sub(r"\'d", " \'d", string)
	string = re.sub(r"\'ll", " \'ll", string)
	string = re.sub(r",", " , ", string)
	string = re.sub(r"!", " ! ", string)
	string = re.sub(r"\(", " \( ", string)
	string = re.sub(r"\)", " \) ", string)
	string = re.sub(r"\?", " \? ", string)
	string = re.sub(r"\s{2,}", " ", string)
	return string.strip().lower()

def get_relative_position(df, max_sentence_length=100):
	# Position data
	pos1 = []
	pos2 = []
	for df_idx in range(len(df)):
		sentence = df.iloc[df_idx]['sentence']
		tokens = nltk.word_tokenize(sentence)
		e1 = df.iloc[df_idx]['e1_pos']
		e2 = df.iloc[df_idx]['e2_pos']

		d1 = ""
		d2 = ""
		for word_idx in range(len(tokens)):
			d1 += str((max_sentence_length - 1) + word_idx - e1) + " "
			d2 += str((max_sentence_length - 1) + word_idx - e2) + " "
		for _ in range(max_sentence_length - len(tokens)):
			d1 += "999 "
			d2 += "999 "
		pos1.append(d1)
		pos2.append(d2)

	return pos1, pos2




