# -*- coding: utf-8 -*-

import argparse
import torch
import torchtext
from torchtext.legacy.data import Field

def stop_word(args):

    SRC = Field(
        sequential=True,
        use_vocab=True,
        init_token="<sos>",
        eos_token="<eos>",
        lower=True,
        fix_length=150,
        pad_first=False,
        truncate_first=False,
        tokenize=str.split,
        stop_words=None, #stop_words=set(stopwords.words("english")),
        preprocessing=None, #torchtext.data.Pipeline(preprocessing),
        postprocessing=None,  # ミニバッチ単位で行う処理 (デフォルト: None)
        dtype=torch.long,
        batch_first=False,  # ミニバッチの次元を最初に追加するかどうか (デフォルト: False)
        include_lengths=False,  # パディングした文とあわせて長さを返すかどうか (デフォルト: False)
        is_target=False
    )

    TRG = Field(
        sequential=True,
        use_vocab=True,
        init_token="<sos>",
        eos_token="<eos>",
        lower=True,
        fix_length=150,
        pad_first=False,
        truncate_first=False,
        tokenize=str.split,
        stop_words=None, #stop_words=set(stopwords.words("english")),
        preprocessing=None, #torchtext.data.Pipeline(preprocessing),
        postprocessing=None,
        dtype=torch.long,
        batch_first=False,
        include_lengths=False,
        is_target=True
    )

    train_data = torchtext.legacy.data.TabularDataset(
                path='../flickr.tkn/train.enjp.tkn',
                format="tsv",
                fields=[("src",SRC),("trg",TRG)],
                skip_header=False,
            )

    SRC.build_vocab(train_data, min_freq = 1)
    TRG.build_vocab(train_data, min_freq = 1)

    src_vocab = sorted(SRC.vocab.freqs.items(), key=lambda x:-x[1])
    trg_vocab = sorted(TRG.vocab.freqs.items(), key=lambda x:-x[1])

    print('src_vocab : {}'.format(len(SRC.vocab)))
    print('trg_vocab : {}'.format(len(TRG.vocab)))

    src_stop_word = [word[0] for word in src_vocab[:500]]
    trg_stop_word = [word[0] for word in trg_vocab[:500]]

    print(src_stop_word)
    print(trg_stop_word)


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-i', '--input', default='../flickr.tkn/train.enjp.tkn' , help='input file (train corpus)')    
    #parser.add_argument('-n', help='nuber of stopword')

    args = parser.parse_args()
    stop_word(args)

main()