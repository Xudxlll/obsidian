---
title: "DBSCAN 分群演算法介紹與實際應用範例"
source: "https://myapollo.com.tw/blog/dbscan/"
author:
published: 2024-09-02T23:39:49CET
created: 2026-07-03
description: "以前在開發 Chrome 擴充 NimoTab 時，有 1 個功能需要將相似/相同的網頁標題分群在一起，例如下圖：當時用的是土炮的方法（但其實類似 DBSCAN），不過後來跟從事機器學習的同事討教有沒有更好的做法時，才知道有 1 個稱為 DBSCAN 的演算法可以使用。本文將介紹 DBSCAN 這個實用的分群演算法，並以實際範例展示如何做到將相似的資料分群在一起，藉此讓大家對 DBSCAN 有更深入的理解。"
tags:
  - "clippings"
---
> [!info] Info
> 覺得我們的內容實用嗎？ MyApollo 電子報讀者募集中！歡迎 [訂閱電子報](https://myapollo.ck.page/709413e150)!

以前在開發 Chrome 擴充 [NimoTab](https://chromewebstore.google.com/detail/nimotab/mhhkfkjgnfddpodoepjigdeaaookhfln?hl=zh-TW) 時，有 1 個功能需要將相似/相同的網頁標題分群在一起，例如下圖：

軟體

![nimotab-clustering.png](https://r.anikit.app/i/PqwdQo8Y5s)

當時用的是土炮的方法（但其實類似 DBSCAN），不過後來跟從事 [機器學習](#) 的同事討教有沒有更好的做法時，才知道有 1 個稱為 DBSCAN 的演算法可以使用。

本文將介紹 DBSCAN 這個實用的分群演算法，並以實際範例展示如何做到將相似的資料分群在一起，藉此讓大家對 DBSCAN 有更深入的理解。

### 本文環境

- Python 3

### 群 (cluster) / 雜訊 (noise)

在理解 DBSCAN 演算法之前，需要先理解 2 個機器學習的重要概念：

分群(Clustering)是機器學習中的一個重要主題，其目標是將一組資料中的相似資料歸納到同一群組。如果資料集中存在多種相似資料，則可以將其分成多個群組。由於分群屬於非監督式學習技術，它可以應用於沒有標準答案的情況。

程式設計

p.s. 如果每一筆資料都有正確答案或者標籤(label)的情況，通常會使用另一種稱為分類(classification)的技術

例如下圖可以明顯感覺到資料能夠分成 2 群，而剩下的 1 個黑色點無法被歸類，這就是雜訊(noise)。

![clusters-demo.png](https://r.anikit.app/i/YukEryGcyE)

雜訊(Noise)在機器學習中指的是那些不符合任何已知群組特徵或模式的資料。這些資料可能是因為異常值、錯誤而產生，通常無法被機器學習模型很好地解釋，甚至可能干擾模型的訓練和預測過程，因此通常需要特別處理或排除。

在分群的應用情境下，雜訊通常指那些無法歸屬於任何一個群組的資料。

### DBSCAN (Density-Based Spatial Clustering of Applications with Noise) 簡介

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) 是一種基於密度的分群演算法，針對集中形狀不規則的資料進行分群，例如以下是 [sklearn](https://scikit-learn.org/stable/index.html) 針對多種分群演算法所做的比較圖：

機器學習與人工智慧

![sphx_glr_plot_cluster_comparison_001.png](https://r.anikit.app/i/1EuPuLL6E8)

其中關於 DBSCAN 的分群結果，可以看到 DBSCAN 對於集中形狀不規則資料分群效果頗好的：

![dbscan-demo.png](https://r.anikit.app/i/mplkzt4Emg)

DBSCAN 的主要特點是 **可以自動處理資料中的雜訊(noise)以及不需要預先指定群數** 。

DBSCAN 通過分析資料點的鄰近密度來判斷哪些點屬於相同的群，並將密度不足的資料點標為雜訊，這使得 **DBSCAN 適合用於含有雜訊的資料集(dataset)** 。

#### 圖解 DBSCAN 核心概念

DBSCAN 有 3 個重要核心概念：

- Core points
- Reachable points
- Outliers

在使用 DBSCAN 時，我們需要定義：

指令碼語言

- 1 個半徑(radius) **ε**
- 1 個群所需要的最少鄰居數 **minPoints**

如果有 1 個點 p 周圍半徑 **ε** 滿足 1 個群所需要的最少鄰居數 **minPoints** （包含 p 點），那點 p 就是 **Core points** ，例如下圖：

![core-points.png](https://r.anikit.app/i/GqfdYFee_J)

然後 DBSCAN 會從 Core points p 點的鄰近點開始，查看每一個鄰近點是否有周圍半徑 **ε** 滿足 1 個群所需要的最少鄰居數 **minPoints** 的情況。如果有的話，這個鄰近點也屬於 Core points；如果沒有的話就屬於 **Reachable points** 。

例如下圖 P, Q, R, S 都符合 Core points 的條件，而 T 點則無法滿足 Core points 的條件，因為 T 點的周圍半徑只有 Q 點，但是 T 點仍落在 Q 點的周圍半徑範圍內，所以 T 屬於 Reachable points，而 P, Q, R, S, T 屬於同 1 個群：

![reachable-points.png](https://r.anikit.app/i/Ee3-AC0pB9)

如果有 1 個點無法滿足 Core points 與 Reachable points 的條件，就屬於 Outliers (或稱雜訊)，例如下圖的 U 點：

![outliers.png](https://r.anikit.app/i/4y4_DgsPzt)

也因為 DBSCAN 會以群內的每個點為中心尋找周圍是否仍有符合 Core points 條件的點，並藉此擴展群的範圍，所以它具有針對集中形狀不規則的資料進行分群的能力，它的運作過程如下，可以看到群的擴展過程：

軟體

![](https://www.youtube.com/watch?v=8gpmwelO0BM)
  

p.s. 可以在 [Visualizing DBSCAN Clustering](https://www.naftaliharris.com/blog/visualizing-dbscan-clustering) 玩看看 DBSCAN

### DBSCAN 演算法

DBSCAN 的演算法虛擬碼(pseudocode)如下所示：

![dbscan-pseudocode.png](https://r.anikit.app/i/Mkc8QkLYVk)

上述虛擬碼的註解其實已經將 DBSCAN 解釋得很清楚，在此不多加贅述。

上圖可以看到 DBSCAN 參數中有距離函式 **distFunc** (distance function)，這代表 **DBSCAN 可以使用任意距離函數來衡量資料跟資料之間的距離** ，最簡單的距離函數可以使用 [歐幾里德距離](https://zh.wikipedia.org/zh-tw/%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E8%B7%9D%E7%A6%BB) ；參數 **eps** 就是我們所定義的半徑(radius) **ε** ；參數 **minPts** 則是 1 個群所需要的最少鄰居數 **minPoints** 。

而上圖的 `RangeQuery()` 虛擬碼如下，它做的事情很單純，即是找出參數 **Q** 點的周圍半徑 **eps** 內有多少筆鄰近的資料：

![query-range.png](https://r.anikit.app/i/R7Y351ZV3M)

### 以 Python 實作 DBSCAN

以 Python 程式碼實作 DBSCAN 的程式碼如下：

指令碼語言

```python
def dbscan(data, distance_func, eps, min_points):
    """
    Performs DBSCAN clustering on the given data.

    Args:
        data: A list of data points.
        distance_func: The distance function to use.
        eps: The radius around each point.
        min_points: The minimum number of points required to form a dense region.

    Returns:
        A list of cluster assignments for each data point.
    """
    labels = [None] * len(data)  # Initialize labels as None (undefined)
    cluster_id = 0

    for i in range(len(data)):
        if labels[i] is not None:  # Already assigned to a cluster or noise
            continue

        neighbors = range_query(data, distance_func, i, eps)
        if len(neighbors) < min_points:
            labels[i] = -1  # Mark as noise
        else:
            cluster_id += 1
            labels[i] = cluster_id
            # Expand cluster
            seeds = neighbors.copy()
            for j in seeds:
                if labels[j] == -1:
                    labels[j] = cluster_id

                if labels[j] is not None:
                    continue

                labels[j] = cluster_id

                new_neighbors = range_query(data, distance_func, j, eps)
                if len(new_neighbors) >= min_points:
                    for k in new_neighbors:
                        if k not in seeds:
                          seeds.append(k)
    return labels
```

前述程式碼的 `dbscan()` 會回傳 1 個長度與參數 `data` 相同的 list，其中每個元素對應的是參數 `data` 的群，如果值為 -1 則代表為雜訊，1 以上的值(含 1)則代表群的編號。

前述程式碼的 `range_query()` 實作如下，其作用是找出特定點的周圍半徑 **eps** 內的資料的索引值：

```python
def range_query(data, distance_func, point_index, eps):
    """Finds the neighbors of a point within a given radius (eps)."""
    neighbors = []
    for i in range(len(data)):
        if distance_func(data[point_index], data[i]) <= eps:
            neighbors.append(i)
    return neighbors
```

如此就實作完 DBSCAN 了！

### DBSCAN 實際應用

假設我們有一大堆新聞文章標題，如果我們想有效率地對文章標題進行整理，因為我們通常不知道要將文章分成幾類，此時就可以使用 DBSCAN 將相似的文章整理在一起。

軟體

而衡量文章標題相似度的距離函數可以使用 [Jaccard Index](https://myapollo.com.tw/blog/jaccard-index-explaination/) ，至於斷詞(tokenize)方式我們可以使用 bigram，這樣做的好處是實作很簡單之外，也可以處理中英文混雜的情況（當然，如果有好的斷詞器也可以使用）。

p.s. bigram 是指將字串斷詞長度為 2 的多個子字串，例如 `我愛演算法` 可以斷詞成 `我愛`, `愛演`, `演算`, `算法` ，除了以字元為單位之外，bigram 也可以用詞做為單位，例如 `(我, 愛)`, `(愛, 演算法)` 也算是 bigram。

以字元為單位的 bigram 程式碼如下：

```python
def bigram_tokenize(text):
    """Tokenizes a text string into bigrams."""
    tokens = []
    for i in range(len(text) - 1):
        tokens.append(text[i:i+2])
    return tokens
```

計算相似度的 Jaccard Index 程式碼如下：

```python
def jaccard_distance(tokens1, tokens2):
    """Calculates the distance between two token lists using Jaccard distance."""
    set1 = set(tokens1)
    set2 = set(tokens2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0
    return 1 - (intersection / union)
```

實際用 1 個例子作為示範，讓各位知道使用 DBSCAN 分群的大致過程。

假設，以下是我們想分群的文章標題（為方便僅顯示五筆）：

```
data = [
    'AI technology transforming industries',
    'AI 技術如何改變行業',
    'Introduction to Machine Learning',
    '機器學習入門',
    'Top 10 Python libraries for data science',
]
```

接著，我們對每一個文章標題進行 bigram 斷詞：

```
tokenized_data = [bigram_tokenize(text) for text in data]
```

再來，交給 DBSCAN 演算法進行分群，使用的距離函數為 Jaccard Index，我們把半徑設定為 0.6，以及群的最少資料數為 3（各位可以自行調整設定）：

```
eps = 0.6       # Adjust the radius as needed
min_points = 3  # Adjust the minimum points as needed
labels = dbscan(tokenized_data, jaccard_distance, eps, min_points)
```

最後，我們把分群結果與原始資料合併顯示：

```python
from collections import defaultdict
from pprint import pprint

d = defaultdict(list)

# Print the cluster assignments
for i in range(len(data)):
  cluster_id = labels[i]
  if cluster_id == -1:
    #print(f"{data[i]} - Noise")
    pass
  else:
    d[cluster_id].append(data[i])

for k, v in d.items():
  print(f"Cluster {k}:")
  pprint(v)
  print('--'*5)
```

分群結果如下，從結果也可以看到一些相似的標題都被分在同 1 群中的狀況：

```javascript
Cluster 1:
['Introduction to Machine Learning',
 'Introduction to Reinforcement Learning',
 'Introduction to cloud computing',
 'Introduction to AI ethics']
----------
Cluster 2:
['人工智慧在醫療中的應用',
 '人工智慧在網路安全中的應用',
 '人工智慧在自動駕駛中的應用',
 '人工智慧在個人化醫療中的應用',
 '人工智慧在自然災害預測中的應用',
 '人工智慧在零售行業中的應用',
 '機器學習在異常偵測中的應用',
 '人工智慧在電子商務中的應用',
 '機器學習在醫療中的應用',
 '人工智慧在預測性維護中的應用',
 '人工智慧在環境可持續性中的應用',
 '人工智慧在法律科技中的應用',
 '人工智慧在個人化客戶體驗中的應用',
 '人工智慧在公共政策中的應用',
 '人工智慧在風險管理中的應用',
 '人工智慧在創意產業中的應用',
 '人工智慧在遊戲中的應用',
 '人工智慧在災難應對中的應用']
----------
Cluster 3:
['Automated machine learning tools',
 'How to train a machine learning model',
 'How to deploy machine learning models',
 'How to learn deep learning',
 'Top machine learning algorithms',
 'AI and machine learning in manufacturing']
----------
Cluster 4:
['人工智慧驅動的聊天機器人',
 '人工智慧驅動的行銷策略',
 '人工智慧驅動的推薦系統',
 '人工智慧驅動的供應鏈管理',
 '人工智慧驅動的虛擬助理',
 '人工智慧驅動的商業智慧']
----------
Cluster 5:
['深度學習在電腦視覺中的應用',
 '深度學習在機器人學中的應用',
 '深度學習在語音辨識中的應用']
```

是否很有趣呢！

p.s. [完整程式碼在此](https://colab.research.google.com/drive/1_CzY_J6c-ID_Zh5hJrTwYtSYIMW1_t2j?usp=sharing)

#### 如何調整 DBSCAN 分群結果

調整 DBSCAN 分群結果的方法有幾個：

1. 調整 eps，也就是半徑大小，如果分群結果雜訊比較多，可以試著增加 eps 以減少雜訊的數量。
2. 調整 minPoints，如果希望成群的條件變嚴苛，則可以調整 minPoints 參數，不過增加 minPoints 會讓成群的條件變嚴苛，也可能導致某些小群組變成雜訊。
3. 調整距離函數，使用合適的距離函式，也能夠改善 DBSCAN 分群的能力。

### 總結

本文所介紹的 DBSCAN 演算法是相當實用的分群演算法，其優點在於：

- 不需事先設定群的數量（例如 [K-means](https://en.wikipedia.org/wiki/K-means_clustering) 需要事先設定群的數量）
- 可以處理雜訊(noise)
- 對集中形狀不規則的資料有較佳的處理能力

本文實際用 Python 程式碼進行實作並展示實際應用的範例，以期讓初學者能夠有足夠的認識基礎，不過各大 [機器學習](#) 相關的框架都有實作 DBSCAN（例如 [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html) ），如果對 DBSCAN 已有足夠理解的話，可以直接使用各大框架所實作的 DBSCAN 即可。

指令碼語言

以上！

Enjoy!

### References

[DBSCAN - Wikipedia](https://en.wikipedia.org/wiki/DBSCAN)

[DBSCAN, Explained in 5 Minutes](https://towardsdatascience.com/dbscan-explained-in-5-minutes-133f6a9766e4)

[不要再用 K-means！ 超實用分群法 DBSCAN 詳解](https://axk51013.medium.com/%E4%B8%8D%E8%A6%81%E5%86%8D%E7%94%A8k-means-%E8%B6%85%E5%AF%A6%E7%94%A8%E5%88%86%E7%BE%A4%E6%B3%95dbscan%E8%A9%B3%E8%A7%A3-a33fa287c0e)

[sklearn - Clustering](https://scikit-learn.org/stable/modules/clustering.html)

> [!info] Info
> 覺得我們的內容實用嗎？ MyApollo 電子報讀者募集中！歡迎 [訂閱電子報](https://myapollo.ck.page/709413e150)!

### 對抗久坐職業傷害

研究指出每天增加 2 小時坐著的時間，會增加大腸癌、心臟疾病、肺癌的風險，也造成肩頸、腰背疼痛等常見問題。

軟體

然而對抗這些問題，卻只需要 **工作時定期休息跟伸展身體** 即可！

你想輕鬆改變現狀嗎？試試看我們的 PomodoRoll 番茄鐘吧！ PomodoRoll 番茄鐘會根據你所設定的專注時間，定期建議你 1 項辦公族適用的伸展運動，幫助你打敗久坐所帶來的傷害！

### 贊助我們的創作

看完這篇文章了嗎? 休息一下，喝杯咖啡吧！

如果你覺得 MyApollo 有讓你獲得實用的資訊，希望能看到更多的技術分享，邀請你贊助我們一杯咖啡，讓我們有更多的動力與精力繼續提供高品質的文章，感謝你的支持！

<iframe title="Comments" src="https://utteranc.es/utterances.html?src=https%3A%2F%2Futteranc.es%2Fclient.js&amp;repo=spitfire-sidra%2Fmyapollo-issues&amp;issue-term=pathname&amp;theme=github-light&amp;crossorigin=anonymous&amp;async=&amp;url=https%3A%2F%2Fmyapollo.com.tw%2Fblog%2Fdbscan%2F&amp;origin=https%3A%2F%2Fmyapollo.com.tw&amp;pathname=blog%2Fdbscan%2F&amp;title=DBSCAN+%E5%88%86%E7%BE%A4%E6%BC%94%E7%AE%97%E6%B3%95%E4%BB%8B%E7%B4%B9%E8%88%87%E5%AF%A6%E9%9A%9B%E6%87%89%E7%94%A8%E7%AF%84%E4%BE%8B+-+MyApollo&amp;description=%E4%BB%A5%E5%89%8D%E5%9C%A8%E9%96%8B%E7%99%BC+Chrome+%E6%93%B4%E5%85%85+NimoTab+%E6%99%82%EF%BC%8C%E6%9C%89+1+%E5%80%8B%E5%8A%9F%E8%83%BD%E9%9C%80%E8%A6%81%E5%B0%87%E7%9B%B8%E4%BC%BC%2F%E7%9B%B8%E5%90%8C%E7%9A%84%E7%B6%B2%E9%A0%81%E6%A8%99%E9%A1%8C%E5%88%86%E7%BE%A4%E5%9C%A8%E4%B8%80%E8%B5%B7%EF%BC%8C%E4%BE%8B%E5%A6%82%E4%B8%8B%E5%9C%96%EF%BC%9A%0A%E7%95%B6%E6%99%82%E7%94%A8%E7%9A%84%E6%98%AF%E5%9C%9F%E7%82%AE%E7%9A%84%E6%96%B9%E6%B3%95%EF%BC%88%E4%BD%86%E5%85%B6%E5%AF%A6%E9%A1%9E%E4%BC%BC+DBSCAN%EF%BC%89%EF%BC%8C%E4%B8%8D%E9%81%8E%E5%BE%8C%E4%BE%86%E8%B7%9F%E5%BE%9E%E4%BA%8B%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92%E7%9A%84%E5%90%8C%E4%BA%8B%E8%A8%8E%E6%95%99%E6%9C%89%E6%B2%92%E6%9C%89%E6%9B%B4%E5%A5%BD%E7%9A%84%E5%81%9A%E6%B3%95%E6%99%82%EF%BC%8C%E6%89%8D%E7%9F%A5%E9%81%93%E6%9C%89+1+%E5%80%8B%E7%A8%B1%E7%82%BA+DBSCAN+%E7%9A%84%E6%BC%94%E7%AE%97%E6%B3%95%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%E3%80%82%0A%E6%9C%AC%E6%96%87%E5%B0%87%E4%BB%8B%E7%B4%B9+&amp;og%3Atitle=DBSCAN+%E5%88%86%E7%BE%A4%E6%BC%94%E7%AE%97%E6%B3%95%E4%BB%8B%E7%B4%B9%E8%88%87%E5%AF%A6%E9%9A%9B%E6%87%89%E7%94%A8%E7%AF%84%E4%BE%8B&amp;session="></iframe><iframe frameborder="0" allow="attribution-reporting; run-ad-auction" src="https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-3095417441650599&amp;output=html&amp;adk=1812271804&amp;adf=3025194257&amp;abgtt=6&amp;lmt=1749052224&amp;plat=9%3A32776%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32%2C43%3A32%2C44%3A32&amp;format=0x0&amp;url=https%3A%2F%2Fmyapollo.com.tw%2Fblog%2Fdbscan%2F&amp;pra=5&amp;asro=0&amp;aimartd=4&amp;aieuf=1&amp;aicrs=1&amp;uach=WyJtYWNPUyIsIjI2LjUuMSIsImFybSIsIiIsIjE0OS4wLjc4MjcuMTk3IixudWxsLDAsbnVsbCwiNjQiLFtbIkdvb2dsZSBDaHJvbWUiLCIxNDkuMC43ODI3LjE5NyJdLFsiQ2hyb21pdW0iLCIxNDkuMC43ODI3LjE5NyJdLFsiTm90KUE7QnJhbmQiLCIyNC4wLjAuMCJdXSwwXQ..&amp;dt=1783047645939&amp;bpp=8&amp;bdt=24108&amp;idt=5314&amp;shv=r20260701&amp;mjsv=m202606290101&amp;ptt=9&amp;saldr=aa&amp;abxe=1&amp;cookie_enabled=1&amp;eoidce=1&amp;nras=1&amp;correlator=6604466219735&amp;frm=20&amp;pv=2&amp;u_tz=480&amp;u_his=3&amp;u_h=1080&amp;u_w=1920&amp;u_ah=983&amp;u_aw=1920&amp;u_cd=24&amp;u_sd=2&amp;dmc=16&amp;adx=-12245933&amp;ady=-12245933&amp;biw=1369&amp;bih=822&amp;scr_x=0&amp;scr_y=0&amp;eid=42532761%2C95395661%2C31099465&amp;oid=2&amp;pvsid=2629748776868910&amp;tmod=2062083860&amp;uas=0&amp;nvt=1&amp;fsapi=1&amp;ref=https%3A%2F%2Fwww.google.com%2F&amp;fc=1920&amp;brdim=240%2C70%2C240%2C70%2C1920%2C30%2C1440%2C903%2C1384%2C822&amp;vis=2&amp;rsz=%7C%7Cs%7C&amp;abl=NS&amp;fu=32768&amp;bc=31&amp;plas=228x644_l%7C269x644_r&amp;bz=1.04&amp;ifi=1&amp;uci=a!1&amp;fsb=1&amp;dtd=5361" title="Advertisement" aria-label="Advertisement"></iframe><iframe width="1005" height="124" frameborder="0" allow="attribution-reporting; run-ad-auction" src="https://googleads.g.doubleclick.net/pagead/html/r20260701/r20190131/zrt_lookup_fy2021.html#RS-3-&amp;adk=1812271801&amp;client=ca-pub-3095417441650599&amp;fa=1&amp;ifi=3&amp;uci=a!3&amp;btvi=1" title="Advertisement" aria-label="Advertisement"></iframe>

機器學習與人工智慧