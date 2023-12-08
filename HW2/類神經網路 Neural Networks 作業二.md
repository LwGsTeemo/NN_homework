# 類神經網路 Neural Networks 作業二


> 學號 112522101 資工碩一
> 姓名 吳宥俞


:::info
* 基本題(使用RBF網路+LMS迴歸)
    1. GUI功能及程式流程
    2. 主要function說明
    3. 實驗結果及分析
:::



## 1 GUI功能及程式流程

---

GUI部分採用Tkinter套件呈現，並使用PAGE圖型編輯器完成UI外觀。
![image](https://hackmd.io/_uploads/HJfOPanXT.png)
> *圖1初始外觀*

##### 使用方法:
i.點擊`Dataset`按鈕，獲得資料集路徑。
ii.輸入`clustering number(K)`、 `Epoch`數值。
iii.按下`Training!`按鈕，開始訓練，下方有進度條，可得知訓練進度。
##### 核心程式流程:
i.當按下`Training!`按鈕時，會去取得輸入的路徑、Epoch、K值， 並將參數傳進 main function 進行訓練。
ii.在訓練過程中，會將**每次訓練的結果**更新於**左邊的方框**，當中**顯示每次車子的位置、前方距離、右方距離、左方距離**。
iii.儲存完路徑後，會將**路徑資料**的路徑軌跡結果展示於**右邊的方框**，當中**顯示車子移動的軌跡**。

> <iframe src="https://giphy.com/embed/MQZZPzEpEs04dYw7Sh" width="480" height="480"  frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
> 
> 圖2流程完成圖(註:左方車子會隨著每次計算結果**一直更新** .gif看起來卡卡的:D)


## 2 主要function說明
作品架構主要有 5 個檔案，5 個檔案皆相互 import:
i.	UIhw2.py:UI 外觀程式碼(大部分都是 PAGE 自動生成)。
ii.	UIhw2_support.py:事件反應程式碼(如按鈕點擊後會做甚麼)
iii.	draw.py:作圖程式碼
iv.	RBFmodel.py:類神經網路程式碼(RBF、LMS)
v.	simple_playground.py:預設主程式，各種狀況判定

    
    
**UIhw2.py、UIhw2_support.py**重點程式碼:


![image](https://hackmd.io/_uploads/Hkr4_a27a.png)
*(ii.)中的`Training!`按鈕，觸發後將參數傳入(v.)*

**RBFmodel.py**重點程式碼:

![image](https://hackmd.io/_uploads/SJJUup3QT.png)
*使用到pandas、numpy套件*

![image](https://hackmd.io/_uploads/HJaIOa3mT.png)
利用Kmeans演算法先找出K個群中心的位置，以利後續代入RBF基底函數。
 
![image](https://hackmd.io/_uploads/HJ3vdanXa.png)
RBF基底函數:![image](https://hackmd.io/_uploads/r14u_p3QT.png)


![image](https://hackmd.io/_uploads/r1cudp37a.png)
LMS回歸:鍵結值的更新按照投影片調整。

![image](https://hackmd.io/_uploads/HJFtupn7a.png)
整體步驟:
步驟一：輸入資料
步驟二：對訓練資料進行正規化
步驟三：利用Kmeans演算法先找出K個群聚中心
步驟四：將每個群聚中心代入RBF基底函數，投影到另一個坐標系
步驟五：將投影完的訓練資料迭代LMS回歸模型，找出誤差值最小的鍵結值


**simple_playground.py** 重點程式碼:
![image](https://hackmd.io/_uploads/SkHsu62X6.png)
主要都寫在 run_example()的函式內，內容為呼叫RBF函式、透過matplotlib作圖、連結Tkinter畫布、輸出檔案等等。


## 3 實驗結果及分析
我發現角度輸出為40的時候，車子才是直直的往上開，所以我有將模型預測出的角度再做一些數值調整，我將(角度*4+40)當作輸出，就可以成功跑到終點了。

模型輸出的數值以下將針對每一個資料集進行分析:

> **train4dAll.txt**(成功跑到終點)
![image](https://hackmd.io/_uploads/HkH0_627p.png)
此資料集內容只有3個方位的距離，如果Epoch都固定10次的情況下，K值設定成大於10的數值，成功機率比較穩定，如果設定小於10個群心的話大約3次才會成功一次。

![image](https://hackmd.io/_uploads/BJzyKahQT.png)
輸出的Track4d.txt檔案(3個方位的距離+輸出角度)

---

> **train6dAll.txt**(成功跑到終點)
![image](https://hackmd.io/_uploads/BJweK637a.png)
此資料集內容除了3個方位的距離，還有車子當下的座標，**但是訓練起來差別不大**。一樣如果Epoch都固定10次的情況下，K值設定成大於10的數值，成功機率比較穩定，如果K=20，基本上每次都成功。如果設定小於10個群心的話平均8次才會成功一次。
![image](https://hackmd.io/_uploads/rkn-Ka37a.png)
輸出的Track6d.txt檔案(車子座標+3個方位的距離+輸出角度)

Extra:以下為兩種資料集訓練失敗的案例:
---
![image](https://hackmd.io/_uploads/B1HQYTh7a.png)
Train6dAll第一個彎道撞牆

![image](https://hackmd.io/_uploads/Skz4F6hXa.png)
Train6dAll第二個彎道撞牆

![image](https://hackmd.io/_uploads/Sk34Ypn7a.png)
Train4dAll第一個彎道撞牆

![image](https://hackmd.io/_uploads/B14L9ThQ6.png)
Train4dAll第二個彎道撞牆

---

:::warning
> **心得結論:**
**在這次的實作自駕車練習中，有沒有車子的座標對於整個結果沒有太大的影響，但是我認為有車子的座標在一些同寬度但卻不同位置的軌道下表現會更準確**，可能是今天的軌道比較簡單，所以兩種訓練資料差別不大。
**實作RBF的時候**，找出適合的K值跟我預想的不太一樣，**原本以為因為輸出-40~40有80個整數點，所以高斯的局部高點要有80個可能表現才會很好，但結果是只要K值10個左右表現就很好了**，此結果令我意外，代表對於這台車子來說，方向盤只要打10個差別較大的角度就可以走到終點。
:::


PS:原(.exe)檔案破百MB，所以有先壓縮了，故打開需要等一陣子。
