import csv
import itertools
import codecs

from django.http import StreamingHttpResponse
from django.utils import timezone


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def export_filtered_csv(queryset):
    """フィルターしたQuerySetからCSVをストリーム出力

    Args:
        queryset (QuerySet): DjangoのQuerySetオブジェクト

    Returns:
        StreamingHttpResponse
    """
    #queryset = Item.objects.all() #この場合全件出力

    # listの先頭にヘッダーを挿入しておくことでStream時にヘッダー出力させる（Stream時のスマートな正解がよくわからない）

    # QuerySetをリスト[辞書]化
    # ダウンロードする項目設定  リレーションはアンダーバー2個で定義可能
    rows = list(queryset.values('subject','category__code','category__name','category__primary_category__name','remarks','created_by_id__full_name','created_at', 'updated_by_id__full_name','updated_at'))

    # 一行目のデータのキーを使ってヘッダーとして挿入する用の辞書{key:key}を作成して先頭に挿入
    header = {}
    for k in rows[0].keys():
        header[k] = k

    rows.insert(0, header)

    # ストリームでのCSV出力
    pseudo_buffer = Echo()
    writer = csv.DictWriter(pseudo_buffer, fieldnames=header)

    # そのままだとExcelで開くときに文字化けするのでUTF8 BOM追加
    # https://stackoverflow.com/questions/30288666/return-a-csv-encoded-in-utf-8-with-bom-from-django
    streaming_content = itertools.chain([codecs.BOM_UTF8], (writer.writerow(row) for row in rows))
    response = StreamingHttpResponse(streaming_content, content_type="text/csv") 
    
    # UTCなのでローカルタイム化してファイル名に使用
    dt_now = timezone.now()
    dt_now_local_str = timezone.localtime(dt_now).strftime('%Y%m%d_%H%M%S') 
    filename = f'data_{dt_now_local_str}.csv'  # ダウンロードcsvファイル名

    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    
    return response

