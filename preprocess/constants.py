import re

DATA_PREFECTURE = """
京都府
北海道
青森県
岩手県
宮城県
秋田県
山形県
福島県
茨城県
栃木県
群馬県
埼玉県
千葉県
東京都
神奈川県
新潟県
富山県
石川県
福井県
山梨県
長野県
岐阜県
静岡県
愛知県
三重県
滋賀県
大阪府
兵庫県
奈良県
和歌山県
鳥取県
島根県
岡山県
広島県
山口県
徳島県
香川県
愛媛県
高知県
福岡県
佐賀県
長崎県
熊本県
大分県
宮崎県
鹿児島県
沖縄県
"""

PREFECTURES = re.findall(r'(\w+)\n',DATA_PREFECTURE)

zenkaku_table = str.maketrans({
    '１': '1',
    '２': '2',
    '３': '3',
    '４': '4',
    '５': '5',
    '６': '6',
    '７': '7',
    '８': '8',
    '９': '9',
    '０': '0',
})

regex_par = re.compile('（.+\）')
def get_inside_par(s: str) -> str:
    """
    全角の（）中の文字列を取り出す

    Args:
        s (str): 処理対象の文字列

    Returns:
        str: （）中の文字列
    """
    return regex_par.search(s).group().strip('（）')