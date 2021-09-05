# -*- coding: utf-8 -*-

import argparse
from collections import Counter
import torch
import copy
import pprint

# 上位500単語ずつ
en_stop_word = ['a', '.', 'in', 'the', 'and', ',', 'with', 'on', 'of', 'is', 'man', 'wearing', 'to', 'woman', 'white', 'are', 'shirt', 'black', 'two', 'while', 'an', 'blue', 'at', 'his', 'people', 'young', 'red', 'standing', 'one', 'front', 'her', 'sitting', 'girl', 'boy', 'holding', 'dog', 'men', 'as', 'green', 'down', 'street', 'other', 'group', 'by', 'brown', 'yellow', 'walking', 'large', 'water', 'playing', 'background', 'up', 'looking', 'from', 'hat', 'three', 'another', 'jacket', 'dressed', 'person', 'their', 'next', 'that', 'little', 'behind', 'through', 'women', 'for', 'orange', 'small', 'over', 'some', 'child', 'building', 'pink', 'stands', 'into', 'ball', 'outside', 'pants', 'children', 'top', 'him', 'jeans', 'around', 'has', 'shorts', 'out', 'it', 'hair', 'gray', 'looks', 'them', 'hand', 'camera', 'running', 'table', '&apos;', '&quot;', 'sits', 'near', 'field', 'dress', 'sidewalk', 'wall', 'crowd', 's', 'grass', 'several', 'something', 'air', 'older', 'riding', 'who', 'side', 'stand', 'dark', 'asian', 't-shirt', 'jumping', 'there', 'player', 'striped', 'back', 'beach', 'he', 'head', 'glasses', 'hands', 'four', 'snow', 'face', 'smiling', 'girls', 'picture', 'along', 'off', 'holds', 'be', 'carrying', 'bike', 'long', 'walks', 'or', 'ground', 'city', 'area', 'soccer', 'purple', 'blond', 'mouth', 'male', 'talking', 'guitar', 'coat', 'each', 'sunglasses', 'cap', 'road', 'boys', 'lady', 'park', 'uniform', 'suit', 'bench', 'look', 'all', 'helmet', 'female', 'dogs', 'baseball', 'working', 'room', 'walk', 'car', 'being', 'sit', 'its', 'bicycle', 'light', 'trees', 'tree', 'they', 'watching', 'sign', 'wooden', 'together', 'many', 'food', 'plays', 'microphone', 'right', 'game', 'stage', 'bag', 'across', 'against', 'she', 'baby', 'tan', 'floor', 'dirt', 'shirts', 'construction', 'sweater', 'using', 'pool', 'under', 'play', 'clothing', 'middle', 'watch', 'team', 'which', 'day', 'left', 'covered', 'colored', 'taking', 'surrounded', 'rock', 'chair', 'old', 'brick', 'towards', 'boat', 'fence', 'beside', 'arms', 'colorful', 'bright', 'watches', 'guy', 'inside', 'tank', 'past', 'doing', 'open', 'what', 'about', 'vest', 'sand', 'tennis', 'window', 'both', 'others', 'shoes', 'hats', 'body', 'appears', 'football', 'very', 'above', 'outdoor', 'eating', 'store', 'elderly', 'players', 'grassy', 'horse', 'performing', 'away', 'like', 'race', 'jumps', 'piece', 'couple', 'ocean', 'runs', 'swimming', 'mountain', 'arm', 'trying', 'reading', 'this', 'someone', 'toy', 'where', 'outfit', 'line', 'train', 'rides', 'basketball', 'clothes', 'during', 'backpack', 'work', 'five', 'skirt', 'number', 'big', 'sweatshirt', 'restaurant', 'waiting', 'high', 'busy', 'stone', 'metal', 'nearby', 'path', 'band', 'have', 'uniforms', 'skateboard', 'between', 'cellphone', 'truck', 'paper', 'plastic', 'making', 'plaid', 'seated', 'singing', 'ice', 'leaning', 'workers', 'hanging', 'climbing', 'short', 'stick', 'full', 'track', 'motorcycle', 'boots', 'flowers', 'laying', 'umbrella', 'foreground', 'getting', 'scarf', 'distance', 'lake', 'onto', 'market', 'concrete', 'toddler', 'kitchen', 'shoulder', 'hard', 'dancing', 'hill', 'tall', 'house', 'set', 'smiles', 'sky', 'posing', 'buildings', 'american', 'lot', 'adults', 'book', 'board', 'equipment', 'cart', 'chairs', 'toward', 'jersey', 'pole', 'flag', 'eyes', 'gloves', 'gear', 'shopping', 'just', 'ride', 'setting', 'outdoors', 'edge', 'river', 'event', 'adult', 'shirtless', 'rope', 'rocks', 'phone', 'glass', 'swing', 'jump', 'ready', 'mountains', 'beard', 'middle-aged', 'kids', 'bus', 'painted', 'cowboy', 'safety', 'filled', 'bags', 'going', 'blond-hair', ';', 'trick', 'object', 'feet', 'african', 'having', 'gold', 'after', 'crowded', 'photo', 'snowy', 'sunny', 'catch', 'steps', 'run', 'machine', 'jackets', 'beautiful', 'corner', 'worker', 'drinking', 'music', 'sun', 'vehicle', 'apron', 'dance', 'subway', 'painting', 'takes', 'facing', 'same', 'cup', 'younger', 'door', 'bottle', 'wave', 'legs', 'lying', 'parked', 'sort', 'bridge', 'different', 'public', 'instruments', 'structure', 'hockey', 'shop', 'sleeping', 'midair', 'winter', 'purse', 'display', 'rider', 'computer', 'graffiti', 'costume', 'fishing', 'gentleman', 'dark-haired', 'cars', 'wood', 'preparing', 'pose', 'night', 'cigarette', 'fire', 'gathered', 'racing', 'drink', 'couch', 'bathing', 'view', 'spectators', 'silver', 'suits', 'counter', 'six', 'various', 'sports', 'onlookers', 'forest', 'can', 'bar', 'also', 'says', 'instrument', 'audience', 'attached', 'tie', 'take', 'leans', 'stairs', 'railing', 'leaves', 'station', 'lawn', 'no', 'fish', 'pointing', 'leather', 'playground', 'fountain', 'scene', 'whilst', 'before', 'guys', 'putting', 'goggles']
jp_stop_word = ['の', 'を', 'て', '、', 'いる', '。', 'に', 'が', 'で', 'た', 'と', '男性', '着', 'し', 'は', '人', '女性', 'シャツ', '立っ', '黒い', '中', '青い', '上', 'れ', '前', 'ある', '座っ', '白い', '犬', '赤い', '持っ', '２', '見', 'な', '二人', 'おり', '服', 'い', '歩い', '小さな', '人々', '若い', 'から', '一人', '１', 'ながら', '乗っ', '少女', 'か', '帽子', '少年', '大きな', '男', 'する', '白', '後ろ', '1', '手', '幼い', '黒', '通り', '女の子', '男の子', '身', '緑', '自転車', '建物', 'ジャケット', 'よう', 'う', '背景', 'つけ', 'その', 'もう', 'ズボン', '子ども', 'かぶっ', '茶色', '近く', '色', 'ジーンズ', '他', '写真', '何', '黄色', '選手', '赤', '３', '走っ', '水', 'テーブル', '青', 'カメラ', 'ピンク', '横', 'たち', 'そば', 'さ', '髪', '歩道', 'かけ', 'ボール', 'グループ', '見える', '黄色い', 'はい', '子供', '頭', 'オレンジ色', '用', '別', 'ため', 'ｔシャツ', '白いシャツ', '木', '向かっ', '茶色い', '緑色', '雪', '着用', '三', '壁', 'ヘルメット', '屋外', '外', '空中', '隣', 'ない', '一方', '付け', '遊ん', '匹', 'ユニフォーム', '金髪', '年配', '顔', '短パン', 'だ', '演奏', '口', '下', 'られ', '着け', '間', '地面', '灰色', 'や', '座り', '入っ', 'ジャンプ', '立ち', '集団', '車', '上着', '眼鏡', '持ち', 'つい', 'サングラス', '芝生', '人たち', 'なっ', '履い', '使っ', '道路', '一', 'も', '目', 'ドレス', 'ところ', 'コート', 'へ', 'ギター', '明るい', '場所', '大勢', '腕', 'マイク', 'オレンジ', 'ポーズ', '長い', '背後', '椅子', 'ベンチ', '方', '作業', '」', 'たり', '「', 'アジア人', '数人', '囲ま', 'ベスト', 'かぶり', '多く', 'スーツ', 'グレー', '女', '床', '書か', '４', 'ストライプ', 'チーム', '置い', 'セーター', '日', '立つ', '周り', '階段', '褐色', '二', '上げ', '岩', '話し', '乗り', '被っ', '彼', '草', '覆わ', '物', '海', '本', '馬', '人物', 'スケートボード', '窓', '公園', '一緒', '黄', 'うち', '部屋', '四', '子どもたち', 'もの', '姿', 'トラック', '数', '店', '・', '一緒に', '自分', '台', '背', '山', '衣装', '高齢', '笑っ', '柄', '向け', '弾い', 'たくさん', 'タンクトップ', 'おもちゃ', '歩き', '見る', '道', '大人', '取っ', '歩く', '両手', '棒', 'レンガ', 'ボート', 'バイク', '撮っ', '話', 'すわっ', '野原', '待っ', '準備', 'スカート', '紫色', '木々', 'とき', 'カラフル', 'バックパック', '縞模様', '座る', '携帯電話', 'この', 'プール', '食べ物', '試合', '街', 'という', 'フットボール', '黒人', '紫', '群衆', '入れ', 'いっぱい', '食べ', '看板', '一団', '野球帽', 'せ', '靴', 'そして', '黒髪', '服装', 'レース', '的', '花', 'バスケットボール', '真ん中', '高い', '傘', '互いに', '家', '並ん', 'コンクリート', 'ピンク色', '袋', '側', '若者', 'レストラン', '足', '付い', 'フェンス', 'くわえ', '付き', 'とっ', '観客', '石', 'スカーフ', '楽器', '飲み物', '背中', '置か', '歌っ', '５', 'ロープ', '砂', '同じ', '黒っぽい', '波', '見つめ', '跳び', '紙', '湖', '子供たち', '伸ばし', '川', '旗', '集まっ', 'はき', '幼児', '木製', '何人', '達', '土', '微笑ん', '水着', '絵', 'オートバイ', '通り過ぎ', '丘', '乗せ', '読ん', '森', '彼女', 'れる', '彼ら', 'バンド', 'いくつか', '運ん', 'ワンピース', '誰か', '背負っ', '遠く', 'サッカー', '膝', '混雑', '沿っ', '列', '笑顔', '柵', 'カップル', '０', '赤ちゃん', 'ショートパンツ', '投げ', 'ビーチ', '時', 'カウボーイ', '作っ', '安全', 'そう', 'ブーツ', '踊っ', '押し', '暗い', 'ステージ', '名', 'ダンス', '小道', '行っ', '走る', 'まま', '食事', 'サッカーボール', '手すり', '街路', '宙', 'あり', '後', '見せ', 'トップス', '水泳', '様子', '通り過ぎる', '手袋', '空', 'エプロン', '制服', 'ブランコ', 'バッグ', '帽', '落書き', '市場', '肩', '両', '脇', '持ち上げ', '方向', '建設作業', '登っ', '牛', '員', '飲ん', 'あごひげ', 'バス', '掛け', '見物人', '年若い', '開け', '非常', '白人', 'プラスチック', '野球', '屋根', '多い', '長袖', '青と白', '全員', 'アジア系', '技', 'お互い', '指', 'まで', '地下鉄', '描い', '巻い', '金属', '庭', '番', '箱', '楽しん', 'ジャージ', '描か', 'として', '作業員', 'こと', '赤ん坊', '耳', 'パンツ', '片手', '履き', '海岸', '最中', '美しい', '乗る', 'スケート', '水域', '浜辺', 'フード', '新聞', '腰', 'たもう', 'しよ', 'でき', '会話', '飛ん', '全身', '電話', '向い', '抱い', 'くる', '金色', 'テント', '中年', 'ひとり', '端', 'カーキ', '性', '者', '上がっ', '縞', 'ドア', 'バケツ', 'フィールド']

