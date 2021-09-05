in_dir=$1
out_dir=$2

MODEL_NAME_OR_PATH=bert-base-multilingual-cased

mkdir $out_dir/tmp

for tvt in test val train
do
    paste -d '|' $in_dir/$tvt.en.tkn $in_dir/$tvt.jp.tkn | sed -e 's/|/ ||| /g' > $out_dir/tmp/$tvt.enjp.tkn

    DATA_FILE=$out_dir/tmp/$tvt.enjp.tkn
    OUTPUT_FILE=$out_dir/tmp/$tvt.tkn.algn

    CUDA_VISIBLE_DEVICES=1 awesome-align \
        --output_file=$OUTPUT_FILE \
        --model_name_or_path=$MODEL_NAME_OR_PATH \
        --data_file=$DATA_FILE \
        --extraction 'softmax' \
        --batch_size 32
done


