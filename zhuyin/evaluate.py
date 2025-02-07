from .model.Encoder import VanillaEncoder
from .model.Decoder import VanillaDecoder
from .model.Seq2Seq import Seq2Seq
from .letterLoader import DataTransformer
from .train import Trainer
from .config import config

import pickle

def build():
    # data_transformer = DataTransformer(config.dataset_paths, use_cuda=config.use_cuda)
    # with open('zhuyin/data_transformer.pkl', 'wb') as f:
    #     pickle.dump(data_transformer, f, -1)
    # exit()
    with open('zhuyin/data_transformer.pkl', 'rb') as f:
        data_transformer = pickle.load(f)

    vanilla_encoder = VanillaEncoder(vocab_size=data_transformer.inp_size,
                                     embedding_size=config.encoder_embedding_size,
                                     lstm_size = config.lstm_size,
                                     output_size=config.encoder_output_size)

    vanilla_decoder = VanillaDecoder(hidden_size=config.decoder_hidden_size,
                                     output_size=data_transformer.out_size,
                                     lstm_size = config.lstm_size,
                                     max_length=data_transformer.max_length,
                                     teacher_forcing_ratio=config.teacher_forcing_ratio,
                                     sos_id=data_transformer.SOS_ID,
                                     use_cuda=config.use_cuda)
    if config.use_cuda:
        vanilla_encoder = vanilla_encoder.cuda()
        vanilla_decoder = vanilla_decoder.cuda()

    seq2seq = Seq2Seq(encoder=vanilla_encoder,
                      decoder=vanilla_decoder)

    trainer = Trainer(seq2seq, data_transformer, config.learning_rate, config.use_cuda)
    trainer.load_model()
    return trainer

def main():
    trainer = build()
    while(True):
        testing_word = input('You say: ')
        if testing_word == "exit":
            break
        results = trainer.evaluate(testing_word)
        print("Model says: %s" % results[0])

if __name__ == "__main__":
    main()
