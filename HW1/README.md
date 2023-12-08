# 類神經網路 Neural Networks 作業一

[![hackmd-github-sync-badge](https://hackmd.io/ihWHe1zdTdiKel9bgaXhCQ/badge)](https://hackmd.io/ihWHe1zdTdiKel9bgaXhCQ)



:::success
<font color="#f00">***10/16更新項目**</font>>
- [x] 進度條正確顯示、解鎖按鈕(可跑多個資料集)、關閉視窗時destroy window()、釋放多餘記憶體
:::


> 學號 112522101 資工碩一
> 姓名 吳宥俞


:::info
* 基本題
    1. GUI功能及程式流程
    2. 主要function說明
    3. 實驗結果及分析
:::



## 1 GUI功能及程式流程

---

GUI部分採用Tkinter套件呈現，並使用PAGE圖型編輯器完成UI外觀。
> ![](https://hackmd.io/_uploads/r1E3xBOZT.png)
> *圖1初始外觀*

##### 使用方法:
i.點擊`Dataset`按鈕，獲得資料集路徑。
ii.輸入`Epoch、Learning rate`數值。
iii.按下`Training!`按鈕，開始訓練，下方有進度條，可得知訓練進度。
##### 核心程式流程:
i.當按下`Training!`按鈕時，會去取得輸入的路徑、Epoch、學習率數值，並將參數傳進main function進行訓練。
ii.在訓練過程中，會將**每次訓練的結果**更新於**左邊的方框**，當中**顯示分類結果、鍵結值、訓練正確率**。
iii.訓練完成後，會將**測試資料**的分類結果展示於**右邊的方框**，當中**顯示分類結果、鍵結值、測試正確率**，並在右下方顯示最佳的訓練正確率、測試正確率。

> <iframe src="https://giphy.com/embed/BF5zJmwGkWZK8YMyhs" width="480" height="408" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
> 
> 圖2流程完成圖(註:左方分類的線會隨著訓練結果**一直更新*** .gif看起來卡卡的:D)


## 2 主要function說明
作品架構主要有3個檔案，3個檔案皆相互import:
	i.**UIhw1.py**:UI外觀程式碼(大部分都是PAGE自動生成)。
	ii.**UIhw1_support.py**:事件反應程式碼(如按鈕點擊後會做甚麼)
	iii.**NeuralNetworkHW1.py**:**感知機及作圖程式碼**
    
    
**UIhw1.py、UIhw1_support.py**重點程式碼:


![](https://hackmd.io/_uploads/ryJ1NSdWp.png)
*(ii.)中的`Training!`按鈕，觸發後將參數傳入(iii.)*

**NeuralNetworkHW1.py**重點程式碼:

![](https://hackmd.io/_uploads/HJFkHBOba.png)
*使用到pandas、numpy、train_test_split、tkinter、matplotlib套件*

![](https://hackmd.io/_uploads/HyLlBHuba.png)
*利用pandas讀取輸入資料，並將每筆資料**最左邊加上閥值-1**，並將資料集切分成(訓練7:測試3)*

![](https://hackmd.io/_uploads/rJw-rHOWa.png)
***步驟一**:網路初始化。初始鍵結值w設為[-1,0,1] (過(0,-1)的水平線)*
 
![](https://hackmd.io/_uploads/SJurrB_-a.png)
***重複步驟二～五，直到達到epoch次數或是訓練正確率達1.0。***

![](https://hackmd.io/_uploads/SJULSSdbp.png)
![](https://hackmd.io/_uploads/HykdrrO-p.png)

![](https://hackmd.io/_uploads/Hk6dSBub6.png)
***步驟三：調整鍵結值向量。***
![](https://hackmd.io/_uploads/HyIYSB_ZT.png)


![](https://hackmd.io/_uploads/rksFBBdba.png)
***步驟四：計算該次的正確率**。並保留最好的鍵結值，拿來testing用*

![](https://hackmd.io/_uploads/ryDJLSdZa.png)
***步驟五：將每次結果透過matplotlib畫圖。**(每次的鍵結值、訓練正確率、分類結果的線)*

## 3 實驗結果及分析
以下將針對每一個資料集進行分析:
> **2ring.txt**(測試準確率:1.0)鍵結值:(-1.4,0.11,-1.0)
![](https://hackmd.io/_uploads/rJnjPBubT.png)
*此**圖為線性可分割**，且資料分布算均勻，故迭代次數不用太大、學習率不用太小就可以使訓練跟測試的正確率達到1.0。*


---

> **2Hcircle1.txt**(測試準確率:1.0) 鍵結值:(-0.6,1.55,-0.58)
> ![](https://hackmd.io/_uploads/H1RpDHOba.png)
*同上，此圖為**線性可分割**，且資料分布算均勻，故迭代次數不用太大、學習率不用太小就可以使訓練跟測試的正確率達到1.0。*


---

> **2CS.txt**(測試準確率:1.0) 鍵結值:(-1.8,0.38,-0.16)
> ![](https://hackmd.io/_uploads/B1Z9uSdWT.png)
*此圖為標準的**線性可分割**，且資料分布非常均勻，兩種類別分的蠻開的，故迭代次數不用太大、學習率不用太小就可以使訓練跟測試的正確率達到1.0。*


---

> **2cring.txt**(測試準確率:1.0) 鍵結值:(-6.0,0.81,-0.75)
> ![](https://hackmd.io/_uploads/BJDjOrO-a.png)
*此圖線性可分割，**但兩種類別在座標上較為靠近**，故使用較多的Epoch、較小的學習率、慢慢接近看看。*
![](https://hackmd.io/_uploads/SJz3urO-a.png)
*調整完後，效果很好。*


---

> **2CloseS3.txt**(測試準確率:0.99) 鍵結值:(0.2,1.37,-0.12)
> ![](https://hackmd.io/_uploads/BJ56_BdZp.png)
*> 此圖**非線性可分割**，且資料不均勻，雖然說**分類結果不會**像最小均方法那樣會受影響，但是在迭代的時候比較常算到黃色的資料，所以就更新的比較慢，**故嘗試增加Epoch次數，但不調整學習率看看**。*
![](https://hackmd.io/_uploads/Hy_gtH_Z6.png)
結果好很多，但是畢竟兩個類別有重疊，**非線性可分割**，所以準確率無法透過一條線準確分類。


---

> **2CloseS2.txt**(測試準確率:1.0) 鍵結值:(0.0,1.17,0.14)
> ![](https://hackmd.io/_uploads/BJh-tS_-p.png)
*此圖兩種類別剛好相切，為線性可分，但是**因為剛好相切，需要剛剛好切到那條線**，**所以把學習率降低，並增加訓練次數**，設定到500次時，準確率剛好為1.0。*


---

> **2CloseS.txt**(測試準確率:1.0) 鍵結值:(0.0,1.2,0.49)
> ![](https://hackmd.io/_uploads/SJeEtHO-a.png)
*此圖兩種類別**非常接近**，為**線性可分**，因為兩類別較為靠近，所以一樣把學習率降低，並增加訓練次數，設定到約450次時，準確率剛好為1.0，**(不過也有可能資料其實有重疊到，剛好被訓練跟測試資料分開來了)***


---

> **2Circle1.txt**(測試準確率:0.889) 鍵結值:(-0.6,0.68,-1.01)
> ![](https://hackmd.io/_uploads/SJvIYBuZa.png)
*> 此圖為**非線性可分割**，無法準確分割，嘗試了增加Epoch，盡量增加正確率。*


---

> **2Ccircle1.txt**(測試準確率:0.667) 鍵結值:(-0.2,0.59,-0.56)
> ![](https://hackmd.io/_uploads/SJzOFruba.png)
> *同上為同心圓，是**非線性可分圖**型，有試過幾次都是從中間切一刀，準確率最好為0.667，**上圖為較特別的狀況**，可能是因為外圈的點多於內圈的點太多，所以直接將外圈的都分在同一類就好，這樣準確率一樣是0.667。:D*


---

> **perceptron2.txt**(測試準確率:0.778) 鍵結值:(0.0,-0.4,0.24)
> 該資料集只有4筆資料，不夠切成訓練集及測試集，故加入3倍相同的資料進去。
> ![](https://hackmd.io/_uploads/BJHhFSuWp.png)
因為資料間距離只有1，所以**學習率設低一些**，讓她**不會來回反覆震盪**。而此圖為**非線性可分**，無法準確分類。(我的圖為了方便看，有將座標固定，所以若分類的線在座標外，就會看不見)


---

> **perceptron1.txt**(測試準確率:1.0) 鍵結值:(0.08,0.12,0.04)
> 該資料集只有4筆資料，不夠切成訓練集及測試集，故加入3倍相同的資料進去。
> ![](https://hackmd.io/_uploads/H1wCFSuWT.png)
*為**線性可分**圖型，但**因距離間只有1，所以學習率設低一些，不讓線反覆震盪**，而Epoch在約50次的時候就找到準確率為1.0的線了。*



---

:::warning
> **心得結論:若非線性可分的資料，靠單層感知機無法準確分類。且若資料間距離較近、需要很精準的線來分類的情況下，學習率需要降低、Epoch次數需增加，正確率才會提升。**
:::


PS:原(.exe)檔案破百MB，所以有先壓縮了，故打開需要等一陣子。