def make_adj_fixlen(args):
    with open(args.input, 'r') as f:
        input_list = f.readlines()
    with open(args.align, 'r') as f:
        align_list = f.readlines()

    orig_src_list = [input_sentence.strip().split(' ||| ')[0] for input_sentence in input_list]
    orig_trg_list = [input_sentence.strip().split(' ||| ')[1] for input_sentence in input_list]

    new_src_list = []
    new_trg_list = []
    new_adj_list = []

    for i, (src, trg, align) in enumerate(zip(orig_src_list, orig_trg_list, align_list)):
        #print(f'{i=}')
        src_vocabs = src.strip().split()
        trg_vocabs = trg.strip().split()
        align_vocabs = align.split()

        adj_dim_demand = len(src_vocabs) + len(align_vocabs) + 3 # ソース文単語数 + アライメント単語数 + <sos> + <eos> + <sep>
        if adj_dim_demand > int(args.adj_size):
            print(f'Skip : {src=}')
            continue
        
        adj = torch.ones((int(args.adj_size), int(args.adj_size)))    # initialize

        # 翻訳モデルの入力に入れる単語列を格納するリスト
        # <sos> Today is a good weather <sep> 今日 天気 <eos>
        # みたいな
        new_src_vocabs = [] # '<sos>は後から入るので ...
        new_src_vocabs += src_vocabs
        new_src_vocabs.append('<sep>')

        count = 0
        for i, num_num in enumerate(align_vocabs):
            num_num = num_num.split('-')
            num0 = int(num_num[0])
            num1 = int(num_num[1])

            if trg_vocabs[num1] in jp_stop_word:
                continue
            else:
                count += 1

            # アライメントが取れている部分の隣接行列の値を0にする
            #print(f'{adj.shape=}')
            #print(len(src_list))
            #print(len(src_list) + num1)
            adj[num0 + 1, len(src_vocabs) + count + 1] = 0    # 間に特殊トークンがあるので+1-1。<sos>トークンのため+1。
            adj[len(src_vocabs) + count + 1, num0  + 1] = 0

            new_src_vocabs.append(trg_vocabs[num1])

        # 隣接行列の左上（オリジナルソース文）を0にする
        adj[:len(src_vocabs) + 2, :len(src_vocabs) + 2] = torch.zeros((len(src_vocabs) + 2, len(src_vocabs) + 2))

        #torch.set_printoptions(edgeitems=150)
        #pprint.pprint(adj[3])


        new_src_list.append(' '.join(new_src_vocabs) + '\n')
        new_adj_list.append(adj)
        new_trg_list.append(trg + '\n')


    with open(args.new_src, 'w') as f:
        f.writelines(new_src_list)
    torch.save(new_adj_list,'{}.pt'.format(args.new_adj))
    with open(args.new_trg, 'w') as f:
        f.writelines(new_trg_list)


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-i', '--input', help='input file of awesome-align. Format: [SRC] ||| [TRG]')
    parser.add_argument('-a', '--align', help='align file')
    parser.add_argument('-n', '--adj_size', help='batch size * n * n')
    
    parser.add_argument('--new_src', help='output file name of new src file')
    parser.add_argument('--new_trg', help='output file name of new trg file')
    parser.add_argument('--new_adj', help='output file name of new adj file')

    args = parser.parse_args()
    #build_bilingual_dict(args)
    make_adj_fixlen(args)



main()