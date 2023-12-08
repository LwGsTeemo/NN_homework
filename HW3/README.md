# 類神經網路 Neural Networks 作業三


> 學號 112522101 資工碩一
> 姓名 吳宥俞


:::info
* 實作Hopfield
    • 顯示回想結果 (基本)
    • 「Basic_Training.txt」是訓練資料，「Basic_Testing.txt」是測試資
    料，測試資料與訓練資料是相對應的 (圖形為9x12矩陣) (基本)
    • 「Bonus_Training.txt」是訓練資料，「Bonus_Testing.txt」是測試
    資料，測試資料與訓練資料是相對應的 (圖形為10x10矩陣) (加分)
    • 可以自行將訓練資料集加入雜訊，並能夠正確回想 (加分) 
:::



## 1 GUI功能及程式流程

---

GUI部分採用Tkinter套件呈現，並使用PAGE圖型編輯器完成UI外觀。
![image](https://hackmd.io/_uploads/rkIW6Iora.png)
> *圖1初始外觀*

##### 使用方法:
i. 點擊`Train Data`按鈕，獲得訓練資料集路徑。
ii. 點擊`Test Data`按鈕，獲得測試資料集路徑。。
iii. 按下 `Start`按鈕，開始訓練，若要加雜訊，選取`Add noise`後再點擊一次`Start`按鈕即可。
iv.	可以點擊`Prev`或是`Next`按鈕，來顯示前一張或下一張的結果。
##### 核心程式流程:
i. 當按下`Start`按鈕時，會去取得輸入的路徑、是否要加入雜訊值， 並將參數傳進 main function 計算鍵結值以及先顯示第一張圖片的結果。
ii.	在點擊`Prev`或是`Next`按鈕時，**才會將該圖片的資訊進行回想(迭代100次)**，並將回想結果顯示出來。 


![image](https://hackmd.io/_uploads/S1JRaLsrT.png)
> 圖2流程完成圖(註:左方是原圖(或加雜訊)，右方是回想結果)


## 2 主要function說明
作品架構主要有 3 個檔案，3 個檔案皆相互 import:
i.	UIhw3.py:UI 外觀程式碼(大部分都是 PAGE 自動生成)。
ii.	UIhw3_support.py:事件反應程式碼(如按鈕點擊後會做甚麼)
iii.	Hopfield.py:類神經網路程式碼(算W、回想迭代、輸出圖片)


    
    
**UIhw3.py、UIhw3_support.py**重點程式碼:


![image](https://hackmd.io/_uploads/Syb-08sS6.png)
*(ii.)中的 Start按鈕，觸發後將參數傳入(iii.)*

**Hopfield.py**重點程式碼:

![image](https://hackmd.io/_uploads/BJkX0Ijr6.png)
*使用到numpy、matplotlib、random 套件*

![image](https://hackmd.io/_uploads/Byr4RIoSa.png)
*txt2ndarray():將輸入的資料分好成每筆資料，並將值賦為1跟-1，以利後續處理*
 
![image](https://hackmd.io/_uploads/BJwB0Lsr6.png)
Hopfield計算鍵結值方法:**(因為對角線算完一定是0，我就直接設為0了)**![image](https://hackmd.io/_uploads/HJQ8ALsSp.png)
![image](https://hackmd.io/_uploads/B1rLRUsST.png)

![image](https://hackmd.io/_uploads/r1BtAUoSa.png)
*回想過程，採用非同步回想(迭代100次)，**這邊theta=0，所以就不扣掉theta了***

![image](https://hackmd.io/_uploads/BkPjC8sB6.png)
*使用random套件來**加入雜訊**，(依老師上課的方法，**以0.25的機率將值互換(1變-1，-1變1)**)*


![image](https://hackmd.io/_uploads/B1bp0UjBT.png)
*將圖顯示到Tkinter的Frame畫布上 *


## 3 實驗結果及分析
基本題的3筆資料(A、C、L)不管**有沒有加入雜訊都能正確回想**。
輸出的結果將針對每一筆資料進行分析:


> **Basic_Testing.txt**(皆回想成功)
![image](https://hackmd.io/_uploads/BkFy1DoB6.png)
A


![image](https://hackmd.io/_uploads/H1Pg1vira.png)
C

![image](https://hackmd.io/_uploads/SyXGJwiB6.png)
L

---

> **Bonus_Testing.txt**(回想成功數:10/15)
![image](https://hackmd.io/_uploads/ByZVJPsHp.png)
![image](https://hackmd.io/_uploads/B1QNkvsST.png)
![image](https://hackmd.io/_uploads/SJdNyDoHp.png)
![image](https://hackmd.io/_uploads/SyiNkPsSp.png)
(上圖回想錯誤)
![image](https://hackmd.io/_uploads/Bkcrkwira.png)
![image](https://hackmd.io/_uploads/ryhrywiHa.png)
(上圖回想錯誤)
![image](https://hackmd.io/_uploads/rkLUJPirT.png)
![image](https://hackmd.io/_uploads/Hy_IyvjBp.png)
(上圖回想錯誤)
![image](https://hackmd.io/_uploads/B1xwJPjr6.png)
![image](https://hackmd.io/_uploads/BkGwkDiSa.png)
(上圖回想錯誤)
![image](https://hackmd.io/_uploads/ryYvkvsSp.png)
![image](https://hackmd.io/_uploads/SyedkwoHT.png)
(上圖回想錯誤)
![image](https://hackmd.io/_uploads/B1SdkDora.png)
![image](https://hackmd.io/_uploads/ryCu1DjH6.png)
![image](https://hackmd.io/_uploads/Sk-KkvoST.png)

此資料集15個資料中，沒加入雜訊的情況下，**有10個正確回想**。
**加入雜訊後，有12個正確回想**，3個回想錯誤，錯誤結果如下:
![image](https://hackmd.io/_uploads/S1xcJvora.png)
![image](https://hackmd.io/_uploads/HJEc1PsS6.png)
![image](https://hackmd.io/_uploads/r1L9ywoH6.png)
(上3張圖皆為回想錯誤)


:::warning
> **心得結論:**
**在這次的實作Hopfield練習中，基本題**每個都長得很不一樣，所以**有沒有加入雜訊對於回想結果的差異不大**，都能夠**正確回想**。而**加分題的資料中**，有些資料長得非常相似，**所以透過加入雜訊有機會可以讓結果變更好**，但是**對於某些資料而言(ex.上半空的，只有下半有交叉的點那張)，不容易回想正確，或許增加資料量可以改善回想結果。**
**實作Hopfield的時候**，設定**合適的迭代次數**在實作上會遇到一些問題，因為資料的長相會影響迭代收斂的快慢，所以直接設定一個值不是一個好方法，要使用條件收斂的方式確保結束後的結果是穩定收斂的會比較好。
:::


PS:原(.exe)檔案破百MB，所以有先壓縮了，故打開需要等一陣子。
