# 隣接行列用のアライメントを生成するスクリプト
# 入力：原言語文[sep]類似文, 目的言語文, アライメントファイル, 最大の隣接行列の大きさ
# 出力：入力文, リファレンス文, アライメントファイル


# dev test
for tvt in test dev
do
    echo $tvt

    python make_adj_src-refphrase.py \
            -s ../aspec.tkn.bpe/aspec_$tvt.en.tkn.bpe \
            -t ../aspec.tkn.bpe/aspec_$tvt.ja.tkn.bpe \
            -a ../aspec.tkn.bpe.align/tmp/$tvt.enja.tkn.bpe.algn \
            -n 250 \
            --new_src ../aspec.tkn.bpe.div/$tvt.src.tkn.bpe \
            --new_trg ../aspec.tkn.bpe.div/$tvt.trg.tkn.bpe \
            --new_adj ../aspec.tkn.bpe.div/$tvt.adj

done

# train
python make_adj_src-refphrase.py \
        -s ../aspec.tkn.bpe.div/train_head.src \
        -t ../aspec.tkn.bpe.div/train_head.trg \
        -a ../aspec.tkn.bpe.div/train_head.algn \
        -n 250 \
        --new_src ../aspec.tkn.bpe.div/train_head.src.tkn.bpe \
        --new_trg ../aspec.tkn.bpe.div/train_head.trg.tkn.bpe \
        --new_adj ../aspec.tkn.bpe.div/train_head.adj
