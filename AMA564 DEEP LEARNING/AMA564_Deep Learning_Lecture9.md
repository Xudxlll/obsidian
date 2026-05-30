# AMA 564 Deep Learning

# 2026 Spring

# Lecture 9

Recurrent Neural Networks   
Long Short-Term Memory   
Word Embedding

# Recurrent Neural Networks

# Translation

![](images/e9b741f3a343a440faeacdc85031a9392d3791df18b559ee94a51202edb61b78.jpg)

<details>
<summary>natural_image</summary>

Abstract graphic with blue and gray shapes, no text or symbols present
</details>

English

![](images/238166b587c6f699be8c4fbf1edc40b124396d684c0cca4c81a9ce0e4f1a4371.jpg)

![](images/bdf1a91cbdc9814ab0f5225549502714032e871821d3551b5ab78ad53d5d1f39.jpg)

Chinese (Traditional)

![](images/1a5ba2cc0b85f144637c6edd0ec3cec8ed440b15b5f7b65b4d4efe6caf902b78.jpg)

he is eating a hot dog

![](images/07b384fbfb9fdfcdf32d2c4f5cbbbce73e4f2b70ffe66ce13ee1c4323c496bd9.jpg)

他在吃熱狗

![](images/d722a8d7ea6d1b9c062703784552bf176bf89a5b52b093117039ad0e26a36600.jpg)

![](images/12c897c3c7a9a953de90c97935c5cf7a63351df382c52d82f9c38cbef359dfcf.jpg)

![](images/28698dbca2fc5e06bad114d895a26e0091a66d61b000dbaf050343cf582cd6a8.jpg)

![](images/985984deb4320badd355be62834262802c755f79e5220774d7e337eeda1dfbd8.jpg)

# Translation

