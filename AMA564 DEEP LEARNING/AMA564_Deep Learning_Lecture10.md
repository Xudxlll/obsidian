# AMA 564 Deep Learning

# 2026 Spring

# Lecture 10

Word Embedding   
Attention   
Transformer

# Word Embedding

In natural language processing (NLP), a word embedding is a representation of a word.   
The embedding is used in text analysis.   
Typically, the representation is a real-valued vector that encodes the meaning of the word in such a way that words that are closer in the vector space are expected to be similar in meaning.

# Extending to larger vocabularies

# Word Embeddings Properties

• Word Similarities / Synonyms   
Linguistic Relationships

Example 2D word embedding space, where similar words are found in similar locations.   
![](images/1a625022af3de2cc4b6ef2e70d9af4118667dcc43f9dae85a213913293e03985.jpg)  
Source: http://suriyadeepan.github.io

![](images/8f0e016b390ce8e5c5fbeb5880a5e54492b8d82e04d2aa439914c317db309b97.jpg)

<details>
<summary>text_image</summary>

king
man
woman
queen
</details>

Male-Female

![](images/83df0ab330d1f292cbde0bd8c262e5bb6e62ebd0a0ae37401ad8265456995095.jpg)

<details>
<summary>text_image</summary>

walked
swam
walking
swimming
</details>

Verbtense

