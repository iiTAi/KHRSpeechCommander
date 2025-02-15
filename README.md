# KHRSpeechCommander

## What's this?
KHRSpeechCommanderは日本語の音声により、近藤科学のKHR-3HVを操作するPythonアプリケーションです。（未完成）

Anthony Zhang氏の[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)により認識した音声のテキストをMeCab([macab-python3](https://pypi.org/project/mecab-python3/))で分かち書きし、得られた形態素から命令を生成します。（シリアル）通信にはneko90氏のCライブラリ[librcb4](https://github.com/nake90/librcb4)を使用しました。

なお、librcb4の関数を組み込んだ共有ライブラリをPythonスクリプトで使用するために、librcb4のMakefileに以下の変更を加えました。（`-fPIC`オプションの追加）

<br>

変更前
```Makefile
CFLAGS := -DLIBRARY_BUILD -Wall -Wextra -g -Iinc
```
変更後
```Makefile
CFLAGS := -DLIBRARY_BUILD -Wall -Wextra -g -Iinc -fPIC
```

## How to use?
環境構築をしたうえで、ヘッドセットやロボットを接続してからアプリ（KHRSpeechCommander.py）を実行し、Runボタンを押すと音声認識が開始します。「右腕を上げて」「右腕と左腕をちょっと開いて」などと命令すると、ロボットが指示通りに動きます。Stopボタンを押すか、「終了」というまで音声認識のプロセスは継続します。

「部位」「程度」「動作」により制御します。

## Execution environment
開発環境はWSL2上のUbuntu-22.04になります。当アプリケーションはLinuxでの動作を想定しています。

実行のために、以下の準備が必要になります。具体的な手順は省略します。
- usbipdの導入と設定
- KHR-3HVの接続設定
- pulseaudioの設定
- GUIアプリケーションの日本語化
- C言語ライブラリの生成
- MeCabの導入と設定
# KHRSpeechCommander

## What's this?
KHRSpeechCommanderは日本語の音声により、近藤科学のKHR-3HVを操作するPythonアプリケーションです。（未完成）

Anthony Zhang氏の[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)により認識した音声のテキストをMeCab([macab-python3](https://pypi.org/project/mecab-python3/))で分かち書きし、得られた形態素から命令を生成します。（シリアル）通信にはneko90氏のCライブラリ[librcb4](https://github.com/nake90/librcb4)を使用しました。

GUIの実装には[Flet](https://github.com/flet-dev/flet)を使用しました。

なお、librcb4の関数を組み込んだ共有ライブラリをPythonスクリプトで使用するために、librcb4のMakefileに以下の変更を加えました。（`-fPIC`オプションの追加）

<br>

変更前
```Makefile
CFLAGS := -DLIBRARY_BUILD -Wall -Wextra -g -Iinc
```
変更後
```Makefile
CFLAGS := -DLIBRARY_BUILD -Wall -Wextra -g -Iinc -fPIC
```

## How to use?
環境構築をしたうえで、ヘッドセットやロボットを接続してからアプリ（KHRSpeechCommander.py）を実行し、Runボタンを押すと音声認識が開始します。「右腕を上げて」「右腕と左腕をちょっと開いて」などと命令すると、ロボットが指示通りに動きます。Stopボタンを押すか、「終了」というまで音声認識のプロセスは継続します。

「部位」「程度」「動作」により制御します。

## Execution environment
開発環境はWSL2上のUbuntu-22.04になります。当アプリケーションはLinuxでの動作を想定しています。

実行のために、以下の準備が必要になります。具体的な手順は省略します。
- usbipdの導入と設定
- KHR-3HVの接続設定
- pulseaudioの設定
- GUIアプリケーションの日本語化
- C言語ライブラリの生成
- MeCabの導入と設定

## License
当アプリケーションは使用したライブラリ及びフレームワークに基づき、`Apache License`、`GPL3`、`BSD3`ライセンスに準拠します。