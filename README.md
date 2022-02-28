# django-crud-template

## 概要
Djangoを使用した簡単なCRUD(作成、参照、更新、削除)Webアプリケーションのテンプレート。  
テンプレのままであれば、DB接続設定だけで動作可能。  
項目もモデルクラス、一覧表示、詳細表示部分を変えるだけ。  
よくあるサンプルに、フィルタ絞り込みデータのCSVストリーミング出力を追加。

## 機能
- 新規入力
- 更新
- 削除
- 詳細表示
- フィルター
- フィルター状態のデータをCSV出力
- ログイン管理（DjangoのAdmin機能流用）
- Adminページ（DjangoのAdmin機能）

## 環境
- M1 MacBook Air
- VSCode
- Django
- MySQL

コマンドが少し異なるだけでWindowsのVSCodeでももちろん使用可能。  
- Mac: python3 manage.py xx  
- Win: python manage.py xx  
など

## Requirements
- Django==4.0.2
- django-crispy-forms==1.14.0
- django-filter==21.1
- mysqlclient==2.1.0
- pytz==2021.3

## MySQL設定
MySQLと設定ソフトは下記参照。  

[https://ichiken-usa.blogspot.com/2022/01/m1-php-env.html](https://ichiken-usa.blogspot.com/2022/01/m1-php-env.html)  

DB名crudで作成。MySQLの設定はこれだけでOK。  
テーブルは後で実行するmigrationで自動作成される。  
/config/settings copy.py を settings.pyに変更。  
settings.py内のDB名、ユーザ、パスワードを自身の環境に合わせて変更して接続できるようにする。  

## VSCodeのPython仮想環境で展開
空のプロジェクトのフォルダを作成。  

このコードをZipダウンロードしてプロジェクトフォルダに貼り付け。（またはクローン） 

VSCodeでプロジェクトフォルダを開く。  
ターミナルを開きカレントフォルダにvenv構築。(現在のフォルダ名がそのまま仮想環境名になる)  

python3 -m venv .

仮想環境インタープリタを選択してターミナルを開き直す。  
仮想環境が見つからない場合はbin内のpythonを選択。

./bin/python

ライブラリをインストール。

pip3 install -r requirements.txt

## DB反映と接続テスト
python3 manage.py makemigrations  
python3 manage.py migrate  
エラーがなければBDにテーブルができている。DB設定間違っているとここで接続エラー。  

python3 manage.py runserver

[http://127.0.0.1:8000](http://127.0.0.1:8000 "Django local server")

ログイン画面にアクセスできれば成功。

## ログイン
スーパーユーザを作成してログインしてみる。

python3 manage.py createsuperuser

- ユーザ名
- メールアドレス
- パスワード2回（簡単すぎると警告あり）

## マスターを登録して入出力テスト
Admin画面でデータのマスターを登録する。

### Item
マスター連携プルダウン用のデータ登録
- Area
- Category
- Primary category

### User
Full name項目に名前入力

一覧画面のNEWボタンから新規登録。  
Filterボタンでデータを絞り込み。
CSVボタンで、フィルターした状態のデータを出力。

## 項目の変更

後日追記