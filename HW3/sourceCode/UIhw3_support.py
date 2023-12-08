#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.6
#  in conjunction with Tcl version 8.6
#    Oct 02, 2023 11:16:51 PM +0800  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import filedialog
import UIhw3
import Hopfield
import numpy as np

_debug = True # False to eliminate debug printing from callback functions.

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.quit)
    # Creates a toplevel widget.
    global _top1, _w1, _weights, _i, _input_pattern_size
    _top1 = root
    _w1 = UIhw3.Toplevel1(_top1)
    _i=0
    _input_pattern_size=0
    _top1.protocol( 'WM_DELETE_WINDOW' , root.quit)
    root.mainloop()

def btn1(*args):
    if _debug:
        print('unknown_support.btn1')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def datasetbtn(*args):
    if _debug:
        file_path = filedialog.askopenfilename()   # 選擇訓練檔案後回傳檔案路徑與名稱
        _w1.l1.set(file_path)
        _w1.Button3['state'] = tk.NORMAL
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def datasetbtn2(*args):
    if _debug:
        file_path = filedialog.askopenfilename()   # 選擇測試檔案後回傳檔案路徑與名稱
        _w1.l2.set(file_path)
        _w1.Button3['state'] = tk.NORMAL
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def startbtn1(*args):
    if _debug:
        #獲取路徑、是否加入雜訊
        trainPath = str(_w1.l1.get())
        testPath = str(_w1.l2.get())
        addNoise = int(_w1.c1.get()) # 0或1
        #呼叫程式
        global _weights,_input_pattern_size
        _weights = Hopfield.calW(trainPath)
        _input_pattern_size = len(Hopfield.txt2ndarray(testPath))
        _input_pattern,_output_pattern = Hopfield.output(testPath,_weights,addNoise)
        Hopfield.plot_patterns(np.vstack((_input_pattern, _output_pattern)))
        _w1.Button3['state'] = tk.NORMAL
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def testbtn1(*args):
    if _debug:
        #獲取路徑
        testPath = str(_w1.l2.get())
        addNoise = int(_w1.c1.get())
        global _i #上一張
        _i-=1
        if _i<0:
            _i=_input_pattern_size-1
        _input_pattern,_output_pattern = Hopfield.output(testPath,_weights,addNoise,i=_i)
        #呼叫程式
        Hopfield.plot_patterns(np.vstack((_input_pattern, _output_pattern)))
        _w1.Button3['state'] = tk.NORMAL
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def testbtn2(*args):
    if _debug:
        #獲取路徑
        testPath = str(_w1.l2.get())
        addNoise = int(_w1.c1.get())
        global _i #下一張
        _i+=1
        if _i>_input_pattern_size-1:
            _i=0
        _input_pattern,_output_pattern = Hopfield.output(testPath,_weights,addNoise,i=_i)
        #呼叫程式
        Hopfield.plot_patterns(np.vstack((_input_pattern, _output_pattern)))
        _w1.Button3['state'] = tk.NORMAL
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

if __name__ == '__main__':
    UIhw3.start_up()



