# AMA 564 Deep Learning

# 2026 Spring

# Lecture 4

# A Short Recap

# Feedforward Neural Networks (Multi-Layer Perceptrons)

• The architecture of a MLP is expressed as a composition of a series of functions

$$
f _ {\theta} (x) = \mathcal {A} _ {L} \circ \sigma \circ \mathcal {A} _ {L - 1} \circ \sigma \circ \dots \circ \sigma \circ \mathcal {A} _ {1} (x), x \in \mathbb {R} ^ {d _ {0}}
$$

where

$$
\mathcal {A} _ {i} (x) = W _ {i} x + b _ {i}, \qquad x \in \mathbb {R} ^ {d _ {i - 1}}
$$

is the i-th linear transformation with

weight matrix $W _ { i } \in \mathbb { R } ^ { d _ { i } \times d _ { i - 1 } }$ and bias vector $b _ { i } \in \mathbb { R } ^ { d _ { i } }$ ,

and $\cdot$ is the activation function,

$\begin{array}{c} \mathsf { e . g . } , \qquad & { } \end{array}$

# Biological Neurons

# Neurons in a neural network:

![](images/08215d6cbf4ca0fc2fe20fed905a979e5d63ceb543b7999cbed9d4ad7ec2ddec.jpg)

<details>
<summary>natural_image</summary>

Illustration of a neuron with branching dendrites against a blue background (no text or symbols)
</details>

Complex connectivity

