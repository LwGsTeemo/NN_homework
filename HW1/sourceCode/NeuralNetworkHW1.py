import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tkinter as tk
import UIhw1_support #tkinter的UI檔案
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #tkinter導入matplotlib
import matplotlib.pyplot as plt

def trainAndTest(Path,Epoch,Lr):
    UIhw1_support._w1.Button3['state'] = tk.DISABLED
    df=pd.read_table(Path,header=None,sep=" ")
    df_data = pd.DataFrame(data=np.c_[df],columns= ['x1','x2','y'])
    df_data.insert(0,'threshold',-1) #神經元之閥值為-1

    X = df_data.drop(labels=['y'],axis=1).values #取二維資料
    Y = df_data['y'].values #取答案
    Yset = list(set(Y))
    X_train, X_test, y_train, y_test = train_test_split(X, Y, 
                        test_size=0.3, random_state=40, stratify=Y)#隨機切割資料集(7:3)

    #視覺化將使用的參數
    # plt.ion()
    fig1 = plt.figure(figsize=(5, 4))
    ax1 = fig1.add_subplot(1,1,1)
    fig2 = plt.figure(figsize=(5, 4))
    ax2 = fig2.add_subplot(1,1,1)
    ax2.clear()
    plt.ion() #讓matplotlib的圖能夠動態更新
    xmin=df_data['x1'].min()
    xmax=df_data['x1'].max()
    ymin=df_data['x2'].min()
    ymax=df_data['x2'].max()
    X1=list()
    X2=list()
    X3=list()
    X4=list()
    for i in X_train:
        X1.append(i[1])
        X2.append(i[2])
    for i in X_test:
        X3.append(i[1])
        X4.append(i[2])

    #開始Training!
    lr = Lr
    epoch = Epoch
    w = np.array([-1,0,1]) #初始w為[0,1] 通過(0,-1)的水平線:0*x1+1*x2+1=0
    k=0
    trainAccuracy=0
    bestTrainAccuracy=0
    bestw=list()
    for i in range(epoch):
        #將UI的進度條加在for迴圈裡面
        UIhw1_support._w1.progressbtn.set(i*(100/epoch))
        #如果正確率==1就停止訓練
        if bestTrainAccuracy==1:
            UIhw1_support._w1.progressbtn.set(100)
            break
        #Epoch大於資料數量時就循環資料
        if k==X_train.shape[0]-1:
            k=0 

        vj=np.dot(w,X_train[k]) #計算w跟x的內積
        yj = Yset[0] if vj>=0 else Yset[1] #激勵函數(sgn二分法)
        #更新鍵結值
        if yj == Yset[0] and y_train[k]==Yset[1]:
            w = w - (lr*X_train[k])
        if yj == Yset[1] and y_train[k]==Yset[0]:
            w = w + (lr*X_train[k])

        #算訓練時的正確率，並記錄最好的weight
        correct=0
        for j in range(X_train.shape[0]):
            tmp = np.dot(w,X_train[j])
            tmp = Yset[0] if tmp>=0 else Yset[1]
            if tmp == y_train[j]:
                correct+=1
        tmpAccuracy = round(correct/X_train.shape[0],3)
        if tmpAccuracy>bestTrainAccuracy:
            bestw=w
            bestTrainAccuracy=tmpAccuracy
        trainAccuracy = tmpAccuracy
        k+=1

        #畫圖(每筆資料的散佈圖、分類結果的線)
        ax1.clear() #每次都先把之前的圖清掉，節省記憶體
        #畫出分類的線
        xplot=np.linspace(xmin, xmax, 100)
        yplot=(-1*w[1]*xplot+w[0])/w[2]       
        #畫出各資料在二維座標上的分布
        ax1.scatter(X1,X2, c=y_train)
        ax1.set_xlim([xmin*1.1-xmax*0.1,xmax*1.1-xmin*0.1])
        ax1.set_ylim([ymin*1.1-ymax*0.1,ymax*1.1-ymin*0.1])
        #畫出每次的鍵結值跟正確率
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax1.text(0.05, 0.95,'Weight:('+str(round(w[0],2))+", "+str(round(w[1],2))+", "+str(round(w[2],2))+')\naccuracy:'+str(trainAccuracy),
                transform=ax1.transAxes, fontsize=8,verticalalignment='top', bbox=props)
        ax1.plot(xplot, yplot)
        canvas1 = FigureCanvasTkAgg(fig1, master=UIhw1_support._w1.Frame1)
        # canvas1.draw()
        canvas1.get_tk_widget().place(x=0,y=0)
        canvas1.flush_events() #畫面刷新
    UIhw1_support._w1.progressbtn.set(100)

    #開始Testing!
    #拿最好的weight計算測試時的正確率
    correct=0
    for i in range(X_test.shape[0]):
        tmp = np.dot(bestw,X_test[i])
        tmp = Yset[0] if tmp>=0 else Yset[1]
        if tmp == y_test[i]:
            correct+=1
    testAccuracy = round(correct/X_test.shape[0],3)

    UIhw1_support._w1.besttrainacc.set("best training accuracy:"+str(bestTrainAccuracy))
    UIhw1_support._w1.testacc.set("testing accuracy:"+str(testAccuracy))

    #testing的作圖
    # UIhw1_support.root.update_idletasks() #畫面刷新
    xplot=np.linspace(xmin, xmax, 100)
    yplot=(-1*bestw[1]*xplot+bestw[0])/bestw[2]
    ax2.scatter(X3,X4, c=y_test)
    ax2.set_xlim([xmin*1.1-xmax*0.1,xmax*1.1-xmin*0.1])
    ax2.set_ylim([ymin*1.1-ymax*0.1,ymax*1.1-ymin*0.1])
    #畫出每次的鍵結值跟正確率
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax2.text(0.05, 0.95,'Weight:('+str(round(bestw[0],2))+", "+str(round(bestw[1],2))+", "+str(round(bestw[2],2))+')\naccuracy:'+str(testAccuracy),
            transform=ax2.transAxes, fontsize=8,verticalalignment='top', bbox=props)
    ax2.plot(xplot, yplot)
    canvas2 = FigureCanvasTkAgg(fig2, master=UIhw1_support._w1.Frame2)
    # canvas2.draw()
    canvas2.get_tk_widget().place(x=0,y=0)
    UIhw1_support.root.update_idletasks() #畫面刷新
    plt.ioff()
    plt.close(fig1)
    plt.close(fig2)