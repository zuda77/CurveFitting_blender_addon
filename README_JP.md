# CurveFitting

## はじめに
モデリングをしていると、頂点の並びが汚くなってしまうことがあります。  
CurveFittingは汚くなった頂点の並びを滑らか整えてくれる、BlenderのAdd-onです。

## 動作環境
Blender ver.3.6  
で開発、動作確認をしています。その他のバージョンでも動作する可能性があります。  
もし、動作しなかったり、エラーが発生する場合は[issues](https://github.com/zuda77/CurveFitting_blender_addon/issues)にご連絡ください。

## インストール方法
1.  最新のCurveFitting.zipを[release](https://github.com/zuda77/CurveFitting_blender_addon/releases)からダウンロードしてください。
2.  Blenderを起動し、ヘッダーメニュー:Edit - Preferences...を選択すると、Preferencesウインドウが表示される。
3.  PreferencesウインドウでAdd-onsボタンをクリックし、右上にあるInstall...ボタンをクリックするとファイルダイアログが表示される。
4.  ファイルダイアログでCurveFitting.zipを選択すると、PreferencesウインドウのAdd-onsリストにCurveFittingが追加される。
5.  Add-onsリストにCurveFittingにチェックマークを付けるとインストールが完了する。

##  使い方
1.  並びを滑らかに整えたい頂点を選択します
2.  右クリックでコンテキストメニューを開き、CurveFittingをクリックします。または、ヘッダーメニューVertex - Curve Fittingでも機能を呼び出すことができます。
3.  スクリーン左下のプロパティパネルの

![grafik](

## ツール

### Set Flow:

![grafik](https://github.com/BenjaminSauder/EdgeFlow/assets/13512160/5397adac-54c4-48c8-9999-e121c85db7d6)

Blenderで「Set Flow」オペレーターを実装する試みで、多くの3Dアプリケーションで人気のあるツールです。このツールは、エッジループをスプライン補間によって調整し、周囲のジオメトリの流れに沿うようにします。

ツールはエッジループの流れに対して直交する方向（画像中のオレンジ色で示されています）で動作します。

**Mix:** 初期頂点位置と補間結果の間をブレンドします。  
**Tension:** オフセットの強度を制御します。  
**Iterations:** 操作を繰り返す回数を指定します。  
**Min Angle:** 平滑化のカットオフ角度を設定します。閾値を超える角度では直線外挿位置に戻ります。

以下の例では、スプライン補間の制御点がコーナー付近にあるため、不自然な膨らみが発生しています。Min Angleを使用することで、アルゴリズムがより適切な解を見つけるように強制できます。

![grafik](https://github.com/BenjaminSauder/EdgeFlow/assets/13512160/778a2e59-435d-4338-b2ff-40fc2c444d82)

**Blend Mode:**   
- Absolute: エッジループに沿った頂点の数でブレンド長を制御します。  
- Factor: エッジループの長さに対する割合でブレンド長を制御します。

**Blend Start:** エッジループの始点からの頂点数 | 部分的な長さ。  
**Blend End:** エッジループの終点からの頂点数 | 部分的な長さ。  
**Blend Curve:** エッジループに沿った値の線形またはスムースステップブレンド。

右の画像では形状が直線から曲線に変化しています。この操作は、循環していないエッジループでのみ機能します。

![grafik](https://github.com/BenjaminSauder/EdgeFlow/assets/13512160/fd584d3f-f232-4351-a251-1863c0d5a4e3)

### Set Linear:

選択された各エッジループを始点と終点の間で直線にします。他のポイントの配置は均等に配置するか、元の距離から投影します。ツールはエッジループの流れの方向（画像中の緑色で示されています）で動作します。

![grafik](https://github.com/BenjaminSauder/EdgeFlow/assets/13512160/f53f5544-a3ea-4afe-aea8-ddb5e792bfbc)

**Space evenly:** ループ上の頂点を均等に配置します。

### Set Curve:

選択された各エッジループをスプラインに沿ってカーブさせます。スプラインはエッジループの最初と最後のエッジによって制御されます。

![grafik](https://github.com/BenjaminSauder/EdgeFlow/assets/13512160/f7e1690d-e852-4dec-bd40-956b470f94bf)

**Mix:** 初期頂点位置と補間結果の間をブレンドします。  
**Tension:** オフセットの強度を制御します。  
**Use Rail:** エッジループの最初と最後のエッジをそのままにします。

### Set Vertex Curve:

頂点の選択に基づいて頂点をカーブに移動します。選択した頂点の順序が結果に影響するため、正しい順序で選択することが重要です。

- **頂点を2つ選択:** ポイント間に半円を構築します。  
- **頂点を3つ選択:** すべての中間点を選択されたポイントを通る円に配置します（選択は始点-中間-終点を想定）。  
- **頂点を4つ以上選択:** スプラインを構築し、すべてのポイントをその上に投影します。

![grafik](https://github.com/BenjaminSauder/EdgeFlow/assets/13512160/26a48c27-a5da-4a8a-b42f-55e700d03b1a)

**Tension:** オフセットの強度を制御します。  
**Use Topology Distance:** パス探索時にエッジの長さを無視し、トポロジー距離のみを使用します。  
**Flip Half Circle:** （2頂点の場合のみ）半円の方向を反転します。  
**Space evenly:** （3頂点以上の場合のみ）頂点を均等に配置します。

## Set Flowの仕組み

最初にこのツールを目にしたとき、動作原理を完全に理解できなかったため、基本的な仕組みについて簡単に説明します。

![grafik](https://github.com/BenjaminSauder/EdgeFlow/assets/13512160/c7875b5a-1f8f-407a-a05f-2f0705ac4cf3)

ツールはエッジループの各エッジを処理し、そのエッジの各頂点を順に処理します。各頂点に対してC1-C4のポイントを検索し、スプライン補間の「制御点」として使用します。これは多くのベクタードローイングプログラムと似た仕組みです。

そのため、周囲のジオメトリに依存します。複数の隣接するエッジループがある場合、それらが互いに影響し合います。同じ操作を数回繰り返すことで全体のバランスが取れ、数回の反復で安定した結果に収束します。このため、反復回数を指定できるオプションが必要です。

## 開発者ノート

Blenderのエッジループ選択を再実装する必要がありました。エッジ選択をソートされたエッジループに変換する必要があったからです。Blenderの選択動作を再現できたのは良かったものの、通常のAPIで実現する方法を見落としている可能性があると感じています。アドバイスがあれば教えてください。

複数のスプライン補間手法を試しましたが、[http://paulbourke.net/miscellaneous/interpolation/](http://paulbourke.net/miscellaneous/interpolation/) から得たHermite補間に落ち着きました。この補間は「Tension」という便利な変数を持っています。
