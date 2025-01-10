# CurveFitting

## はじめに
モデリングをしていると、頂点の並びが汚くなってしまうことがあります。  
CurveFittingは元の形状は保ったまま、汚くなった頂点の並びを滑らか整えます。

## 動作環境
Blender ver.3.6 で開発、動作確認をしています。  
その他のバージョンでも動作する可能性があります。  
もし、動作しなかったり、エラーが発生する場合は[issues](https://github.com/zuda77/CurveFitting_blender_addon/issues)にご連絡ください。

## インストール方法
1.  最新のCurveFitting.zipを[release](https://github.com/zuda77/CurveFitting_blender_addon/releases)からダウンロードしてください。
2.  Blenderを起動し、ヘッダーメニュー:Edit - Preferences...を選択すると、Preferencesウインドウが表示されます。
3.  PreferencesウインドウでAdd-onsボタンをクリックし、右上にあるInstall...ボタンをクリックするとファイルダイアログが表示されます。
4.  ファイルダイアログでCurveFitting.zipを選択すると、PreferencesウインドウのAdd-onsリストにCurveFittingが追加されます。
5.  Add-onsリストにCurveFittingにチェックマークを付けるとインストールが完了します。

##  使い方
1.  並びを滑らかに整えたい頂点を選択します。このとき、頂点はedgeで結合されている必要があります。
2.  右クリックでコンテキストメニューを開き、Curve Fittingをクリックします。または、ヘッダーメニューVertex - Curve Fittingでも機能を呼び出すことができます。
3.  スクリーン左下のプロパティパネルのCurve Degreeの値を変えて、カーブをお好みに調整します。

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/prop_2deg.PNG"> <br>
プロパティパネル
</P>

## 機能
Curve Fittingは選択された頂点から算出した多項式近似曲線上に頂点を移動します。

#### - Curve Degree
プロパティパネルのCurve Degreeは、多項式近所曲線の次数を設定します。  
次数を大きくすると複雑な形状にフィッティングしますが、形の単純さは失われます。元の頂点列の形に合わせてお好みで調整してください。  
次の表は次数を1から4まで変更したときの例を示します。

|Curve Degree|頂点モデル|曲線イメージ|
|:-:|:-:|:-:|
|処理前<br>元形状|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/before.PNG" width="45%">|-|
|1|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_1deg.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_1deg.PNG)|
|2|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_2deg.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_2deg.PNG)|
|3|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_3deg.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_3deg.PNG)|
|4|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_4deg.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_4deg.PNG)|

  
#### - Ends Weight
選択された頂点列の開始点と終点を移動しづらくする数値です。デフォルト値10で、数値が大きくなるほど開始点と終点は移動しづらくなります。最低値は1のときは、計算された近似曲線に従って開始点と終点が移動します。

## アルゴリズム
Curve Fittingのアルゴリズムは次の通りです。

1.  選択された頂点列をPとする。
2.  Pを主成分分析する。得られた主成分ベクトル1,2,3をそれぞれi,j,k軸とする。
3.  Pのxyz座標をijk座標に変換する。P(x,y,z) -> P(i,j,k)
5.  Pの各点を結んで作る曲線をi,j,k軸に射影したとき、重なりがない軸を走査軸とする。下図において操作軸はi軸となる。
6.  ij平面にPを射影し、近似曲線を最小二乗法で算出する。
7.  Pの座標i対応する、変換後の座標j'を近似曲線から算出する。
8.  座標k'を同様に算出する。更新された頂点列をP'(i,j',k')とする。
9.  更新されたP'をxyz座標に変換する。P'(i,j',k') -> P'(x',y',z')
10.  P'(x',y',z')をBlenderに適用する。

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/algorithm.PNG" width="45%"> <br>
Curve Fitting のアルゴリズム
</P>

## 開発者ノート

Blenderのエッジループ選択を再実装する必要がありました。エッジ選択をソートされたエッジループに変換する必要があったからです。Blenderの選択動作を再現できたのは良かったものの、通常のAPIで実現する方法を見落としている可能性があると感じています。アドバイスがあれば教えてください。

複数のスプライン補間手法を試しましたが、[http://paulbourke.net/miscellaneous/interpolation/](http://paulbourke.net/miscellaneous/interpolation/) から得たHermite補間に落ち着きました。この補間は「Tension」という便利な変数を持っています。
