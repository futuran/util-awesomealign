

for tvt in test val train
do
    echo $tvt

    python make_adj_fixlen.py \
            -i ../flickr.tkn.align/tmp/$tvt.enjp.tkn \
            -a ../flickr.tkn.align/tmp/$tvt.tkn.algn \
            -n 150 \
            --new_src ../flickr.tkn.align/$tvt.src.tkn \
            --new_trg ../flickr.tkn.align/$tvt.trg.tkn \
            --new_adj ../flickr.tkn.align/$tvt.adj

    paste ../flickr.tkn.align/$tvt.src.tkn ../flickr.tkn.align/$tvt.trg.tkn > ../flickr.tkn.align/$tvt.enjp.tkn

done