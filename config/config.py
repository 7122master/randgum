import torch
# Define hyper parameter
use_cuda = True if torch.cuda.is_available() else False

# setting device on GPU if available, else CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)
print()

#Additional Info when using cuda
if device.type == 'cuda':
    print(torch.cuda.get_device_name(0))
    print('Memory Usage:')
    print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
    print('Cached:   ', round(torch.cuda.memory_cached(0)/1024**3,1), 'GB')

# for dataset
dataset_paths = [
	'./data/chinese_word.txt',
	'./data/chinese_word_2.txt',
	'./data/chinese_poetry.txt',
	'./data/chinese_poetry_2.txt',
	'./data/names.txt',
	'./data/slang.txt',
	'./data/chinese_article.txt',
	]



# for training
num_epochs = 100
batch_size = 128
learning_rate = 1e-3

# for model
encoder_embedding_size = 256
encoder_output_size = 256
decoder_hidden_size = encoder_output_size
teacher_forcing_ratio = .5
lstm_size = 5
# max_length = 20

# for logging
checkpoint_name = 'auto_encoder.pt'
