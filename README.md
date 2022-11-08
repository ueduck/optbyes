# optbyes - Byesを最小にするスケジュールの作成 -
byesを最小にするスケジューリングを作成します．またそのようなスケジュールが存在しない場合は，実行不能であることを知らせます．

## 環境構築方法
本プログラムは[Python 3.10](https://www.python.org)を利用しています．またパッケージ管理には[Poetry](https://python-poetry.org)を利用しています．
まずはじめに[Python.orgのダウンロードページ](https://www.python.org/downloads/)より，Pyhton 3.10をインストールしてください．また，
```
curl -sSL https://raw.githubusercontent.com/python-poetry/
```
によってPoetryをインストールしてください．次に本リポジトリをcloneしてください．
```
git clone https://github.com/hrt0809/optbyes
```
最後に本リポジトリ中の```pyproject.toml```を使って仮想環境を作成します．
```
poetry install
```
を実行して仮想環境を作成してください．```pyproject.toml```の中身，特に[tool.poetry.dependencies]の書き方については，[依存関係仕様](https://cocoatomo.github.io/poetry-ja/dependency-specification/)が参考になります．
