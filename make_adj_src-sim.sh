# 隣接行列用のアライメントを生成するスクリプト
# 入力：原言語文, 目的言語文, アライメントファイル, 最大の隣接行列の大きさ
# 出力：対訳辞書

for tvt in test dev train
do
    echo $tvt

    python make_adj_src-sim.py \
            -s ../aspec.tkn.bpe.retrieve/merge/aspec_$tvt.en.tkn.with_match.bpe \
            -t ../aspec.tkn.bpe.retrieve/merge/aspec_$tvt.ja.tkn.with_match.bpe \
            -a ../aspec.tkn.bpe.retrieve.align/tmp/$tvt.enja.tkn.bpe.algn \
            -n 250 \
            --new_src ../aspec.tkn.bpe.retrieve.align/$tvt.src.tkn.bpe \
            --new_trg ../aspec.tkn.bpe.retrieve.align/$tvt.trg.tkn.bpe \
            --new_adj ../aspec.tkn.bpe.retrieve.align/$tvt.adj

done