import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pdb
import pypinyin


class Model(nn.Module):
	def __init__(self, dim_neck, dim_emb, freq):
		super(Model, self).__init__()
		self.lstm = nn.LSTM(64, 1128, 1)
		#36個注音符號
		#16 * 4 = 64個音母
		#ㄅㄆㄇㄈ	ㄉㄊㄋㄌ	ㄍㄎㄏ	ㄐㄑㄒ	ㄓㄔㄕㄖ	ㄗㄘㄙ	ㄧㄨㄩ	ㄚㄛㄜㄝ	ㄞㄟㄠㄡ	ㄢㄣㄤㄥ	ㄦ
	def forward(self, x, c_org):