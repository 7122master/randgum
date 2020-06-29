# -*- coding: UTF-8 -*-

import torch
import numpy as np
from pypinyin import pinyin, Style
import pdb
from tqdm import tqdm
from torch.autograd import Variable


class Vocabulary(object):

	def __init__(self):
		self.all_table = ['SOS', 'EOS', 'PAD', 'UNK']
		self.all_ind = {'SOS': 0,'EOS': 1,'PAD': 2,'UNK': 3}
		self.zhuyin_table = ['SOS','EOS','PAD','UNK','ㄅ','ㄆ','ㄇ','ㄈ','ㄉ','ㄊ','ㄋ','ㄌ','ㄍ','ㄎ','ㄏ','ㄐ','ㄑ','ㄒ','ㄓ','ㄔ','ㄕ','ㄖ','ㄗ','ㄘ','ㄙ','ㄧ','ㄨ','ㄩ','ㄚ','ㄛ','ㄜ','ㄝ','ㄞ','ㄟ','ㄠ','ㄡ','ㄢ','ㄣ','ㄤ','ㄥ','ㄦ']
		self.zhuyin_ind = {'SOS': 0,'EOS': 1,'PAD': 2,'UNK': 3,'ㄅ': 4,'ㄆ': 5,'ㄇ': 6,'ㄈ': 7,'ㄉ': 8,'ㄊ': 9,'ㄋ': 10,'ㄌ': 11,'ㄍ': 12,'ㄎ': 13,'ㄏ': 14,'ㄐ': 15,'ㄑ': 16,'ㄒ': 17,'ㄓ': 18,'ㄔ': 19,'ㄕ': 20,'ㄖ': 21,'ㄗ': 22,'ㄘ': 23,'ㄙ': 24,'ㄧ': 25,'ㄨ': 26,'ㄩ': 27,'ㄚ': 28,'ㄛ': 29,'ㄜ': 30,'ㄝ': 31,'ㄞ': 32,'ㄟ': 33,'ㄠ': 34,'ㄡ': 35,'ㄢ': 36,'ㄣ': 37,'ㄤ': 38,'ㄥ': 39,'ㄦ': 40}

		self.num_zhuyin = len(self.zhuyin_table)
		self.num_all = len(self.all_table)
		self.max_length = 0 #Could be more or less, I don't know

		self.word_list = []

	def build_vocab(self, data_paths):
		"""Construct the relation between words and indices"""
		for data_path in data_paths:
			print("Cur path: " + data_path)
			with open(data_path, 'r', encoding='utf-8') as dataset:
				for word in tqdm(dataset):
					word = word.strip('\n')

					self.word_list.append(word)
					if self.max_length < len(word):
						self.max_length = len(word)

					for char in word:
						if char not in self.all_table:
							self.all_table.append(char)
							self.all_ind[char] = len(self.all_table) - 1
							self.num_all += 1

		print(self.all_table)

	def sequence_to_zhuyin(self, sequence, add_eos=False, add_sos=False):
		"""Transform a char sequence to index sequence
			:param sequence: a string composed with chars
			:param add_eos: if true, add the <EOS> tag at the end of given sentence
			:param add_sos: if true, add the <SOS> tag at the beginning of given sentence
		"""
		index_sequence = [self.zhuyin_ind['SOS']] if add_sos else []

		for char in self.split_sequence(sequence):
			ch = pinyin(char, style=Style.BOPOMOFO)[0][0][0]
			if ch not in self.zhuyin_table:
				index_sequence.append((self.zhuyin_ind['UNK']))
			else:
				index_sequence.append(self.zhuyin_ind[ch])

		if add_eos:
			index_sequence.append(self.zhuyin_ind['EOS'])

		return index_sequence

	def sequence_to_letter(self, sequence, add_eos=False, add_sos=False):
		"""Transform a char sequence to index sequence
			:param sequence: a string composed with chars
			:param add_eos: if true, add the <EOS> tag at the end of given sentence
			:param add_sos: if true, add the <SOS> tag at the beginning of given sentence
		"""
		index_sequence = [self.all_ind['SOS']] if add_sos else []

		for char in self.split_sequence(sequence):
			if char not in self.all_table:
				index_sequence.append((self.all_ind['UNK']))
			else:
				index_sequence.append(self.all_ind[char])

		if add_eos:
			index_sequence.append(self.all_ind['EOS'])

		return index_sequence

	def sound_to_sequence(self, indices):
		"""Transform a list of indices
			:param indices: a list
		"""
		sequence = ""
		for idx in indices:
			char = self.all_table[idx]
			if char == "EOS":
				break
			else:
				sequence += char
		return sequence

	def zhuyin_to_sequence(self, indices):
		"""Transform a list of indices
			:param indices: a list
		"""
		sequence = ""
		for idx in indices:
			char = self.zhuyin_table[idx]
			if char == "EOS":
				break
			else:
				sequence += char
		return sequence

	def split_sequence(self, sequence):
		"""Vary from languages and tasks. In our task, we simply return chars in given sentence
		For example:
			Input : alphabet
			Return: [a, l, p, h, a, b, e, t]
		"""
		return [char for char in sequence]

	def __str__(self):
		ret = "Vocab information:\n"
		ret += "Characters: " + str(len(self.all_table))
		return ret


