#---------------
#Code is modified from    : http://zake7749.github.io/2017/09/28/Sequence-to-Sequence-tutorial/
#Access original code from: https://github.com/zake7749/Sequence-to-Sequence-101
#---------------

import torch.nn as nn
from torch.nn.utils.rnn import  pack_padded_sequence, pad_packed_sequence

class VanillaEncoder(nn.Module):

    def __init__(self, vocab_size, embedding_size, output_size):
        """Define layers for a vanilla rnn encoder"""
        super(VanillaEncoder, self).__init__()

        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, embedding_size)
        self.gru = nn.GRU(embedding_size, output_size)

    def forward(self, input_seqs, input_lengths, hidden=None):
        embedded = self.embedding(input_seqs)
        packed = pack_padded_sequence(embedded, input_lengths)
        packed_outputs, hidden = self.gru(packed, hidden)
        outputs, output_lengths = pad_packed_sequence(packed_outputs)
        return outputs, hidden