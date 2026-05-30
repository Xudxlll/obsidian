# AMA 564 Deep Learning

# 2026 Spring

# Lecture 5

32x32x3 image   
![](images/bc75468bd245d931b1d869f7dec50a2e169eaddf2847ac25f350469ca679f322.jpg)

<details>
<summary>text_image</summary>

32 height
32 width
3 depth
</details>

![](images/1fe2bf07b2d27c10c1d1ad37e3f60c1e948ab2f43452fea30204d9e74394fe4a.jpg)

<details>
<summary>text_image</summary>

32x32x3 image
32 height
32
width
3
depth
Filters always extend the full
depth of the input volume
5x5x3 filter
Convolve the filter with the in
i.e. "slide over the image spa
computing dot products"
</details>

mage tially,

![](images/a1d194b8c9fa129fe904b6d631aed4413bfaa6a2a0cd7a50070978eaa241c18e.jpg)

<details>
<summary>text_image</summary>

32x32x3 image
5x5x3 filter w
32
32
1 number:
the result of
filter and a s
(i.e. 5*5*3 =
</details>

#

f taking a dot product between the small 5x5x3 chunk of the image = 75-dimensional dot product + bias)

$$
\boldsymbol {w} ^ {T} \boldsymbol {x} + \boldsymbol {b}
$$