class DataTransformer(object):

	def __init__(self, path, use_cuda = False):
		self.indices_sequences = []
		self.use_cuda = use_cuda

		# Load and build the vocab
		self.vocab = Vocabulary()
		self.vocab.build_vocab(path)
		self.PAD_ID = self.vocab.zhuyin_ind["PAD"]
		self.SOS_ID = self.vocab.zhuyin_ind["SOS"]
		self.inp_size = self.vocab.num_zhuyin
		self.out_size = self.vocab.num_all
		self.max_length = self.vocab.max_length

		self._build_training_set(path)

	def _build_training_set(self, path):
		# Change sentences to indices, and append <EOS> at the end of all pairs
		for word in tqdm(self.vocab.word_list):
			in_seq = self.vocab.sequence_to_zhuyin(word, add_eos=True)
			out_seq = self.vocab.sequence_to_letter(word, add_eos=True)
			# input and target are not the same in auto-encoder
			self.indices_sequences.append([in_seq, out_seq[:]])

	def mini_batches(self, batch_size):
		input_batches = []
		target_batches = []

		np.random.shuffle(self.indices_sequences)
		mini_batches = [
			self.indices_sequences[k: k + batch_size]
			for k in range(0, len(self.indices_sequences), batch_size)
		]

		for batch in mini_batches:
			seq_pairs = sorted(batch, key=lambda seqs: len(seqs[0]), reverse=True)  # sorted by input_lengths
			input_seqs = [pair[0] for pair in seq_pairs]
			target_seqs = [pair[1] for pair in seq_pairs]

			input_lengths = [len(s) for s in input_seqs]
			in_max = input_lengths[0]
			input_padded = [self.pad_sequence(s, in_max) for s in input_seqs]

			target_lengths = [len(s) for s in target_seqs]
			out_max = target_lengths[0]
			target_padded = [self.pad_sequence(s, out_max) for s in target_seqs]

			input_var = Variable(torch.LongTensor(input_padded)).transpose(0, 1)  # time * batch
			target_var = Variable(torch.LongTensor(target_padded)).transpose(0, 1)  # time * batch

			if self.use_cuda:
				input_var = input_var.cuda()
				target_var = target_var.cuda()

			yield (input_var, input_lengths), (target_var, target_lengths)

	def pad_sequence(self, sequence, max_length):
		sequence += [self.PAD_ID for i in range(max_length - len(sequence))]
		return sequence

	def evaluation_batch(self, words):
		"""
		Prepare a batch of var for evaluating
		:param words: a list, store the testing data 
		:return: evaluation_batch
		"""
		evaluation_batch = []

		for word in words:
			indices_seq = self.vocab.sequence_to_zhuyin(word, add_eos=True)
			evaluation_batch.append([indices_seq])

		seq_pairs = sorted(evaluation_batch, key=lambda seqs: len(seqs[0]), reverse=True)
		input_seqs = [pair[0] for pair in seq_pairs]
		input_lengths = [len(s) for s in input_seqs]
		in_max = input_lengths[0]
		input_padded = [self.pad_sequence(s, in_max) for s in input_seqs]

		input_var = Variable(torch.LongTensor(input_padded)).transpose(0, 1)  # time * batch

		if self.use_cuda:
			input_var = input_var.cuda()

		return input_var, input_lengths

if __name__ == '__main__':
	vocab = Vocabulary()
	vocab.build_vocab([
	'./data/chinese_word.txt',
	'./data/chinese_word_2.txt',
	'./data/chinese_poetry.txt',
	'./data/chinese_poetry_2.txt',
	'./data/names.txt',
	'./data/slang.txt',
	'./data/chinese_article.txt'
	])
	print(vocab)

	test = "大家好"
	print("Sequence before transformed:", test)
	ids = vocab.sequence_to_zhuyin(test)
	print("Indices sequence:", ids)
	sent = vocab.zhuyin_to_sequence(ids)
	print("Sequence after transformed:",sent)

	data_transformer = DataTransformer([
	'./data/chinese_word.txt',
	'./data/chinese_word_2.txt',
	'./data/chinese_poetry.txt',
	'./data/chinese_poetry_2.txt',
	'./data/names.txt',
	'./data/slang.txt',
	'./data/chinese_article.txt'
	], use_cuda=False)

	for ib, tb in data_transformer.mini_batches(batch_size=3):
		print("B0-0")
		print(ib, tb)
		break
