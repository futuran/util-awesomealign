# 対訳辞書を生成するスクリプト
# 入力：原言語文, 目的言語文, アライメントファイル
# 出力：対訳辞書

import argparse
import pprint
import collections

import spacy
spacy_ja = spacy.load('ja_core_news_sm')
spacy_en = spacy.load('en_core_web_sm')

def get_stopword():
    sw_en = set(spacy.lang.en.stop_words.STOP_WORDS)
    sw_ja = set(spacy.lang.ja.stop_words.STOP_WORDS)
    return sw_en, sw_ja


def make_dict(args):
    with open(args.src, 'r') as f:
        src_list = f.readlines()
    with open(args.trg, 'r') as f:
        trg_list = f.readlines()
    with open(args.align, 'r') as f:
        align_list = f.readlines()

    sw_en, sw_ja = get_stopword()

    para_vocabs = []

    for i, (src, trg, align) in enumerate(zip(src_list, trg_list, align_list)):

        # 単語に分解
        src_vocabs = src.lower().strip().split()
        trg_vocabs = trg.lower().strip().split()
        align_vocabs = align.split()

        # アライメントの取れた単語対を辞書に格納
        for j, num_num in enumerate(align_vocabs):
            num_num = num_num.split('-')
            num0 = int(num_num[0])
            num1 = int(num_num[1])

            if (src_vocabs[num0] not in sw_en) and (trg_vocabs[num1] not in sw_ja):
                para_vocabs.append('{}\t{}'.format(src_vocabs[num0], trg_vocabs[num1]))


    para_vocabs_dict = collections.Counter(para_vocabs).most_common()
    para_vocabs_dict = ['{}\t{}\n'.format(x[0],x[1]) for x in para_vocabs_dict]
    #print(para_vocabs_dict)
    with open(args.out, 'w') as f:
        f.writelines(para_vocabs_dict)


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-s', '--src', help='src file of awesome-align.')
    parser.add_argument('-t', '--trg', help='trg file of awesome-align.')
    parser.add_argument('-a', '--align', help='align file')
    
    parser.add_argument('-o', '--out', help='output file name of para_vocabs dict file')

    args = parser.parse_args()
    make_dict(args)


main()