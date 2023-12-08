import numpy as np
import matplotlib.pyplot as plt
import random
import UIhw3_support
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #tkinter導入matplotlib

def txt2ndarray(path):
    fp = open(path, 'r', encoding='utf-8')
    string = fp.read()
    fp.close()
    row_list = string.splitlines()
    #return .txt data to ndarray data
    data_list = list()
    data = list()
    for row in row_list:
        for word in row:
            if(word==" "):
                data_list.append(1)
            else:
                data_list.append(-1)
        if row == "":
            data.append(data_list)
            data_list = list()
    data.append(data_list)

    return np.array(data)    

def train_hopfield_network(patterns):
    num_patterns, pattern_size = patterns.shape
    weights = np.zeros((pattern_size, pattern_size)) #初始化W
    for i in range(num_patterns):
        pattern = patterns[i, :]
        weights += np.outer(pattern, pattern) #外積(或是內積轉置後的自己)
        # weights += np.dot(pattern, pattern.T) #外積(或是內積轉置後的自己)
    np.fill_diagonal(weights, 0) #對角為0
    weights /= pattern_size #(1/P)*W

    return weights

def update_hopfield_network(input_pattern, weights, max_iter=100):
    pattern_size = len(input_pattern)
    for _ in range(max_iter): #非同步聯想
        for i in range(pattern_size):
            input_pattern[i] = np.sign((np.dot(weights[i, :], input_pattern)))

    return input_pattern

def addnoise(input_pattern): #加入雜訊(以0.25的機率將1變-1,將-1變1)
    for i in input_pattern:
        dice = random.randint(0,3)
        if dice == 0:
            input_pattern[i] *= -1

    return input_pattern

def plot_patterns(patterns): #將結果化在tkinter上
    num_patterns, pattern_size = patterns.shape
    if pattern_size == 100:
        pattern_col,pattern_row = 10,10
    else:
        pattern_col,pattern_row = 12,9
    fig1 = plt.figure(figsize=(10,4))
    plt.ion()
    ax1 = fig1.add_subplot(1,1,1)
    ax1.clear()
    for i in range(num_patterns):
        plt.subplot(1, num_patterns, i + 1)
        plt.imshow(patterns[i, :].reshape((pattern_col,pattern_row)), cmap='gray')
    canvas1 = FigureCanvasTkAgg(fig1, master=UIhw3_support._w1.Frame1)
    canvas1.get_tk_widget().place(x=0,y=0)
    canvas1.flush_events() #畫面刷新
    UIhw3_support.root.update_idletasks()
    plt.ioff()

def calW(path):
    patterns_data = txt2ndarray(path)
    # Hopfield網路 算鍵結值
    weights = train_hopfield_network(patterns_data)

    return weights

def output(testPath,weights,addNoise=0,i=0):
    # 讀取測試資料，並丟入W算輸出
    input_pattern = txt2ndarray(testPath)[i]  # 使用第i個資料當輸入
    if addNoise==1:
        input_pattern = addnoise(input_pattern)
    output_pattern = update_hopfield_network(input_pattern.copy(), weights, max_iter=100)

    return input_pattern,output_pattern
