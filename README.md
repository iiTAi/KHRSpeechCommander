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

## Execution environment
開発環境はWSL2上のUbuntu-22.04になります。当アプリケーションはLinuxでの動作を想定しています。

実行環境の用意のために、以下の手順を踏む必要があります。
(後で記述)
