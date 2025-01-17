# CurveFitting

## はじめに
Blenderでモデリングをしていると、頂点の並びが汚くなってしまうことがあります。  
CurveFittingは元の形状は保ったまま、頂点の汚い並びを滑らか整えます。

## 動作環境
Blender 4.2 以降  
もし、Blender v3.6以前のバージョンにインストールする場合は, CurveFitting V0.1.xを使用してください.

## インストール方法
### Githubから
1.  最新のCurveFitting.zipを[release](https://github.com/zuda77/CurveFitting_blender_addon/releases)からダウンロードしてください。
2.  Blenderを起動し、ヘッダーメニュー:Edit - Preferences...を選択すると、Preferencesウインドウが表示されます。
3.  PreferencesウインドウでAdd-onsボタンをクリックし、右上にあるInstall...ボタンをクリックするとファイルダイアログが表示されます。
4.  ファイルダイアログでCurveFitting.zipを選択すると、PreferencesウインドウのAdd-onsリストにCurveFittingが追加されます。
5.  Add-onsリストにCurveFittingにチェックマークを付けるとインストールが完了します。
### Blender Extensionから
1.  [Blender Extension](https://extensions.blender.org/add-ons/curvefitting/)サイト上の"Get add-on"ボタンをクリックしてください。

##  使い方
1.  並びを滑らかに整えたい頂点を選択します。このとき、頂点はedge、または、faceで結合されている必要があります。
2.  右クリックでコンテキストメニューを開き、Curve Fitting -> Curveをクリックすると曲線に、Curve Fitting -> Surfaceは曲面に対して処理されます。
3.  ヘッダーメニューVertex - Curve Fittingでも同様に機能を呼び出すことができます。
5.  スクリーン左下のプロパティパネルのCurve Degreeの値を変えて、カーブや面形状をお好みに調整します。

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/prop_2deg.PNG"> <br>
プロパティパネル
</P>

## 機能
Curve Fittingは選択された頂点から算出した多項式で近似された曲線、または、曲面上に頂点を移動します。

#### - Curve Degree
プロパティパネルのCurve Degreeは、多項式の次数を設定します。  
次数を大きくすると複雑な形状にフィッティングしますが、形の単純さは失われます。元の頂点列の形に合わせてお好みで調整してください。  
次の表は次数を1から4まで変更したときの例を示します。

|Curve Degree|頂点モデル<br>Curve|頂点モデル<br>Surface|曲線イメージ|
|:-:|:-:|:-:|:-:|
|処理前<br>元形状|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/before.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_before.PNG" width="45%">|-|
|1|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_1deg.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_1deg.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_1deg.PNG)|
|2|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_2deg.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_2deg.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_2deg.PNG)|
|3|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_3deg.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_3deg.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_3deg.PNG)|
|4|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_4deg.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_4deg.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_4deg.PNG)|

  
#### - border Weight
Curveの場合は、選択された頂点列の開始点と終点を移動しにくくする数値です。デフォルト値10です。  
Surfaceの場合は、選択された頂点をメンバーとする面集合の外周にある点を移動しにくくする数値です。デフォルト値は1です。  
数値が大きくなるほど開始点と終点は移動しにくくなります。最低値は1のときは、計算された近似曲線に従って開始点と終点が移動します。

## アルゴリズム
### Curve Fitting - Curve

1.  選択された頂点列を点群Pとする。(下図 青色の点)
2.  点群Pを主成分分析する。得られた主成分ベクトル1,2,3をそれぞれi,j,k軸とする。
3.  点群Pのxyz座標をijk座標に変換する。P(x,y,z) -> P(i,j,k)
5.  点群Pの各点を結んで作る曲線をi,j,k軸に射影したとき、重なりがない軸を走査軸とする。下図において操作軸はi軸となる。
6.  ij平面にPを射影し、近似曲線を最小二乗法で算出する。
7.  点群Pの座標i対応する、変換後の座標j'を近似曲線から算出する(下図 オレンジ色の点)。
8.  座標k'を同様に算出する(下図 緑色の点)。更新された頂点列を点群P'(i,j',k')とする。
9.  更新された点群P'をxyz座標に変換する。P'(i,j',k') -> P'(x',y',z')
10.  点群P'(x',y',z')をBlenderに適用する。

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/algorithm.PNG" width="80%"> <br>
Curve Fitting - Curveのアルゴリズム
</P>  

### Curve Fitting - Surfase  
1.  選択された頂点を点群Pとする。(下図 青色の点)  
2.  点群Pの平均座標をもつ点をCとする  
3.  点群Pをメンバーに持つ複数の面を面Sとする  
4.  面Sの法線ベクトルの平均ベクトルをベクトルkとする  
5.  ベクトルkを法線ベクトルとして点Cを通る面を面Tとする。ベクトルi,j,kが互いに直交するように、面Tに沿ってベクトルi,jを適当作る。今回のコードでは面T上にPを射影し、点Cから射影した最も遠い点までをベクトルiとした。ベクトルjはベクトルi,kの外積で算出する。
6.  点群Pのxyz座標をijk座標に変換する。P(x,y,z) -> P(i,j,k)  
7.  近似曲面Fをk'=F(i,j)として、近似曲面Fを最小二乗法で算出する。  
8.  近似曲面の式k'=F(i,j)から点群Pの位置を更新する。P(i,j,k) -> P'(i,j,k')    
9.  更新された点群P'をxyz座標に変換する。P'(i,j',k') -> P'(x',y',z')  
10.  P'(x',y',z')をBlenderに適用する。  

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surface_fitting_algorithm2.PNG" width="40%"> <br>
Curve Fitting - Curveのアルゴリズム
</P>

## Note
Curve Fittingのアルゴリズムは直交座標系のみを実装しているため、円や渦巻といった平面に射影したときに重なりが発生する形状では、処理が失敗します。

## License
 "Curve Fitting"のライセンスは [GPL-3.0 license](https://www.gnu.org/licenses/gpl-3.0.html).としています。
 
## Author
* Zuda77

ご意見、ご要望、バグ報告は[issues](https://github.com/zuda77/CurveFitting_blender_addon/issues)にご連絡ください。
