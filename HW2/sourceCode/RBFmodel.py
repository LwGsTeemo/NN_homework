import numpy as np
import pandas as pd

def kmeans(X, k, max_iters=100):
    # 隨機初始化中心
    centers = X[np.random.choice(range(len(X)), k, replace=False)]
    for i in range(max_iters):
        # 計算每個點到中心的距離
        distances = np.linalg.norm(X[:, np.newaxis] - centers, axis=2)
        # 分配每個點到最近的中心
        labels = np.argmin(distances, axis=1)
        # 更新中心
        new_centers = np.array([X[labels == j].mean(axis=0) for j in range(k)])
        # 如果中心不再變化，結束迭代
        if np.all(centers == new_centers):
            break
        centers = new_centers

    return centers, labels

def rbf_weight(x, centers, gamma=1.0):
    if len(x.shape) == 1:  # 單點輸入
        return np.exp(-gamma * np.linalg.norm(x - centers, axis=1)**2)
    else:  # 多點輸入
        return np.exp(-gamma * np.linalg.norm(x[:, np.newaxis] - centers, axis=2)**2)

def lms_regression(X, y, learning_rate=0.01, num_epochs=1000):
    num_features = X.shape[1]
    weights = np.random.randn(num_features)

    for epoch in range(num_epochs):
        for i in range(X.shape[0]):
            prediction = np.dot(X[i], weights)
            error = y[i] - prediction
            weights += learning_rate * error * X[i]

    return weights

def model(data,k=3,num_epochs=1000):
    #輸入資料
    df = pd.DataFrame(data)
    X_train = df.iloc[:,-4:-1].values
    y_train = df.iloc[:,-1].values

    #正規化
    X_train = (X_train - np.mean(X_train, axis=0)) / np.std(X_train, axis=0)

    # 使用 KMeans 聚類算法找到 RBF 中心
    centers,label = kmeans(X_train, k, max_iters=1000)

    # 計算 RBF 核
    X_rbf_train=[]
    for i in X_train:
        X_rbf_train.append(rbf_weight(i, centers))
    X_rbf_train = np.array(X_rbf_train)

    # 使用 LMS 算法進行回歸
    weights = lms_regression(X_rbf_train, y_train, learning_rate=0.01, num_epochs=num_epochs)

    return weights,centers

def predict(state,weights,centers):
    # 預測並評估模型 ex:state=[0,0,0]3個位置的距離
    y_pred = rbf_weight(state, centers)
    y_pred = np.dot(y_pred, weights)

    return y_pred