![](images/c2ebe7d32d65e58abc9a353310bbff2a346358b6ff4bf565c23781a798c973d0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["32x32x3 image"] --> B["convolve (slide) over all spatial locations"]
    C["5x5x3 filter"] --> B
    B --> D["activation maps"]
```
</details>

![](images/09d49c2ced27f3d0ab615d43a2c179b272475beec80cc95e13ecf0b442729898.jpg)

<details>
<summary>natural_image</summary>

3D geometric diagram showing two stacked blue and teal squares with dashed lines indicating projection or perspective (no text or symbols)
</details>

Output

Filter

Input

Padding

![](images/5ba238d47424409c0ff86922730e58d4576860c87e2d19f54fbb1ab44ed062a7.jpg)

<details>
<summary>text_image</summary>

3
32
32
</details>

![](images/3f6efac265b3197d08bbcf67a681cb71a0ce2ef99f7f00ba2a34cbfc13b8b2ea.jpg)  
1 number: Convolution Layers

activation maps   
![](images/7a59f9f379ae5310de014ad7bbbccbbf214426f3cd9c05ae078a206fe43ec24f.jpg)

<details>
<summary>text_image</summary>

28
28
6
</details>

Stack these up to get a new “image” of size 28x28x6!

CNN is a sequence of Convolution Layers , interspersed with activation functions.

![](images/c630d29375b79aeb36f321b9570afa1cda52bc5f7e8b425e1f95f5788c999d7f.jpg)

CONV,

ReLU

e.g. 6 5x5x3

filters

CONV,

ReLU

e.g. 10 5x5x6

filters

CONV,

ReLU

# Pooling Layer is a down sampling strategy.

1. Construct better translationally invariant features.   
2. Learn more compact features.

![](images/f368ba233c8cd4e1c40edb2496f51433592a34a59d83c19d49c9cb046bb3b1a4.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["224x224x64"] --> B["pool"]
    C["112x112x64"] --> D["downsampling"]
    E["224"] --> F["downsampling"]
    G["112"] --> H["downsampling"]
    I["112"] --> J["downsampling"]
```
</details>

# Famous CNN Architectures

LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. Proceedings of the IEEE, 86(11), 2278-2324.

![](images/e6c178747c25572c5ba7a87adbfd55c33f607f40ac6232ee6335ec62ff781a83.jpg)

<details>
<summary>bar</summary>

| Layer | Feature Maps | Convolutional Segments | Subsampling Segments |
|-------|--------------|------------------------|----------------------|
| C1    | feature maps  | 6@28x28                | -                    |
| C3    | f. maps      | 16@10x10               | -                    |
| S2    | f. maps      | 6@14x14                | -                    |
| S4    | f. maps      | 16@5x5                 | -                    |
| C5    | layer        | 120                    | -                    |
| F6    | layer        | 84                     | -                    |
| OUTPUT | -            | -                      | 10                   |
</details>

![](images/7347d4a8a22bc88efcff953d8b19ea4376fa595c63cf47b07c10c63adfc80711.jpg)

<details>
<summary>other</summary>

| Layer | Layer Count |
|-------|-------------|
| C1: feature maps | 6@28x28 |
| C3: f. maps | 16@10x10 |
| S2: f. maps | 6@14x14 |
| S4: f. maps | 16@5x5 |
| C5: layer | 120 |
| F6: layer | 84 |
| OUTPUT | 10 |
The image displays a schematic representation of the neural network layers and connections. The input dimension is labeled as 32x32. The bottom section shows convolutional, subsampling, and full connection layers.
</details>

# Key Summary:

7 Layers (input layer not counted)   
3 Convolution Layers (C1; C3; C5)   
2 Pooling Layers (S2; S4)   
2 Fully Connected Layers (F6; Output)

Sigmoid Activation!

![](images/73c917217b3ba992b5fcbb14fe632c614e1cfaf0a5c874f7e1e3b10b2ec0c603.jpg)

<details>
<summary>bar</summary>

| Layer | Layer Description         | Value |
|-------|---------------------------|-------|
| C1    | Feature Maps               | 6@28x28 |
| C3    | f. maps                   | 16@10x10 |
| S2    | f. maps                   | 6@14x14 |
| S4    | f. maps                   | 16@5x5 |
| C5    | Layer                     | 120   |
| F6    | Layer                     | 84    |
| OUTPUT | Output                    | 10    |
</details>

Details:

# C1: Convolution Layer

Input channel: 1 £ Output channel: 6

Input size: 1 x 32 x 32

Kernel size: 5 x 5

Output size: 6 x 28 x 28

![](images/817a1430a39ac06c3a1fd44c492e761c1e868fe6991795de785096b9a3829e3b.jpg)

<details>
<summary>bar</summary>

| Layer | Feature Maps | Layer Count |
|-------|--------------|-------------|
| C1    | feature maps  | 6@28x28     |
| C3    | f. maps      | 16@10x10    |
| S2    | f. maps      | 6@14x14     |
| S4    | f. maps      | 16@5x5      |
| C5    | layer        | 120         |
| F6    | layer        | 84          |
| OUTPUT|          | 10          |
</details>

# Details:

# S2: Max Pooling Layer

Input size: 6 x 28 x 28

Pooling size: 2 x 2

Output size: 6 x 14 x 14

![](images/c2ff0b85ffbc78ac9bfeb4bb99135e7675463a741c5918334eaf1e4d1d041019.jpg)

<details>
<summary>bar</summary>

| Layer | Layer Description         | Count |
|-------|---------------------------|-------|
| C1    | Feature Maps              | 6@28x28 |
| C2    | Subsampling               | 6@14x14 |
| C3    | f. maps                   | 16@10x10 |
| C4    | f. maps                  | 16@5x5 |
| C5    | Layer                     | 120   |
| F6    | Layer                     | 84    |
| OUTPUT | Output                    | 10    |
</details>

# Details:

# C3: Convolution Layer

Input channel: 6

Output channel: 16

Input size: 6 x 14 x 14

Kernel size: 5 x 5

Output size: 16 x 10 x 10

![](images/d3092c7d165af3856fae147e25fbe62f561e239a0914e393cb11612dfb18c9e2.jpg)

<details>
<summary>other</summary>

| Layer | Layer Description         | Feature Maps | Convolution Type |
|-------|---------------------------|--------------|------------------|
| C1    | Feature Maps              | 6@28x28      | Convolutions      |
| C2    | Subsampling               | 6@14x14      | Subsampling      |
| C3    | f. maps                  | 16@10x10     | Convolutions      |
| C4    | f. maps                  | 16@5x5       | Subsampling      |
| C5    | Layer                     | 120          | Full connection   |
| F6    | Layer                     | 84           | Full connection   |
| OUTPUT | Output                    | -            | Gaussian connections |
</details>

# Details:

# S4: Max Pooling Layer

Input size: 16 x 10 x 10

Pooling size: 2 x 2

Output size: 16 x 5 x 5

![](images/53dd51fbb118287d2ce18808c3f6c1ed35d44eba8b1172ea11e8fd0ba4468ce0.jpg)

<details>
<summary>bar</summary>

| Layer | Layer Description         | Dimension |
|-------|---------------------------|---------|
| C1    | Feature Maps               | 6@28x28 |
| C2    | Subsampling               | 6@14x14 |
| C3    | f. maps                   | 16@10x10 |
| C4    | f. maps                   | 16@5x5  |
| C5    | Layer                     | 120     |
| F6    | Layer                     | 84      |
| OUTPUT | Output                    | 10      |
</details>

# Details:

# C5: Convolution Layer

Input channel: 16

Output channel: 120

Input size: 16 x 5 x 5

Kernel size: 5 x 5

Output size: 1 x 120

![](images/f5a4d349cf816d44ffe62ed96e000571993786bc205104ee4554fa3ed146a2ec.jpg)

<details>
<summary>bar</summary>

| Layer | Feature Maps | Convolutional Segments | Subsampling Segments |
|-------|--------------|------------------------|----------------------|
| C1    | feature maps  | 6@28x28                | -                    |
| C3    | f. maps      | 16@10x10               | -                    |
| S2    | f. maps      | 6@14x14                | -                    |
| S4    | f. maps      | 16@5x5                 | -                    |
| C5    | layer        | 120                    | -                    |
| F6    | layer        | 84                     | -                    |
| OUTPUT| -            | -                      | 10                   |
</details>

Details:

# F6: Fully Connected Layer

Input size: 1 x 120

Output size: 1 x 84

![](images/322a4b9fe4fd306c89ba39ecc1b89b7e6742d3f915705053249cc0bda0cf2b31.jpg)

<details>
<summary>bar</summary>

| Layer | Layer Description         | Count |
|-------|---------------------------|-------|
| C1    | Feature Maps               | 6@28x28 |
| C2    | Subsampling               | 6@14x14 |
| C3    | f. maps                   | 16@10x10 |
| C4    | f. maps                   | 16@5x5 |
| C5    | Layer                     | 120   |
| F6    | Layer                     | 84    |
| OUTPUT | Output                    | 10    |
</details>

# Details:

# Output: Fully Connected Layer

Input size: 1 x 84

Output size: 1 x 10

![](images/1c95edc5bd3e13e4d9fc503c6ed8df925cce6d2373c2ec47cb223d7847fcf5ee.jpg)

<details>
<summary>bar</summary>

| Layer | Feature Maps | Convolutional Segments | Subsampling Segments |
|-------|--------------|------------------------|----------------------|
| C1    | feature maps  | 6@28x28                | -                    |
| C3    | f. maps      | 16@10x10               | -                    |
| S2    | f. maps      | 6@14x14                | -                    |
| S4    | f. maps      | 16@5x5                 | -                    |
| C5    | layer        | 120                    | -                    |
| F6    | layer        | 84                     | -                    |
| OUTPUT | -            | -                      | 10                   |
</details>

# Summary Remark:

A Simple CNN architecture.

Use Sigmoid as activation function.

Convolution layer can convert a tensor to a vector!

![](images/fa6d51e3d17ac446556ee9df6f02ad8e1691db93cc8e08b7a5d274a25b3bc1fd.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    INPUT["INPUT 32x32"] --> A["A"]
    A --> B["Convolutions"]
    A --> C["Subsampling"]
    A --> D["Convolutions"]
    A --> E["Full connection"]
    A --> F["Full connection"]
    A --> G["Gaussian connections"]
    
    subgraph Input Layer
        H["3"]
    end
    
    subgraph Convolutional Layers
        I["3:0"]
        J["3:3"]
        K["3:5"]
        L["3:7"]
        M["3:9"]
        N["4:11"]
        O["4:13"]
        P["4:15"]
        Q["4:17"]
        R["4:19"]
        S["4:21"]
        T["4:23"]
        U["4:25"]
        V["4:27"]
        W["4:29"]
        X["4:31"]
        Y["4:33"]
        Z["4:35"]
        AA["4:37"]
        AB["4:39"]
        AC["4:41"]
        AD["4:43"]
        AE["4:45"]
        AF["4:47"]
        AG["4:49"]
        AH["4:51"]
        AI["4:53"]
        AJ["4:55"]
        AK["4:57"]
        AL["4:59"]
        AM["4:61"]
        AN["4:63"]
        AO["4:65"]
        AP["4:67"]
        AQ["4:69"]
        AR["4:71"]
        AS["4:73"]
        AT["4:75"]
        AU["4:77"]
        AV["4:79"]
        AW["4:81"]
        AX["4:83"]
        AY["5"]
    end
    
    subgraph Subsampling
        AZ["3:0"]
        BA["3:3"]
        BB["3:5"]
        BC["3:7"]
        BD["3:9"]
        BE["4:11"]
        BF["4:13"]
        BG["4:15"]
        BH["4:17"]
        BI["4:19"]
        BJ["4:21"]
        BK["4:23"]
        BL["4:25"]
        BM["4:27"]
        BN["4:29"]
        BO["4:31"]
        BP["4:33"]
        BQ["4:35"]
        BR["4:37"]
        BS["4:39"]
        BT["4:41"]
        BU["4:43"]
        BV["4:45"]
        BW["4:47"]
        BX["4:49"]
        BY["4:51"]
        BZ["5"]
    end
    
    subgraph Full Connections
        CA["5:0"]
        CB["5:1"]
        CC["5:2"]
        DD["5:3"]
        EE["5:4"]
        FF["5:5"]
        DG["5:6"]
        DH["5:7"]
        DI["5:8"]
        DJ["5:9"]
    end
    
    subgraph Full Connection
        CE["5:0"]
        CF["5:1"]
        CG["5:2"]
        CH["5:3"]
    end
    
    subgraph Gaussian Connections
        CI["0, 1, 2, 3, 4, 5, 6, 7, 8, 9"]
```
</details>

Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). Imagenet classification with deep convolutional neural networks. NIPS.

![](images/1a38b24787119ccaca93690678885306527b1436d7b337cfe1a380bd8447624a.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Size: 11"] --> B["Max pooling"]
    C["Input Size: 224"] --> D["Max pooling"]
    B --> E["Output dimensions: 1000, 2048"]
    D --> F["Output dimensions: 2048"]
    style A fill:#f9f,stroke:#333
    style C fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style D fill:#ccf,stroke:#333
    style E fill:#cfc,stroke:#333
    style F fill:#cfc,stroke:#333
    subgraph Stride of 4
        B -->|55| C
        D -->|55| C
    end
    subgraph Max pooling
        B -->|128| C
        D -->|128| C
    end
    subgraph Dense Layer
        E -->|192| F
        F -->|128| Dense
    end
```
</details>

![](images/a6d8766920f3e9e80700544b5d416b5783fa598f9c3471e55c827cd0fff757a6.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input data 227×227×3"] --> B["Conv1 55×55×96"]
    B --> C["Conv2 27×27×256"]
    C --> D["Conv3 13×13×384"]
    D --> E["Conv4 13×13×384"]
    E --> F["Conv5 13×13×256"]
    F --> G["FC6 4096"]
    F --> H["FC7 4096"]
    F --> I["FC8 1000"]
```
</details>

![](images/c5f87d96633432fe5aea30dd38404b59267301329c15f0597ea3809c1f18a325.jpg)

CNNs that use ReLU achieved a 25% error rate on CIFAR-10 is six times faster than those that used tanh.

AlexNet uses 3 x 3 max pooling with stride 2.

<table><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td></tr></table>

Stride 2

![](images/e72c4fa5f05262de4ad403abe9bd965969089c5856aa51a1ac0b7de6b6947bc2.jpg)

<details>
<summary>natural_image</summary>

Simple 2x2 grid with pink and white cells (no text or symbols)
</details>

Feature Map

![](images/452ed7f11126b1456cd01174de5018c2d4564cf6f5d4e1582c5e2fca96f8ab0e.jpg)  
Generalization and Overfitting

![](images/85b887dd3ab02d3960a1c6eec6aded109a10f1cf3402acdb7f60882f06d8faf9.jpg)

<details>
<summary>scatter</summary>

| Time | Values |
|------|--------|
| 1    | 0.8    |
| 2    | 0.75   |
| 3    | 0.7    |
| 4    | 0.65   |
| 5    | 0.6    |
| 6    | 0.55   |
| 7    | 0.5    |
| 8    | 0.45   |
| 9    | 0.4    |
| 10   | 0.35   |
| 11   | 0.3    |
| 12   | 0.25   |
| 13   | 0.2    |
| 14   | 0.15   |
| 15   | 0.1    |
| 16   | 0.05   |
| 17   | 0.0    |
| 18   | -0.05  |
| 19   | -0.1   |
| 20   | -0.15  |
| 21   | -0.2   |
| 22   | -0.25  |
| 23   | -0.3   |
| 24   | -0.35  |
| 25   | -0.4   |
| 26   | -0.45  |
| 27   | -0.5   |
| 28   | -0.55  |
| 29   | -0.6   |
| 30   | -0.65  |
| 31   | -0.7   |
| 32   | -0.75  |
| 33   | -0.8   |
| 34   | -0.85  |
| 35   | -0.9   |
| 36   | -0.95  |
| 37   | -1.0   |
| 38   | -1.05  |
| 39   | -1.1   |
| 40   | -1.15  |
| 41   | -1.2   |
| 42   | -1.25  |
| 43   | -1.3   |
| 44   | -1.35  |
| 45   | -1.4   |
| 46   | -1.45  |
| 47   | -1.5   |
| 48   | -1.55  |
| 49   | -1.6   |
| 50   | -1.65  |
| 51   | -1.7   |
| 52   | -1.75  |
| 53   | -1.8   |
| 54   | -1.85  |
| 55   | -1.9   |
| 56   | -1.95  |
| 57   | -2.0   |
| 58   | -2.05  |
| 59   | -2.1   |
| 60   | -2.15  |
| 61   | -2.2   |
| 62   | -2.25  |
| 63   | -2.3   |
| 64   | -2.35  |
| 65   | -2.4   |
| 66   | -2.45  |
| 67   | -2.5   |
| 68   | -2.55  |
| 69   | -2.6   |
| 70   | -2.65  |
| 71   | -2.7   |
| 72   | -2.75  |
| 73   | -2.8   |
| 74   | -2.85  |
| 75   | -2.9   |
| 76   | -2.95  |
| 77   | -3.0   |
| 78   | -3.05  |
| 79   | -3.1   |
| 80   | -3.15  |
| 81   | -3.2   |
| 82   | -3.25  |
| 83   | -3.3   |
| 84   | -3.35  |
| 85   | -3.4   |
| 86   | -3.45  |
| 87   | -3.5   |
| 88   | -3.55  |
| 89   | -3.6   |
| 90   | -3.65  |
| 91   | -3.7   |
| 92   | -3.75  |
| 93   | -3.8   |
| 94   | -3.85  |
| 95   | -3.9   |
| 96   | -3.95  |
| 97   | -4.0   |
| 98   | -4.05  |
| 99   | -4.1   |
| 100  | -4.15  |
</details>

(High bias error)

![](images/af088d72c7230b2c29b7f14df8cd8dd4238a307de89afe7b2b3adaa6b42ecb6a.jpg)

<details>
<summary>scatter</summary>

| Time | Values |
|------|--------|
| 0    | 1.0    |
| 1    | 0.8    |
| 2    | 0.6    |
| 3    | 0.4    |
| 4    | 0.2    |
| 5    | 0.1    |
| 6    | 0.3    |
| 7    | 0.5    |
| 8    | 0.7    |
| 9    | 0.9    |
| 10   | 1.1    |
| 11   | 1.3    |
| 12   | 1.5    |
| 13   | 1.7    |
| 14   | 1.9    |
| 15   | 2.1    |
| 16   | 2.3    |
| 17   | 2.5    |
| 18   | 2.7    |
| 19   | 2.9    |
| 20   | 3.1    |
| 21   | 3.3    |
| 22   | 3.5    |
| 23   | 3.7    |
| 24   | 3.9    |
| 25   | 4.1    |
| 26   | 4.3    |
| 27   | 4.5    |
| 28   | 4.7    |
| 29   | 4.9    |
| 30   | 5.1    |
| 31   | 5.3    |
| 32   | 5.5    |
| 33   | 5.7    |
| 34   | 5.9    |
| 35   | 6.1    |
| 36   | 6.3    |
| 37   | 6.5    |
| 38   | 6.7    |
| 39   | 6.9    |
| 40   | 7.1    |
| 41   | 7.3    |
| 42   | 7.5    |
| 43   | 7.7    |
| 44   | 7.9    |
| 45   | 8.1    |
| 46   | 8.3    |
| 47   | 8.5    |
| 48   | 8.7    |
| 49   | 8.9    |
| 50   | 9.1    |
| 51   | 9.3    |
| 52   | 9.5    |
| 53   | 9.7    |
| 54   | 9.9    |
| 55   | 10.1   |
| 56   | 10.3   |
| 57   | 10.5   |
| 58   | 10.7   |
| 59   | 10.9   |
| 60   | 11.1   |
| 61   | 11.3   |
| 62   | 11.5   |
| 63   | 11.7   |
| 64   | 11.9   |
| 65   | 12.1   |
| 66   | 12.3   |
| 67   | 12.5   |
| 68   | 12.7   |
| 69   | 12.9   |
| 70   | 13.1   |
| 71   | 13.3   |
| 72   | 13.5   |
| 73   | 13.7   |
| 74   | 13.9   |
| 75   | 14.1   |
| 76   | 14.3   |
| 77   | 14.5   |
| 78   | 14.7   |
| 79   | 14.9   |
| 80   | 15.1   |
| 81   | 15.3   |
| 82   | 15.5   |
| 83   | 15.7   |
| 84   | 15.9   |
| 85   | 16.1   |
| 86   | 16.3   |
| 87   | 16.5   |
| 88   | 16.7   |
| 89   | 16.9   |
| 90   | 17.1   |
| 91   | 17.3   |
| 92   | 17.5   |
| 93   | 17.7   |
| 94   | 17.9   |
| 95   | 18.1   |
| 96   | 18.3   |
| 97   | 18.5   |
| 98   | 18.7   |
| 99   | 18.9   |
| 100  | -      |
</details>

(Balance between biasand variance)

![](images/65f55eb993256fa70115bca977a69dc56fab4a209ed9b25cadb4c71bb4a66ea0.jpg)

<details>
<summary>line</summary>

| Time | Values |
|------|--------|
| 0    | 10     |
| 1    | 8      |
| 2    | 6      |
| 3    | 4      |
| 4    | 2      |
| 5    | 0      |
| 6    | -2     |
| 7    | -4     |
| 8    | -6     |
| 9    | -8     |
| 10   | -10    |
| 11   | -8     |
| 12   | -6     |
| 13   | -4     |
| 14   | -2     |
| 15   | 0      |
| 16   | 2      |
| 17   | 4      |
| 18   | 6      |
| 19   | 8      |
| 20   | 10     |
| 21   | 8      |
| 22   | 6      |
| 23   | 4      |
| 24   | 2      |
| 25   | 0      |
| 26   | -2     |
| 27   | -4     |
| 28   | -6     |
| 29   | -8     |
| 30   | -10    |
| 31   | -8     |
| 32   | -6     |
| 33   | -4     |
| 34   | -2     |
| 35   | 0      |
| 36   | 2      |
| 37   | 4      |
| 38   | 6      |
| 39   | 8      |
| 40   | 10     |
| 41   | 8      |
| 42   | 6      |
| 43   | 4      |
| 44   | 2      |
| 45   | 0      |
| 46   | -2     |
| 47   | -4     |
| 48   | -6     |
| 49   | -8     |
| 50   | -10    |
| 51   | -8     |
| 52   | -6     |
| 53   | -4     |
| 54   | -2     |
| 55   | 0      |
| 56   | 2      |
| 57   | 4      |
| 58   | 6      |
| 59   | 8      |
| 60   | 10     |
| 61   | 8      |
| 62   | 6      |
| 63   | 4      |
| 64   | 2      |
| 65   | 0      |
| 66   | -2     |
| 67   | -4     |
| 68   | -6     |
| 69   | -8     |
| 70   | -10    |
| 71   | -8     |
| 72   | -6     |
| 73   | -4     |
| 74   | -2     |
| 75   | 0      |
| 76   | 2      |
| 77   | 4      |
| 78   | 6      |
| 79   | 8      |
| 80   | 10     |
| 81   | 8      |
| 82   | 6      |
| 83   | 4      |
| 84   | 2      |
| 85   | 0      |
| 86   | -2     |
| 87   | -4     |
| 88   | -6     |
| 89   | -8     |
| 90   | -10    |
| 91   | -8     |
| 92   | -6     |
| 93   | -4     |
| 94   | -2     |
| 95   | 0      |
| 96   | 2      |
| 97   | 4      |
| 98   | 6      |
| 99   | 8      |
| 100  | 10     |
</details>

(High variance error)

A highly complex model may not be overfitting if (1) A large and complex dataset is available; (2) a large number of model parameters are zero!!!

![](images/992deaf6e42cd89aa8c00ed2c4a5d9197ab7c786c18714f0fd4a3f15161aae2b.jpg)

000

Resize&Crop

955

955

Random Crops

2

![](images/36745708f702632f42f436198e133858fe1a1120d1e95e7cc2ba0d06ac97ef30.jpg)

<details>
<summary>text_image</summary>

Mirror Image
</details>

![](images/5f7499a5fa46e1a81fa01b5569890ab0ed26efc8c6a0972513ce58424f6fe394.jpg)

<details>
<summary>natural_image</summary>

Close-up of a tabby cat with green eyes and white whiskers, looking upward (no text or symbols visible)
</details>

Rotation   
![](images/cb615be239f31c2d5405bca0fa8f009d8b24e6ae33fc8334f6cddeb2a8d34244.jpg)

<details>
<summary>natural_image</summary>

Close-up of a tabby cat with green eyes and striped whiskers, looking upward (no text or symbols visible)
</details>

![](images/fafab4d40f1a0b87ab9c9738236c7bf55314685fbddaed0d7efc82bfb9c12c0c.jpg)

<details>
<summary>natural_image</summary>

Close-up of a tabby cat with green eyes looking upward (no text or symbols visible)
</details>

![](images/a2cf9bd268f797f3eb0c4f4c7f7acd288916da8b81faccaab14d53b761b8fae0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Layer"] --> B["Hidden Layer"]
    B --> C["Output Layer"]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#f96,stroke:#333
```
</details>

![](images/cad612b998f5422aa90c677fdb097511f22be2384e039438cd08c5cff87ed694.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Node"] --> B["Hidden Node 1"]
    A --> C["Hidden Node 2"]
    A --> D["Hidden Node 3"]
    B --> E["X̄"]
    C --> F["X̄"]
    D --> G["X̄"]
    E --> H["Output Node"]
    F --> H
    G --> H
    H --> I["X̄"]
    H --> J["X̄"]
    I --> K["Output Node"]
    J --> K
    style A fill:#cce5ff,stroke:#333
    style B fill:#cce5ff,stroke:#333
    style C fill:#cce5ff,stroke:#333
    style D fill:#cce5ff,stroke:#333
    style E fill:#cce5ff,stroke:#333
    style F fill:#cce5ff,stroke:#333
    style G fill:#cce5ff,stroke:#333
    style H fill:#cce5ff,stroke:#333
    style I fill:#cce5ff,stroke:#333
    style J fill:#cce5ff,stroke:#333
```
</details>

A dropout layer randomly sets input elements to zero with a given probability.

AlexNet uses dropout layers with a probability 0.5.

![](images/6ac2b42990b6ed4acdf4c337ecd7b1696ded13cdc1000851706fcd4032743f04.jpg)

<details>
<summary>text_image</summary>

INTERNET
</details>

<table><tr><td></td><td>Top 1 Error</td><td>Top 5 Error</td></tr><tr><td>Before AlexNet</td><td>47.1%</td><td>28.2%</td></tr><tr><td>AlexNet</td><td>37.5%</td><td>17%</td></tr></table>

Simonyan, K., & Zisserman, A. (2014). Very deep convolutional networks for large-scale image recognition. ICLR 2015.

VGG-16   
![](images/3c61805067f8f851d109fd02b04657fe4cc2b6c0874b6d5d14aa6cc10380002d.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input"] --> B["Conv 1-1"]
    B --> C["Conv 1-2"]
    C --> D["Pooing"]
    D --> E["Conv 2-1"]
    E --> F["Conv 2-2"]
    F --> G["Pooing"]
    G --> H["Conv 3-1"]
    H --> I["Conv 3-2"]
    I --> J["Conv 3-3"]
    J --> K["Pooing"]
    K --> L["Conv 4-1"]
    L --> M["Conv 4-2"]
    M --> N["Conv 4-3"]
    N --> O["Pooing"]
    O --> P["Conv 5-1"]
    P --> Q["Conv 5-2"]
    Q --> R["Conv 5-3"]
    R --> S["Pooing"]
    S --> T["Dense"]
    T --> U["Dense"]
    U --> V["Dense"]
    V --> W["Output"]
```
</details>

The Architecture

The architecture depicted belowis VGG16.   
![](images/8c47caeebb056f3995783b453419ddcf04440e02166a3b39f50da5a6b57daf9a.jpg)

<details>
<summary>bar</summary>

| Model                  | Operations       |
| ---------------------- | ---------------- |
| convolution+ReLU       | 224 × 224 × 3    |
| convolution+ReLU       | 224 × 224 × 64   |
| max pooling           | 112 × 112 × 128 |
| max pooling           | 56 × 56 × 256    |
| max pooling           | 28 × 28 × 512    |
| max pooling           | 14 × 14 × 512    |
| fully connected+ReLU   | 7 × 7 × 512      |
| fully connected+ReLU   | 1 × 1 × 4096     |
| fully connected+ReLU   | 1 × 1 × 1000     |
| softmax                | -                |
</details>

Key Idea of VGG: Replace the large convolution filter by stacking some smaller convolution filters.

![](images/57be4c441a8da5089f32040d492e490cd86cda4e296e4162eb284b907691afe7.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph AlexNet
        A["FC (1000)"] --> B["FC (4096)"]
        B --> C["FC (4096)"]
        C --> D["3 × 3 MaxPool, stride 2"]
        D --> E["3 × 3 Conv (384), pad 1"]
        E --> F["3 × 3 Conv (384), pad 1"]
        F --> G["3 × 3 Conv (384), pad 1"]
        G --> H["3 × 3 MaxPool, stride 2"]
        H --> I["5 × 5 Conv (256), pad 2"]
        I --> J["3 × 3 MaxPool, stride 2"]
        J --> K["11 × 11 Conv (96), stride 4"]
    end

    subgraph VGG
        L["FC (1000)"] --> M["FC (4096)"]
        M --> N["FC (4096)"]
        N --> O["..."]
        O --> P["..."]
        P --> Q["..."]
        Q --> R["..."]
        R --> S["..."]
        S --> T["..."]
    end

    style AlexNet fill:#f9f,stroke:#333
    style VGG fill:#bbf,stroke:#333
```
</details>

An example: Replace a 5 x 5 filter with two 3 x 3 filters.

![](images/78210ba14c7f6855bd69f7eb55edd644981fc339eeb6bca28be6bebec607590c.jpg)

<details>
<summary>natural_image</summary>

Diagram of two stacked solar panels with red connecting lines, no text or symbols present
</details>

two successive 3x3 convolutions

![](images/6a13cd3c527816ea3773d21a48dc80e95e1a1d224aadf56ed2de654246b541d1.jpg)

<details>
<summary>natural_image</summary>

Simple line drawing of a 3D geometric shape resembling a truncated cone or frustum (no text or symbols)
</details>

5x5 convolution

1. More concise and generalizable.   
2. Smaller filters can achieve better performance than a larger filter.   
3. Demonstrate that increase depth can boost performance.

Classification: ImageNet Challenge top-5 error   
![](images/06b1acff6d976338e4404b87a575f86af05b3a34f7a4eb5e6ef8743c6f4c8119.jpg)

<details>
<summary>bar</summary>

| Model | Layer Count |
| :--- | :--- |
| ILSVRC'15 ResNet | 3.57 |
| ILSVRC'14 GoogleNet | 6.7 |
| ILSVRC'14 VGG | 7.3 |
| ILSVRC'13 | 11.7 |
| ILSVRC'12 AlexNet | 16.4 |
| ILSVRC'11 | 25.8 |
| ILSVRC'10 | 28.2 |
152 layers (dashed orange line) are annotated.
</details>

![](images/fcd0323e8b28e7019ae56b991f854a97720d3774d7254218f128f5688d8bf35d.jpg)

<details>
<summary>bubble</summary>

| Model           | Top-1 accuracy [%] | Operations [G-Ops] | Bubble Size (M) |
|-----------------|--------------------|--------------------|-----------------|
| Inception-v4    | 80                 | 20                 | 155             |
| Xception        | 78                 | 18                 | 125             |
| ResNet-152      | 77                 | 16                 | 95              |
| VGG-16          | 70                 | 30                 | 95              |
| VGG-19          | 70                 | 40                 | 155             |
| Inception-v3    | 76                 | 8                  | 35              |
| DenseNet-201    | 75                 | 7                  | 35              |
| DenseNet-169    | 74                 | 6                  | 35              |
| ResNet-50       | 76                 | 16                 | 125             |
| DenseNet-121    | 75                 | 8                  | 35              |
| ResNet-34       | 73                 | 7                  | 35              |
| MobileNet-v2    | 72                 | 2                  | 5               |
| MobileNet-v1    | 71                 | 2                  | 5               |
| ResNet-18       | 69                 | 3                  | 5               |
| GoogLeNet       | 68                 | 3                  | 5               |
| ENet            | 68                 | 2                  | 5               |
| fd-MobileNet     | 65                 | 1                  | 5               |
| BN-NIN          | 62                 | 2                  | 5               |
| ShuffleNet      | 62                 | 2                  | 5               |
| SqueezeNet      | 58                 | 1                  | 5               |
| BN-AlexNet      | 57                 | 1                  | 5               |
| AlexNet         | 54                 | 1                  | 5               |
</details>

![](images/b674494e606c1f4bafdb643cde7c121e509a5972977f6e03400b965d2aa45ee4.jpg)

<details>
<summary>line</summary>

| iter. (1e4) | 20-layer | 56-layer |
| ----------- | -------- | -------- |
| 0           | 20.0     | 20.0     |
| 1           | 15.0     | 18.0     |
| 2           | 12.0     | 19.0     |
| 3           | 10.0     | 17.0     |
| 4           | 5.0      | 8.0      |
| 5           | 3.0      | 6.0      |
| 6           | 2.0      | 5.0      |
</details>

![](images/e1a2727917f535ddb229c8dd141e1734e7d966153df08bca8d02612c10ef513a.jpg)

<details>
<summary>line</summary>

| iter. (1e4) | 20-layer | 56-layer |
| ----------- | -------- | -------- |
| 0           | ~20      | ~20      |
| 1           | ~15      | ~18      |
| 2           | ~13      | ~19      |
| 3           | ~10      | ~17      |
| 4           | ~10      | ~14      |
| 5           | ~10      | ~14      |
| 6           | ~10      | ~14      |
</details>

Deep model may be difficult to optimize.

Intuitive sense: Deep model should be at least as good as shallow ones?

Revolution of Depth   
![](images/b87c2a9fee0c39a19a088fb60c2951dd5fc34a89fb4dd5bf7d4287f22d4737f1.jpg)

<details>
<summary>bar</summary>

| Model           | Layer Count |
| --------------- | ----------- |
| ILSVRC'15 ResNet | 3.57        |
| ILSVRC'14 GoogleNet | 6.7         |
| ILSVRC'14 VGG    | 7.3         |
| ILSVRC'13        | 11.7        |
| ILSVRC'12 AlexNet | 16.4       |
| ILSVRC'11        | 25.8        |
| ILSVRC'10        | 28.2        |
</details>

ImageNet Classification top-5 error (%)

He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. CVPR.

![](images/a706c36ffd18f3317cadc8d2bf083b3fd2d3a71a4d631de2270277892439da74.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["ResNet - 152"] --> B["7X7 conv, 64"]
    B --> C["3X3 conv, 64"]
    C --> D["3X3 conv, 64"]
    D --> E["3X3 conv, 64"]
    E --> F["3X3 conv, 64"]
    F --> G["3X3 conv, 64"]
    G --> H["3X3 conv, 64"]
    H --> I["3X3 conv, 128"]
    I --> J["3X3 conv, 128"]
    J --> K["152 layers"]
    K --> L["3X3 conv, 512"]
    L --> M["3X3 conv, 512"]
    M --> N["3X3 conv, 512"]
    N --> O["fc 6"]
```
</details>

Key numbers: 152 layers for ImageNet.

3.57% Top 5 Error!!!

A Key Motivation: It is not easy to learn an identity mapping f(x) = x.   
![](images/66c54801ba9abf8c62edd1bd0a4f34c4e2df9e0c7368bf0a18d1bbc4585fe9c2.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["H(x)"] --> B["conv"]
    B --> C["X"]
    D["“Plain” layers"] --> E["conv"]
    E --> F["relu"]
    F --> B
```
</details>

![](images/79b0298aaa9609e3642c34f949831abf2fec633c9e2eb92d3778585257003566.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["+"] -->|relu| B["conv"]
    B --> C["F(x)"]
    C --> D["conv"]
    D --> E["X"]
    E --> F["Residual block"]
    style A fill:#fff,stroke:#000
    style B fill:#fff,stroke:#000
    style C fill:#fff,stroke:#000
    style D fill:#fff,stroke:#000
    style E fill:#fff,stroke:#000
    style F fill:#fff,stroke:#000
```
</details>

A Key Motivation: It is not easy to learn an identity mapping f(x) = x.

![](images/b19aee76f32b0645a1f729bd5f8c809d67808b1e394d6bb3dfacb1f8aa6c1071.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["H(x)"] --> B["conv"]
    B --> C["X"]
    D["“Plain” layers"] --> E["conv"]
    E --> F["relu"]
    F --> B
```
</details>

![](images/7012e91e2c772cac5ef73031e4196faf244a6a58c06504e73ee4e5030021a8d8.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["+"] -->|relu| B["conv"]
    B --> C["F(x)"]
    C --> D["conv"]
    D --> E["X"]
    E --> F["Residual block"]
    style A fill:#fff,stroke:#000
    style B fill:#fff,stroke:#000
    style C fill:#fff,stroke:#000
    style D fill:#fff,stroke:#000
    style E fill:#fff,stroke:#000
    style F fill:#fff,stroke:#000
```
</details>

An identity mapping can now be obtained if F = 0.

![](images/8c09d41cd260f2bb3822120a0ab38b6c2a01dea7b75bef81c09c0e2e55ee26f6.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["F(x) + x"] --> B["conv"]
    B --> C["X identity"]
    D["F(x)"] --> E["conv"]
    E --> F["X Residual block"]
    G["relu"] --> H["+"]
    I["relu"] --> J["conv"]
    J --> K["X Residual block"]
```
</details>

In a plain network, if we want to learn H(x), now, we only need to learn its residual:

$$
F (x) = H (x) - x
$$

# A stack of three types of residual blocks:

Stage 1: 3x3 convolution filters with 64 channels.

Stage 2: 3x3 convolution filters with 128 channels

Stage 3: 3x3 convolution filters with 512 channels

![](images/77c3538abd041bbf14d98504946dc2101cc47736046a463d506ecc3d0fb35714.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["ResNet - 152"] --> B["7X7 conv, 64"]
    B --> C["3X3 conv, 64"]
    C --> D["3X3 conv, 64"]
    D --> E["3X3 conv, 64"]
    E --> F["3X3 conv, 64"]
    F --> G["3X3 conv, 64"]
    G --> H["3X3 conv, 64"]
    H --> I["3X3 conv, 128"]
    I --> J["3X3 conv, 128"]
    J --> K["152 layers"]
    K --> L["3X3 conv, 512"]
    L --> M["3X3 conv, 512"]
    M --> N["3X3 conv, 512"]
    N --> O["fc 6"]
    style A fill:#66b3ff,stroke:#333
    style O fill:#ffeb99,stroke:#333
```
</details>

![](images/f86686ea3a46cd5c5088fbefa19cd2d48883f2120f65edc797b288cfba2e6396.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["ResNet - 152"] --> B["7X7 conv, 64"]
    B --> C["3X3 conv, 64"]
    C --> D["3X3 conv, 64"]
    D --> E["3X3 conv, 64"]
    E --> F["3X3 conv, 64"]
    F --> G["3X3 conv, 64"]
    G --> H["3X3 conv, 64"]
    H --> I["3X3 conv, 64"]
    I --> J["3X3 conv, 128"]
    J --> K["3X3 conv, 128"]
    K --> L["152 layers"]
    L --> M["3X3 conv, 512"]
    M --> N["3X3 conv, 512"]
    N --> O["3X3 conv, 512"]
    O --> P["fc 6"]
```
</details>

No fully connected layers before output.

For very deep neural networks (i.e., 50+ layers), we can use “bottleneck” building blocks to improve efficiency.

![](images/116760b4d9a48ff9348dfd8ce1f75f8919108aae63532f0bcea8b24125d8a6c8.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["28x28x256 input"] --> B["1x1 conv, 64"]
    B --> C["3x3 conv, 256"]
    C --> D["1x1 conv, 256 output"]
    D --> E["BN, relu"]
    E --> F["+"]
    F --> G["output"]
    style A fill:#f9f,stroke:#333
    style G fill:#ccf,stroke:#333
```
</details>

- Initialization using He’s Xaiver initialization.   
- Batch normalization after each convolution layer.   
- SGD + Momentum (0.9)   
- Dynamic learning rate scheduling.   
- No dropout used in He’s ResNet paper.

Consider a 10-layer DNN with tanh activation function. If we initialize all the weights with normal distribution N(0, 0.01).

![](images/42c203928c0c852df3d84a28fd2f47a2571f888635c775abf2eb06dd18cafb3c.jpg)

The outputs of the last a few layers are almost zeros.

Consider a 10-layer DNN with tanh activation function. If we initialize all the weights with normal distribution N(0, 1).

![](images/f41390effbc18c0b757aa4f1352c786d1d351ce9d41b93d19a93554ddb5ac213.jpg)

The outputs are close to -1 or 1, the gradients will be very small for tanh activation function.

Key Motivation: Keep a same variance for the input and the output.

Consider a 10-layer DNN with tanh activation function. If we initialize all the weights with normal distribution N(0, 1)/sqrt(n\_in).

![](images/6aebb1d1bfcbecf3966d0e706bc520c06ffad08fafe92e3682f5ff1fca9ebb5e.jpg)

Consider $y = w _ { 1 } x _ { 1 } + w _ { 2 } x _ { 2 } + \cdots + w _ { n } x _ { n } , x _ { \mathrm { i } }$ are i.i.d. with zero mean, $w _ { i }$ are i.i.d with zero mean.

Target: Compute $\cdot$ .

$\mathbb { L } \mathrm { e m m a }$

Thus, $-$ and

$$
V a r [ y ] = V a r [ w _ {1} x _ {1} + w _ {2} x _ {2} + \dots + w _ {n} x _ {n} ] = \sum_ {i = 1} ^ {n} V a r [ w _ {i} x _ {i} ] = n V a r [ w _ {i} ] V a r [ x _ {i} ]
$$

Thus,

$$
V a r [ w _ {i} ] = 1 / n
$$

Consider a 10-layer DNN with ReLu activation function. If we initialize all the weights with normal distribution N(0, 1)/sqrt(n\_in).

![](images/d4678de25d14a814039d02822c95c2792c06222ad21d57b9a4e3e8eff5888d24.jpg)

Not that good for the last a few layers.

Key Motivation: Assume that only a half of the neurons are activated in each layer.

He’s Xavier initialization: N(0, 1)/sqrt(n\_in/2).

![](images/65f7d6dd3f3d7a59ae478844de81e8e81bc0d175e19a110a443b0807e0fd98b6.jpg)

# Bach Normalization

![](images/f5d716560a125871fcc3d0935e26ee84e1020c98ab11f62e8b311b14073c3169.jpg)

<details>
<summary>line</summary>

| x | Activation Function | Derivative |
| --- | --- | --- |
| 0 | 0.0 | 0.0 |
| 1 | 0.1 | 0.05 |
| 2 | 0.3 | 0.15 |
| 3 | 0.6 | 0.3 |
| 4 | 0.9 | 0.5 |
| 5 | 1.0 | 0.7 |
| 6 | 1.0 | 0.8 |
| 7 | 1.0 | 0.9 |
| 8 | 1.0 | 0.95 |
| 9 | 1.0 | 0.98 |
| 10 | 1.0 | 0.99 |
| 11 | 1.0 | 0.995 |
| 12 | 1.0 | 0.998 |
| 13 | 1.0 | 0.999 |
| 14 | 1.0 | 0.9995 |
| 15 | 1.0 | 0.9998 |
| 16 | 1.0 | 0.9999 |
| 17 | 1.0 | 0.99995 |
| 18 | 1.0 | 0.99998 |
| 19 | 1.0 | 0.99999 |
| 20 | 1.0 | 0.999995 |
| 21 | 1.0 | 0.999998 |
| 22 | 1.0 | 0.999999 |
| 23 | 1.0 | 0.9999995 |
| 24 | 1.0 | 0.9999998 |
| 25 | 1.0 | 0.9999999 |
| 26 | 1.0 | 0.99999995 |
| 27 | 1.0 | 0.99999998 |
| 28 | 1.0 | 0.99999999 |
| 29 | 1.0 | 0.999999995 |
| 30 | 1.0 | 0.999999998 |
| 31 | 1.0 | 0.999999999 |
| 32 | 1.0 | 0.9999999995 |
| 33 | 1.0 | 0.9999999998 |
| 34 | 1.0 | 0.9999999999 |
| 35 | 1.0 | 0.99999999995 |
| 36 | 1.0 | 0.99999999998 |
| 37 | 1.0 | 0.99999999999 |
| 38 | 1.0 | 0.999999999995 |
| 39 | 1.0 | 0.999999999998 |
| 40 | 1.0 | 0.9999999999985 |
| 41 | 1.0 | 0.9999999999988 |
| 42 | 1.0 | 0.99999999999885 |
| 43 | 1.0 | 0.9988888888888 |
| 44 | 1.0 | 0.866666666668 |
| 45 | 1.0 | 0.646444444448 |
| 46 | 1.0 | 0.435222222222 |
| 47 | 1.0 | 0.234100000000 |
| 48 | 1.0 | -0.1338777777775 |
| 49 | 1.0 | -0.333755555558 |
| 50 | 1.0 | -0.533633333338 |
| 51 | 1.0 | -0.7335111111125 |
| 52 | 1.0 | -0.8333888888888 |
| 53 | 1.0 | -0.8666666666688 |
| 54 | 1.0 | -0.886444444448 |
| 55 | 1.0 | -0.8666666666688 |
| 56 | 1.0 | -0.736333333338 |
| 57 | 1.0 | -0.533633333338 |
| 58 | 1.0 | -0.333755555558 |
| 59 | 1.0 | -0.1338777777775 |
| 60 | 1.0 | -0.1338777777775 |
| 61 | 1.0 | -0.1338777777775 |
| 62 | 1.0 | -0.1338777777775 |
| 63 | 1.0 | -0.1338777777775 |
| 64 | 1.0 | -0.1338777777775 |
| 65 | 1.0 | -0.1338777777775 |
| 66 | 1.0 | -0.1338777777775 |
| 67 | 1.0 | -0.1338777777775 |
| 68 | 1.0 | -0.1338777777775 |
| 69 | 1.0 | -0.1338777777775 |
| 70 | 1.0 | -0.1338777777775 |
| 71 | 1.0 | -0.1338777777775 |
| 72 | 1.0 | -0.1338777777775 |
| 73 | 1.0 | -0.1338777777775 |
| 74 | 1.0 | -0.1338777777775 |
| 75 | 1.0 | -0.1338777777775 |
| 76 | 1.0 | -0.1338777777775 |
| 77 | 1.0 | -0.1338777777775 |
| 78 | 1.0 | -0.1338777777775 |
| 79 | 1.0 | -0.13387777777% |
| ... (additional values) are not provided in the image.) The data is presented in a table format with columns: "Activation Function" and "Derivative". The values for the Activation Function are calculated as: (x) * (ln(x) / (ln(x)) + (ln(x)) * (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) = (x) * (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)) / (ln(x)).
</details>

![](images/d7b4a7feddc634230623758442e3be77d7da9a724e5c220b2ee207a24089f91b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input Layer 1"] --> B["Hidden Layer 1"]
    C["Input Layer 2"] --> B
    D["Input Layer 3"] --> B
    E["Input Layer 4"] --> B
    F["Input Layer 5"] --> B
    B --> G["Output Layer 1"]
    B --> H["Output Layer 2"]
    B --> I["Output Layer 3"]
    B --> J["Output Layer 4"]
    G --> K["Output Layer 5"]
    H --> K
    I --> K
    J --> K
    style A fill:#d4edda
    style C fill:#d4edda
    style D fill:#d4edda
    style E fill:#d4edda
    style F fill:#d4edda
    style G fill:#999999
    style H fill:#999999
    style I fill:#999999
    style J fill:#999999
    style K fill:#6666ff
    style L fill:#6666ff
```
</details>

(gradually diminishes)

Activation Inputs   
![](images/67e40f543abf8949201007f01a821feeec00cca30e4639906530285aa9320615.jpg)

<details>
<summary>line</summary>

| x    | y (Gray Line) | y (Red Dashed Line) |
|------|---------------|---------------------|
| 0.0  | 6.0           | 6.0                 |
| 0.1  | 2.0           | -2.0                |
| 0.2  | 0.0           | -4.0                |
| 0.3  | -2.0          | -6.0                |
| 0.4  | -4.0          | -8.0                |
| 0.5  | -6.0          | -10.0               |
| 0.6  | -8.0          | -12.0               |
| 0.7  | -10.0         | -14.0               |
| 0.8  | -12.0         | -16.0               |
| 0.9  | -14.0         | -18.0               |
</details>

Sigmoid Activation and Gradient

Consider an output of a linear layer:

$$
y = W x
$$

The following scenarios are challenging:

1. $E [ x ] \neq 0 .$   
2. $V a r [ x ]$ is large.

# We WANT

1. $E [ x ] = 0 ,$   
2. $V a r [ x ] = 1 . $

Batch Normalization is to normalize each dimension of the activations at some layer:

$$
\hat {x} ^ {(k)} = \frac {x ^ {(k)} - E [ x ^ {(k)} ]}{\sqrt {\operatorname{Var} [ x ^ {(k)} ]}}.
$$

![](images/78d9833aceffcdfd91d30a2292f074049dcd67067c63dd1c900f0f2c16e7960f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Input Layer
        n1["Input n"] --> n2["Input n"]
        n2 --> n3["Input n"]
        n3 --> n4["Input n"]
        n4 --> n5["Input n"]
        n5 --> n6["Input n"]
        n6 --> n7["Input n"]
        n7 --> n8["Input n"]
        n8 --> n9["Input n"]
        n9 --> n10["Input n"]
        n10 --> n11["Output 3"]
    end

    subgraph Output Layer
        b1["Input b"] --> b2["Output 3"]
        b2 --> b3["Output 3"]
        b3 --> b4["Output 3"]
        b4 --> b5["Output 3"]
        b5 --> b6["Output 3"]
        b6 --> b7["Output 3"]
        b7 --> b8["Output 3"]
    end

    style Input Layer fill:#f9f,stroke:#333
    style Output Layer fill:#bbf,stroke:#333
```
</details>

Input data batch : $x ^ { 1 } , \dots , x ^ { N } \in R ^ { d }$

![](images/f923403b1de63e86c76104983d790e4b91dce216911f5c2b1d886c96def49ac8.jpg)

<details>
<summary>text_image</summary>

x¹ x² ... xᴺ
</details>

$$
\pmb {\mu} _ {j} = \frac {1}{N} \sum_ {i = 1} ^ {N} x _ {j} ^ {i}
$$

$$
\pmb {\sigma} _ {j} ^ {2} = \frac {1}{N} \sum_ {i = 1} ^ {N} \left(x _ {j} ^ {i} - \mu_ {j}\right) ^ {2}
$$

$$
\widehat {x} _ {j} ^ {i} = \frac {x _ {j} ^ {i} - \mu_ {j}}{\sqrt {\sigma_ {j} ^ {2} + \varepsilon}}
$$

Input data batch : $x ^ { 1 } , \dots , x ^ { N } \in R ^ { d }$ , Learnable scale $\cdot$ and $\cdot$

$$
\pmb {\mu} _ {j} = \frac {1}{N} \sum_ {i = 1} ^ {N} x _ {j} ^ {i}
$$

$$
\pmb {\sigma} _ {j} ^ {2} = \frac {1}{N} \sum_ {i = 1} ^ {N} \left(x _ {j} ^ {i} - \mu_ {j}\right) ^ {2}
$$

$$
\widehat {x} _ {j} ^ {i} = \frac {x _ {j} ^ {i} - \mu_ {j}}{\sqrt {\sigma_ {j} ^ {2} + \varepsilon}}
$$

$$
y _ {j} ^ {i} = \gamma_ {j} \widehat {x} _ {j} ^ {i} + \beta_ {j}
$$

$$
\pmb {\mu} _ {j} = E \big [ \mu_ {j} ^ {t r a i n} \big ]
$$

$$
\pmb {\sigma} _ {j} ^ {2} = E \big [ (\sigma_ {j} ^ {2}) ^ {t r a i n} \big ]
$$

$$
\widehat {x} _ {j} ^ {i} = \frac {x _ {j} ^ {i} - \mu_ {j}}{\sqrt {\sigma_ {j} ^ {2} + \varepsilon}}
$$

$$
y _ {j} ^ {i} = \gamma_ {j} \widehat {x} _ {j} ^ {i} + \beta_ {j}
$$

It is a linear operator during testing.

![](images/763505c3aef3bed65d7aec7d07909a3175b6f76c0f0d3ba399c432226cfd2bfa.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Sigmoid"] --> B["BN"]
    B --> C["Conv"]
```
</details>

![](images/1f7a4308433d1d4bdf57e19e522b4ad5f59d17d8090a2342cff3a96873a02e96.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Sigmoid"] --> B["BN"]
    B --> C["FC"]
```
</details>

Suggested Reading: Batch normalization in 3 levels of understanding

Why does Batch Normalization work?

https://www.youtube.com/watch?v=nUUqwaxLnWs

https://www.youtube.com/watch?v=DtEq44FTPM4

# Other Famous CNN Architectures

Huang, G., Liu, Z., Van Der Maaten, L., & Weinberger, K. Q. (2017). Densely connected convolutional networks. CVPR

![](images/db09682ba4d30e4dbdfe30ff473b5564b0d1b817d7f40a153eb840fa1c1810ea.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input"] --> B["x0"]
    B --> C["H1"]
    C --> D["x1"]
    D --> E["H2"]
    E --> F["x2"]
    F --> G["H3"]
    G --> H["x3"]
    H --> I["H4"]
    I --> J["Transition Layer"]
    style A fill:#f9f,stroke:#333
    style J fill:#bbf,stroke:#333
```
</details>

Szegedy, C., Liu, W., Jia, Y., Sermanet, P., Reed, S., Anguelov, D., ... & Rabinovich, A. (2015). Going deeper with convolutions. CVPR

![](images/daf3957a2783052176d9366f173cf3902ef7c6d140d5cb1e465efb21383ece81.jpg)

<details>
<summary>flowchart</summary>

Process flowchart for a chemical or industrial process involving multiple stages with inputs, outputs, and conditional branches.
</details>

![](images/f8195b1e1d430fc63cd92f67bffea7b33e94ea003cbd5ded987b3459de15035f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Filter concatenation"] --> B["3×3 convolutions"]
    A --> C["5×5 convolutions"]
    A --> D["1×1 convolutions"]
    B --> E["1×1 convolutions"]
    C --> F["1×1 convolutions"]
    D --> G["3×3 max pooling"]
    E --> H["Pervious layer"]
    F --> H
    G --> H
```
</details>

Key component.