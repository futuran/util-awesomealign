# -*- coding: utf-8 -*-

# 隣接行列用のアライメントを生成するスクリプト
# 入力：原言語文, 目的言語文, アライメントファイル, 最大の隣接行列の大きさ
# 出力：対訳辞書
#
# aspec, 英日翻訳
# NFRでの入力を想定して、src [sep] trg　のフォーマットにおけるアライメント情報に書き換えている
# 出力は対称行列

import argparse
from collections import Counter
import torch
import copy
import pprint

def make_adj_fixlen(args):
    with open(args.src, 'r') as f:
        src_list = f.readlines()
    with open(args.trg, 'r') as f:
        trg_list = f.readlines()
    with open(args.align, 'r') as f:
        align_list = f.readlines()

    orig_src1_list = []
    orig_src2_list = []

    for i, input_sentence in enumerate(src_list):
        if len(input_sentence.strip().split(' ||| ')) != 2:
            print('No.{} {}'.format(i, input_sentence.strip()))
        else:
            orig_src1_list.append(input_sentence.strip().split(' ||| ')[0])
            orig_src2_list.append(input_sentence.strip().split(' ||| ')[1])

    orig_trg_list = [x.strip() for x in trg_list]

    new_src_list = []
    new_trg_list = []
    new_adj_list = []

    for i, (src1, src2, trg, align) in enumerate(zip(orig_src1_list, orig_src2_list, orig_trg_list, align_list)):

        # 単語に分解
        src1_vocabs = src1.lower().strip().split()
        src2_vocabs = src2.lower().strip().split()
        align_vocabs = align.split()

        # アライメントが１つも取れないものは無視
        if len(align_vocabs) == 0:
            print('\nSentence No.{} is skipped'.format(i))
            print(f'no adj')
            continue

        # 行列の最大サイズを超えるものは無視
        # GPUメモリに載らなくならないように...
        # CONDITION : <sos> + src1 + <sep> + src2 + <eos> > args.adj_size
        if len(src1_vocabs) + len(src2_vocabs) + 3 > int(args.adj_size):
            print('\nSentence No.{} is skipped'.format(i))
            print(f'adj_size is too small')
            print(len(src1_vocabs) + len(src2_vocabs) + 3)
            continue

        # 翻訳モデルの入力に入れる単語列を格納するリスト
        # ソース１ <sep> ソース２
        # <sos>と<eos>は後から挿入されるのでここでは不要
        new_src_vocabs = [] # '<sos>は後から入るので ...
        new_src_vocabs += src1_vocabs
        new_src_vocabs.append('<sep>')
        new_src_vocabs += src2_vocabs

        # 隣接行列の各成分のうち、アライメントの取れた部分にゼロを代入
        continue_flag = False
        adj = []
        for j, num_num in enumerate(align_vocabs):
            num_num = num_num.split('-')
            num0 = int(num_num[0])
            num1 = int(num_num[1])

            if num0 + num1 + 1 > len(src1_vocabs) + len(src2_vocabs) + 1:
                print('\nSentence No.{} is skipped'.format(i))
                print('length is over!')
                continue_flag = True
                break

            adj.append('{}-{}'.format(str(num0), str(len(src1_vocabs) + 1 + num1)))
            adj.append('{}-{}'.format(str(len(src1_vocabs) + 1 + num1), str(num0)))

        if continue_flag == True:
            continue_flag = False
            continue


        new_src_list.append(' '.join(new_src_vocabs) + '\n')
        new_adj_list.append(' '.join(adj) + '\n')
        new_trg_list.append(trg + '\n')

    print(new_src_list[-1].strip())
    print(new_adj_list[-1].strip())
    print(new_trg_list[-1].strip())


    with open(args.new_src, 'w') as f:
        f.writelines(new_src_list)
    with open(args.new_adj, 'w') as f:
        f.writelines(new_adj_list)
    with open(args.new_trg, 'w') as f:
        f.writelines(new_trg_list)


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-s', '--src', help='src file of awesome-align. Format: [SRC] ||| [SIM]')
    parser.add_argument('-t', '--trg', help='trg file of awesome-align.')
    parser.add_argument('-a', '--align', help='align file')
    parser.add_argument('-n', '--adj_size', help='batch size * n * n')
    
    parser.add_argument('--new_src', help='output file name of new src file')
    parser.add_argument('--new_trg', help='output file name of new trg file')
    parser.add_argument('--new_adj', help='output file name of new adj file')

    args = parser.parse_args()
    make_adj_fixlen(args)



main()