![](images/d35ba6df26b550b43c605cba1c3b7156231dc7767a8c1517b99b6d51eafa53ce.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Spain"] --> B["Madrid"]
    C["Italy"] --> D["Rome"]
    E["Germany"] --> F["Berlin"]
    G["Turkey"] --> H["Ankara"]
    I["Russia"] --> J["Moscow"]
    K["Canada"] --> L["Ottawa"]
    M["Japan"] --> N["Tokyo"]
    O["Vietnam"] --> P["Hanoi"]
    Q["China"] --> R["Beijing"]
```
</details>

Country-Capital

Three examples of relationships that are automatically uncovered during wordembedding training – male-female, verb tense, and country-capital.

# Extending to larger vocabularies

# The most popular algorithms include

1. Word2Vec algorithm from Google   
2. GloVe algorithm from Stanford   
3. fasttext algorithm from Facebook

# • Continuous Skip-gram Model:

predicts words within a certain range before and after the current word in the same sentence.

# • Continuous Bag-of-Words Model (CBOW):

predicts the middle word based on surrounding context words. The context consists of a few words before and after the current (middle) word. This architecture is called a bag-of-words model as the order of words in the context is not important.

To train a neural network with a single hidden layer to perform a prediction task. But the goal is to learn the weights of the hidden layer–these weights are the “word vectors”.

“The wide road shimmered in the hot sun.” 

<table><tr><td>Window Size</td><td>Text</td><td>Skip-grams</td></tr><tr><td rowspan="3">2</td><td>[ The wide road shimmered ] in the hot sun.</td><td>wide, the wide, road wide, shimmered</td></tr><tr><td>The [ wide road shimmered in the ] hot sun.</td><td>shimmered, wide shimmered, road shimmered, in shimmered, the</td></tr><tr><td>The wide road shimmered in [ the hot sun ].</td><td>sun, the sun, hot</td></tr><tr><td rowspan="3">3</td><td>[ The wide road shimmered in ] the hot sun.</td><td>wide, the wide, road wide, shimmered wide, in</td></tr><tr><td>[ The wide road shimmered in the hot ] sun.</td><td>shimmered, the shimmered, wide shimmered, road shimmered, in shimmered, the shimmered, hot</td></tr><tr><td>The wide road shimmered [ in the hot sun ].</td><td>sun, in sun, the sun, hot</td></tr></table>

$\_$ One-hot embedding of the input word

$\_$ One-hot embedding of the target word

$\boldsymbol { \hat { y } } = \left( \hat { y } _ { 1 } , \cdots , \hat { y } _ { V } \right)$ Predicted vector of probabilities

![](images/b8041d135308ca628ab0fa49821f3fb627996f153bb4eaf182a21bce940daf00.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Input
        X1["x₁"] -->|0| N["N"]
        X2["x₂"] -->|0| N
        X3["xᵢ"] -->|1| X["Embedding matrix"]
        X4["xᵥ"] -->|0| X
    end

    subgraph Hidden
        N -->|h₁| V["V="]
        N -->|h₂| V
        N -->|h₃| V
        N -->|...| V
        N -->|hₙ| V
    end

    subgraph Context Matrix
        V --> M["V"]
        M --> N["Matrix W'"]
        N --> N'[N=]
        M --> N'[N=]
    end

    Outputよmax["Output softmax"]
    style Input fill:#f9f,stroke:#333
    style Hidden fill:#ccf,stroke:#333
    style Context Matrix fill:#cfc,stroke:#333
```
</details>

![](images/5af37e2ff2b220c9440a18410f28c836ab77e5efc30e93326aaa66ced2b1dc2a.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Input
        X1["Input x₁"] -->|0| N["N"]
        X2["Input x₂"] -->|0| N
        X3["Input xᵢ"] -->|1| Matrix_W["Matrix W"]
        X4["Input xᵥ"] -->|0| Embedding["Embedding matrix"]
    end

    subgraph Hidden
        N["N"] -->|V=| H1["h₁"]
        N -->|V=| H2["h₂"]
        N -->|V=| H3["h₃"]
        N -->|V=| HN["hₙ"]
        H1 --> V["V"]
        H2 --> V
        H3 --> V
        HN --> V
    end

    subgraph Context Matrix
        V["V"] --> M["Matrix W'"]
        M --> N["N"]
        N --> M
        M --> N
    end

    Outputsoftmax["Output softmax y₁"] --> Y1["y₁"]
    Outputsoftmax --> Y2["y₂"]
    Outputsoftmax --> Yj["yⱼ"]
    Outputsoftmax --> YV["yᵥ"]
    style Hidden fill:#f9f,stroke:#333
    style Context Matrix fill:#bbf,stroke:#333
```
</details>

Rows of embedding matrix W are the embeddings of words.

$$
\left[ \begin{array}{l l l l l} 0 & 0 & 0 & 1 & 0 \end{array} \right] \times \left[ \begin{array}{l l l} 1 7 & 2 4 & 1 \\ 2 3 & 5 & 7 \\ 4 & 6 & 1 3 \\ 1 0 & 1 2 & 1 9 \\ 1 1 & 1 8 & 2 5 \end{array} \right] = \left[ \begin{array}{l l l} 1 0 & 1 2 & 1 9 \end{array} \right]
$$

Rows of embedding matrix W are the embeddings of words.

# “The quick brown fox jumps over the lazy dog.”

# Window size: 2 Sentence

The quickbrownfox jumps over the lazy dog.

The quick brown foxjumps over the lazy dog.

The quick brown foxjumpsover the lazy dog.

The quick brown fox jumpsoverthe lazy dog.

# Training Samples CBOW

(quick, brown), the)

(the,brown,fox),quick)

(the, quick,fox,jumps),brown)

(quick,brown,jumps,over),fox)

$X _ { 1 } , X _ { 2 } , \dots , X _ { w }$ A bag of One-hot embeddings of the input words

$\_$ One-hot embedding of the target word

$\cdot$ Predicted vector of probabilities

Input   
![](images/e04dc5563ea57a990090dcd005e43ca48a0956a6abd0de87a1e3dcfee8afff39.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Input Layer
        direction TB
        A["0"] --> B["X"]
        C["1"] --> B
        D["0"] --> E["X"]
        F["1"] --> E
        G["0"] --> H["X"]
        I["0"] --> H
        J["1"] --> K["X"]
        L["0"] --> K
        M["1"] --> N["X"]
    end

    subgraph Hidden Layer
        N["Matrix W\nV = avg\nh₁\nh₂\nh₃\n...\nhₙ"] --> O["X"]
        P["Matrix W'"] --> O
        O --> Q["V"]
        Q --> R["Output softmax\n0\ny₁\n...\n1\n...\n0"]
    end

    style N fill:#f9f,stroke:#333
    style O fill:#ccf,stroke:#333
    style P fill:#cfc,stroke:#333
    style Q fill:#fcc,stroke:#333
    style R fill:#cff,stroke:#333
```
</details>

Input   
![](images/85f515f3c0e6f0c3eb6b53567c95107f3c751c78de60ca2cc0ada7cb6036c361.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Input Layer
        A["0"] --> B["X"]
        C["1"] --> B
        D["..."] --> B
        E["0"] --> F["X"]
        G["1"] --> F
        H["..."] --> F
        I["0"] --> J["X"]
        K["1"] --> J
        L["..."] --> J
        M["0"] --> N["X"]
    end

    subgraph Hidden Layer
        O["Matrix W"] --> P["V = avg"]
        Q["h₁"] --> R["X"]
        S["h₂"] --> R
        T["h₃"] --> R
        U["..."] --> R
        V["..."] --> R
        W["..."] --> R
        X["h_N"] --> R
        Y["V"] --> Z["Matrix W'"]
    end

    subgraph Output Softmax
        AA["0"] --> AB["y₁"]
        AC["..."] --> AD["yⱼ"]
        AE["1"] --> AF["yᵥ"]
        AG["..."] --> AF
        AH["0"] --> AI["yᵥ"]
    end

    style Hidden Layer fill:#f9f,stroke:#333
    style Output Softmax fill:#bbf,stroke:#333
```
</details>

Rows of embedding matrix W are the embeddings of words.

![](images/3b1135e54e21527d84a60c5501a8d1dc415947c7037d6b78d4cca0d5ac502fdc.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph_Input_1["Input"]
        W_t_minus_2["W(t-2)"] --> SUM["SUM"]
        W_t_minus_1["W(t-1)"] --> SUM
        W_t_plus_1["W(t+1)"] --> SUM
        W_t_plus_2["W(t+2)"] --> SUM
    end

    subgraph_Projection_1["Projection"]
        SUM --> W_t["W(t)"]
    end

    subgraph_Output_1["Output"]
        W_t_minus_2 --> W_t_minus_1["W(t-1)"]
        W_t_minus_1 --> W_t_plus_1["W(t+1)"]
        W_t_plus_1 --> W_t_plus_2["W(t+2)"]
    end

    SUM --> W_t
    style Input_1 fill:#f9f,stroke:#333
    style Projection_1 fill:#bbf,stroke:#333
    style Output_1 fill:#bfb,stroke:#333
```
</details>

When vocabulary is extremely large, calculating the denominator of SoftMax is computationally impractical.

• Hierarchical Softmax (Morin and Bengio (2005))   
• Negative Sampling (Mikolov et al. (2013))

![](images/2a24e7386f04397558c84d2be8dfaebe6874a42bf74e5fb37d0e2b9def543b56.jpg)

<details>
<summary>bar_line</summary>

| Question | Value |
| :--- | :--- |
| "What" | 0.11 |
| "I'm" | 0.28 |
| "Horse" | 0.03 |
| "Why" | 0.15 |
| "Huh" | 0.09 |
| "No" | 0.17 |
| "Yes" | 0.05 |
| "Sup" | 0.11 |
</details>

![](images/4785a1489ca468e03dda4f3301a3fcb15e023605892e612752068ac9aa03c5a3.jpg)

$$
\text { Computed   V   times   for   all   vocabs } \left\{ \begin{array}{l} \left[ \begin{array}{c} p (w _ {1} | w ^ {(t)}) \\ p (w _ {2} | w ^ {(t)}) \\ p (w _ {3} | w ^ {(t)}) \\ \vdots \\ p (w _ {V} | w ^ {(t)}) \end{array} \right] = \frac {\exp (W _ {\text { output }} \cdot h)}{\sum_ {i = 1} ^ {V} \exp (W _ {\text { output } _ {(i)}} \cdot h)} \in \mathbb {R} ^ {V} \\ \text { where   V   is   very   large } \\ \text { aegis4048.github.io } \\ \text { V   computations   are   needed   to } \end{array} \right.
$$

$$
\text { Complexity } = O (V + V) \approx O (V)
$$

getnormalizationfactor

$$
\left[ \begin{array}{c} p (D = 1 | w, c _ {p o s}) \\ p (D = 1 | w, c _ {n e g, 1}) \\ p (D = 1 | w, c _ {n e g, 2}) \\ p (D = 1 | w, c _ {n e g, 3}) \\ \vdots \\ p (D = 1 | w, c _ {n e g, K}) \end{array} \right]
$$

$$
= \frac {1}{1 + e x p (- (\{c _ {p o s} \} \cup W _ {n e g}) \cdot h)} \in \mathbb {R} ^ {K + 1} \tag {7}
$$

# Vanilla Skip-Gram

# Negative Sampling

W\_output (old) 

<table><tr><td>-0.560</td><td>0.340</td><td>0.160</td></tr><tr><td>-0.910</td><td>-0.440</td><td>1.560</td></tr><tr><td>-1.210</td><td>-0.130</td><td>-1.320</td></tr><tr><td>1.670</td><td>-0.150</td><td>-1.030</td></tr><tr><td>1.720</td><td>-1.460</td><td>0.730</td></tr><tr><td>0.000</td><td>1.390</td><td>-0.120</td></tr><tr><td>-0.060</td><td>1.520</td><td>-0.790</td></tr><tr><td>0.800</td><td>1.850</td><td>-1.670</td></tr><tr><td>-1.370</td><td>1.320</td><td>-0.480</td></tr><tr><td>0.670</td><td>1.990</td><td>-1.850</td></tr><tr><td>-1.520</td><td>-1.740</td><td>-1.860</td></tr></table>

（11X3）

Learning R. 

<table><tr><td>-</td><td>0.05</td><td>×</td></tr></table>

grad\_W\_output 

<table><tr><td>0.064</td><td>0.071</td><td>-0.014</td></tr><tr><td>0.098</td><td>0.015</td><td>0.063</td></tr><tr><td>0.069</td><td>0.089</td><td>0.045</td></tr><tr><td>0.014</td><td>0.085</td><td>0.079</td></tr><tr><td>-0.021</td><td>0.067</td><td>0.071</td></tr><tr><td>-0.098</td><td>-0.088</td><td>0.091</td></tr><tr><td>-0.072</td><td>-0.078</td><td>-0.089</td></tr><tr><td>0.046</td><td>-0.079</td><td>-0.053</td></tr><tr><td>-0.049</td><td>-0.087</td><td>0.025</td></tr><tr><td>-0.060</td><td>0.092</td><td>0.042</td></tr><tr><td>0.074</td><td>0.050</td><td>0.070</td></tr></table>

（11X3)

=   
W\_output (new) 

<table><tr><td>-0.563</td><td>0.336</td><td>0.161</td></tr><tr><td>-0.915</td><td>-0.441</td><td>1.557</td></tr><tr><td>-1.213</td><td>-0.134</td><td>-1.322</td></tr><tr><td>1.669</td><td>-0.154</td><td>-1.034</td></tr><tr><td>1.721</td><td>-1.463</td><td>0.726</td></tr><tr><td>0.005</td><td>1.394</td><td>-0.125</td></tr><tr><td>-0.056</td><td>1.524</td><td>-0.786</td></tr><tr><td>0.798</td><td>1.854</td><td>-1.667</td></tr><tr><td>-1.368</td><td>1.324</td><td>-0.481</td></tr><tr><td>0.673</td><td>1.985</td><td>-1.852</td></tr><tr><td>-1.524</td><td>-1.743</td><td>-1.864</td></tr></table>

（11X3）

W\_output (old) 

<table><tr><td>-0.560</td><td>0.340</td><td>0.160</td></tr><tr><td>-0.910</td><td>-0.440</td><td>1.560</td></tr><tr><td>-1.210</td><td>-0.130</td><td>-1.320</td></tr><tr><td>1.670</td><td>-0.150</td><td>-1.030</td></tr><tr><td>1.720</td><td>-1.460</td><td>0.730</td></tr><tr><td>0.000</td><td>1.390</td><td>-0.120</td></tr><tr><td>-0.060</td><td>1.520</td><td>-0.790</td></tr><tr><td>0.800</td><td>1.850</td><td>-1.670</td></tr><tr><td>-1.370</td><td>1.320</td><td>-0.480</td></tr><tr><td>0.670</td><td>1.990</td><td>-1.850</td></tr><tr><td>-1.520</td><td>-1.740</td><td>-1.860</td></tr></table>

（11×3）

LearningR. 

<table><tr><td>-</td><td>0.05</td><td>×</td></tr></table>

grad\_W\_output 

<table><tr><td>Not computed!</td></tr><tr><td>aegis4</td></tr></table>

<table><tr><td>Positive sample, w_o</td></tr><tr><td>Negative sample, k=1</td></tr><tr><td>Negative sample, k=2</td></tr><tr><td>Negative sample, k=3</td></tr></table>

<table><tr><td>0.031</td><td>0.030</td><td>0.041</td></tr><tr><td>-0.090</td><td>0.031</td><td>-0.065</td></tr><tr><td>0.056</td><td>0.098</td><td>-0.061</td></tr><tr><td>0.069</td><td>0.084</td><td>-0.044</td></tr></table>

=   
W\_output(new)

<table><tr><td>-0.560</td><td>0.340</td><td>0.160</td></tr><tr><td>-0.910</td><td>-0.440</td><td>1.560</td></tr><tr><td>-1.210</td><td>-0.130</td><td>-1.320</td></tr><tr><td>1.670</td><td>-0.150</td><td>-1.030</td></tr><tr><td>1.720</td><td>-1.460</td><td>0.730</td></tr><tr><td>0.000</td><td>1.390</td><td>-0.120</td></tr><tr><td>-0.060</td><td>1.520</td><td>-0.790</td></tr><tr><td>0.798</td><td>1.849</td><td>-1.672</td></tr><tr><td>-1.366</td><td>1.318</td><td>-0.477</td></tr><tr><td>0.667</td><td>1.985</td><td>-1.847</td></tr><tr><td>-1.523</td><td>-1.744</td><td>-1.858</td></tr></table>

（11X3）

# Binomial Classification

(regression, logistic)

(regression,machine)

(regression, sigmoid)

(regression, supervised)

(regression, neural)

# VS

(regression, zebra)

(regression, pimples)

(regression, Gangnam-Style)

(regression, toothpaste)

(regression, idiot)

Likely to observe

$$
p (D = 1 | w, c _ {p o s}) \approx 1
$$

Unlikely to observe

$$
p (D = 1 | w, c _ {n e g}) \approx 0
$$

Drilling fluids serve to balance formation pressures while drilling to ensure wellbore stability. They also carry cutings to the surface and cool the bit. The drilling engineer traditionally designs drilling fluids|with|two primary goals in mind: ↑

· To ensure safe, stable boreholes, which is accomplishel acceptable mud-weight window   
·To achieve high rates of penetration so that rig time and wellcost can be minimized4048.github.io

These|primary considerations do not include well productivity concerns. A growing recognition of the importance of drilling-induced formation damage has|led|to the use of drill-in fluids (fluids used to drill through the pay zone) that minimize formation damage. This page discusses the formation damage that may be associated with various types of drilling fluids.

Center word: drilling

$$
K = 5
$$

$$
i t e r = 1
$$

$$
i t e r = 2
$$

$$
i t e r = 3
$$

$$
i t e r = 4
$$

Current context word: engineer

$$
p \big (D = 1 | w _ {d r i l l i n g}, c _ {e n g i n e e r} \big)
$$

$$
p (D = 1 | w _ {d r i l l i n g}, c _ {m i n i m i z e d})
$$

$$
p (D = 1 | w _ {d r i l l i n g}, c _ {p r i m a r y})
$$

$$
p (D = 1 | w _ {d r i l l i n g}, c _ {c o n c e r n s})
$$

$$
p (D = 1 | w _ {d r i l l i n g}, c _ {l e d})
$$

$$
p \big (D = 1 \big | w _ {d r i l l i n g}, c _ {p a g e} \big)
$$

![](images/5e82e07ca8386d58520dc1e70654ee823bcdc25058d71cf08f1cf4bb74867a81.jpg)

![](images/5f3ce3d21b523b9bc4ef3203e709efdec320f1f85c7a352478ce78747f3b8734.jpg)

![](images/f83520387a503709f8bde360a6e920ff5aa96ee633fe96229de5e308b8994035.jpg)

# Attention

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. Advances in neural information processing systems, 30.

Google citation: 172734

![](images/5cc397280922a0cb42fbc5339fbbaf6e51cf125e625771b1f108d29ecbd78976.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["INPUT\nJe suis étudiant"] --> B["THE TRANSFORMER"]
    B --> C["OUTPUT\nI am a student"]
```
</details>

![](images/2d885df858562e62a795fbb42a0714c21a443aed394ae77ee55e7369dbfc7168.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["INPUT: Je suis étudiant"] --> B["THE TRANSFORMER"]
    B --> C["OUTPUT: I am a student"]
    B --> D["OUTPUT: I am a student"]
    D --> E["ENCODERS"]
    E --> F["DECODERS"]
    F --> G["INPUT: Je suis étudiant"]
```
</details>

![](images/63361153182bd0f44462b2d517a6bbf234398311571322ebbcfe369183bbead0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["INPUT"] --> B["Je suis étudiant"]
    B --> C["ENCODER"]
    C --> D["ENCODER"]
    D --> E["ENCODER"]
    E --> F["ENCODER"]
    F --> G["ENCODER"]
    G --> H["ENCODER"]
    H --> I["ENCODER"]
    I --> J["ENCODER"]
    J --> K["ENCODER"]
    K --> L["ENCODER"]
    L --> M["ENCODER"]
    M --> N["ENCODER"]
    N --> O["ENCODER"]
    O --> P["ENCODER"]
    P --> Q["ENCODER"]
    Q --> R["ENCODER"]
    R --> S["ENCODER"]
    S --> T["ENCODER"]
    T --> U["ENCODER"]
    U --> V["ENCODER"]
    V --> W["ENCODER"]
    W --> X["ENCODER"]
    X --> Y["ENCODER"]
    Y --> Z["ENCODER"]
    Z --> AA["ENCODER"]
    AA --> AB["ENCODER"]
    AB --> AC["ENCODER"]
    AC --> AD["ENCODER"]
    AD --> AE["ENCODER"]
    AE --> AF["ENCODER"]
    AF --> AG["ENCODER"]
    AG --> AH["ENCODER"]
    AH --> AI["ENCODER"]
    AI --> AJ["ENCODER"]
    AJ --> AK["ENCODER"]
    AK --> AL["ENCODER"]
    AL --> AM["ENCODER"]
    AM --> AN["ENCODER"]
    AN --> AO["ENCODER"]
    AO --> AP["ENCODER"]
    AP --> AQ["ENCODER"]
    AQ --> AR["ENCODER"]
    AR --> AS["ENCODER"]
    AS --> AT["ENCODER"]
    AT --> AU["ENCODER"]
    AU --> AV["ENCODER"]
    AV --> AW["ENCODER"]
    AW --> AX["ENCODER"]
    AX --> AY["ENCODER"]
    AY --> AZ["ENCODER"]
    AZ --> BA["ENCODER"]
    BA --> BB["ENCODER"]
    BB --> BC["ENCODER"]
    BC --> BD["ENCODER"]
    BD --> BE["ENCODER"]
    BE --> BF["ENCODER"]
    BF --> BG["ENCODER"]
    BG --> BH["ENCODER"]
    BH --> BI["ENCODER"]
    BI --> BJ["ENCODER"]
    BJ --> BK["ENCODER"]
    BK --> BL["ENCODER"]
    BL --> BM["ENCODER"]
    BM --> BN["ENCODER"]
    BN --> BO["ENCODER"]
    BO --> BP["ENCODER"]
    BP --> BQ["ENCODER"]
    BQ --> BR["ENCODER"]
    BR --> BS["ENCODER"]
    BS --> BT["ENCODER"]
    BT --> BU["ENCODER"]
    BU --> BV["ENCODER"]
    BV --> BW["ENCODER"]
    BW --> BX["ENCODER"]
    BX --> BY["ENCODER"]
    BY --> BZ["ENCODER"]
    BZ --> CA["ENCODER"]
    CA --> CB["ENCODER"]
    CB --> CC["ENCODER"]
    CC --> CD["ENCODER"]
    CD --> CE["ENCODER"]
    CE --> CF["ENCODER"]
    CF --> CG["ENCODER"]
    CG --> CH["ENCODER"]
    CH --> CI["ENCODER"]
    CI --> CJ["ENCODER"]
    CJ --> CK["ENCODER"]
    CK --> CR["ENCODER"]
    CR --> CS["ENCODER"]
    CS --> CT["ENCODER"]
    CT --> CU["ENCODER"]
    CU --> CV["ENCODER"]
    CV --> CW["ENCODER"]
    CW --> CX["ENCODER"]
    CX --> CY["ENCODER"]
    CY --> CZ["ENCODER"]
    CZ --> DA["ENCODER"]
    DA --> DB["ENCODER"]
    DB --> DC["ENCODER"]
    DC --> DD["ENCODER"]
    DD --> DE["ENCODER"]
    DE --> DF["ENCODER"]
    DF --> DG["ENCODER"]
    DG --> DH["ENCODER"]
    DH --> DI["ENCODER"]
    DI --> DJ["ENCODER"]
    DJ --> DK["ENCODER"]
    DK --> DL["ENCODER"]
    DL --> DV["ENCODER"]
    DV --> DW["ENCODER"]
    DW --> DX["ENCODER"]
    DX --> DY["ENCODER"]
```
</details>

Encode the input information (obtain the embedding)   
Decode the information (predict words)

![](images/72ff70bb0682bed843ad2d558ae2ab20f7f0a3d1379bfbb0a88543ae95c025d4.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Input
        X1["x₁"] -->|0| N["N"]
        X2["x₂"] -->|0| N
        X3["..."] -->|...| N
        Xi["xᵢ"] -->|1| N
        XV["xᵥ"] -->|0| N
    end

    subgraph Hidden
        N -->|h₁, h₂, h₃| V["V="]
        V --> X
        X --> hN["hₙ"]
        H["Matrix W"] -->|Vector of word i| N
        hN -->|...| hN
        hN -->|...| hN
    end

    subgraph Context Matrix
        V --> V["V"]
        V --> Matrix_W'[Matrix W']
        Matrix_W' -->|Vector of word j| N["N="]
        N --> Output["Output softmax"]
    end

    style Hidden fill:#f9f,stroke:#333
    style Context Matrix fill:#bbf,stroke:#333
```
</details>

What are the disadvantages of MLP?

![](images/65a01325bba41cd4217a17864705dfa1d0f5fe42bf761770a2aab48fbad6d4fd.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["ENCODER"] --> B["Feed Forward Neural Network"]
    B --> C["Self-Attention"]
    C --> A
```
</details>

![](images/d60958284f8099ab2d7e3077e7086878ac069c13e1fe20eb87813a93d6d0c2c5.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["ENCODER"] --> B["Feed Forward"]
    A --> C["Self-Attention"]
    D["DECODER"] --> E["Feed Forward"]
    D --> F["Encoder-Decoder Attention"]
    D --> G["Self-Attention"]
    B <--> C
    E <--> F
    G <--> G
```
</details>

The additional attention layer is to help the model focuses on the right parts of the data!

![](images/52de8999067d331233783ea0d712ba83f7500ac865c24402686e8aae24c3193f.jpg)

<details>
<summary>text_image</summary>

original
</details>

![](images/60c210db87934c62162816ea5ccd6a49d0e0f39ee0c3d4b3e06ee71a6b87b7c5.jpg)

<details>
<summary>text_image</summary>

men
Fixation Length
High Low
</details>

![](images/9c55d74dbb06932329569af6bd1fb2208f01c1db1e7cd2eb254ea84b7d503e20.jpg)

<details>
<summary>text_image</summary>

women
Fixation Length
High
Low
</details>

source: https://packageinsight.com/the-importance-of-visual-attention/

![](images/b564d93e83a7d7a4174eb322e1552bafdeb695491e4168cb88b2020d6a3e9dc3.jpg)

<details>
<summary>text_image</summary>

Tel: 212-285-0668
錦江飯店
健康堂
喜運來大酒來
AHEAD
知乎 @赵强
</details>

![](images/6a037009d926b4f5b3338b0e62b4083d12095b73118c224aa47cb841a182783a.jpg)

<details>
<summary>text_image</summary>

Tel: 212-285-0668
錦江飯店
健康堂
喜運來大酒來
AHEAD
知乎 @赵强
</details>

![](images/0f8c72b769aff8db3b4a01ab4533930ebc09a892b7eb42ff52db0a88e8b76a4e.jpg)

<details>
<summary>text_image</summary>

Tel:212-285-0668
錦江飯店
健康堂
喜運來大酒來
AHEAD
優の良品
知乎 @赵强
</details>

![](images/07d520c3dba86fb9abccd0b8deb5608c570084388d20b2165d2738dd5c594734.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["ENCODER"] --> B["Feed Forward"]
    B --> C["Self-Attention"]
    C --> D["X1 Je"]
    C --> E["X2 suis"]
    C --> F["X3 étudiant"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#cfc,stroke:#333
    style D fill:#fcc,stroke:#333
    style E fill:#cff,stroke:#333
    style F fill:#ffc,stroke:#333
```
</details>

Conceptually, the attention layer will give some weights to the embedding of each word.

![](images/bd8dc544f449a28a4431e6258f85682d4dcc79c4161749a28713a44b4c509221.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph Self_Attention
        X1["X1"] --> Z1["Z1"]
        X2["X2"] --> Z2["Z2"]
    end

    subgraph Machine
        X1 --> Z1
        X2 --> Z2
    end

    R1["r1"] --> Feed_Neural_Network["Feed Forward Neural Network"]
    R2["r2"] --> Feed_Neural_Network
    style Self_Attention fill:#f9f9f9,stroke:#333
    style Machine fill:#f9f9f9,stroke:#333
```
</details>

The word at each position passes through a self-attention process. Then, they each pass through a feed-forward neural network -- the exact same network with each vector flowing through it separately.

# Consider translating the following sentence:

“The animal didn't cross the street because it was too tired”

# Question: What does the word “it” refer to?

The context is very important!!!

![](images/37a7e66c1db724099e41dadc8a3e07a5bb2863cfb0f6eb6a44e4f2921374348f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["The"] --> B["animal"]
    A --> C["didn"]
    A --> D["'_"]
    A --> E["t_"] 
    A --> F["cross"]
    A --> G["the"]
    A --> H["street"]
    A --> I["because"]
    A --> J["it_"] 
    A --> K["was_"] 
    A --> L["too_"] 
    A --> M["tire"]
    A --> N["d_"] 
    O["The"] --> P["animal"]
    O --> Q["didn"]
    O --> R["'_"]
    O --> S["t_"] 
    O --> T["cross"]
    O --> U["the"]
    O --> V["street"]
    O --> W["because"]
    O --> X["it_"] 
    O --> Y["was_"] 
    O --> Z["too_"] 
    O --> AA["tire"]
    O --> AB["d_"] 
    AC["Attention: Input - Input"] --> AD
    AD --> AE
    AE --> AF
    AF --> AG
    AG --> AH
    AH --> AI
    AI --> AJ
    AJ --> AK
    AK --> AL
    AL --> AM
    AM --> AN
    AN --> AO
    AO --> AP
    AP --> AQ
    AQ --> AR
    AR --> AS
    AS --> AT
    AT --> AU
    AU --> AV
    AV --> AW
    AW --> AX
    AX --> AY
    style A fill:#f9f,stroke:#333
    style AG fill:#ccf,stroke:#333
    style AH fill:#cfc,stroke:#333
```
</details>

![](images/a348d784d85c339ce1b919089c85cc505e165d74e94fae87ec80d721a37bc93c.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["The"] --> B["animal"]
    A --> C["didn"]
    A --> D["'-"]
    A --> E["t_"]
    A --> F["cross"]
    A --> G["the"]
    A --> H["street"]
    A --> I["because"]
    I --> J["it"]
    I --> K["was"]
    I --> L["too"]
    I --> M["tire"]
    I --> N["d_"]
    O["The"] --> P["animal"]
    O --> Q["didn"]
    O --> R["'-"]
    O --> S["t_"]
    O --> T["cross"]
    O --> U["the"]
    O --> V["street"]
    O --> W["because"]
    W --> X["it"]
    W --> Y["was"]
    W --> Z["too"]
    W --> AA["tire"]
    W --> AB["d_"]
```
</details>

Self-attention

![](images/11f3096bc80859acd882564f5eeb8b0f4fdefcd1146d4e71903bbc8ed49fd92f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph_LSTM_Memory_Cell["LSTM Memory Cell"]
        A["Forget gate"] --> B["σ"]
        C["Input gate"] --> D["σ"]
        E["tanh"] --> F["σ"]
        G["tanh"] --> H["×"]
        I["×"] --> J["×"]
        K["+"] --> L["+"]
    end
    subgraph_Output_Gage["Output gate"]
        M["tanh"] --> N["×"]
        O["σ"] --> P["×"]
        Q["h_t"] --> R["ht"]
        S["h_t-1"] --> T["x_t"]
    end
    style LSTM_Memory_Cell fill:#f9f,stroke:#333
    style Output_Gage fill:#ccf,stroke:#333
    style Output_Gage fill:#cfc,stroke:#333
```
</details>

LSTM

![](images/8aa7135c96cefb1eb2738ed60a8692fcb15435e00e8e61de42a506f34c8cf995.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph_Encoder_1["ENCODER #1"]
        A["Feed Forward Neural Network"] --> B["Self-Attention"]
        C["Feed Forward Neural Network"] --> B
        D["z1"] --> B
        E["z2"] --> B
    end
    subgraph_Encoder_2["ENCODER #2"]
        F["r1"] --> G["Self-Attention"]
        H["r2"] --> I["Machines"]
    end
    J["x1"] --> K["Thinking"]
    L["x2"] --> M["Machines"]
    style Encoder_1 fill:#f9f,stroke:#333
    style Encoder_2 fill:#bbf,stroke:#333
```
</details>

Step 1: Given the embedding x, we will compute the Query vector, the Key vector, and the Value vector.

How to create Q, K, V?

These vectors are created by multiplying the embedding by three matrices that we trained during the training process.

Input

Embedding

Queries

Keys

Values

![](images/0b7d51ca7577d8adc4c010e8042263152333c8499cd5786d971102d3bc7c5225.jpg)

![](images/9bf26bbf2512f4b3c069b8fc3b8ed1e1c650fda19038fb6ecc601cd2ba55fd2f.jpg)

![](images/72f42c852bdd16d2ae5cb137495e0803a9f816056a557b4e6ae3056489690e39.jpg)

![](images/d6a8fe14c2919a69af1488dcd26d945c4fd2cd08f107fdc689631092b1660e87.jpg)

Machines

![](images/f266159eda05b91803ecebd6d5d174b42a2582aaf1cc27f24b61ff197779413a.jpg)

![](images/7f3c4a666c398fbb1470e4c8ed88530940f903f1d3819cc0296c03ce7ea26de3.jpg)

![](images/a44a8e06b40d40cde053189b06e1ddee4ec38650321ed641d0cb7b02cc5ccbfb.jpg)

![](images/0c682242396ee31aa33c41b63e6da8c804f42b6b4221a4c6a90560e866fbf4d4.jpg)

(Dimension 64)

![](images/d49b9b051efe5785e80eb5fffb8394ae00dfc4f80b6b85e282f4c87f34a4cf27.jpg)

<details>
<summary>natural_image</summary>

Grid pattern with 10 cells in light gray and 3 cells in light purple, no text or symbols present
</details>

WQ

![](images/c30ce0afab0a34343ad39451f3a2834cdd6268b1cf6352ab6c4ab2195980e95b.jpg)

<details>
<summary>natural_image</summary>

Grid pattern with 10 squares in orange border, no text or symbols present
</details>

![](images/1652befd8b1da2ef8a38fb5a18dfd779c00fa940eadf502a0c89acc308f25432.jpg)

<details>
<summary>natural_image</summary>

Grid pattern with 10 squares in light blue, no text or symbols present
</details>

Step 2: The score is calculated by taking the dot product of the query vector with the key vector of the respective word we’re scoring.

Input

Embedding

Queries

Keys

Values

Score

![](images/ef65a83f9445335bac450d3c963bae57dd6caf9c5a5b3cfb8f94360be5c1772e.jpg)

$\mathsf { q } _ { 1 }$

![](images/74844cebbaacd5987c23e347ce41f9e36b381ff92db5719276db252d371e2a8f.jpg)

$\cdot$

![](images/700e8ea2eb6bcafc6e6d3b16ef08d9811e2375a478e4042ce5f346ca1bde6c59.jpg)

$\boldsymbol { \mathsf { v } } _ { 1 }$

![](images/2a0e5b634324e6f5c56044835bc69274e1c1d175d343a6b535b2879e5f1cb0e4.jpg)

$$
\mathbf {q} _ {1} \cdot \mathbf {k} _ {1} = 1 1 2
$$

![](images/f925751d1ea3c989f931b81d3d8e4e2de29f56d0da8e058dac4d73bcfedbf299.jpg)

$\mathbf { q } _ { 2 }$

![](images/ce3099396f070c641d97431a33c961f07f4f8588ad733f7078611ed00f25d84f.jpg)

${ \bf k } _ { 2 }$

![](images/ae7e4cc666e1f898e04cc42f2f08d3bd0b8a3f88c6777cd50758d0bc71035ba0.jpg)

$\mathsf { v } _ { 2 }$

![](images/7b6e61e694d91387a77b59269c1fca1008b68310a3581ee1a34ac9b80ac0914c.jpg)

$$
\mathbf {q} _ {1} \cdot \mathbf {k} _ {2} = 9 6
$$

Step 3: normalize the score by $\sqrt { d _ { k } }$ , where $\sqrt { d _ { k } }$ is the dimension of the key vector.

Input

Embedding

Queries

Keys

Values

Score

Divide by $8 ( \sqrt { d _ { k } } )$

Softmax

![](images/15ac3d53dab18c4b377f51a0c6484b064760e03829056d16759fbdaa9a9e2462.jpg)

![](images/196f5a8b3271429e1b2d4df596ba47bc2130ba3a3904f1d0c4a1aea5818af609.jpg)

![](images/cd40ea6c7548d4b0718e851881cd786860eeeb428c7154f4fa1ff36e7ae8233b.jpg)

![](images/9395bfe88af41f903814712f284d737e2d3f3b47ea9a911f961618e4acd1f927.jpg)

$$
\mathbf {q} _ {1} \cdot \mathbf {k} _ {1} = 1 1 2
$$

![](images/0d6c828f606a04823f31f5e142097dfc437fd68dd2a2108fdc6974160afdb1ce.jpg)

![](images/eccfe53e213e43ba10d8e60cf0bdb37c461f056846be98f441b5b36c32472622.jpg)

![](images/5eb145751bc57b369eaab1b03ffd4499333e345968a337e27d24bb6f460b9eae.jpg)

![](images/ae67cc504426cd263868af05e6d6d8106a77dec5c4d54910a3c26ae1b7ecb768.jpg)

$$
\mathbf {q} _ {1} \cdot \mathbf {k} _ {2} = 9 6
$$

Step 4: Further normalize the score by softmax.   
![](images/e216849d330ebae936c71ea0967c39dbaf2d7d29d052555abc481f445791ea4e.jpg)

Step 5: Multiply each value vector by the softmax score (in preparation to sum them up).

![](images/faab845146a1158ff1b7329d0964cdd0111b19cb9dc057502295335bd1aa87c8.jpg)

<details>
<summary>bar</summary>

| Input        | Thinking | Machines |
| ------------ | -------- | -------- |
| Embedding    | x₁       | x₂       |
| Queries      | q₁       | q₂       |
| Keys         | k₁       | k₂       |
| Values       | v₁       | v₂       |
| Score        | q₁ • k₁ = 112 | q₁ • k₂ = 96 |
| Divide by 8 (√dk) | 14     | 12       |
| Softmax      | 0.88     | 0.12     |
| Softmax X Value | v₁     | v₂      |
| Sum          | z₁       | z₂      |
</details>

Step 6: Sum up the weighted value vectors. This produces the output of the self-attention layer at this position (for the first word).

![](images/7afad584c9d3ae5c989a8624ec11d899939e85d5097b760bd3a5d82f10affae2.jpg)

<details>
<summary>bar</summary>

| Input        | Thinking | Machines |
| ------------ | -------- | -------- |
| Embedding    | x₁       | x₂       |
| Queries      | q₁       | q₂       |
| Keys         | k₁       | k₂       |
| Values       | v₁       | v₂       |
| Score        | q₁ • k₁ = 112 | q₁ • k₂ = 96 |
| Divide by 8 (√dk) | 14     | 12       |
| Softmax      | 0.88     | 0.12     |
| Softmax X Value | v₁     | v₂      |
| Sum          | z₁       | z₂      |
</details>

Create the Q, K, V: Every row in the X matrix corresponds to a word in the input sentence. Here, $W ^ { Q } , W ^ { K } , W ^ { V }$ are trained parameters.

![](images/a1f365797ce9defc6d578482dcac2bc570140e6f008a8dab7f889809bc7e6140.jpg)

![](images/7f15c397ff42468629120a0ffbca1e2b54d2a1ddff53f479f4b13ce92a24530a.jpg)

<details>
<summary>text_image</summary>

softmax( Q × K^T ) V
√d_k
</details>

![](images/9ef14a7922f9554c4f120c3955c2f9aa99a77b536cab660feb5f03f37e6fad1e.jpg)

<details>
<summary>text_image</summary>

= \n\nZ
</details>

![](images/df8eaf5f8ccf3c1f249ad2847025d8898756157f914daabfe9d0d2043832380d.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["MatMul"] --> B["SoftMax"]
    B --> C["Mask (opt.)"]
    C --> D["Scale"]
    D --> E["MatMul"]
    E --> F["Q"]
    E --> G["K"]
    E --> H["V"]
    A --> I["Upward arrows"]
    I --> A
```
</details>

# Attention Animation

https://www.bilibili.com/video/BV1dt4y1J7ov/?spm\_id\_from=333.337.search-

card.all.click&vd\_source=cc88065420e6f003010306f4a620f7f3

# Attention in Neural Networks

https://www.youtube.com/watch?v=W2rWgXJBZhU

# Attention Mechanism In a nutshell

https://www.youtube.com/watch?v=oMeIDqRguLY

# The math behind Attention: Keys, Queries, and Values matrices

https://www.youtube.com/watch?v=UPtG\_38Oq8o

# Transformer

X   
![](images/ac1a39f3f71c95ddc3adc6b80403576415fdd2aa377bdfdfa5ba39e0078aaa06.jpg)  
ATTENTION HEAD #0

![](images/57720157e6e41779881ae7ea860434d70ee65e4092a04bf5506215a7e128c0a7.jpg)

![](images/f5674382f389dbdd82d18839e13f251ce2732bc07681b54deedf5273910457df.jpg)  
WoQ

![](images/3f309490cda9a489b500f126e9cc839efc6b5c0f54de417dd1e4bbb8de392551.jpg)

![](images/728f5384356facd86c897ee1dde065d19329f72b584cf3998d29de18ca72d257.jpg)

![](images/4f99060641c57e28bcb4e8025eab7d05cb82b80fe65cfb1d43884a7d42a54700.jpg)

![](images/f0dcc06c33347cdace31206fc8c1e5164e5b09826b48abc133842a707fc0fc40.jpg)

ATTENTION HEAD #1   
![](images/3955e420f16e32dd32424a83e6540b7b750f553925ae80136f43ebcbb4aec234.jpg)

![](images/5720118746c2f7d82a48426b6d770ca7bdbd5391c9a8e4478b16dcd1322f182f.jpg)

![](images/d83123cc80e97ef65470cfb85924ff6b52b07110c960fc65fd1a00c2a1924a7f.jpg)

![](images/92ee01a700128982c6c5bd76a78a5602cf3d9d68ac18a598fe62cea1049c3c3d.jpg)

![](images/b40161dfe199d9fb29315e6e8778707b8bf589f4d6035afdfd401c80232d9b72.jpg)

![](images/f01f956ba262404453164bdfc1d7688487b34320fbb7a7b9111c634537ed0cf7.jpg)

# Motivations:

1. Increase capability for focusing on different positions of the input sequence data.   
2. Increase the representation power of the value vectors.

![](images/c64634a29f2e7216658de43b723410005b3b0a66daa816e05fb00388cb8fad2b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["X"] --> B["Thinking Machines"]
    B --> C["Calculating attention separately in eight different attention heads"]
    D["ATTENTION HEAD #0"] --> E["Z₀"]
    F["ATTENTION HEAD #1"] --> G["Z₁"]
    H["ATTENTION HEAD #7"] --> I["Z₇"]
```
</details>

1) Concatenate all the attention heads

![](images/e543edfa4cef36a9b57d3959ea4d64a79c7bfa96c0f69705f2faf359c65f9681.jpg)

<details>
<summary>text_image</summary>

Z₀ Z₁ Z₂ Z₃ Z₄ Z₅ Z₆ Z₇
</details>

2) Multiply with a weight matrix W° that was trained jointly with the model

X

3) The result would be the Z matrix that captures information from all the attention heads.We can send this forward to the FFNN

![](images/b2d5abafae884c1bf1b17b42cde024fc57539874c215d004870be0c246353632.jpg)

<details>
<summary>text_image</summary>

= \n\nZ
</details>

![](images/53b05312bba3b7ee53a7ca5ed448148c03576ceb36768fb898a778786c278598.jpg)

<details>
<summary>text_image</summary>

W°
</details>

1) This is our input sentence\*

2) We embed each word\*

3) Split into 8 heads. We multiply X or R with weight matrices

4) Calculate attention using the resulting Q/K/V matrices

5) Concatenate the resulting Z matrices, then multiply with weight matrix W to produce the output of the layer

![](images/b88d87695fb999a51486f0151f44c115a5180b9eb9d9b13e66ce58aa8b7a2ccc.jpg)

\* In all encoders other than #0, we don't need embedding. We start directly with the output of the encoder right below this one

![](images/f31b25a9b416330c05f2cf6b67fd28e91a5a62c18aa47c59f48dd38afc90bd12.jpg)

![](images/84b047c860e20e3967c931b4df2a75f37757360135baa219e1204642b454ede3.jpg)

<details>
<summary>text_image</summary>

W₀^Q
W₀^K
W₀^V
</details>

![](images/07fa723989e3d6e36ddfdff13aaa81559642c13fc5224b5a5bc99850c707c1cb.jpg)

<details>
<summary>text_image</summary>

Q₀
K₀
V₀
</details>

![](images/79f808accd3c56d6582aefc511df5636ffa818cb0a7cef75e4c62842db190dbf.jpg)

![](images/f13a693b46ff7c51784db5bb5ad103c5aa371a4ce89b0eca7484ec13d5683103.jpg)

<details>
<summary>text_image</summary>

W₁^Q
W₁^K
W₁^V
</details>

![](images/95ba6f03150e7bee4b3c1b60d424e1165665552cc83379c5db940b072dfacc13.jpg)

![](images/c1af66c69d9313534a5966c0f1bd8b9ed21a6545d7157cce6e6706e26af6257d.jpg)

![](images/c95410d3a923031f3255590b71d0d9690dcf54ee3dfd13331992cc7a0499ee7a.jpg)

<details>
<summary>text_image</summary>

W7^Q
W7^K
W7^V
</details>

![](images/5d5794e46762b9fc1f6364493996a7cca142ede3360d18ccc9830f160864a4cb.jpg)

<details>
<summary>text_image</summary>

Q7
K7
V7
</details>

![](images/c0d4c0c25e8044d0a83c1d5b324df949cb1959ce5d7fb10b4a8a7a4c74a85f7d.jpg)

![](images/bcc3ba8832ca8fba88f0be87f88eecfb537d4cd7050ee30d61f94b4ece45641e.jpg)

<details>
<summary>text_image</summary>

W°
</details>

![](images/dc20ac12c28bd24c371bf84673e127e9f845c7a366b42364c79b44c21e3ed238.jpg)

![](images/e1771ad73c1da493feaf7ac692d4f23c359f925062320511a1864b6541180a7a.jpg)

<details>
<summary>tree</summary>

| Part       | Value |
| ---------- | ----- |
| The_       | 1     |
| animal_    | 1     |
| didn_      | 1     |
| _          | 1     |
| t_         | 1     |
| cross_     | 1     |
| the_       | 1     |
| street_    | 1     |
| because_   | 1     |
| it_        | 1     |
| was_       | 1     |
| too_       | 1     |
| tire       | 1     |
| d_         | 1     |
</details>

![](images/8451cba9ab127de9da6fbeebe151328db9e16772e5536fa103516b52f2dd3a94.jpg)

<details>
<summary>other</summary>

| Input Type | Attention Direction |
| ---------- | ------------------- |
| The        | 100                 |
| animal     | 80                  |
| didn       | 70                  |
| '          | 60                  |
| t          | 50                  |
| cross      | 40                  |
| the        | 30                  |
| street     | 20                  |
| because    | 10                  |
| it         | 5                   |
| was        | 3                   |
| too        | 2                   |
| tire       | 1                   |
| d          | 0                   |
</details>

Challenges: Difficult to explain if we put all of them together!!! Position information is not really embedded.

![](images/eea0b6098c30546cf684fc27d6a6a039c5d5e91bc455f4fe4816bd19995bea94.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["ENCODER #0"] --> B["DECODER #0"]
    C["ENCODER #1"] --> D["DECODER #1"]
    E["EMBEDDINGS"] --> F["POSITIONAL ENCOING"]
    G["Embedding WITH TIME SIGNAL"] --> H["X1 = Je"]
    I["Positional ENCOING"] --> J["t1 + suis"]
    K["Embeddings"] --> L["X1 + étudiant"]
    style A fill:#e6f3ff,stroke:#333
    style C fill:#e6f3ff,stroke:#333
    style E fill:#e6f3ff,stroke:#333
    style G fill:#e6f3ff,stroke:#333
    style B fill:#e6f3ff,stroke:#333
    style D fill:#e6f3ff,stroke:#333
    style F fill:#e6f3ff,stroke:#333
    style J fill:#e6f3ff,stroke:#333
    style L fill:#e6f3ff,stroke:#333
```
</details>

Idea: Create an additional vector with the same dimension which helps it determine the position of each word or the distance between different words in the sequence.

POSITIONAL ENCODING

EMBEDDINGS

INPUT

![](images/cf06458250ab334e256de833e1a963984516aadaed60060ef5dc670c6b25f6fe.jpg)

<details>
<summary>text_image</summary>

0 0 1 1
</details>

+   
![](images/14b4974793df29eacdd1b0910e2ac4ed342f920f48ac91c5c528b97ec884dca5.jpg)

![](images/8c8a81c8c5e7c687c4ae417b6280c8bd8c3c30b4d2c32374ac0fc7f575b4658c.jpg)

<details>
<summary>heatmap</summary>

| Value | Color |
|---|---|
| 0.84 | Green |
| 0.0001 | Teal |
| 0.54 | Green |
| 1 | Yellow |
</details>

+   
![](images/2b23d555640f1e3528854cf7c5318c3eac5a21e767a1a52046f05d5f3e8c7384.jpg)

![](images/ee2eca0a3729ce60eb936066010804a737006229fc19c99d13d650e7cfd710c1.jpg)

<details>
<summary>heatmap</summary>

| Value |
|---|
| 0.91 |
| 0.0002 |
| -0.42 |
| 1 |
</details>

+   
![](images/0a8a3551152ea53f1e8b8907eef7dc398713de00e2650c8241f850fea9e4e70c.jpg)

Let t be the desired position in an input sentence, $\vec { p _ { t } } \in \mathbb { R } ^ { d }$ corresponding encoding, and d be the encoding dimension (where $d \equiv _ { 2 } 0 )$ Then $f : \mathbb { N } \to \mathbb { R } ^ { d }$ will be te function that produces the output vector $\xrightarrow [ { p _ { t } ^ { \prime } } ] { }$ and it is defined as follows:

$$
\overrightarrow {p _ {t}} ^ {(i)} = f (t) ^ {(i)} := \left\{ \begin{array}{l l} \sin (\omega_ {k}. t), & \text { if } i = 2 k \\ \cos (\omega_ {k}. t), & \text { if } i = 2 k + 1 \end{array} \right.
$$

where

$$
\omega_ {k} = \frac {1}{1 0 0 0 0 ^ {2 k / d}}
$$

![](images/6253723a06e5c244be4b98f98c9efe1043e7eb9ef6b28defa752b06d537b8d36.jpg)

<details>
<summary>heatmap</summary>

| Depth | Position | Value  |
|-------|----------|--------|
| 0     | 0        | 1.00   |
| 0     | 10       | 0.75   |
| 0     | 20       | 0.50   |
| 0     | 30       | 0.25   |
| 0     | 40       | 0.00   |
| 0     | 50       | -0.25  |
| 10    | 0        | 0.75   |
| 10    | 10       | 0.50   |
| 10    | 20       | 0.25   |
| 10    | 30       | 0.00   |
| 10    | 40       | -0.25  |
| 10    | 50       | -1.00  |
| 20    | 0        | 0.75   |
| 20    | 10       | 0.50   |
| 20    | 20       | 0.25   |
| 20    | 30       | 0.00   |
| 20    | 40       | -0.25  |
| 20    | 50       | -1.00  |
| 30    | 0        | 0.75   |
| 30    | 10       | 0.50   |
| 30    | 20       | 0.25   |
| 30    | 30       | 0.00   |
| 30    | 40       | -0.25  |
| 30    | 50       | -1.00  |
| 40    | 0        | 0.75   |
| 40    | 10       | 0.50   |
| 40    | 20       | 0.25   |
| 40    | 30       | 0.00   |
| 40    | 40       | -0.25  |
| 40    | 50       | -1.00  |
| 50    | 0        | 0.75   |
| 50    | 10       | 0.50   |
| 50    | 20       | 0.25   |
| 50    | 30       | 0.00   |
| 50    | 40       | -0.25  |
| 50    | 50       | -1.00  |
| 60    | 0        | 0.75   |
| 60    | 10       | 0.50   |
| 60    | 20       | 0.25   |
| 60    | 30       | 0.00   |
| 60    | 40       | -0.25  |
| 60    | 50       | -1.00  |
| 70    | 0        | 0.75   |
| 70    | 10       | 0.50   |
| 70    | 20       | 0.25   |
| 70    | 30       | 0.00   |
| 70    | 40       | -0.25  |
| 70    | 50       | -1.00  |
| 80    | 0        | 0.75   |
| 80    | 10       | 0.50   |
| 80    | 20       | 0.25   |
| 80    | 30       | 0.00   |
| 80    | 40       | -0.25  |
| 80    | 50       | -1.00  |
| 90    | 0        | 0.75   |
| 90    | 10       | 0.50   |
| 90    | 20       | 0.25   |
| 90    | 30       | 0.00   |
| 90    | 40       | -0.25  |
| 90    | 50       | -1.00  |
| 100   | 0        | 0.75   |
| 100   | 10       | 0.50   |
| 100   | 20       | 0.25   |
| 100   | 30       | 0.00   |
| 100   | 40       | -0.25  |
| 100   | 50       | -1.00  |
| 110   | 0        | 0.75   |
| 110   | 10       | 0.50   |
| 110   | 20       | 0.25   |
| 110   | 30       | 0.00   |
| 110   | 40       | -0.25  |
| 110   | 50       | -1.00  |
| 120   | 0        | 0.75   |
| 120   | 10       | 0.50   |
| 120   | 20       | 0.25   |
| 120   | 30       | -1.75   |
|          |          |         |
</details>

![](images/07c41fc2247278cac69303b72a973c8e8da91775a7935ff3e9f6efedb8f2c13f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Encoder #1"] --> B["Add & Normalize"]
    A --> C["Feed Forward"]
    A --> D["Add & Normalize"]
    A --> E["Self-Attention"]
    B --> F["Positional Encoding"]
    C --> G["Residual connection"]
    D --> H["Thinking"]
    E --> I["Machines"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#cfc,stroke:#333
    style D fill:#fcc,stroke:#333
    style E fill:#cff,stroke:#333
    style F fill:#ffc,stroke:#333
    style G fill:#cfc,stroke:#333
    style H fill:#cfc,stroke:#333
```
</details>

![](images/0ab95449d8c3edefe05f4bb3e1b41654b4af3cc61554b9973b1e2f5acbb25dd3.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Add & Normalize"] --> B["Feed Forward"]
    B --> C["Z1"]
    B --> D["Z2"]
    C --> E["LayerNorm( X + Z ) "]
    D --> F["Self-Attention"]
    E --> G["POSitional Encoding"]
    F --> H["Thinking"]
    F --> I["Machines"]
    J["ENCODER #1"] --> K["Input: x1, x2"]
    style A fill:#d4edda,stroke:#000
    style B fill:#d4edda,stroke:#000
    style C fill:#d4edda,stroke:#000
    style D fill:#d4edda,stroke:#000
    style E fill:#d4edda,stroke:#000
    style F fill:#d4edda,stroke:#000
    style G fill:#d4edda,stroke:#000
    style H fill:#d4edda,stroke:#000
    style I fill:#d4edda,stroke:#000
```
</details>

![](images/dddb83fbc34a0d93bd2d2f6ba35763ec2def2127faa826883879c206f75ddf4a.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph_Encoder_1["ENCODER #1"]
        A["Add & Normalize"] --> B["Self-Attention"]
        C["Add & Normalize"] --> D["Feed Forward"]
        E["Add & Normalize"] --> F["Feed Forward"]
        G["Add & Normalize"] --> H["Feed Forward"]
        I["Add & Normalize"] --> J["Feed Forward"]
        K["Add & Normalize"] --> L["Feed Forward"]
        M["Add & Normalize"] --> N["Feed Forward"]
        O["Add & Normalize"] --> P["Feed Forward"]
        Q["Add & Normalize"] --> R["Feed Forward"]
        S["Add & Normalize"] --> T["Feed Forward"]
        U["Add & Normalize"] --> V["Feed Forward"]
        W["Add & Normalize"] --> X["Feed Forward"]
        Y["Add & Normalize"] --> Z["Feed Forward"]
        AA["Add & Normalize"] --> AB["Feed Forward"]
        AC["Add & Normalize"] --> AD["Feed Forward"]
        AE["Add & Normalize"] --> AF["Feed Forward"]
        AG["Add & Normalize"] --> AH["Feed Forward"]
        AI["Add & Normalize"] --> AJ["Feed Forward"]
        AK["Add & Normalize"] --> AL["Feed Forward"]
        AM["Add & Normalize"] --> AN["Feed Forward"]
        AO["Add & Normalize"] --> AP["Feed Forward"]
        AQ["Add & Normalize"] --> AR["Feed Forward"]
        AS["Add & Normalize"] --> AT["Feed Forward"]
        AU["Add & Normalize"] --> AV["Feed Forward"]
        AW["Add & Normalize"] --> AX["Feed Forward"]
        AY["Softmax"] --> AZ["Linear"]
        BA["DECODER #2"] --> BB["Decoder #1"]
    end

    subgraph_Encoder_2["ENCODER #2"]
        B --> AC
        D --> AE
        F --> AG
        H --> AI
        J --> AQ
        AL --> AM
    end

    subgraph_Decoder_1["DECODER #1"]
        B --> AA
        D --> AB
        E --> AC
        F --> AD
        G --> AE
        H --> AF
        I --> AG
        J --> AH
        K --> AI
        AA --> AJ
        AB --> AK
        AC --> AL
        AD --> AM
        AE --> AN
        AF --> AO
        AG --> AP
        AH --> AQ
        AI --> AQ
        AJ --> AQ
        AK --> AQ
    end

    style Encoder_1 fill:#f9f,stroke:#333
    style Decoder_1 fill:#bbf,stroke:#333
    style Encoder_2 fill:#dfd,stroke:#333
    style Decoder_2 fill:#dfd,stroke:#333
```
</details>

Decoding time step:①2 3 4 5 6

OUTPUT

![](images/f2708e05fbfd1b939d4042dc782994c1ace698186ae8abffa2c4c30e7613fd54.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["INPUT"] --> B["EMBEDDING WITH TIME SIGNAL"]
    A --> C["EMBEDDINGS"]
    C --> D["ENCODER"]
    D --> E["DECODER"]
    E --> F["Linear + Softmax"]
    F --> G["ENCODER"]
    G --> H["DECODER"]
    H --> I["DECODER"]
    I --> J["Linear + Softmax"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#ccf,stroke:#333
    style D fill:#cfc,stroke:#333
    style E fill:#cfc,stroke:#333
    style F fill:#fcc,stroke:#333
    style G fill:#fcc,stroke:#333
    style H fill:#fcc,stroke:#333
    style I fill:#fcc,stroke:#333
    style J fill:#fcc,stroke:#333
```
</details>

Decoding time step: 1②3 4 5 6

OUTPUT

![](images/335e7052ab9970bf1377bd1fad42a20e0e8bcff6e5d5af127f48ec145a79fb9f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input"] --> B["Je"]
    A --> C["suis"]
    A --> D["étudiant"]
    E["EMBEDDING WITH TIME SIGNAL"] --> F["ENCODERS"]
    G["Previous OUTPUTS"] --> H["DECODERS"]
    I["Linear + Softmax"] --> J["ENCODERS"]
    K["K_encdec"] --> L["V_encdec"]
    M["1"] --> N["DECODERS"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#ccf,stroke:#333
    style D fill:#ccf,stroke:#333
    style E fill:#cfc,stroke:#333
    style F fill:#fcc,stroke:#333
    style G fill:#fcc,stroke:#333
    style H fill:#fcc,stroke:#333
    style I fill:#fcc,stroke:#333
    style J fill:#fcc,stroke:#333
    style K fill:#cff,stroke:#333
    style L fill:#ffc,stroke:#333
    style M fill:#ffc,stroke:#333
    style N fill:#ffc,stroke:#333
```
</details>

Warning: The self-attention layer is only allowed to attend to earlier positions in the output sequence. This is done by masking future positions (setting them to - inf) before the softmax step in the self-attention calculation.

# Convert the output of the decoder to words

Which word in our vocabulary is associated with this index?

Get the index of the cell with the highest value (argmax)

5

log\_probs

![](images/d18a0a8a7aac5ae584b3d4bccc0fbb7a802c5cf719db50158f01a547a7ad7192.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Softmax"] --> B["... vocab_size"]
    C["Linear"] --> D["... vocab_size"]
    A --> E["0 1 2 3 4 5 ... vocab_size"]
    C --> F["0 1 2 3 4 5 ... vocab_size"]
    G[" "] --> H[" "]
```
</details>

logits

Decoder stack output

# Train the Transformer

1. English to German: WMT 2014 English-German dataset (4.5 M sentence pairs). Vocabulary token size: 37000.   
2. English to French: WMT 2014 English-French dataset (36 M sentence pairs). Vocabulary token size: 32000.

Training batch size: one batch contains about 25000 source tokens and 25000 target tokens.

Optimizer: ADAM with $\beta _ { 1 } = 0 . 9 , \ \beta _ { 2 } = 0 . 9 8 , \epsilon = 1 0 ^ { - 9 }$ . The learning rate is scheduled as

$$
l _ {r} = d _ {m o d e l} ^ {- 0. 5} \times \min \big (n u m _ {s t e p} ^ {- 0. 5}, n u m _ {s t e p} \times n u m _ {w a r m u p} ^ {- 1. 5} \big),
$$

where ?????????????????? = 400.

Regularization: Dropout for each sublayer with probability 0.1.

# Applications

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). Bert: Pre-training of deep bidirectional transformers for language understanding. NAACL.

![](images/d03529d01ed00d1c2f0853801d0a5bc7b59b99df8e387a99ff0c5244a3da4956.jpg)

<details>
<summary>text_image</summary>

NLP
BERT、GPT
Transformer
Attention
</details>

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). Bert: Pre-training of deep bidirectional transformers for language understanding. NAACL.

![](images/0ff6c139a4c97267d47b5b0adc4b35847da4ba78dadb17624b3774c335357a1b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    NSP["NSP"] --> C["C"]
    NSP --> T1["T₁"]
    MaskLM["Mask LM"] --> TN["Tₙ"]
    MaskLM --> TSEP["T[{SEP}"]
    MaskLM --> T1'[T₁']
    MaskLM --> TM["Tₘ'"]
    BERT["BERT"] --> ECLS["E[CLS"]]
    BERT --> ENEN["EN"]
    BERT --> ESEP1["E[{SEP}"]
    BERT --> E1'1["E₁'"]
    BERT --> EMEM["EM'"]
    ECLS --> [CLS]
    ECLS --> Tok1["Tok 1"]
    ECLS --> ...[...]
    ENEN --> TokN["Tok N"]
    ESEP1 --> [SEP]
    E1'1 --> Tok1a["Tok 1"]
    EMEM --> TokM["TokM"]
    MaskLM --> MaskSentenceA["Masked Sentence A"]
    MaskLM --> MaskSentenceB["Masked Sentence B"]
    MaskSentenceA --> UnlabeledSentenceA["Unlabeled Sentence A and B Pair"]
    MaskSentenceB --> UnlabeledSentenceA2["Unlabeled Sentence A and B Pair"]
```
</details>

Pre-training

![](images/bf5577b42f0eea0def680158481f9edc19ef1fc0ef110ae2950e27fcb2519254.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph MNLI
        A["Input Layer"]
        B["NER"]
        C["SQuAD"]
    end

    subgraph NER
        D["Input Layer"]
        E["Input Layer"]
        F["SQuAD"]
    end

    subgraph SQuAD
        G["Output Layer"]
        H["Output Layer"]
        I["BERT"]
    end

    J["Question Answer Pair"] --> K["Question"]
    K --> L["Paragraph"]
    L --> M["Start/End Span"]
    M --> N["Output Layer"]
    style MNLI fill:#f9f,stroke:#333
    style NER fill:#bbf,stroke:#333
    style SQuAD fill:#dfd,stroke:#333
    style SQuAD fill:#dfd,stroke:#333
    style SQuAD fill:#dfd,stroke:#333
    style BERT fill:#dfd,stroke:#333
    style SQuAD fill:#dfd,stroke:#333
```
</details>

Fine-Tuning

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). Language models are few-shot learners. Advances in neural information processing systems, 33, 1877-1901.

![](images/bcd260bb8a3c2f9b1a83d14a1766bb6412e3c5a8c7b1ec042bf0ad9d4ab4abf4.jpg)

<details>
<summary>text_image</summary>

OpenAI GPT-3
</details>