He is eating a hot dog   
![](images/48fd1fc6cf40693ca51d19c970e27f2da123acb4a2125191e22ac9847a5f55a0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Layer"] --> B["Node 1"]
    A --> C["Node 2"]
    A --> D["Node 3"]
    A --> E["Node 4"]
    A --> F["Node 5"]
    G["Hidden Layer"] --> H["Node 1"]
    G --> I["Node 2"]
    G --> J["Node 3"]
    G --> K["Node 4"]
    G --> L["Node 5"]
    M["Output Layer"] --> N["Node 1"]
    M --> O["Node 2"]
    M --> P["Node 3"]
    M --> Q["Node 4"]
    M --> R["Node 5"]
```
</details>

他 在 吃 热 狗

# Translation

He is a lucky dog   
![](images/b376e0cb6ac23f4502cade10754c154d4ceecf8973a5cb0ada438461ce78429b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Layer"] --> B["Node 1"]
    A --> C["Node 2"]
    A --> D["Node 3"]
    A --> E["Node 4"]
    A --> F["Node 5"]
    G["Hidden Layer"] --> H["Node 1"]
    G --> I["Node 2"]
    G --> J["Node 3"]
    G --> K["Node 4"]
    G --> L["Node 5"]
    M["Output Layer"] --> N["Node 1"]
    M --> O["Node 2"]
    M --> P["Node 3"]
    M --> Q["Node 4"]
    M --> R["Node 5"]
```
</details>

他 是 个 幸运 儿

He is eating a hot dog 6 words

He is a lucky dog 5 words

Two sentences have different length

Motivation:

the neural network should work on data with different length

He is eating a hot dog

He is a lucky dog

The word ‘dog’ has different meanings.

The translation depends on the words before ‘dog’

hot dog

lucky dog

Motivation:

the neural network should work with sequential-dependent data

# Speech to Text

![](images/a5ec88afe1c18474bb39930a95ccc48a697e45e85999ae7fae3677330746a264.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Speech"] --> B["Text"]
```
</details>

# Sentiment classification

"I love this movie. I've seen it many times and it's still awesome."

"This movie is bad. I don't like it it all. It's terrible."

![](images/52d2730a763f74ac9260f526c7741913cb4c0c06e8f6512b0a463a7962806f6f.jpg)

<details>
<summary>natural_image</summary>

Simple black right-pointing arrow on white background (no text or symbols)
</details>

![](images/f9d0a7e83182e0e2b5e57f38d953fda7de1a8c8c22e872ad0b07dca09556dde9.jpg)

<details>
<summary>natural_image</summary>

Green circular icon with a white thumbs-up symbol (no text or numbers)
</details>

![](images/65b7a417a5901b8f4c0497339c574cf8ff21d37c609db19529705a65d1575b9e.jpg)

<details>
<summary>natural_image</summary>

Simple black right-pointing arrow on white background (no text or symbols)
</details>

![](images/ae6aedf1f6ae8c5f0a4541acacfaeb2660cd757202d41262918d44bfe4c82513.jpg)

<details>
<summary>natural_image</summary>

Red circular icon with a white thumbs-down symbol (no text or numbers)
</details>

# Video activity classification

![](images/60c67dfa554e90e5a0fbec4bf22ce582c327df64306a546217c54b245a7dd39c.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of a person standing on grass, no visible text or symbols
</details>

Boxing

![](images/f9a25cb66429ff782fdb18d9bac42e77d9c1f7b261ea7269bec1ed769b37c697.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of a person standing on a paved surface, no visible text or symbols
</details>

Clapping

![](images/eb7a5df4e4af81a30ff7dfca919794a1c58cac5321599add35206ac10221a1a4.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of a person standing with arms raised, wearing a T-shirt and pants (no visible text or symbols)
</details>

Waving

![](images/b4c974b65134cd1571187697d968af5345da041d22c1c5fc17248f2c8553d958.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of a person walking on a paved path, no visible text or symbols
</details>

Walking

![](images/27bc6f5d7f18884e03ec3a4eff6c0a752cd5be02d6e553dc5cac05e94fbd3d42.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of a person playing soccer on the ground, framed by blue rectangular frames (no text or symbols visible)
</details>

Jogging

![](images/f9ac15ebfda51d8516f669b14141e9842282f0a5c92ac3d00246a5499d04b836.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of a person in motion, possibly running or walking, with no visible text or symbols.
</details>

Running

Recurrent Neural Networks (RNNs) are the modern standard to deal with time-dependent and/or sequencedependent problems.   
This type of network is “recurrent” in the sense that they can revisit or reuse past states as inputs to predict the next or future states.   
• They have memory. Memory is what allows us to incorporate our past thoughts and behaviors into our future thoughts and behaviors.

• The structure of traditional neural networks is relatively simple: input layer-hidden layer-output layer.   
The biggest difference between RNN and traditional neural networks is that each time the previous output is brought to the next hidden layer and trained together.

![](images/b24273ad17b8690c74d7f05aacec2ae4b638b224f5949c5d3baf39f1a9bc5cbf.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input"] --> B["Hidden"]
    C["Input"] --> B
    D["Output"] --> B
    B --> E["Feedback Loop"]
    style A fill:#f9f,stroke:#333
    style C fill:#bbf,stroke:#333
    style D fill:#dfd,stroke:#333
```
</details>

If we need to judge the user's intention from his/her speak (asking the weather, asking the time, setting an alarm...),

The user says, “What time is it?"

What time is it?

We segment this sentence firstly.

Input the words into the RNN in order.

First use "what" as the input of the RNN and get the output $" { \pmb \sigma } _ { 1 } "$

What time

Then input "time" to the RNN network in order, and get output $" { \pmb { o } } _ { 2 } "$

![](images/561948ac8ce2031ab950e52cde22a7293ff72df52496530bf49137c357fd48e7.jpg)

<details>
<summary>text_image</summary>

01
↑
●
↑
What time is it ?
</details>

Then input "time" to the RNN network in order, and get output "???????? “

When "time" enters, the previous hidden layer of "what" also has an effect (part of the hidden layer "time" of was black).

![](images/6716ee83de48c9a1ea6f69fd4e0467caba01fcba817ba71fdb7837655ab12044.jpg)

<details>
<summary>text_image</summary>

01
What time is it ?
</details>

By analogy, all the previous inputs have an impact on the future output.

We can see that the circular hidden layer contains all the previous colors. As shown below:

![](images/b7a5ac17366866b94ed0a91008784986b1e38bf1be57f050ae47d9a8d96d690e.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    O1["O1"] -->|↑| A["●"]
    O2["O2"] -->|↑| B["●"]
    A --> C["→"]
    B --> D["↑"]
    style A fill:#000,stroke:#000,color:#fff
    style B fill:#000,stroke:#000,color:#fff
    note right of A: 'What' is it ?
```
</details>

Lastly, to judge the user’s intention, we only need the output " ???????? " in the last layer:

![](images/54f126694c7cd21eff1d23154557794f3d15c6a93e8b83bcf4523907ae58648b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    O1["O1"] --> A["●"]
    A --> B["→"]
    B --> C["O2"]
    C --> D["○"]
    D --> E["→"]
    E --> F["O3"]
    F --> G["○"]
    G --> H["→"]
    H --> I["O4"]
    I --> J["○"]
    J --> K["→"]
    K --> L["O5"]
    L --> M["○"]
    M --> N["↑"]
    N --> O["?"]
```
</details>

# Many-to-one RNN

Classification : Positive or negative?   
![](images/39261f7165ebcd1329ce1f3c9c8a8f2f24fad2b2485bf0ed7850fdb67cf4a6ed.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["This"] --> B["movie"]
    B --> C["is"]
    C --> D["good"]
    style A fill:#d4edda,stroke:#333
    style B fill:#d4edda,stroke:#333
    style C fill:#d4edda,stroke:#333
    style D fill:#d4edda,stroke:#333
```
</details>

Source: https://goodboychan.github.io/python/deep\_learning/tensorflowkeras/2020/12/06/01-RNN-Many-to-one.html

# One-to-Many RNN

![](images/abe9edf30f9cc282a402750969b5872d9149fdf450c8df0e9d046a38b75be785.jpg)

<details>
<summary>natural_image</summary>

Black and white dog jumping over a blue and white hurdle in an outdoor field (no text or symbols visible)
</details>

One toMany   
![](images/aedf4d5c475de1caaae687e1490d86c3c9ce79e00c076312b678e9e5d6947d2b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A[" "] --> B[" "]
    C[" "] --> D[" "]
    E[" "] --> F[" "]
    G[" "] --> H[" "]
    I[" "] --> J[" "]
    K[" "] --> L[" "]
    M[" "] --> N[" "]
    O[" "] --> P[" "]
    Q[" "] --> R[" "]
    S[" "] --> T[" "]
    U[" "] --> V[" "]
    W[" "] --> X[" "]
    Y[" "] --> Z[" "]
    AA[" "] --> AB[" "]
    AC[" "] --> AD[" "]
    AE[" "] --> AF[" "]
    AG[" "] --> AH[" "]
    AI[" "] --> AJ[" "]
    AK[" "] --> AL[" "]
    AM[" "] --> AN[" "]
    AO[" "] --> AP[" "]
    AQ[" "] --> AR[" "]
    AS[" "] --> AT[" "]
    AU[" "] --> AV[" "]
    AW[" "] --> AX[" "]
    AY[" "] --> AZ[" "]
    BA[" "] --> BB[" "]
    BC[" "] --> BD[" "]
    BE[" "] --> BF[" "]
    BG[" "] --> BH[" "]
    BI[" "] --> BJ[" "]
    BK[" "] --> BL[" "]
    BM[" "] --> BN[" "]
    BO[" "] --> BP[" "]
    BQ[" "] --> BR[" "]
    BS[" "] --> BT[" "]
    BU[" "] --> BV[" "]
    BW[" "] --> BX[" "]
    BY[" "] --> BZ[" "]
    CA[" "] --> CB[" "]
    CC[" "] --> CD[" "]
    CE[" "] --> CF[" "]
    CG[" "] --> DH[" "]
    DI[" "] --> DJ[" "]
    DK[" "] --> DL[" "]
    DM[" "] --> DJ
    DB[" "] --> DC[" "]
    DD[" "] --> DV[" "]
    DW[" "] --> DX[" "]
    DX --> DW
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DX
    DX --> DW
    DX --> BX
    DX --> BY
    DX --> DA
    DX --> PX
    DX --> DZ
    DX --> DR
    DX --> CX
    DX --> CY
    DX --> CZ
    DX --> DA
    DX --> PX
    DX --> DZ
    DX --> CX
    DX --> CY
    DX --> CZ
    DX --> CX
    DX --> CY
    DX --> CX
    DX --> CX
    DX --> CX
    DX --> CX
```
</details>

# Different Types of RNN

one to one

![](images/af292eedd973e3728b1067d4ace4518c7432e1659f4440d356da603e2b68193b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A[" "] --> B[" "]
    B --> C[" "]
```
</details>

one to many

![](images/05d617b892582e93f9299df3ffdacb9ee00fb44a26dde29268429ae007468eb6.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A[" "] --> B[" "]
    C[" "] --> D[" "]
    E[" "] --> F[" "]
    G[" "] --> H[" "]
    I[" "] --> J[" "]
    K[" "] --> L[" "]
    M[" "] --> N[" "]
    O[" "] --> P[" "]
    Q[" "] --> R[" "]
    S[" "] --> T[" "]
    U[" "] --> V[" "]
    W[" "] --> X[" "]
    Y[" "] --> Z[" "]
    AA[" "] --> AB[" "]
    AC[" "] --> AD[" "]
    AE[" "] --> AF[" "]
    AG[" "] --> AH[" "]
    AI[" "] --> AJ[" "]
    AK[" "] --> AL[" "]
    AM[" "] --> AN[" "]
    AO[" "] --> AP[" "]
    AQ[" "] --> AR[" "]
    AS[" "] --> AT[" "]
    AU[" "] --> AV[" "]
    AW[" "] --> AX[" "]
    AY[" "] --> Z
    AZ[" "] --> AA
    BA[" "] --> AB
    BB[" "] --> AC
    BC[" "] --> AD
    BD[" "] --> AE
    BF[" "] --> AG
    BG[" "] --> AH
    BH[" "] --> AI
    BI[" "] --> AJ
    BJ[" "] --> AK
    BK[" "] --> AL
    BL[" "] --> AM
    BM[" "] --> AN
    BN[" "] --> AO
    BO[" "] --> AP
    BP[" "] --> AQ
    BQ[" "] --> AA
    BR[" "] --> AB
    BS[" "] --> AC
    BT[" "] --> AD
    BU[" "] --> AE
    BV[" "] --> AG
    BW[" "] --> AX
    BX[" "] --> AY
    BY[" "] --> AZ
    BZ[" "] --> BA
    BWB[" "] --> BA
```
</details>

many to one

![](images/30a5c0aa57c341011696595ec8e7a13981fb72bf47c073bdb4efe352284e9f82.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Block 1"] --> B["Process Block 1"]
    B --> C["Process Block 2"]
    C --> D["Output Block 3"]
    D --> E["Final Output Block"]
```
</details>

many to many

![](images/4eaf42af2046872e48ede1a8d1e7ed6aaa44990e6eb6771b279cfc418da05a8e.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input 1"] --> B["Green Box"]
    C["Input 2"] --> D["Green Box"]
    E["Input 3"] --> F["Green Box"]
    G["Input 4"] --> H["Green Box"]
    B --> I["Output 1"]
    D --> J["Output 2"]
    F --> K["Output 3"]
    H --> L["Output 4"]
```
</details>

many to many

![](images/075a420f91e59321a74b940e0feefb8c99719882a337614a5b403a19d1784cf7.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Block 1"] --> B["Block 2"]
    B --> C["Block 3"]
    D["Block 4"] --> E["Block 5"]
    E --> F["Block 6"]
    G["Block 7"] --> H["Block 8"]
    H --> I["Block 9"]
    style A fill:#cce5ff,stroke:#333
    style B fill:#cce5ff,stroke:#333
    style C fill:#cce5ff,stroke:#333
    style D fill:#cce5ff,stroke:#333
    style E fill:#cce5ff,stroke:#333
    style F fill:#cce5ff,stroke:#333
    style G fill:#cce5ff,stroke:#333
    style H fill:#cce5ff,stroke:#333
    style I fill:#cce5ff,stroke:#333
```
</details>

Source: http://karpathy.github.io/2015/05/21/rnn-effectiveness/

# Many-to-Many RNN

many to many   
![](images/1fb95e672cdb0bbe8e16493c0b1eceffb18b670db71b86a3521bb0427d0d9841.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Step 1"] --> B["Step 2"]
    B --> C["Step 3"]
    C --> D["Step 4"]
    D --> E["Step 5"]
    E --> F["Step 6"]
    F --> G["Step 7"]
    G --> H["Step 8"]
    H --> I["Step 9"]
    I --> J["Step 10"]
    J --> K["Step 11"]
    K --> L["Step 12"]
    L --> M["Step 13"]
    M --> N["Step 14"]
    N --> O["Step 15"]
    O --> P["Step 16"]
    P --> Q["Step 17"]
    Q --> R["Step 18"]
    R --> S["Step 19"]
    S --> T["Step 20"]
    T --> U["Step 21"]
    U --> V["Step 22"]
    V --> W["Step 23"]
    W --> X["Step 24"]
    X --> Y["Step 25"]
    Y --> Z["Step 26"]
    Z --> AA["Step 27"]
    AA --> AB["Step 28"]
    AB --> AC["Step 29"]
    AC --> AD["Step 30"]
```
</details>

many to many   
![](images/0b37687a2284301f3462125ed98524fbb8581c3448b4aed49838bb84200549bf.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Block 1"] --> B["Block 2"]
    C["Block 3"] --> D["Block 4"]
    B --> D
    D --> E["Output"]
    style A fill:#cce5ff,stroke:#333
    style C fill:#cce5ff,stroke:#333
    style B fill:#99ccff,stroke:#333
    style D fill:#99ccff,stroke:#333
    style E fill:#ff9999,stroke:#333
```
</details>

# Elman Network

![](images/8457ba89ab3067334d0f4021672bb2b6ee1d2ea0cc4e81b677a5676a7d7d992f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    x["Input Layer x"] -->|w¹| h["Hidden Layer h"]
    h -->|w| c["Clonal Node c"]
    c -->|w| h
    h -->|w²| y["Output Layer ŷ"]
    style h fill:#f9f,stroke:#333
    style c fill:#ccf,stroke:#333
    style x fill:#cfc,stroke:#333
    style y fill:#fcc,stroke:#333
    note right of h: "hidden layer"
    note right of c: "cloned state (memory)"
```
</details>

![](images/5fbad6ea3d6935b4be6dc4a7cee71df50e85de4f12f975a58cfd85da05dadab0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["x_t"] -->|w^1| B["h_t"]
    C["xt"] -->|w^1| B
    B -->|w^2| D["c_t"]
    E["output layer at t"] --> F["\hat{y}_t"]
    G["output layer at t+1"] --> H["\hat{y}_{t+1}"]
    I["hidden layer"] --> J["h_t"]
    K["hidden layer"] --> L["c_t"]
    M["hidden layer"] --> N["h_{t+1}"]
    O["hidden layer"] --> P["c_{t+1}"]
    Q["hidden layer"] --> R["x_{t+1}"]
    S["hidden layer"] --> T["h_{t+1}"]
    U["hidden layer"] --> V["c_{t+1}"]
    W["hidden layer"] --> X["h_{t+1}"]
    Y["hidden layer"] --> Z["c_{t+1}"]
    style A fill:#fff,stroke:#000
    style C fill:#fff,stroke:#000
    style D fill:#fff,stroke:#000
    style E fill:#fff,stroke:#000
    style F fill:#fff,stroke:#000
    style H fill:#fff,stroke:#000
    style I fill:#fff,stroke:#000
    style J fill:#fff,stroke:#000
    style K fill:#fff,stroke:#000
    style L fill:#fff,stroke:#000
    style M fill:#fff,stroke:#000
    style N fill:#fff,stroke:#000
    style O fill:#fff,stroke:#000
    style P fill:#fff,stroke:#000
    style Q fill:#fff,stroke:#000
    style R fill:#fff,stroke:#000
    style S fill:#fff,stroke:#000
    style T fill:#fff,stroke:#000
    style U fill:#fff,stroke:#000
    style V fill:#fff,stroke:#000
```
</details>

# Elman Network

$$
\begin{array}{l} X _ {1} \colon \mathsf {H e} \qquad \longrightarrow \quad h _ {1} = \sigma_ {h} (\mathsf {W} _ {h} X _ {1} + U _ {h} h _ {0} + b _ {h}) \quad \longrightarrow \quad Y _ {1} = \sigma_ {y} (\mathsf {W} _ {y} h _ {1} + b _ {y}) \\ X _ {2}: \text {is} \quad \longrightarrow \quad h _ {2} = \sigma_ {h} \left(\mathrm{W} _ {h} X _ {2} + U _ {h} h _ {1} + b _ {h}\right) \quad \longrightarrow \quad Y _ {2} = \sigma_ {y} \left(\mathrm{W} _ {y} h _ {2} + b _ {y}\right) \\ X _ {3} \colon \mathbf {a} \qquad \longrightarrow \quad h _ {3} = \sigma_ {h} (\mathsf {W} _ {h} X _ {3} + U _ {h} h _ {2} + b _ {h}) \quad \longrightarrow \quad Y _ {3} = \sigma_ {y} (\mathsf {W} _ {y} h _ {3} + b _ {y}) \\ X _ {4}: \text {   lucky   } \longrightarrow h _ {4} = \sigma_ {h} (W _ {h} X _ {4} + U _ {h} h _ {3} + b _ {h}) \longrightarrow Y _ {4} = \sigma_ {y} (W _ {y} h _ {4} + b _ {y}) \\ X _ {5} \colon \mathsf {d o g} \quad \longrightarrow \quad h _ {5} = \sigma_ {h} (\mathsf {W} _ {h} X _ {5} + U _ {h} h _ {4} + b _ {h}) \quad \longrightarrow \quad Y _ {5} = \sigma_ {y} (\mathsf {W} _ {y} h _ {5} + b _ {y}) \\ \end{array}
$$

![](images/b9d96eeaf7032245f8c3b51d63ea9a3ffc10c4cf459f3691b3943c14cf7186d6.jpg)

![](images/b3f9bc6b108ed171010f2f17fdd072645a5ca13d1ecccf986fa8099c26d5852c.jpg)

![](images/ca24965d1e438e0afa5d3f5c30dbe79abe1f060ebe8bdcc04e59f18efd449b5b.jpg)

![](images/6a2c49cb53d840f372e05790e59373f561c2b4c35ab60804494115079e1a1592.jpg)

# Jordan Network

![](images/5e2480a86349a9e2fd5631ac19eb489131a5863dff5032e699ef89e0ec2505ce.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    x["Input x"] --> h["Hidden Layer h"]
    h --> y["Output y"]
    y --> h
    h --> μ[Hidden Layer μ]
    μ --> y
    style h fill:#f9f,stroke:#333
    style μ fill:#ccf,stroke:#333
    style x fill:#cfc,stroke:#333
    note right of h: "hidden layer"
    note right of μ: "running average (memory)"
    note left of y: "output layer"
    note right of μ: "1"
    note right of x: "input layer"
    note left of h: "w²"
    note right of μ: "1"
```
</details>

![](images/0a4c2b652c91034cac27403c49365bff03db12fe845f0a6c73e4ae922b0da79c.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["x_t"] -->|w^1| B["h_t"]
    B -->|w^2| C["\hat{y}_t"]
    C -->|1| D["\mu_t"]
    D -->|1| E["h_{t+1}"]
    E -->|w^1| F["x_{t+1}"]
    F -->|w^2| G["\hat{y}_{t+1}"]
    G -->|1| H["\mu_{t+1}"]
    H -->|1| I["Output Layer at t+1"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#cfc,stroke:#333
    style D fill:#fcc,stroke:#333
    style E fill:#cff,stroke:#333
    style F fill:#ffc,stroke:#333
    style G fill:#fcf,stroke:#333
    style H fill:#fcf,stroke:#333
    style I fill:#fff,stroke:#333
```
</details>

# Jordan Network

$$
\begin{array}{l} X _ {1}: \mathsf {H e} \quad \longrightarrow \quad h _ {1} = \sigma_ {h} (\mathsf {W} _ {h} X _ {1} + U _ {h} Y _ {0} + b _ {h}) \quad \longrightarrow \quad Y _ {1} = \sigma_ {y} (\mathsf {W} _ {y} h _ {1} + b _ {y}) \\ X _ {2}: \text {is} \quad \longrightarrow \quad h _ {2} = \sigma_ {h} \left(W _ {h} X _ {2} + U _ {h} Y _ {1} + b _ {h}\right) \longrightarrow Y _ {2} = \sigma_ {y} \left(W _ {y} h _ {2} + b _ {y}\right) \\ X _ {3}: \mathbf {a} \quad \longrightarrow \quad h _ {3} = \sigma_ {h} \left(\mathrm{W} _ {h} X _ {3} + U _ {h} Y _ {2} + b _ {h}\right) \longrightarrow Y _ {3} = \sigma_ {y} \left(\mathrm{W} _ {y} h _ {3} + b _ {y}\right) \\ X _ {4}: \text {   lucky   } \longrightarrow h _ {4} = \sigma_ {h} (W _ {h} X _ {4} + U _ {h} Y _ {3} + b _ {h}) \longrightarrow Y _ {4} = \sigma_ {y} (W _ {y} h _ {4} + b _ {y}) \\ X _ {5}: \mathsf {d o g} \quad \longrightarrow \quad h _ {5} = \sigma_ {h} (\mathrm{W} _ {h} X _ {5} + U _ {h} Y _ {4} + b _ {h}) \quad \longrightarrow \quad Y _ {5} = \sigma_ {y} (\mathrm{W} _ {y} h _ {5} + b _ {y}) \\ \end{array}
$$

RNN Unfolded over time   
![](images/4522980f24190b790c32bb1bcb7c6364d76f0106439fab3976f2b4660116b218.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    h[" h "] -->|A| y1["y(t-2)"]
    h -->|B| x1["x(t-2)"]
    h -->|C| h2["h(t-2)"]
    h -->|C| h3["h(t-1)"]
    h2 -->|A| y2["y(t-1)"]
    h2 -->|B| x2["x(t-1)"]
    h3 -->|A| y3["y(t)"]
    h3 -->|B| x3["x(t)"]
    h3 -->|C| h4["h(t)"]
    h4 -->|A| y4["y(t+1)"]
    h4 -->|B| x4["x(t+1)"]
    h4 -->|C| h5["h(t+1)"]
    h5 -->|A| y5["y(t+1)"]
    h5 -->|B| x5["x(t+2)"]
    h5 -->|C| h6["h(t+2)"]
    x1 -->|A| y6["y(t+2)"]
    x2 -->|B| x2["x(t+2)"]
    x3 -->|C| h7["h(t)"]
    x4 -->|A| y7["y(t+2)"]
    x5 -->|B| x5["x(t+2)"]
```
</details>

A dynamical system   
Source: Simplilearn.com

RNN Unfolded over time   
![](images/56526016eab2b1b49f9d64f66961d13265e7af4b63226285c2e10c98397be6bd.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    O1["O1"] --> A["●"]
    O2["O2"] --> B["●"]
    A --> C["→"]
    B --> D["↑"]
    style A fill:#000,stroke:#000,color:#fff
    style B fill:#000,stroke:#000,color:#fff
    note right of A: 'What is it ?'
```
</details>

![](images/5a102f9c2a1f15f4409d7692f56ec1f0a1dd2e9ecd0b334c058c641c2217695a.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph Input_States
        y["y"] --> L["L"]
        L --> ŷ[ŷ]
        ŷ --> o["o"]
        o --> h["h"]
        h --> x["x"]
        x --> y
        y --> L
        L --> ŷ
        ŷ --> o
    end

    subgraph Output_States
        y_t_minus_1["y_{t-1}"] --> L_t_minus_1["L_{t-1}"]
        L_t_minus_1 --> ŷ_t_minus_1["ŷ_{t-1}"]
        L_t --> o_t_minus_1["o_{t-1}"]
        o_t_minus_1 --> h_t_minus_1["h_{t-1}"]
        o_t_minus_1 --> X_t_minus_1["X_{t-1}"]
        o_t_minus_1 --> X_t["X_t"]
        o_t_minus_1 --> X_t_plus_1["O_{t+1}"]
    end

    h -->|softmax Wyh| o
    o -->|softmax Wyh| h
    x -->|softmax Wxh| h
    h -->|softmax Wyh| o_t_minus_1
    o_t_minus_1 --> h_t_minus_1
    o_t_minus_1 --> h_t
    h_t_minus_1 --> X_t_minus_1
    h_t --> X_t
    h_t --> X_t_plus_1
    h_t --> X_t_plus_1
    h_t --> X_t_plus_1
    h_t --> O_t_minus_1
    h_t --> O_t
    h_t --> O_t
    h_t --> O_t_plus_1
    h_t --> O_t_plus_1

    y_t_minus_1 --> L_t_minus_1
    L_t --> ŷ_t_minus_1
    ŷ_t_minus_1 --> o_t_minus_1
    o_t --> h_t_minus_1
    o_t --> h_t
    y_t --> L_t
    L_t --> ŷ_t
    ŷ_t --> o_t
    o_t --> H_t_plus_1
    o_t --> H_t

    y_t_plus_1 --> L_t_plus_1
    L_t_plus_1 --> ŷ_t_plus_1
    ŷ_t_plus_1 --> O_t_plus_1

    y_t --> L_t
    L_t --> ŷ_t

    y_t_plus_1 --> L_t_plus_1
    L_t_plus_1 --> ŷ_t_plus_1

    y_t_plus_1 --> L_t_plus_1

    y_t --> L_t

    y_t_plus_1 --> L_t_plus_1

    b_y["b_y"] --> h
    b_h["b_h"] --> x

    style Input_States fill:#f9f,stroke:#333
    style Output_States fill:#bbf,stroke:#333
```
</details>

Source: https://mmuratarat.github.io/2019-02-07/bptt-of-rnn

The RNN is defined by

$$
h _ {t} = f _ {h} \left(X _ {t}, h _ {t - 1}\right) = \phi_ {h} \left(W _ {x h} ^ {T} \cdot X _ {t} + W _ {h h} ^ {T} \cdot h _ {t - 1} + b _ {h}\right)
$$

$$
\hat {y} _ {t} = f _ {o} (h _ {t}) = \phi_ {o} (W _ {y h} ^ {T} \cdot h _ {t} + b _ {y})
$$

where $W _ { x h } , W _ { h h }$ and $W _ { y h }$ are weight matrices for the input, recurrent connections, and the output, respectively and $\phi _ { h }$ and $\phi _ { o }$ are elementwise nonlinear functions.

The Loss function is defined by

$$
\begin{array}{l} L (\hat {y}, y) = \sum_ {t = 1} ^ {T} L _ {t} (\hat {y} _ {t}, y _ {t}) \\ = - \sum_ {t} ^ {T} y _ {t} \log \hat {y} _ {t} \\ = - \sum_ {t = 1} ^ {T} y _ {t} \log [ \text { softmax } (o _ {t}) ] \\ \end{array}
$$

Note that the weight $W _ { y h }$ is shared across all the time sequence. Therefore, we can differentiate to it at the each time step and sum all together:

$$
\begin{array}{l} \frac {\partial L}{\partial W _ {y h}} = \sum_ {t} ^ {T} \frac {\partial L _ {t}}{\partial W _ {y h}} \\ = \sum_ {t} ^ {T} \frac {\partial L _ {t}}{\partial \hat {y} _ {t}} \frac {\partial \hat {y} _ {t}}{\partial o _ {t}} \frac {\partial o _ {t}}{\partial W _ {y h}} \\ \end{array}
$$

Similarly, we can get the gradient with respect to bias $b _ { y }$ :

$$
\begin{array}{l} \frac {\partial L}{\partial b _ {y}} = \sum_ {t} ^ {T} \frac {\partial L _ {t}}{\partial \hat {y} _ {t}} \frac {\partial \hat {y} _ {t}}{\partial o _ {t}} \frac {\partial o _ {t}}{\partial b _ {y}} \\ = \sum_ {t} ^ {T} (\hat {y} _ {t} - y _ {t}) \\ \end{array}
$$

Now, let’s go through the details to derive the gradient with respect to $W _ { h h }$ , considering at the time step $t + 1$

$$
\frac {\partial L _ {t + 1}}{\partial W _ {h h}} = \frac {\partial L _ {t + 1}}{\partial \hat {y} _ {t + 1}} \frac {\partial \hat {y} _ {t + 1}}{\partial h _ {t + 1}} \frac {\partial h _ {t + 1}}{\partial W _ {h h}}
$$

But, the hidden state $h _ { t + 1 }$ partially depends also on $h _ { t } , h _ { t - 1 } , \ldots , h _ { 1 }$

$$
\frac {\partial L _ {t + 1}}{\partial W _ {h h}} = \sum_ {k = 1} ^ {t + 1} \frac {\partial L _ {t + 1}}{\partial \hat {y} _ {t + 1}} \frac {\partial \hat {y} _ {t + 1}}{\partial h _ {t + 1}} \frac {\partial h _ {t + 1}}{\partial h _ {k}} \frac {\partial h _ {k}}{\partial W _ {h h}}
$$

Aggregate the gradients with respect to $W _ { h h }$ over the whole timesteps with backpropagation,

$$
\frac {\partial L}{\partial W _ {h h}} = \sum_ {t} ^ {T} \sum_ {k = 1} ^ {t + 1} \frac {\partial L _ {t + 1}}{\partial \hat {y} _ {t + 1}} \frac {\partial \hat {y} _ {t + 1}}{\partial h _ {t + 1}} \frac {\partial h _ {t + 1}}{\partial h _ {k}} \frac {\partial h _ {k}}{\partial W _ {h h}}
$$

Further, we can take the derivative with respect to $W _ { x h }$ over the whole sequence as

$$
\frac {\partial L}{\partial W _ {x h}} = \sum_ {t} ^ {T} \sum_ {k = 1} ^ {t + 1} \frac {\partial L _ {t + 1}}{\partial \hat {y} _ {t + 1}} \frac {\partial \hat {y} _ {t + 1}}{\partial h _ {t + 1}} \frac {\partial h _ {t + 1}}{\partial h _ {k}} \frac {\partial h _ {k}}{\partial W _ {x h}}
$$

Note: Because of recursive derivative, we need to compute

$$
\prod_ {j = k} ^ {t} \frac {\partial h _ {j + 1}}{\partial h _ {j}} = \frac {\partial h _ {t + 1}}{\partial h _ {k}} = \frac {\partial h _ {t + 1}}{\partial h _ {t}} \frac {\partial h _ {t}}{\partial h _ {t - 1}} \dots \frac {\partial h _ {k + 1}}{\partial h _ {k}}
$$

This can lead to vanishing gradient or exploding gradient.

Decay of information through time   
![](images/3b14265c828ee6c962c4bcf7c406471a96fdf36574fa932a2c2ecfc181e2ca6e.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Time t = 0"] --> B["Time t = 1"]
    B --> C["Time t = 2"]
    C --> D["Time t = 3"]
    D --> E["Time t = 4"]
    E --> F["Time t = 5"]
    F --> G["Time t = 6..."]
    G --> H["..."]
    H --> I["Time t = 100"]
```
</details>

Source: O'Reilly Media

Decay of information through time   
![](images/d87e42e421f94376f11b155a7edda178daf74eef9264c1cbb1fb497aaae7daa0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    O1["O1"] -->|↑| A["●"]
    O2["O2"] -->|↑| B["●"]
    A --> C["→"]
    B --> D["↑"]
    style A fill:#000,stroke:#000,color:#fff
    style B fill:#000,stroke:#000,color:#fff
    note right of A: What is it ?
```
</details>

![](images/40191a4fdd1acc6262f8a7fa7fa9d4eef1d8b12c9838b7f03117a40c73e396e7.jpg)

<details>
<summary>natural_image</summary>

Circular color gradient design with no text or symbols
</details>

# Long Short-Term Memory

The intuition behind the LSTM architecture is to create an additional module in a neural network that learns when to remember and when to forget pertinent information.   
• In other words, the network, effectively learns which information might be needed later on in a sequence and when that information is no longer needed.

![](images/1678220d9688390b317cdce22a8647047027453f4e201a743c04f4aeb99f602c.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input"] --> B["RNN"]
    B --> C["Working Memory"]
    C --> D["Long-term Memory"]
    D --> E["LSTM"]
    E --> F["Working Memory"]
    F --> G["Output"]
    H["Input"] --> I["Output"]
    J["Output"] --> K["Output"]
    style B fill:#cce5ff,stroke:#333
    style E fill:#cce5ff,stroke:#333
```
</details>

Source: Research Gate

In addition to the hidden state $\pmb { h } _ { t }$ , LSTM also keeps a memory cell $c _ { t }$   
![](images/7030949555aa6a7660c0a9ccce9b0bc35ec6f758401c3458527d66201b3d7617.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Ct-1"] --> B["Forget gate"]
    B --> C["σ"]
    B --> D["σ"]
    B --> E["tanh"]
    E --> F["×"]
    G["ht-1"] --> H["Xt"]
    H --> I["Output gate"]
    I --> J["tanh"]
    J --> K["×"]
    L["ht"] --> M["Output gate"]
    M --> N["Output gate"]
    style A fill:#99ccff,stroke:#333
    style G fill:#99ccff,stroke:#333
    style L fill:#99ccff,stroke:#333
    style M fill:#99ccff,stroke:#333
    subgraph LSTM_Memory_Cell
        B -->|↑| I
        C -->|↑| I
        D -->|↑| I
        E -->|↑| I
        F -->|↑| I
        G -->|↑| I
        H -->|↓| I
        I --> J
        I --> K
        I --> L
        I --> M
    end
    subgraph LSTM_Memory_Cell
        J -->|↓| K
        K --> L
        L --> M
        M --> N
    end
```
</details>

The forward pass of an LSTM cell with a forget gate are

$$
f _ {t} = \sigma_ {g} (W _ {f} x _ {t} + U _ {f} h _ {t - 1} + b _ {f})
$$

$$
i _ {t} = \sigma_ {g} (W _ {i} x _ {t} + U _ {i} h _ {t - 1} + b _ {i})
$$

$$
o _ {t} = \sigma_ {g} (W _ {o} x _ {t} + U _ {o} h _ {t - 1} + b _ {o})
$$

$$
\tilde {c} _ {t} = \sigma_ {c} (W _ {c} x _ {t} + U _ {c} h _ {t - 1} + b _ {c})
$$

$$
c _ {t} = f _ {t} \odot c _ {t - 1} + i _ {t} \odot \tilde {c} _ {t}
$$

$$
h _ {t} = o _ {t} \odot \sigma_ {h} (c _ {t})
$$

where the initial values are $\pmb { c _ { 0 } = 0 }$ and $\pmb { h _ { 0 } } = \mathbf { 0 }$ , and the operator ⊙ denotes the Hadamard product (element-wise product).

中 $\mathbf { I } _ { t } ^ { n _ { t } } \in \mathbb { R } ^ { d }$ : input vector to the LSTM unit   
$f _ { i } \in ( 0 , 1 ) ^ { h }$ : forget gate's activation vector   
$i _ { t } \in ( 0 , 1 ) ^ { h }$ : input/update gate's activation vector   
$\sigma _ { \ell } \in ( 0 , 1 ) ^ { h }$ : output gate's activation vector

$h _ { t } \in ( - 1 , 1 ) ^ { h }$ : hidden state vector   
$\tilde { \bar { c } } _ { t } \in ( - 1 , 1 ) ^ { h }$ : cell input activation vector   
$c _ { t } \in \mathbb { R } ^ { h }$ Ct R： : cell state vector

![](images/d7f54e1a31e84ed1780c1475fcf689183e1a48d0408ff92995053f86cc191ffe.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["ct-1"] --> B["X"]
    B --> C["f_t"]
    C --> D["σ"]
    D --> E["i_t"]
    E --> F["σ"]
    F --> G["tanh"]
    G --> H["σ"]
    H --> I["ot"]
    I --> J["x"]
    J --> K["tanh"]
    K --> L["xt"]
    L --> M["h_t-1"]
    M --> N["xt"]
    N --> O["+"]
    O --> P["x"]
    P --> Q["tanh"]
    Q --> R["xt"]
    R --> S["ht"]
    S --> T["yt"]
    T --> U["Ct"]
    U --> V["ct"]
```
</details>

# Wikipedia: Gated Recurrent Unit

![](images/33075c177b37b79825614b290f68150530a1989193f9976db3fd2a831728680c.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["x_t"] --> B["σ"]
    B --> C["r_t"]
    C --> D["x"]
    D --> E["z_t"]
    E --> F["σ"]
    F --> G["1-"]
    G --> H["x"]
    H --> I["tanh"]
    I --> J["+"]
    J --> K["h_t"]
    K --> L["h_{t-1}"]
    style A fill:#f9f,stroke:#333
    style L fill:#ccf,stroke:#333
```
</details>

$$
z _ {t} = \sigma \left(W _ {z} \cdot [ h _ {t - 1}, x _ {t} ]\right)
$$

$$
r _ {t} = \sigma \left(W _ {r} \cdot [ h _ {t - 1}, x _ {t} ]\right)
$$

$$
\tilde {h} _ {t} = \tanh \left(W \cdot [ r _ {t} * h _ {t - 1}, x _ {t} ]\right)
$$

$$
h _ {t} = (1 - z _ {t}) * h _ {t - 1} + z _ {t} * \tilde {h} _ {t}
$$

# Word Embedding

In natural language processing (NLP), a word embedding is a representation of a word.   
The embedding is used in text analysis.   
Typically, the representation is a real-valued vector that encodes the meaning of the word in such a way that words that are closer in the vector space are expected to be similar in meaning.

# One-hot word embedding

• In a one-hot encoding, or “1-of-N” encoding, the embedding space has the same number of dimensions as the number of words in the vocabulary   
• Each word embedding is predominantly made up of zeros, with a “1” in the corresponding dimension for the word.

# One-hot word embedding

Example of a one-hot embedding scheme for a nine-word vocabulary. Word embeddings are read as rows of this table.

Vocabulary: Man,woman, boy, girl, prince, princess, queen, king, monarch

![](images/b218c7caa102e1c43a3fe49abb717cc3b502ec320d3728db4971f990d94c183b.jpg)

<details>
<summary>natural_image</summary>

Solid red right-pointing arrow shape (no text or symbols)
</details>

<table><tr><td></td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr><tr><td>man</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>woman</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>boy</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>girl</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>prince</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>princess</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>queen</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>king</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>monarch</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td></tr></table>

Each word gets a 1x9 vector representation

# One-hot word embedding

The number of dimensions, increases linearly as we add words to the vocabulary. For a vocabulary of 50,000 words, each word is represented with 49,999 zeros, and a single “one” value in the correct location. The memory use is prohibitively large.   
• The embedding matrix is very sparse, mainly made up of zeros.   
. There is no shared information between words and no commonalities between similar words. All words are the same “distance” apart in the embedding space.

# Custom embedding

Manually choosing dimensions that make sense for the vocabulary.

Vocabulary: Man,woman, boy, girl,prince, princess,queen, king,monarch

![](images/683d3778d8e1b71e86d7399820b1db8950962fdd5fc01beba92331b290865c46.jpg)

<details>
<summary>natural_image</summary>

Solid red right-pointing arrow shape (no text or symbols)
</details>

<table><tr><td></td><td>Femininity</td><td>Youth</td><td>Royalty</td></tr><tr><td>Man</td><td>0</td><td>0</td><td>0</td></tr><tr><td>Woman</td><td>1</td><td>0</td><td>0</td></tr><tr><td>Boy</td><td>0</td><td>1</td><td>0</td></tr><tr><td>Girl</td><td>1</td><td>1</td><td>0</td></tr><tr><td>Prince</td><td>0</td><td>1</td><td>1</td></tr><tr><td>Princess</td><td>1</td><td>1</td><td>1</td></tr><tr><td>Queen</td><td>1</td><td>0</td><td>1</td></tr><tr><td>King</td><td>0</td><td>0</td><td>1</td></tr><tr><td>Monarch</td><td>0.5</td><td>0.5</td><td>1</td></tr></table>

Each word getsa 1x3vector

Similarwords... similarvectors

# Custom embedding

1. The set of embeddings is more efficient, each word is represented with a 3-dimensional vector.   
2. Similar words have similar vectors here. i.e. there’s a smaller distance between the embeddings for “girl” and “princess”, than from “girl” to “prince”. In this case, distance is defined by Euclidean distance.   
3. The embedding matrix is much less sparse, and we could potentially add further words to the vocabulary without increasing the dimensionality. For instance, the word “child” might be represented with [0.5, 1, 0].   
4. Relationships between words are captured and maintained, e.g. the movement from king to queen, is the same as the movement from boy to girl, and could be represented by [+1, 0, 0].

# Extending to larger vocabularies

# Word Embeddings Properties

• Word Similarities / Synonyms   
Linguistic Relationships

Example 2D word embedding space, where similar words are found in similar locations.   
![](images/dc03573e832b72db4e4ea0c26d96e4edb0c142f60aa347d2f3f9d80a64534b22.jpg)  
Source: http://suriyadeepan.github.io

Country and Capital Vectors Projected by PCA   
![](images/0c875779db76a311457e45d741b047686ec3e7f67ca1422549096866daa13d4d.jpg)  
2D PCA projection of word embeddings showing the linear “capital city of” relationship captured by the word-embedding training process.

![](images/9cbd47f1b9170cb4de73ae7f1b89ac3f1b766cc0471bf09ecc49a624a465807a.jpg)

<details>
<summary>text_image</summary>

king
man
woman
queen
</details>

Male-Female

![](images/f30c2dedee00b9a1e8fb460a4b483c6509aa4aaac41faafafb5e725832e6bd15.jpg)

<details>
<summary>text_image</summary>

walked
swam
walking
swimming
</details>

Verb tense

![](images/3f230f3c8a57637b15c1e75b7ac32f1fb1440c135421c610400e9c800b067d8d.jpg)

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

# Example

# Data set: surnames from 18 countries

![](images/8b44301ca58904ca8605b6fb900f822f4c8cddc837694d1aca6ef149b8e5368e.jpg)  
Arabic.txt

![](images/7efbfe573706869753eaf0026c44948aa612facbc4c4e94988a5e2ffb0b55086.jpg)  
Chinese.txt

![](images/7e58e888f43c9425edc352f48941d6770b7f3c18676582b18ad128fd31c84e12.jpg)  
Czech.txt

![](images/adcc63c582e96807b51243c3d588135d41b525005d4b5c06b33636d995873671.jpg)  
Dutch.txt

![](images/0c5bf47213b36bd1e2f7de1c7176601ffc44ae1c42849feaee21db2e44396de3.jpg)  
English.txt

![](images/3645038a09d617679a6e18334f462d4e20a88d49a2a5a707fab36159a05753eb.jpg)  
French.txt

![](images/76df61df608a7d07bb1f66390de1fd8be2f31d42fcfbd93bf0e91f2148da63a0.jpg)  
German.txt

![](images/2b0f952aaf429455aedafed789a0ea7c764cc30ad1205466017e72a024e0f7b2.jpg)  
Greek.txt

![](images/63e77a59a9285fc643be879aa4986fd6edd5e32bee2e5334c2ac3a2b018ee34a.jpg)  
Irish.txt

![](images/6a39a053b9906f69ed88ae2d71ee416d2da772f12ebd8da512fc8994d5ced2cd.jpg)  
Italian.txt

![](images/638b4a1639d06dc6ac0a381daac03107e14c312edcd1653e12f31bd4ba9a0be2.jpg)  
Japanese.txt

![](images/a5c4dc45da37fef90f6ab36db69535c5cb88476ed95c49f5786a187922ca79f7.jpg)  
Korean.txt

![](images/1b3cd6a6c3c6b5b44e65cf2b07db85010e920fa3180b3d5b75e48a3147a6716f.jpg)  
Polish.txt

![](images/5f083cc4ddd5a4f86d9f1270e071effb506f7abfe747d8da00a6dbb885d506f3.jpg)  
Portuguese.txt

![](images/68258509ed5dd6ad96327714e8e3800389aa2c28b53e1974c664e9f352d34755.jpg)  
Russian.txt

![](images/f62c61c41bbb936b5413b10df7f8188deadb8f48f0bfa2be4834ed34d46dddd5.jpg)  
Scottish.txt

![](images/972eab9fc8009c3a48ab1802d42a1694fbf98949b5ea465b4f171bd0fb0d5763.jpg)  
Spanish.txt

![](images/e0412b73069f15129803668fada86b91c70098f78119e15d0938e27ea6d2ad11.jpg)  
Vietnamese.txt

<table><tr><td colspan="6">Chinese.txt</td></tr><tr><td>Ang</td><td>Abbas</td><td>Ababko</td><td>Abel</td><td></td><td></td></tr><tr><td>Au-Yong</td><td>Abbey</td><td>Abaev</td><td>Abraham</td><td></td><td></td></tr><tr><td>Bai</td><td>Abbott</td><td>Abagyan</td><td>Adam</td><td></td><td></td></tr><tr><td>Ban</td><td>Abdi</td><td>Abaidulin</td><td>Albert</td><td></td><td></td></tr><tr><td>Bao</td><td>Abel</td><td>Abaidullin</td><td>Allard</td><td></td><td></td></tr><tr><td>Bei</td><td>Abraham</td><td>Abaimoff</td><td>Archambault</td><td></td><td></td></tr><tr><td>Bian</td><td>Abrahams</td><td>Abaimov</td><td>Armistead</td><td></td><td></td></tr><tr><td>Bui</td><td>Abrams</td><td>Abakeliya</td><td>Arthur</td><td></td><td></td></tr><tr><td>Cai</td><td>Ackary</td><td>Abakovsky</td><td>Augustin</td><td></td><td></td></tr><tr><td>Cao</td><td>Ackroyd</td><td>Abakshin</td><td>Babineaux</td><td></td><td></td></tr><tr><td>Cen</td><td>Acton</td><td>Abakumoff</td><td>Baudin</td><td></td><td></td></tr><tr><td>Chai</td><td>Adair</td><td>Abakumov</td><td>Beauchene</td><td></td><td></td></tr><tr><td>Chaim</td><td>Adam</td><td>Abakumtsey</td><td>Beaulieu</td><td></td><td></td></tr><tr><td>Chan</td><td>Adams</td><td>Abakushin</td><td>Beaumont</td><td></td><td></td></tr><tr><td>Chang</td><td>Adamson</td><td>Abalakin</td><td>Bélanger</td><td></td><td></td></tr><tr><td>Chao</td><td>Adanet</td><td>Abalakoff</td><td>Bellamy</td><td></td><td></td></tr><tr><td>Che</td><td>Addams</td><td>Abalakov</td><td>Bellerose</td><td></td><td></td></tr><tr><td>Chen</td><td>Adderley</td><td>Abaleshev</td><td>Belrose</td><td></td><td></td></tr><tr><td>Cheng</td><td>Addinall</td><td>Abalihin</td><td>Berger</td><td></td><td></td></tr><tr><td>Cheung</td><td>Addis</td><td>Abalikhin</td><td>Béringer</td><td></td><td></td></tr><tr><td>Chew</td><td>Addison</td><td>Abalkin</td><td>Bernard</td><td></td><td></td></tr><tr><td>Chieu</td><td>Addley</td><td>Abalmasoff</td><td>Bertrand</td><td></td><td></td></tr><tr><td>Chong</td><td>Aderson</td><td>Abalmasov</td><td>Bisset</td><td></td><td></td></tr><tr><td>Chou</td><td>Adey</td><td>Abaloff</td><td>Bissette</td><td></td><td></td></tr><tr><td>Chu</td><td>Adkins</td><td>Abalov</td><td>Blaise</td><td></td><td></td></tr><tr><td>Cui</td><td>Adlam</td><td>Abamelek</td><td>Blanc</td><td></td><td></td></tr><tr><td>Dai</td><td>Adler</td><td>Abanin</td><td>Blanchet</td><td></td><td></td></tr><tr><td>Deng</td><td>Adrol</td><td>Abankin</td><td>Blanchett</td><td></td><td></td></tr><tr><td>Ding</td><td>Adsett</td><td>Abarinoff</td><td>Bonfils</td><td></td><td></td></tr><tr><td>Dong</td><td>Agar</td><td>Abarinov</td><td>Bonheur</td><td></td><td></td></tr><tr><td>Dou</td><td>Ahern</td><td>Abasheev</td><td>Bonhomme</td><td></td><td></td></tr><tr><td>Duan</td><td>Aherne</td><td>Abashev|</td><td>Bonnaire</td><td></td><td></td></tr><tr><td>Eng</td><td>Ahmad</td><td>Abashidze</td><td>Bonnay</td><td></td><td></td></tr><tr><td>Fan</td><td>Ahmed</td><td>Abashin</td><td>Bonner</td><td></td><td></td></tr><tr><td>Fei</td><td>Aikman</td><td>Abashkin</td><td>Bonnet</td><td></td><td></td></tr><tr><td>Feng</td><td>Ainley</td><td>Abasov</td><td>Borde</td><td></td><td></td></tr><tr><td>Foong</td><td>Ainsworth</td><td>Abatsiev</td><td>Bordelon</td><td></td><td></td></tr></table>

# Target:

Train a classifier using RNN to classify surname into 18 country categories

Embedding: One-hot embedding   
```python
import unicodedata
import string

all_letters = string.ascii_letters + " .;;"
n_letters = len(all_letters)

print(all_letters)
print(n_letters) 
```

abcdefghijklmnopqrstuvWxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ., ; ' 57

Embedding: One-hot embedding   
```python
# Find letter index from all_letters, e.g. "a" = 0
def letterToIndex(letter):
    return all_letters.find(letter)
print(all_letters.find('a'))
print(all_letters.find('A'))
print(all_letters.find('J')) 
```

```txt
0
26
35 
```

Embedding: One-hot embedding   
```python
import torch
# Just for demonstration, turn a letter into a <1 x n_letters> Tensor
def letterToTensor(letter):
    tensor = torch.zeros(1, n_letters)
    tensor[0][letterToIndex(letter)] = 1
    return tensor

print(letterToTensor('a'))
print(letterToTensor('B'))
print(letterToTensor('J')) 
```

```lua
tensor([[1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.
    0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],)

tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.]
tensor([[0.., 0.., 0.., 0.., 0.., 0.., 0.., 0.., 1.], 
```

Build RNN   
```python
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
    super(RNN, self).__init__()
    self.hidden_size = hidden_size
    self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
    self.i2o = nn.Linear(input_size + hidden_size, output_size)
    self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
    combined = torch.cat((input, hidden), 1)
    hidden = self.i2h(combined)
    output = self.i2o(combined)
    output = self.softmax(output)
    return output, hidden

    def initHidden(self):
    return torch.zeros(1, self.hidden_size)

n_hidden = 128
rnn = RNN(n_letters, n_hidden, n_categories) 
```

# Forward pass in RNN

```python
input = letterToTensor('A')
hidden = torch.zeros(1, n_hidden)
output, next_hidden = rnn(input, hidden)
print(output) 
```

```txt
tensor([[-3.1146, -3.9119, -2.8865, -2.4666, -2.9795, -3.5882, -3.4682, -3.0312, -3.1896, -2.5168, -3.0321, -3.2578, -2.9676, -2.1635, -2.5508, -2.7902, -2.6268, -2.9879]], grad_fn=<LogSoftmaxBackward0>) 
```

# Train the model

criterion = nn.NLLLoss(). # Negative log likelihood loss   
```python
learning_rate = 0.005 # If you set this too high, it might explode.
# If too low, it might not learn 
```

```python
def train(category_tensor, line_tensor):
    hidden = rnn.initHidden()
    rnn.zero_grad()

    for i in range(line_tensor.size()[0]):
    output, hidden = rnn(line_tensor[i], hidden)

    loss = criterion(output, category_tensor)
    loss.backward()

    # Add parameters' gradients to their values, mul
    for p in rnn.parameters():
    p.data.add_(p.grad.data, alpha=-learning_rat

    return output, loss.item() 
```

# Training Process

```csv
5000 2% (0m 6s) 0.0121 Brisimitzakis / Greek √
10000 5% (0m 12s) 2.3322 Wizner / German × (Czech)
15000 7% (0m 19s) 1.5737 Alesio / Spanish × (Italian)
20000 10% (0m 25s) 2.5522 Horner / German × (English)
25000 12% (0m 32s) 0.2332 Giang / Vietnamese √
30000 15% (0m 38s) 2.0818 Jorda / Polish × (Spanish)
35000 17% (0m 45s) 0.3461 Ly / Vietnamese √
40000 20% (0m 51s) 1.4224 Lindsay / English × (Scottish)
45000 22% (0m 59s) 0.7342 Daher / Arabic √
50000 25% (1m 5s) 1.5104 Bauer / Arabic × (German)
55000 27% (1m 12s) 0.4402 Paquet / French √
60000 30% (1m 18s) 1.0985 Kuang / Chinese √
65000 32% (1m 25s) 1.9924 Caiazzo / Portuguese × (Italian)
70000 35% (1m 31s) 0.0066 Maolmhuaidh / Irish √
75000 37% (1m 38s) 0.5535 Dao / Vietnamese √
80000 40% (1m 44s) 0.0000 Cuidightheach / Irish √
85000 42% (1m 51s) 0.4375 Park / Korean √
90000 45% (1m 57s) 0.2562 Thai / Vietnamese √
95000 47% (2m 3s) 0.0537 Zielinski / Polish √
100000 50% (2m 10s) 0.0243 Hlutkov / Russian √ 
```

# Training Process

105000 52% (2m 16s) 1.2543 Shu / Korean X (Chinese)   
110000 55% (2m 23s）0.3678 Thean / Chinese √   
115000 57% (2m 28s）0.8697 Medeiros / Portuguese √   
120000 60% (2m 35s) 2.3523 Miazga / Japanese X (Polish)   
125000 62% (2m 41s)0.1248 Malinowski / Polish √   
130000 65% (2m 48s）0.3051 Santana / Portuguese √   
135000 67% (2m 54s)4.7025 Samuel / Arabic X (Irish)   
140000 70% (3m 1s）0.1119 Morrison / Scottish √  
145000 72% (3m 7s）0.7417 Cremonesi / Italian √   
150000 75% (3m 14s) 1.6909 Moreno / Spanish X (Portuguese)   
155000 77% (3m 20s)1.5550 Jez / Chinese X (Polish)   
160000 80% (3m 27s) 4.0158 Chromy / Irish X (Czech)   
165000 82% (3m 33s)0.2522 O'Donnell / Irish √   
170000 85% (3m 40s)0.3419 Airaldi / Italian √   
175000 87% (3m 46s) 1.5858 Robles / Spanish √   
180000 90% (3m 53s)0.0202 Arnoni / Italian √   
185000 92% (3m 59s) 2.8040 Legg / Vietnamese X (English)   
190000 95% (4m 6s) 1.7104 Oliver / French X (Spanish)   
195000 97% (4m 12s)0.4689 Luc / Vietnamese √   
200000 100% (4m 18s） 5.7895 Tsoumada / Japanese X (Greek)

Training Loss   
![](images/8c086bd6b3158221232e5e1dbf1dde5a8e397292e56b5353c4c778d73d22247c.jpg)

<details>
<summary>line</summary>

| x    | y      |
| ---- | ------ |
| 0    | 1.27   |
| 25   | 1.23   |
| 50   | 1.18   |
| 75   | 1.19   |
| 100  | 1.16   |
| 125  | 1.17   |
| 150  | 1.14   |
| 175  | 1.15   |
| 200  | 1.16   |
</details>

Result   
![](images/f99455af63ef75b2caaf23e2dc6c9c34de6790672e48d59bf2105b947ed28b4c.jpg)

# Result

> Dovesky   
(-0.87) Russian   
(-0.96)Czech   
(-1.84）English   
> Wang   
(-0.58)Chinese   
(-1.42） Korean  
(-2.42）Scottish

> Jackson

(-1.35）English

(-1.59)Scottish

(-1.73）Czech

> Peterson

(-0.63)Scottish

(-1.75）Dutch

(-1.85）German

> Satoshi

(-0.83)Arabic

(-1.31)Italian

(-1.74） Japanese

> Abraham

(-1.47) Russian

(-1.64）English

(-2.00） Vietnamese