![](images/24a46ae52d6334940f280a9ab8570c04cdcc579ae880a428f86a43cb1e013f59.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Input Layer
        A1[" "] --> B1[" "]
        A2[" "] --> B1[" "]
        A3[" "] --> B1[" "]
        A4[" "] --> B1[" "]
    end

    subgraph Output Layer
        B1[" "] --> C1[" "]
        B1[" "] --> C2[" "]
        B1[" "] --> C3[" "]
        B1[" "] --> C4[" "]
        B1[" "] --> C5[" "]
        B1[" "] --> C6[" "]
        B1[" "] --> C7[" "]
        B1[" "] --> C8[" "]
        B1[" "] --> C9[" "]
    end

    style Input Layer fill:#f9f,stroke:#333
    style Output Layer fill:#ccf,stroke:#333
```
</details>

hidden layer 1 hidden layer 2

Layer structure

Fully connected

Computational efficient

Universality of Neural Networks   
![](images/400589242f0ce8c42785e7cbbf416a3baa31224baa940c9f648b9eaa8ceed230.jpg)

<details>
<summary>line</summary>

| x      | actual | pred |
| ------ | ------ | ---- |
| -1.00  | -0.3   | 0.1  |
| -0.75  | -0.8   | 0.2  |
| -0.50  | -0.2   | 0.1  |
| -0.25  | 0.6    | 0.1  |
| 0.00   | 1.0    | 0.3  |
| 0.25   | 0.6    | 0.1  |
| 0.50   | -0.2   | 0.2  |
| 0.75   | -0.5   | 0.1  |
| 1.00   | -0.3   | 0.1  |
</details>

Neural networks can approximate regression functions very well.

# Universality of Neural Networks

![](images/0db97401f9ce73b37b16e7077085bc2912efb9f56555d01b4ad5781eb0c85611.jpg)

<details>
<summary>scatter</summary>

| x    | y    | Class   |
| ---- | ---- | ------- |
| -10  | -10  | Class 1 |
| -5   | -5   | Class 1 |
| 0    | 0    | Class 1 |
| 5    | 5    | Class 1 |
| 10   | 10   | Class 1 |
| -10  | 5    | Class 2 |
| -5   | 10   | Class 2 |
| 0    | 5    | Class 2 |
| 5    | 10   | Class 2 |
| 10   | 5    | Class 2 |
</details>

![](images/ef6bf7a350924d4e9bace5414a72bfd831a4fe7d3dad3372e6c6e0efca5ce900.jpg)

<details>
<summary>area</summary>

| Region   | Value |
| -------- | ----- |
| Class 1  | -3.0  |
| Class 1  | -2.0  |
| Class 1  | -1.0  |
| Class 1  | 0.0   |
| Class 1  | 1.0   |
| Class 1  | 2.0   |
| Class 1  | 3.0   |
| Class 1  | 4.0   |
| Class 1  | 5.0   |
| Class 2  | -3.0  |
| Class 2  | -2.0  |
| Class 2  | -1.0  |
| Class 2  | 0.0   |
| Class 2  | 1.0   |
| Class 2  | 2.0   |
| Class 2  | 3.0   |
| Class 2  | 4.0   |
| Class 2  | 5.0   |
</details>

![](images/b319a87a2c401a7cf2c22a5063c7c18d7d9dd6ca3e384800ab2c9d321f582c01.jpg)

<details>
<summary>area</summary>

| x    | Class 1 | Class 2 |
| ---- | ------- | ------- |
| -10  | -5      | -5      |
| -8   | 7       | -5      |
| -6   | -5      | -5      |
| -4   | 2       | -5      |
| -2   | 0       | -5      |
| 0    | 0       | -5      |
| 2    | 2       | -5      |
| 4    | -5      | -5      |
| 6    | 7       | -5      |
| 8    | -5      | -5      |
</details>

![](images/eeec47b89f402974fae7dd151e283a3cca00f3ea8a6dc1a078f90ea37144be9f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Layer"] --> B["Hidden Layer 1"]
    A --> C["Hidden Layer 2"]
    A --> D["Hidden Layer 3"]
    B --> E["Output Layer"]
    C --> F["Output Layer"]
    D --> G["Output Layer"]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bbf,stroke:#333
    style D fill:#bbf,stroke:#333
    style E fill:#fff,stroke:#333
    style F fill:#fff,stroke:#333
    style G fill:#fff,stroke:#333
```
</details>

![](images/b6d521823ed8f55716d95b6d47412daffa21e106501eeea262ddee77ff758855.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A[" "] --> B[" "]
    A --> C[" "]
    B --> D[" "]
    B --> E[" "]
    C --> F[" "]
    C --> G[" "]
    D --> H[" "]
    D --> I[" "]
    E --> J[" "]
    E --> K[" "]
    F --> L[" "]
    F --> M[" "]
    G --> N[" "]
    G --> O[" "]
    H --> P[" "]
    H --> Q[" "]
    I --> R[" "]
    I --> S[" "]
    J --> T[" "]
    J --> U[" "]
    K --> V[" "]
    K --> W[" "]
    L --> X[" "]
    L --> Y[" "]
    M --> Z[" "]
    M --> AA[" "]
    N --> AB[" "]
    N --> AC[" "]
    O --> AD[" "]
    O --> AE[" "]
```
</details>

![](images/82e79281c9d42a1d5d5e3d80af7ef36296a2879c6a7a2fc54fe40161837ac0b5.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["∫"] --> B["∫"]
    A --> C["∫"]
    A --> D["∫"]
    A --> E["∫"]
    B --> F["∫"]
    C --> G["∫"]
    D --> H["∫"]
    E --> I["∫"]
    style A fill:#fff,stroke:#000
    style B fill:#fff,stroke:#000
    style C fill:#fff,stroke:#000
    style D fill:#fff,stroke:#000
    style E fill:#fff,stroke:#000
    style F fill:#fff,stroke:#000
    style G fill:#fff,stroke:#000
    style H fill:#fff,stroke:#000
    style I fill:#fff,stroke:#000
```
</details>

Neural networks can also approximate classification regions very well.

Recall the regression problem   
![](images/4b0362404c98be3a2c396bd686a0670d070c35828cd5a7925bdba46cce69d859.jpg)

<details>
<summary>bar_line</summary>

| x      | y (red line) | y (blue dots) |
| ------ | ------------ | ------------- |
| -10.0  | 1.2          | 0.9           |
| -7.5   | 0.0          | -0.4          |
| -5.0   | -0.6         | -0.8          |
| -2.5   | 0.4          | 0.5           |
| 0.0    | 0.0          | -0.1          |
| 2.5    | -0.2         | -0.3          |
| 5.0    | 0.1          | 0.4           |
| 7.5    | 0.7          | 0.6           |
| 10.0   | -1.2         | -1.1          |
</details>

How do we solve for ?? ?

1. Initialize $\begin{array} { r l } { \mathbb { R } ^ { s } } & { { } \mathbb { R } ^ { s } } \end{array}$   
2. Calculate the gradient at $\theta _ { t }$   
3. Move a step $\alpha _ { t }$   
4. Iterate until stop.

Data $( X _ { i } , Y _ { i } ) , i = 1 , \ldots , n .$   
To find a network

$$
\boldsymbol {f} (\boldsymbol {x}; \boldsymbol {\theta})
$$

such that

$$
\Sigma \big (Y _ {i} - f (X _ {i}; \theta) \big) ^ {2}
$$

is minimized over

?? = {??: ?? ??; ?? ???? ?? ???????????? ?????????????? ?????????????????????????? ???? $\in \mathbb { R } ^ { s } \}$

# Recall the regression problem

![](images/5d5fcbf8e1b2ec85b9c8a8c3e321670dbbcf38f958ca2bcf7d1bf81e35e24bfc.jpg)

<details>
<summary>scatter</summary>

| x       | y     |
| ------- | ----- |
| -1.00   | 0.00  |
| -0.95   | 0.10  |
| -0.90   | 0.05  |
| -0.85   | 0.00  |
| -0.80   | -0.10 |
| -0.75   | -0.20 |
| -0.70   | -0.30 |
| -0.65   | -0.40 |
| -0.60   | -0.50 |
| -0.55   | -0.60 |
| -0.50   | -0.70 |
| -0.45   | -0.80 |
| -0.40   | -0.90 |
| -0.35   | -1.00 |
| -0.30   | -1.10 |
| -0.25   | -1.20 |
| -0.20   | -1.30 |
| -0.15   | -1.40 |
| -0.10   | -1.50 |
| -0.05   | -1.60 |
| 0.00    | -1.70 |
| 0.05    | -1.80 |
| 0.10    | -1.90 |
| 0.15    | -2.00 |
| 0.20    | -2.10 |
| 0.25    | -2.20 |
| 0.30    | -2.30 |
| 0.35    | -2.40 |
| 0.40    | -2.50 |
| 0.45    | -2.60 |
| 0.50    | -2.70 |
| 0.55    | -2.80 |
| 0.60    | -2.90 |
| 0.65    | -3.00 |
| 0.70    | -3.10 |
| 0.75    | -3.20 |
| 0.80    | -3.30 |
| 0.85    | -3.40 |
| 0.90    | -3.50 |
| 0.95    | -3.60 |
| 1.00    | 3.50  |
</details>

Data $( X _ { i } , Y _ { i } ) , i = 1 , \dots , n$   
To find a network

$$
\boldsymbol {f} (\boldsymbol {x}; \boldsymbol {\theta})
$$

such that

$$
\sum \phi (Y _ {i} - f (X _ {i}; \theta))
$$

is minimized over

$$
\mathcal {F} = \{f: f (x; \theta) i s a
$$

???????????? ??????????????

$$
\text { parameterized   by } \theta \in \mathbb {R} ^ {s} \}
$$

How do we solve for ?? ?

1. Initialize $\begin{array} { r l } { \mathbb { R } ^ { s } } & { { } \mathbb { R } ^ { s } } \end{array}$   
2. Calculate the gradient at $\theta _ { t }$ (with different ??) $\phi )$   
3. Move a step $\cdot$   
4. Iterate until stop

![](images/9a037417ab2d5e335c6ebb718929fd9313d2db3a2c977838f02d10d0e9a8d316.jpg)

<details>
<summary>tree</summary>

| Node | Weight    |
|------|-----------|
| w0   | 0.8622    |
| w1   | 0.5377    |
| x1   | -0.4336   |
| w2   | 0.3188    |
| x2   | 1.8339    |
| w3   | -1.3077   |
| x3   | -2.2588   |
| *    | 0.5846    |
| *    | 2.9539    |
| Σ    | 3.5684    |
| σ    | 0.9726    |
| L    | 0.4730    |
</details>

![](images/29eefe870aa2c290126e55e24696cbabf9047b88ba00b12dc564522451e16646.jpg)

1. An Introduction to Computer Vision Problem   
2. DNN for Image Classification Problems   
3. Convolution   
4. Convolutional Neural Network   
5. Pooling

# Computer Vision Problems

![](images/8045799f8935ca3a98e4aefe07b3141901a9069dc311a42236b9b62917633ccc.jpg)

# Object Detection = What,and Where

![](images/dc38b5a1ee640837f71039bcc26368f2f48706449cc84cc89fed14d22fec33a8.jpg)

<details>
<summary>other</summary>

| Location | Value |
| --- | --- |
| car | 1.000 |
| dog | 0.997 |
| horse | 0.993 |
| person | 0.992 |
| person | 0.979 |
</details>

# Computer Vision Task: Object Segmentation

![](images/e6aaa84319de2d4baf32a2310ec43e0ec16c9079bdd581659741140992dc3f9e.jpg)

<details>
<summary>natural_image</summary>

Two people observing sheep in a grassy field with wooden fence and netting (no visible text or symbols)
</details>

![](images/0352ec54b6e93ca19b664469e9d0f1fa9880d75000a8aca134372a50c6b19528.jpg)

<details>
<summary>text_image</summary>

dog
sheep
sheep
sheep
person
person
</details>

![](images/973bb3d86403e4c7a2fe0212357318c60f3485708f75dba0806b2b40a4f73066.jpg)

<details>
<summary>natural_image</summary>

Vintage steam locomotive with smoke plumes at a train station platform (no visible text or symbols)
</details>

![](images/05e518092b2e77f8835e5f772fdc554f7a4b393b0ca97e305a0324e7b19277ed.jpg)

<details>
<summary>text_image</summary>

person
train
person photo
</details>

![](images/da3d33bb69ed8287f2cfa9825f848a938fa8fbefafc5cb37503bef4946c280cc.jpg)

<details>
<summary>text_image</summary>

WOW
HOSTED BY HEAD WIL
</details>

![](images/48dcd4bea14136d0073f5c868cbe824443f76f5ff25573665a92e413bfd01319.jpg)

<details>
<summary>text_image</summary>

WOW
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
person
tennis racket
tennis racket
</details>

![](images/12b14e4f4aafa7ab7f2c47bad910bba055422e145ab81ff3354493b3e5a58195.jpg)

<details>
<summary>natural_image</summary>

Soccer match in progress on a grass field, players in orange and gray uniforms competing for the ball (no visible text or symbols)
</details>

![](images/a13996a3ee76535356d13ca7abc6309d0bdda65e3b677c32c2801f48cb83686f.jpg)

<details>
<summary>text_image</summary>

person
person
person
sports ball
</details>

![](images/14aa04eac3015a82dd530e836c936f6b854976dc853b157beba130d89a63f34f.jpg)

<details>
<summary>natural_image</summary>

Baseball player in action hitting a ball during a match, wearing jersey number 22 and helmet (no visible text or symbols)
</details>

![](images/f1509bfeab95f9a28a33618719687df8cc15cd870d082f3b91d5d4499c52d60e.jpg)

<details>
<summary>text_image</summary>

sports ball
baseball bat
person
person
</details>

![](images/f7fa550e3d3d2a8db7b4f6e069c42fea4ec4fc72ab0183b78fc1bd0cad0db170.jpg)

<details>
<summary>natural_image</summary>

Exterior view of a historic stone tower with clock face and arched windows under a blue sky (no signage or text visible)
</details>

![](images/abde7c561c6369c07ec1e3e0a866d027d72b19c48ffa590849d452b4b64357cb.jpg)

<details>
<summary>text_image</summary>

clock
clock
</details>

![](images/87849bdd6e5f399567a76492f43474bb38456800cc66565bdb1c6ddfefa23396.jpg)

<details>
<summary>natural_image</summary>

Assorted donuts including pastries, chocolate chips, and various dusted pastries arranged in a grid (no text or labels visible)
</details>

![](images/8244e6d420f77a1c32ca9a9a6ebf44667e232626c2059f0dcf7601eaaa95af3a.jpg)

<details>
<summary>text_image</summary>

donut
donut
donut
donut
donut
donut
donut
donut
donut
donut
</details>

# Computer Vision Task: Art Style Transformation

A   
![](images/035239e702380da3d149f14e845dabfa379a705958c94c4026832d79aeb6c9d1.jpg)

<details>
<summary>natural_image</summary>

Scenic view of a European riverside town with colorful buildings along a riverbank under a clear blue sky (no visible text or signage)
</details>

B   
![](images/9a53d6c3f397d139e72c4234c7501e502b1120b03da660b4d7a1b64648027f2a.jpg)

<details>
<summary>natural_image</summary>

Painting of a European town at night with colorful buildings and trees (no text or symbols)
</details>

![](images/cb3d4a26161a101b784e9fce4c7e346e589026dc077ecf22495c1b8021fe4c42.jpg)

<details>
<summary>natural_image</summary>

Dramatic painting of a ship navigating rough seas with smoke and clouds (no text or symbols)
</details>

![](images/c112dcba92509dd809eb9acf2fdaf55a534acf4319da9cc6cd8f9fe783f3b612.jpg)

<details>
<summary>natural_image</summary>

Close-up of a textured, greenish surface with no visible text or symbols
</details>

C   
![](images/7695b1bf94f0b2c9d95fbee0f998e79fc05a3ca2787d21dd5f715069d60c05ae.jpg)

<details>
<summary>natural_image</summary>

Painting of a European night scene with a starry sky and colorful buildings (no text or symbols)
</details>

D   
![](images/ef07587f704b339fbf025f0b5d7df8542f573c01bbb0817ea5bf99540455c554.jpg)

<details>
<summary>natural_image</summary>

Painting of a European town at sunset with colorful buildings and a prominent church tower (no text or symbols)
</details>

![](images/27f0c485cf01182aac34c55447ce4668276ee6e7339021b74543a752f014f56f.jpg)

<details>
<summary>natural_image</summary>

Painting of Van Gogh's Starry Night at dusk with a tall tree and distant hills (no text or symbols)
</details>

![](images/9a3ab9ca24617599400a912cb812e4aa31c0822b5ae8d66e3cf8fb4cc380a207.jpg)

<details>
<summary>natural_image</summary>

Abstract painting of a dark tree with flowing blue and yellow brushstrokes, no text or symbols present
</details>

![](images/d32a5ea829610be8f47e6d0dc20837cd6ae77f766762d8d8e2e550f29efc124b.jpg)

<details>
<summary>natural_image</summary>

Painting of a figure standing on a wooden bridge under a dramatic sky with orange and blue hues (no text or symbols)
</details>

![](images/e325d3105b9dbd0ea6b9890e5ccf211681f79f8c3a4edb6fb0e389bf190d16b2.jpg)

<details>
<summary>natural_image</summary>

Abstract textured painting with layered brushstrokes in shades of brown and black (no text or symbols)
</details>

# Computer Vision Task: Image Captioning

![](images/85c4733b44402d36a8fc9f26191343bff9e9ea0d67a8643daa50f6a80b64fe99.jpg)

<details>
<summary>natural_image</summary>

Man playing guitar outdoors, wearing a T-shirt with 'HAPPY LIME STONES' and 'FUS TOUR' text (no visible signage or symbols on instrument)
</details>

"man inblack shirtisplaying guitar.

![](images/ea72defbe03649ec0b1cfe0a4042b5baa817b52e35287a67ede4e8f0c7ea48e0.jpg)

<details>
<summary>natural_image</summary>

Worker in safety gear operating machinery near a green fence (no visible text or symbols)
</details>

"construction worker in orange safety vest isworking on road."

![](images/7000d83ee1768f8ae81c6e66531e12cd7208de08c28810754cc1b1300fce856d.jpg)

<details>
<summary>natural_image</summary>

A baby and adult sitting on a red carpet with colorful LEGO blocks, no visible text or symbols.
</details>

"two young girlsare playing with legotoy"

![](images/45101f2fd8dbce325275fb62da034e028b9647efe50ce8afb8980dc698c62f10.jpg)

<details>
<summary>natural_image</summary>

Person performing a mid-air acrobatic kick over a lake, with trees and distant buildings in the background (no visible text or symbols)
</details>

"boyisdoing backflipon wakeboard."

![](images/ba73270ec35c021b3e72200518080ef802709a56cc21373343426a33a46c300b.jpg)

<details>
<summary>natural_image</summary>

Child in pink dress jumping on grass with green trees and flowers in background (no text or symbols)
</details>

"girl inpink dress is jumping in

![](images/b69a08d92623cfd0f245cc0b944d314f0dd897763133320b0d6e9e9d943d87ee.jpg)

<details>
<summary>natural_image</summary>

Black and white dog jumping over a blue and white hurdle in an outdoor arena (no text or symbols visible)
</details>

"blackand white dog jumpsover

![](images/7175c9173648e2e9922db181fa3274dffc48521fc53bfb2ea87d6070a62f0d08.jpg)

<details>
<summary>natural_image</summary>

A young girl climbing a blue playground tube outdoors, surrounded by trees (no visible text or symbols)
</details>

"young girlinpink shirtis swinging on swing."

![](images/7d4c5feb36a69b03e6c14d013e90aff568730bfc5bc37abe2f758249b4d966f5.jpg)

<details>
<summary>natural_image</summary>

Swider in blue suit and red vest wading on water, no visible text or symbols
</details>

"man in blue wetsuit is surfing on wave.

# Computer Vision Task: Visual Question Answering

![](images/d4eb567554981a443c0204b03176166187b4df26782d29e24b7c69acd4ee5f9a.jpg)

<details>
<summary>text_image</summary>

7'0
</details>

What colorare hereyes? What is themustachemade of?

![](images/96cbb81d6f50b3a98e0f505b0323ac40013b9793e66d1992d5803e4fbbe1298f.jpg)

<details>
<summary>natural_image</summary>

Close-up of a large pizza with visible toppings including cheese, tomatoes, and sauce on a wooden surface (no text or symbols)
</details>

Howmany slices of pizzaare there? lsthisavegetarianpizza？

![](images/96677f7cc642cab1c53b4cf6c3a70f18efcb56629ce4fda3ba6d63e423a2b77e.jpg)

<details>
<summary>natural_image</summary>

Illustration of a person sitting on a checkered picnic table outdoors under a sunny sky, with other activities including football, baseball, and tennis visible (no text or symbols)
</details>

Isthisperson expecting company? What is just under the tree?

![](images/f32b0e206255af9b77a324bc630cc8b90227b6ccd1d2f0b59318cd76b551691b.jpg)

<details>
<summary>natural_image</summary>

Man in white shirt and glasses holding a green fruit outdoors near a wooden path and trees (no visible text or symbols)
</details>

Doesitappeartoberainy? Doesthisperson have20/20vision?

# Computer Vision Task: Image Generation

![](images/1274d2b7aab169bb2c404868c852ab21df9d92512119110073af4e29107406a6.jpg)

# IMGENET Large Scale Visual Recognition Challenge

The Image Classification Challenge: 1,000 object classes 1,431,167 images

![](images/7a31d6f102721f7b30d81eecdafa781c0f7605665316b8a40c66907ded83a96b.jpg)

<details>
<summary>natural_image</summary>

Child playing a large gong with wooden sticks, surrounded by a drum and wooden barrel (no visible text or symbols)
</details>

# Output:

Scale

T-shirt

Steel drum

Drumstick

Mud turtle

![](images/2b7fd7e2648f1fc5ec87e641845bb6948d22556b10db0430eba5c4229a02debd.jpg)

# Output:

Scale

T-shirt

Giant panda

Drumstick

Mud turtle

![](images/866cd56506ebc8368f5fb4db2ecbb14cab64782ead2594263120349cb58a9b45.jpg)

Russakovsky et al. arXiv, 2014

![](images/3935153094fc0a0de0a446337f49d4fc4003f31c7830ce92d94fa46e6dbb6dab.jpg)

<details>
<summary>natural_image</summary>

Portrait of a smiling woman with shoulder-length brown hair wearing a patterned scarf (no text visible)
</details>

Feifei Li

# DNN for Image Classification Problem

![](images/28861118321884534222ddaaabe45dbb029144314c4f54b456b8ccdddcb3bdbe.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input"] --> B["HIDDEN"]
    A --> C["OUTPUT"]
    D["Cat Icon"] --> B
    D --> C
    B --> E["Output"]
    C --> E
    style A fill:#f9f,stroke:#333
    style D fill:#ccf,stroke:#333
```
</details>

# Deep Neural Networks (Multi-Layer Perceptrons)

• The architecture of a MLP is expressed as a composition of a series of functions

$$
f _ {\theta} (x) = \mathcal {A} _ {L} \circ \sigma \circ \mathcal {A} _ {L - 1} \circ \sigma \circ \dots \circ \sigma \circ \mathcal {A} _ {1} (x), x \in \mathbb {R} ^ {d _ {0}}
$$

where

$$
\mathcal {A} _ {i} (x) = W _ {i} x + b _ {i}, \qquad x \in \mathbb {R} ^ {d _ {i - 1}}
$$

is the i-th linear transformation with

weight matrix $W _ { i } \in \mathbb { R } ^ { d _ { i } \times d _ { i - 1 } }$ and bias vector $b _ { i } \in \mathbb { R } ^ { d _ { i } }$ ,

and $\cdot$ is the activation function,

$\mathsf { e . g . } , \mathsf { R e L U } \sigma ( x ) = \operatorname* { m a x } \{ x , 0 \} . \mathsf { S i g m o i d } \sigma ( x ) = ( 1 + e ^ { - x } ) ^ { - 1 } .$

![](images/13f1f7c4facaf9411967c2a99a579f97aa3465f4e38af1b3bff33614521c8d80.jpg)

<details>
<summary>natural_image</summary>

A smiling corgi dog standing outdoors on a paved path, with green foliage in the background (no text or symbols visible)
</details>

columr   
![](images/a49fb98f26d972104253eed0969b6e1d9c5e9acd19845ad9830d2aac11f3dfed.jpg)

<details>
<summary>heatmap</summary>

| row | 0 | 1 | 2 |
|---|---|---|---|
| 0 | .392 | .482 | .576 |
| 1 | .478 | .63 | |
| 2 | .580 | .79 | |
| 0 | .169 | .263 | .376 |
| 1 | .263 | .44 | |
| 2 | .373 | .60 | |
| 0 | .306 | .376 | .451 |
| 1 | .376 | .478 | .561 |
| 2 | .443 | .569 | .674 |
</details>

![](images/0f123088e92299b2730937ff0b0afc3cd0071a02c8a67c9de83d3c8432367891.jpg)

<details>
<summary>text_image</summary>

m
3
n
1
1
3*m*n
</details>

![](images/a9ed426034df3460341c1daecb071b02f4dd341ed30ac08645ae4607c370d58b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input 3*m*n"] --> B["Hidden"]
    B --> C["Output"]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bfb,stroke:#333
```
</details>

<table><tr><td>airplane</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>automobile</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>bird</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>cat</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>deer</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>dog</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>frog</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>horse</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>ship</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>truck</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

Training Profile (SGD with Momentum)   
![](images/12bed1be6397d581dc3c6e4f9677734911e1a841814ae56766880334a5c39995.jpg)

<details>
<summary>line</summary>

| Epochs | training loss | test loss |
| ------ | ------------- | --------- |
| 0      | 1.8           | 1.6       |
| 20     | 0.9           | 1.35      |
| 40     | 0.4           | 1.7       |
| 60     | 0.2           | 2.0       |
| 80     | 0.1           | 2.3       |
| 100    | 0.05          | 2.45      |
</details>

Training Profile (SGD with Momentum)   
![](images/6dff0dfc258221cfaf3cd780a5d4d067c8deae8fd12c7f11623716b34be122c8.jpg)

<details>
<summary>line</summary>

| Epochs | Test Accuracy |
| ------ | ------------- |
| 0      | 0.44          |
| 10     | 0.53          |
| 20     | 0.55          |
| 30     | 0.54          |
| 40     | 0.54          |
| 50     | 0.53          |
| 60     | 0.53          |
| 70     | 0.54          |
| 80     | 0.54          |
| 90     | 0.54          |
| 100    | 0.54          |
</details>

Overfitting!!!

Training Profile (SGD with Momentum)   
![](images/1b26a3b570d62d22772bf0c1969b9c9b7b16e5382cd6b5462fc8520902b5b19a.jpg)

<details>
<summary>line</summary>

| Epochs | training loss | test loss |
| ------ | ------------- | --------- |
| 0      | 1.8           | 1.6       |
| 20     | 0.9           | 1.35      |
| 40     | 0.4           | 1.7       |
| 60     | 0.2           | 2.0       |
| 80     | 0.1           | 2.3       |
| 100    | 0.05          | 2.45      |
</details>

Training Profile (SGD with Momentum)   
![](images/34292294289570e537ce6f66bb88f25d88a7b1c49aca086b4ac27b4db9479d8f.jpg)

<details>
<summary>line</summary>

| Epochs | Test Accuracy |
| ------ | ------------- |
| 0      | 0.44          |
| 10     | 0.53          |
| 20     | 0.55          |
| 30     | 0.54          |
| 40     | 0.54          |
| 50     | 0.53          |
| 60     | 0.53          |
| 70     | 0.54          |
| 80     | 0.54          |
| 90     | 0.54          |
| 100    | 0.54          |
</details>

# Convolution

![](images/f6c90b03d7c615e818632a0cc222e5997e44ecca1edeb57bd6334d3e1ca9c205.jpg)

<details>
<summary>text_image</summary>

Center element of the kernel is placed over the source pixel. The source pixel is then replaced with a weighted sum of itself and nearby pixels.
(4 x 0)
(0 x 0)
(0 x 0)
(0 x 0)
(0 x 1)
(0 x 1)
(0 x 0)
(0 x 1)
+ (-4 x 2)
-8
Source pixel
Convolution kernel
(emboss)
New pixel value (destination pixel)
</details>

Key Advantage: Contain Spatial Information.

![](images/40cfdc30a70cc8c3934f690dfe78efc74bb38ebf16691aafae13fd9e4eaca28d.jpg)

<details>
<summary>natural_image</summary>

Close-up of mechanical components including a metallic valve and tubing assembly (no visible text or symbols)
</details>

![](images/d959fc6dd9fb3c71085901dc994feb0d2db225e3ec7742d07d206214954f7fdc.jpg)

<details>
<summary>natural_image</summary>

Black-and-white illustration of a spacecraft in flight, showing its cockpit, armaments, and surrounding terrain (no text or symbols)
</details>

Sobel operator:

$$
\mathbf {G} _ {x} = \left[ \begin{array}{l l l} + 1 & 0 & - 1 \\ + 2 & 0 & - 2 \\ + 1 & 0 & - 1 \end{array} \right] * \mathbf {A} \quad \text {and} \quad \mathbf {G} _ {y} = \left[ \begin{array}{l l l} + 1 & + 2 & + 1 \\ 0 & 0 & 0 \\ - 1 & - 2 & - 1 \end{array} \right] * \mathbf {A}
$$

32x32x3 image   
![](images/dc8a00e41606d552bc01bbd4d0be748669e7b78b9aee5d98285d18e5935c2756.jpg)

<details>
<summary>text_image</summary>

32 height
32 width
3 depth
</details>

![](images/8616a24569626a63d96e5c1f86e705c4a00743ba2c9cbc3b04b99a0e58e2b8bb.jpg)

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
</details>

mage tially, computing dot products”

![](images/365b933cc3c14c25cebdc52000e47b9ad0a66eca19585ead31db8b434fdfda5a.jpg)

<details>
<summary>text_image</summary>

32x32x3 image
5x5x3 filter w
32
32
1 number:
the result of
filter and a
(i.e. 5*5*3 =
</details>

#

of taking a dot product between the small 5x5x3 chunk of the image = 75-dimensional dot product + bias)

$$
\boldsymbol {w} ^ {T} \boldsymbol {x} + \boldsymbol {b}
$$

![](images/e680e847a0dfd8e5e61df3f2339c85b1d5c9c59ee2da4395624ed478fdb0ae96.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["32x32x3 image"] --> B["convolve (slide) over all spatial locations"]
    C["5x5x3 filter"] --> B
    B --> D["activation maps"]
```
</details>

![](images/1fb317f7541ac0c008abb6d9c17c399b26191e58612f638ba8742cc61eb37e6e.jpg)

<details>
<summary>natural_image</summary>

3D geometric diagram showing two stacked blue squares with a top panel, connected by lines to form a grid structure (no text or symbols)
</details>

Output

Filter

Input

Padding

![](images/2cae0010d4568076eaf51b037cbe997e12ead4cb9e87780768f7702a90dddd36.jpg)

<details>
<summary>text_image</summary>

32x32x3 image
2 5x5x3 filters
convolve (slide) over all spatial
locations
32
32
3
</details>

activation maps

![](images/1dfdb819683bb17f02413952bd6e9661b0c657806a43f544b7143cb493df9d06.jpg)

<details>
<summary>natural_image</summary>

3D diagram of two stacked panels with red numbers 2 and 28, no text or symbols present
</details>

![](images/55202b51a84f63648868c1ba2c864a2df277e4dc62bb2f5ede3b626b86f9f317.jpg)

<details>
<summary>text_image</summary>

3
32
32
</details>

1 number: Convolution Layers   
activation maps   
![](images/4231d26ebcbc8f0222f873c51e6bf1117a20fc7a6161b997c35e1ce64a51498b.jpg)

<details>
<summary>text_image</summary>

28
28
6
</details>

Stack these up to get a new “image” of size 28x28x6!

7

![](images/617398c5cf7db7bd1f476a0243358fe341486811fcf750ee3662320d47a0b8d9.jpg)

<details>
<summary>text_image</summary>

Grid pattern with alternating pink and white cells, likely representing a binary or data matrix
</details>

7

7x7 input (spatially) assume 3x3 filter

![](images/18c72ea8c544cae27549b53669c396b5fa638600573de695dab9e3afeaf3a6c8.jpg)

<details>
<summary>text_image</summary>

7
7
</details>

7x7 input (spatially) assume 3x3 filter

![](images/e9d8d2c80f842c23ff5b211b5137271f14a66ab64f95e0bd4410bcf3315b5ccf.jpg)

<details>
<summary>text_image</summary>

7
7
</details>

7x7 input (spatially) assume 3x3 filter

![](images/452ee90f75b96b744f088bff905fd467c2f737e59c81bb442a13133c349a130a.jpg)

<details>
<summary>text_image</summary>

7
7
</details>

7x7 input (spatially) assume 3x3 filter

7

<table><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

7

7x7 input (spatially) assume 3x3 filter

7

![](images/3bc5069b829139182280e41921d9e0806d543cc19b8ba7d349624c6d2547ebec.jpg)

<details>
<summary>text_image</summary>

Grid pattern with alternating pink and white squares, likely a puzzle or grid layout
</details>

7

7x7 input (spatially)

assume 3x3 filter

=> 5 x 5 Output

7

![](images/e6b283bf1a63497e5e89770ba00b1350b4943bc0b2cc717a9a689a876a41eb89.jpg)

<details>
<summary>text_image</summary>

Grid pattern with alternating pink and white cells, likely a puzzle or grid layout
</details>

7

7x7 input (spatially) assume 3x3 filter applied with stride 2

7

![](images/75f7dce72ac842c186ee20eab74209f5630849484a80f9bee26a7803c18179e2.jpg)

<details>
<summary>natural_image</summary>

Grid pattern with a central pink square filled with black lines, no text or symbols present
</details>

7

7x7 input (spatially) assume 3x3 filter applied with stride 2

7

<table><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

7

7x7 input (spatially) assume 3x3 filter applied with stride 2

=> 3 x 3 Output

7

![](images/092d4c87b6cfa24fd0d7e0bb30e8cb5b9cc3facbd9eb8cb74072c8c0c3952be3.jpg)

<details>
<summary>text_image</summary>

Grid pattern with alternating pink and white cells, likely a puzzle or grid layout
</details>

7

7x7 input (spatially)

assume 3x3 filter

applied with stride 3 ?

![](images/a2940eb8e231982fea883bc7ca60a057e6598ad7ad78cea5942eb9973ceb0c9f.jpg)

<details>
<summary>heatmap</summary>

| Row | Col 1 | Col 2 | Col 3 |
|-----|-------|-------|-------|
| 1   | 7     |       |       |
| 2   |       |       |       |
| 3   |       |       |       |
| 4   |       |       |       |
| 5   |       |       |       |
| 6   |       |       |       |
| 7   |       |       |       |
</details>

7x7 input (spatially) assume 3x3 filter applied with stride 3 ?

# doesn’t fit!

cannot apply 3x3 filter on 7x7 input with stride 3.

N

![](images/9625c47deefdeb5858a48f9a4fe4f942db6f5489a6cd46b0db4ab10654077c79.jpg)

<details>
<summary>text_image</summary>

Grid with red letter 'F' in the first cell, likely indicating a mathematical or logical pattern.
</details>

Output size:

(N - F) / stride + 1

N

e.g. N = 7, F = 3:

stride 1 => (7 - 3)/1 + 1 = 5

stride 2 => (7 - 3)/2 + 1 = 3

stride 3 => (7 - 3)/3 + 1 = 2.33

Padding: Pad zeros on the boundary.

<table><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

e.g. input 7x7

3x3 filter, applied with stride 1

pad with 1 pixel border => what is the output?

Padding: Pad zeros on the boundary.

<table><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

e.g. input 7x7

3x3 filter, applied with stride 1

pad with 1 pixel border => what is the output?

7 x 7 Output !

Recall:

(N - F) / stride + 1

# Padding: Pad zeros on the boundary.

<table><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

In general, common to see CONV layers with stride 1, filters of size FxF, and zero-padding with (F-1)/2. (will preserve size spatially)

e.g. F = 3 => zero pad with 1

$$
F = 5 \Rightarrow \text { zero   pad   with } 2
$$

$$
F = 7 \Rightarrow \text { zero   pad   with } 3
$$

![](images/16101753b901319a8c3ce3a9daf0a38b161b03a5140c6130b9a00cf69563e0f4.jpg)

<details>
<summary>text_image</summary>

Input size:
8
Kernel size:
2
Padding:
0
Dilation:
1
Stride:
1
</details>

![](images/fd8810191ec0d29c30e70b25355b622dc46126d6b8081f5289be23a6546a20c8.jpg)

<details>
<summary>text_image</summary>

Input (8 × 8):
</details>

https://ezyang.github.io/convolution-visualizer/

![](images/1d025ecbef51d47be8f3072ded5c786e45a23df7ac8411e3461551f767f0b101.jpg)  
Source: https://towardsdatascience.com/visualizing-the-fundamentals-of-convolutional-neural-networks-6021e5b07f69

Convolution of an image 17x17 with an edge detector kernel 3x3.

Input   
![](images/0752cacedbc417478a87f7fe3024f90d69f67021808c099995b87a8ab6b39be2.jpg)

<details>
<summary>natural_image</summary>

Yellow U.S. Navy biplane in flight against a clear blue sky (no visible text or symbols)
</details>

Result   
Kernel   
![](images/5fc38b965602e563651cea86abd79b2ee2cc52d283c9c311ebbdd8e58a4b5619.jpg)

![](images/55e4fdb0fe9d95ef994a31e8ba0937da95fedf31e7959eeadbada0d990f606f5.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of a vintage biplane in flight, showing fuselage and fuselage details (no visible text or symbols)
</details>

Source: https://towardsdatascience.com/visualizing-the-fundamentals-of-convolutional-neural-networks-6021e5b07f69

Input   
![](images/a72da69d23a7f7cfe3b04c0d876fbc7d843074fd68e8ef453ca67b75d6775c04.jpg)

<details>
<summary>natural_image</summary>

Yellow U.S. Navy biplane in flight against a clear blue sky (no visible text or symbols)
</details>

Result   
Kernel   
![](images/f7011311de5e8ad8bfc4e85fe0b737dbeaf761117ba955bbcfe21639feeadede.jpg)

![](images/842cdbb40d7ba1640d16da1b35d16bc4b8232d7a8dc0d07c2ca18848194ae308.jpg)

<details>
<summary>natural_image</summary>

Blurred grayscale image of an indistinct object with spherical ends and a central body, no visible text or symbols.
</details>

Source: https://towardsdatascience.com/visualizing-the-fundamentals-of-convolutional-neural-networks-6021e5b07f69

Input   
![](images/2e13fa72f2c6f1da647f161a284dbef81cb8960aee3e35da739f3a462ff08687.jpg)

<details>
<summary>natural_image</summary>

Yellow U.S. Navy biplane in flight against a clear blue sky (no visible text or symbols)
</details>

Result   
Kernel   
![](images/47e63826c8fcb0399b0acef45aa958e6cfb21e6bd7822e597dd604e9faf0c6f4.jpg)

![](images/168aa41062da98b95e84f7cd8f4fcee0c6b44c1426063ce6230e7e7fbf647040.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of a vintage biplane in flight against a dark sky (no visible text or markings)
</details>

Source: https://towardsdatascience.com/visualizing-the-fundamentals-of-convolutional-neural-networks-6021e5b07f69

Stride: 2

Time: 7.54

Shape: (391,391)

Stride: 4

Time: 1.91

Shape: (195,195)

![](images/eb3466505dcb5485e2c28f5ba25eb6be7998f0ecfe1a16335156c0fa289dba83.jpg)

<details>
<summary>natural_image</summary>

Silhouette of a vintage airplane with two wheels and a body, no visible text or symbols
</details>

Stride: 8

Time: 0.49

Shape: (97,97)

![](images/645cfadb69d322e81617299444cc76245d42cbb98d9b9d5241ed758660ddfd26.jpg)

<details>
<summary>text_image</summary>

TOMATO
4
</details>

Stride: 16

Time: 0.17

Shape: (48,48)

![](images/0812f8a62e1b15b568979cfa6e6ee20dbf35b5898ac5b248aa245e932675cbd7.jpg)

<details>
<summary>natural_image</summary>

Blurred grayscale image of a vehicle or toy with no visible text, numbers, or symbols.
</details>

![](images/a4b05bbe9500ba6c10fbea22eda8dca7291b33e9c148e39d31d6ba3695e7deae.jpg)

<details>
<summary>natural_image</summary>

Pixelated grayscale image of an airplane in flight (no visible text or symbols)
</details>

# Convolutional Neural Network

CNN is a sequence of Convolution Layers , interspersed with activation functions.

![](images/1d00b30485af1b6c50479e643801947bc9ddf0ce3669808086ede90f09e5beb1.jpg)

<details>
<summary>text_image</summary>

32
CONV
ReLU
e.g. 6 5x5x3
filters
32
3
28
6
28
</details>

CNN is a sequence of Convolution Layers , interspersed with activation functions.32

![](images/3a78db448a4c8be969588300a64d45502cc911717929612963b92cc99c798e62.jpg)

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

![](images/112f39045b914f5d7933c9e00239dc2754e423681a3f8da2532273c9e6282958.jpg)

<details>
<summary>text_image</summary>

56
56
64
</details>

1x1 CONV with 32 filters (each filter has size 1x1x64, and performs a 64-dimensional dot product)   
![](images/bd27d8c95429581b8b71820bcf6d3ccca5dc810328b6777e49004a8761e7d158.jpg)

<details>
<summary>bar</summary>

| Dimension | Value |
|---|---|
| Height | 32 |
| Width | 56 |
| Top Margin | 56 |
</details>

![](images/7ffa468c31fa7d8cd12b8afba6e69a863ab9c5873a37cfcafc844db44d9e6b23.jpg)

<details>
<summary>bar</summary>

| Dimension | Value |
| --------- | ----- |
| Top Left  | 64    |
| Top Right | 56    |
| Bottom Left | 56   |
| Bottom Right | 56  |
</details>

1x1 CONV with 32 filters (each filter has size 1x1x64, and performs a 64-dimensional dot product)   
![](images/088f9dd622bdd87993d97d77b51fe62d549de18ca16641f1824783ab50e7d8bb.jpg)

<details>
<summary>bar</summary>

| Dimension | Value |
|---|---|
| Height | 32 |
| Top Section | 56 |
| Bottom Section | 56 |
</details>

1x1 convolution kernel is meaningful! It computes the dot product over the channels.

# CONV2D

# Examples

```txt
>>> # With square kernels and equal stride
>>> m = nn.Conv2d(16, 33, 3, stride=2)
>>> # non-square kernels and unequal stride and with padding
>>> m = nn.Conv2d(16, 33, (3, 5), stride=(2, 1), padding=(4, 2))
>>> # non-square kernels and unequal stride and with padding and dilation
>>> m = nn.Conv2d(16, 33, (3, 5), stride=(2, 1), padding=(4, 2), dilation=(3, 1))
>>> input = torch.randn(20, 16, 50, 100)
>>> output = m(input) 
```

# The bias affects the activation.

![](images/b0407b5d91c247a51df4ee8a7fb2a299dbef888ffc010118a3764a00dcbf1ed2.jpg)

<details>
<summary>line</summary>

| u     | ReLU(u) |
|-------|---------|
| bias  | 0       |
| > 0   | linear |
</details>

![](images/d1064323b08d129e51beb531e1d459226146eaf126a819bdee7daa83be9f47bc.jpg)

<details>
<summary>line</summary>

| u    | ReLU(u) |
| ---- | ------- |
| 0    | 0       |
| bias=0 | 0     |
| u    | >0      |
</details>

![](images/08c3c225888eac45a91a1af120bd33b58f18271ca1c18f7bd2c949973f9d64d8.jpg)

<details>
<summary>line</summary>

| u     | ReLU(u) |
|-------|---------|
| below bias | 0       |
| above bias | 0       |
</details>

Source: https://towardsdatascience.com/visualizing-the-fundamentals-of-convolutional-neural-networks-6021e5b07f69

Input Image 

<table><tr><td>252</td><td>251</td><td>246</td><td>207</td><td>90</td></tr><tr><td>250</td><td>242</td><td>236</td><td>144</td><td>41</td></tr><tr><td>252</td><td>244</td><td>228</td><td>102</td><td>43</td></tr><tr><td>250</td><td>243</td><td>214</td><td>59</td><td>52</td></tr><tr><td>248</td><td>243</td><td>201</td><td>44</td><td>54</td></tr></table>

Kernel 

<table><tr><td>1</td><td>0</td><td>-1</td></tr><tr><td>1</td><td>0</td><td>-1</td></tr><tr><td>1</td><td>0</td><td>-1</td></tr></table>

Convolution Output 

<table><tr><td>44</td><td>284</td><td>536</td></tr><tr><td>74</td><td>424</td><td>542</td></tr><tr><td>107</td><td>525</td><td>494</td></tr></table>

Convolution 

<table><tr><td rowspan="4">ReLU</td><td colspan="3">Output</td></tr><tr><td>44</td><td>284</td><td>536</td></tr><tr><td>74</td><td>424</td><td>542</td></tr><tr><td>107</td><td>525</td><td>494</td></tr></table>

# ReLU activation function makes the negative inputs to be zero.

![](images/21d5d4fb262a4e4b26b0e1c1fb49f1af5945985a818a59eab9c22b6fafd7d60d.jpg)

<details>
<summary>heatmap</summary>

| Input | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|
| 1     |   |   |   |   |   |
| 2     |   |   |   |   |   |
| 3     |   |   |   |   |   |
| 4     |   |   |   |   |   |
| 5     |   |   |   |   |   |
</details>

![](images/5cb73249e16919beb49067dedc7eca82e1cecb37b3d986f8f390debd3660a759.jpg)

<details>
<summary>bar</summary>

Kernel
| Category | Value |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
</details>

![](images/efff4863a8ca9bd67cc324f46756371591f6472a416a3416b3786a2a8773661f.jpg)

<details>
<summary>heatmap</summary>

Convolution Output
| | 1 | 2 | 3 |
|---|---|---|---|
| 1 | Dark Grey | Light Grey | White |
| 2 | Dark Grey | Light Grey | White |
| 3 | Dark Grey | White | Light Grey |
</details>

![](images/553ef411a9046b75b798f48e91508f9a1c0210a235d8dbf3d440cdb18ddb0713.jpg)

<details>
<summary>heatmap</summary>

ReLU Output
| | 1 | 2 | 3 |
|---|---|---|---|
| 1 | Black | White | Light Gray |
| 2 | Black | White | White |
| 3 | Black | Dark Gray | Dark Gray |
</details>

Bias:500   
![](images/147aa485fc633fbed0ed263ec457f9aec8827bf5d572edb88fed8e5e84911eb5.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of a vintage airplane with visible wheels and body (no text or symbols)
</details>

Bias:0   
![](images/551bfc795b10b74213fa7a7a48720a67ce5ef1d64b0d38036a9fa04819cce605.jpg)

<details>
<summary>natural_image</summary>

Abstract grayscale image with no discernible text, symbols, or identifiable objects
</details>

Bias: -500   
![](images/69df08332ecd0d21ce3dd641593c14851127e9beaea1c17ccd86c338427b7595.jpg)

<details>
<summary>natural_image</summary>

Completely black image with no visible content or text
</details>

Bias: -1000   
![](images/dac025306d92b3d176d8427d5973702586a7ac8fe6c938574afe2bbff9585dc2.jpg)

<details>
<summary>natural_image</summary>

Completely black image with no visible content or text
</details>

# Pooling

# Pooling Layer is a down sampling strategy.

1. Construct better translationally invariant features.   
2. Learn more compact features.

![](images/614637d0d9d2083e7fe011b82349980671cd53286a1179bc5b6c72dd5d77494e.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["224x224x64"] --> B["pool"]
    C["112x112x64"] --> D["downsampling"]
    E["224"] --> F["downsampling"]
    G["112"] --> H["downsampling"]
```
</details>

<table><tr><td>1</td><td>1</td><td>2</td><td>4</td></tr><tr><td>5</td><td>6</td><td>7</td><td>8</td></tr><tr><td>3</td><td>2</td><td>1</td><td>0</td></tr><tr><td>1</td><td>2</td><td>3</td><td>4</td></tr></table>

max pool with 2x2 filters and stride 2

<table><tr><td>6</td><td>8</td></tr><tr><td>3</td><td>4</td></tr></table>

Max Pooling Layer is robust to small perturbation.

<table><tr><td>1</td><td>1</td><td>2</td><td>4</td></tr><tr><td>5</td><td>6</td><td>7</td><td>8</td></tr><tr><td>3</td><td>2</td><td>1</td><td>0</td></tr><tr><td>1</td><td>2</td><td>3</td><td>4</td></tr></table>

average pool with 2x2 filters and stride 2

<table><tr><td>3.25</td><td>5.25</td></tr><tr><td>2</td><td>1.75</td></tr></table>

Given a D x M x N tensor, if we apply the pooling operator with size K x K and Stride P, what are the dimensions of the output?

$$
D \times ((M - K) / P + 1) \times ((N - K) / P + 1)
$$

# MAXPOOL2D

![](images/f2b2c146aea4cf376e73fd5a14afa2459140554267d1060ab161c54e8abe5bea.jpg)

Examples:

```txt
>>> # pool of square window of size=3, stride=2
>>> m = nn.MaxPool2d(3, stride=2)
>>> # pool of non-square window
>>> m = nn.MaxPool2d((3, 2), stride=(2, 1))
>>> input = torch.randn(20, 16, 50, 32)
>>> output = m(input) 
```

# Receptive Fields

For convolution with kernel size K, each element in the output depends on a K x K receptive field in the input.

![](images/f54b594ca263c39677e05a33a3bd9b1b29c773b72fc7abf233ef5f06cbb8733c.jpg)

<details>
<summary>natural_image</summary>

Simple geometric diagram showing a square connected to a larger square via dashed lines (no text or symbols)
</details>

Input

Output

Each successive convolution contains multiple regions from the previous one.

![](images/ac61af7ce6d93e8396f5483bd415a0a138d19b1af6023bcb2ac096154c238b84.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input Block 1"] --> B["Process Unit 1"]
    C["Input Block 2"] --> D["Process Unit 2"]
    E["Output Block 3"] --> F["Output Block 4"]
```
</details>

Suggested Reading: Computing receptive fields of convolutional neural network.

![](images/a35fa018e9dc16c31d89c08825fec2847ce7becba7eb6630c504d56f6f826424.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["INPUT (28 x 28 x 1)"] --> B["n1 channels (24 x 24 x n1)"]
    B --> C["n1 channels (12 x 12 x n1)"]
    C --> D["n2 channels (8 x 8 x n2)"]
    D --> E["n2 channels (4 x 4 x n2)"]
    E --> F["flattened"]
    F --> G["fc_3 Fully-Connected Neural Network ReLU activation"]
    F --> H["fc_4 Fully-Connected Neural Network"]
    G --> I["(with dropout)"]
    H --> J["OUTPUT"]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bbf,stroke:#333
    style D fill:#bbf,stroke:#333
    style E fill:#bbf,stroke:#333
    style F fill:#bfb,stroke:#333
    style G fill:#cfc,stroke:#333
    style H fill:#cfc,stroke:#333
```
</details>

Source: https://www.analyticsvidhya.com/blog/2020/10/what-is-the-convolutional-neural-network-architecture/

Convolution Neural Network (CNN)   
![](images/3b989815e003b891d471cc85aa26769b887501e01e9c51bb76bd876f2cd72fb3.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input"] --> B["Kernel"]
    B --> C["Convolution + ReLU"]
    C --> D["Pooling"]
    D --> E["Convolution + ReLU"]
    E --> F["Pooling"]
    F --> G["Convolution + ReLU"]
    G --> H["Feature Maps"]
    H --> I["Flatten Layer"]
    I --> J["Fully Connected Layer"]
    J --> K["Classification"]
    K --> L["SoftMax Activation Function"]
    L --> M["Output: Horse 0.2, Zebra 0.7, Dog 0.1"]
    style A fill:#f9f,stroke:#333
    style L fill:#bbf,stroke:#333
```
</details>

Source: https://developersbreach.com/convolution-neural-network-deep-learning/

![](images/8922d6ebc3a4661c8fd146ecde67ef6aef6aec8f000289319271884a608cb1a6.jpg)

<details>
<summary>text_image</summary>

7
</details>

Input Layer (28 x 28 x 1)

<table><tr><td>0.003</td><td>-0.077</td><td>-0.037</td><td>0.039</td><td>-0.095</td></tr><tr><td>0.103</td><td>-0.345</td><td>0.22</td><td>0.01</td><td>0.137</td></tr><tr><td>0.028</td><td>-0.259</td><td>-0.108</td><td>-0.077</td><td>0.14</td></tr><tr><td>-0.078</td><td>-0.062</td><td>0.021</td><td>-0.015</td><td>-0.018</td></tr><tr><td>-0.042</td><td>0.067</td><td>0.088</td><td>0.051</td><td>0.2</td></tr></table>

<table><tr><td>0.028</td><td>0.06</td><td>0.046</td><td>0.069</td><td>0.214</td></tr><tr><td>-0.093</td><td>-0.019</td><td>0.036</td><td>0.23</td><td>-0.115</td></tr><tr><td>-0.265</td><td>-0.43</td><td>-0.266</td><td>-0.278</td><td>-0.328</td></tr><tr><td>-0.005</td><td>-0.029</td><td>-0.244</td><td>-0.132</td><td>-0.216</td></tr><tr><td>0.111</td><td>-0.035</td><td>0.197</td><td>0.183</td><td>0.136</td></tr></table>

Kernels= 2x(5x5x1) Stride=1,Activation=ReLU

![](images/f3c924da4642335bb2472082394e371e2a303a79756a60eb44d056312fb4b21b.jpg)

<details>
<summary>text_image</summary>

7
</details>

![](images/9d784cf286d63be775d550ec3869dd4531f70893f53ac6a84b241840b65ef3be.jpg)

<details>
<summary>text_image</summary>

Pixelated image showing a horizontal bar and a downward arrow on a dark grid background, possibly indicating a measurement or annotation.
</details>

Actiyation 2.Layer 1

Visualizing Convolutional Neural Networks Layer by Layer