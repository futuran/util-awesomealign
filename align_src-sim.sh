# AwesomeAlignを実行するスクリプト
# 原言語文-類似文間でのアライメントをとる
# 入力ディレクトリに置かれているコーパスの命名フォーマットは以下の通り
# in_dir/train.lang1.tkn

in_dir=../aspec.tkn.bpe.retrieve/merge
out_dir=../aspec.tkn.bpe.retrieve.align/

MODEL_NAME_OR_PATH=bert-base-multilingual-cased

mkdir -p $out_dir/tmp

for tvt in test dev train
do
    #paste -d '|' $in_dir/aspec_$tvt.en.tkn.with_match.bpe $in_dir/aspec_$tvt.ja.tkn.with_match.bpe | sed -e 's/|/ ||| /g' > $out_dir/tmp/$tvt.enja.tkn.bpe

    DATA_FILE=$in_dir/aspec_$tvt.en.tkn.with_match.bpe
    OUTPUT_FILE=$out_dir/tmp/$tvt.enja.tkn.bpe.algn

    CUDA_VISIBLE_DEVICES=1 awesome-align \
        --output_file=$OUTPUT_FILE \
        --model_name_or_path=$MODEL_NAME_OR_PATH \
        --data_file=$DATA_FILE \
        --extraction 'softmax' \
        --batch_size 32
done


