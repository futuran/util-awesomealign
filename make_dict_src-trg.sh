# 対訳辞書を生成するスクリプト
# 入力：原言語文, 目的言語文, アライメントファイル
# 出力：対訳辞書

tvt="train"
python make_dict_src-trg.py \
        -s ../aspec.tkn/aspec_$tvt.en.tkn \
        -t ../aspec.tkn/aspec_$tvt.ja.tkn \
        -a ../aspec.tkn.align/tmp/$tvt.enja.tkn.algn \
        -o ../aspec.tkn.dict/$tvt.dict
