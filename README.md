# MazeExplore

## 環境構築

スタートメニューから「Windows PowerShell」を起動し、以下のコマンドを順番に実行してください。

### scoopのインストール
1. 次のコマンドを実行
```
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
```
2. コマンドを実行したら確認のメッセージが表示されるので、「Y」と入力してEnterを押下
3. 次のコマンドを実行
```
iwr -useb get.scoop.sh | iex
```

### gitのインストール
```
scoop install git
```

### pythonのインストール
```
scoop install python@3.11.0
```

### pygameのinstall
```
pip install pygame
```

### VSCodeのインストール
```
scoop bucket add extras
```
```
scoop install vscode
```

### VSCodeの拡張機能をインストール
スタートメニューから「Visual Studio Code」を起動し、次の拡張機能をインストール
- Japanese Language Pack for Visual Studio 
- Python Extension Pack


【インストール手順】
1. 「拡張機能」ボタンを押下
2. 検索欄にインストールする拡張機能の名前を入力
3. 「インストール」ボタンを押下
![image](https://github.com/user-attachments/assets/57d167ec-7d5e-4440-b756-cdb411a6c7ad)

### プロジェクトファイルのダウンロード
1. デスクトップに新しいフォルダを作成　例）MazeGameなど
2. Visual Studio Codeの画面左上の「ファイル」→「フォルダを開く...」から作成したフォルダを開く
3. 「Ctrl + @」でターミナルを表示して、次のコマンドを実行
```
git clone https://github.com/Riuji-Takada/MazeExplore.git
```
![image](https://github.com/user-attachments/assets/77bf92d5-dcc8-4562-abff-708f321689ad)
