# AMA 564 Deep Learning

# 2026 Spring

# Lecture 11

Pretraining   
BERT   
PEFT

![](images/710d26ecfb626a33e315fba43a70ed077314450bbcdb2090b506c4ba24286e5c.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Unlabeled corpus from internet"] --> B["Base model, i.e., GPT-3 DeepSeek-V3-Base"]
    C["Conversations written by human"] --> D["Supervised fine-tuning (SFT)"]
    D --> E["SFT model"]
    F["Prompts written by human"] --> G["Reinforcement learning (RL)"]
    G --> H["RL model"]
    I["RL from human feedback (RLHF)"] --> J["Instruct model i.e., InstructGPT ChatGPT Qwen-Instruct"]
    K["Reasoning model i.e., GPT-o1 DeepSeek-R1 Kimi k1.5 QwQ"] --> H
```
</details>

Step1

Collect demonstration data, and train a supervised policy.

A prompt is sampled from our prompt dataset.

A labeler demonstrates the desired output behavior.

This data is used to fine-tune GPT-3 with supervised learning.

![](images/1d2028ab377319b5559c0954d78e12296df6148a97f6844c5600d000a457833c.jpg)

Explain the moon landing to a 6 year old

![](images/981270557373b41c604ba5d7311b7b19baac47c6b2e8a9249bf5387072fd97e7.jpg)

Some people went to the moon...

![](images/01841ef3d9e204cd28522d256b3e7b49afd28bf9bd3d3b0cca12da2522a41b79.jpg)  
自自目

Step 2

Collect comparison data, and train a reward model.

A prompt and several model outputs are sampled.

A labeler ranks the outputs from best to worst.

This data is used to train our reward model.

![](images/560a2d629aef239bd288dca548acb02c40b1e0a24233ce8a367c167708265784.jpg)

Explain the moon landing to a6 year old

![](images/12abd1f5aac0487d84af4caa9deb60d2bf3f9eec3700251af1c95f3a648f8591.jpg)

![](images/0059688fdc2ed37a1c063feedf722d3881df430c8c29b85f6422b5233b128b36.jpg)

![](images/acebfbbe77a763addbf929129598f425bce47fef89e402b3316a525daf8b2636.jpg)

melie ol\_

![](images/b3e4c48951879756bfa32563327c3386bebf37633cea5dd972ef2295d130aaf0.jpg)

Peeple went t the moon

![](images/f0961846b553931eba50fff7c3ae3d76805a432a4f4302aff171b6294ea21720.jpg)

![](images/dcc91cc6c83d46d384e69f3bc9d0175fa87cd1de2520986be88b0b03cacee0e1.jpg)

![](images/c8fb72e283a18d206cf53a8f935a4ce60a933e51da21d097bf0edc9b49bd5783.jpg)

RM   
![](images/c7d254d88776380cf76a4104d003d2ee9363710899e0385dbb74613926dbfcdf.jpg)

![](images/68c61c7ab68f5bfac769518e6ebe24842cd96dff27b5a888f8356a3e6da666a0.jpg)

Step 3

Optimize a policy against the reward model using reinforcement learning.

A new prompt is sampled from the dataset.

The policy generates an output.

The reward model calculates a reward for the output.

The reward is used to update the policy using PPO.

![](images/106bbb50c434114ae7ee54c9b2a47839b39f35710f697163a57a23deed228914.jpg)

about frogs

![](images/471a67ae52c6abcfd7b4c5638c80a93437e2a5a27dd00ae11c594b0dc0b92457.jpg)

Once upon a time...

![](images/1e5d18c4bfacfef1e25b75cd5265cba7b22c4bda0471a85bfe913d6ceb3cadd6.jpg)  
rk  
Figure 2: A diagram illustrating the three steps of our method: (1) supervised fine-tuning (SFT),(2) reward model (RM) training,and (3) reinforcement learning via proximal policy optimization (PPO) on this reward model. Blue arrows indicate that this data is used to train one of our models.In Step 2, boxes A-D are samples from our models that get ranked by labelers.See Sectionfor more details on our method.

# Pretraining

![](images/5d0316aabff0b700ed1ab0c154cf27fe7c366fe86469407a9f00b8899ed22c32.jpg)

<details>
<summary>line</summary>

| Date     | Models with highest EM | Other models |
| -------- | ---------------------- | ------------ |
| Jan '18  | 70                     | -            |
| Sep '18  | 75                     | -            |
| Jan '19  | 85                     | -            |
| May '19  | 88                     | -            |
| Sep '19  | 90                     | -            |
| Jan '20  | 90                     | -            |
| May '20  | 90                     | -            |
| Sep '20  | 90                     | -            |
| Jan '21  | 90                     | -            |
| May '21  | 90                     | -            |
</details>

Pretraining has had a major, tangible impact on how well NLP systems work

# Keys in pretraining:

1. Make sure your model can process large-scale, diverse datasets.   
2. Use unlabeled data.   
3. Compute-aware scaling.

Tokenizer   
![](images/dbd864fcdbe7b81b8bcaca6063ae3a76853bd9b8774b4ac9ee7d34801f2bdaee.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["unbelievable day!"] --> B["unbelievable"]
    A --> C["day"]
    A --> D["!"]
    E["Word-Base"] --> F["unbelievable day!"]
    F --> G["u n b e l i e v a b l e d a y !"]
    F --> H["Character-Based"]
    H --> I["unbelievable day!"]
    I --> J["un"]
    I --> K["bel"]
    I --> L["ievable"]
    I --> M["day"]
    I --> N["!"]
    O["Byte Pair Encoding"] --> P["unbelievable day!"]
    P --> Q["un"]
    P --> R["bel"]
    P --> S["ievable"]
    P --> T["day"]
    P --> U["!"]
    V["Splits text into words; simple but fails on rare words."] --> A
    W["Splits text into characters; flexible but lacks context."] --> E
    X["Bergles frequent pairs; balances flexibility and efficiency."] --> O
```
</details>

“Byte Pair Encoding (BPE) is a data compression technique that iteratively merges the most frequent pair of consecutive bytes (or characters) in a text or data sequence into a single, new symbol. The process is repeated until a specified number of merges is reached or no more frequent pairs remain”.

![](images/aa0d2ed15f550607cad6ded9de061d7c73b8fed6d0f472ed2a6c19a6af71d967.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Initialize Vocabulary"] --> B["Tokenize Text"]
    B --> C["Count Pair Frequencies"]
    C --> D{Merge Most Frequent Pair}
    D -->|No| C
    D -->|Yes| E["Final Vocabulary"]
    C --> F{Reached Vocabulary Size?}
    F -->|Yes| E
```
</details>

# Dictionary

5low   
2 lower   
6 newest   
3widest

5low   
2lower   
6 newest   
3widest

5low   
2lower   
6 newest   
3 widest

# Vocabulary

I, o, w,e, r,n,w, s,t,i, d

l,o, w,e,r,n,w, s,t,i, d,es

l,o,w,e,r，n,w,s,t,i,d,e,est

Common words end up being a part of the subword vocabulary, while rarer words are split into (sometimes intuitive, sometimes not) components.

![](images/75ed1fcd65d4fd8e0bbe5c007fa60575a5618ae970e6ffaa3aec4fb4ae175534.jpg)

![](images/d4b8a83472ed59a94900a8d867055f251d20fa248d36d54237088b0d220b00a0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["... the movie was ..."] --> B["Pretrained (word embeddings)"]
    C["Not pretrained"] --> D["Pretrained"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#cfc,stroke:#333
    style D fill:#fcc,stroke:#333
```
</details>

[Recall, movie gets the same word embedding, no matter what sentence it shows up in]

# Potential Issues:

1. The training data we have for our downstream task (like question answering) must be sufficient to teach all contextual aspects of language.   
2. Most of the parameters in our network are randomly initialized!

1. (Almost) all parameters in the networks are initialized via pretraining.   
2. Pretraining methods hide parts of the input from the model, and train the model to reconstruct those parts.

![](images/979b461f8074ab204c4a94952fd1198130d8a330c9c119c6155da5df4a919f83.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["... the movie was ..."] --> B["Pretrained jointly"]
    B --> C["Left side of red box with bidirectional arrows"]
    B --> D["Right side of red box with bidirectional arrows"]
    B --> E["Left side of red box with bidirectional arrows"]
    B --> F["Right side of red box with bidirectional arrows"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
```
</details>

[This model has learned how to represent entire sentences through pretraining]

# Step1: Pretrain (on language modeling)

Lots of text; learn general things!

![](images/8e0614fded2a90e4dd4bba72a553af84de696cf2fd6afceea41fc925a517f061.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Iroh"] --> B["goes"]
    B --> C["to"]
    C --> D["make"]
    D --> E["tasty"]
    E --> F["tea"]
    F --> G["END"]
    style A fill:#f9f,stroke:#333
    style G fill:#f9f,stroke:#333
    note1["(Transformer, LSTM, ++)"]
    note2["goes"] --> note1
    note3["to"] --> note2
    note4["make"] --> note3
    note5["tasty"] --> note4
    note6["tea"] --> note5
    note7["END"] --> note6
```
</details>

# Step 2: Finetune (on your task)

Not many labels; adapt to the task!

![](images/41b5934dff5ad0982bd4a4591ec6050f0b8e8516d344e94232f81d480405427d.jpg)

<details>
<summary>text_image</summary>

(Transformer, LSTM, ++ )
... the movie was ...
</details>

CompositionofthePilebyCategory   
![](images/dc5b6514f562b1bf3b2a6fff45e8a157e23f7e22d21a817ea6f97d63d0be55ce.jpg)

<table><tr><td>Model</td><td>Training Data</td></tr><tr><td>BERT</td><td>BookCorpus, English Wikipedia</td></tr><tr><td>GPT-1</td><td>BookCorpus</td></tr><tr><td>GPT-3</td><td>CommonCrawl, WebText, English Wikipedia, and 2 book databases (“Books 1” and “Books 2”)</td></tr><tr><td>GPT-3.5+</td><td>Undisclosed</td></tr></table>

![](images/b56a85c31f934db13ac2372995c36bb735ac7ea99982873ed3b3b3f9b6f2ccab.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Layer"] --> B["Hidden Layer 1"]
    A --> C["Hidden Layer 2"]
    B --> D["Output Layer"]
    C --> D
    D --> E["Output Layer"]
    style A fill:#f9f,stroke:#333
    style E fill:#bbf,stroke:#333
```
</details>

# Encoders

Gets bidirectional context -can condition on future!   
. How do we train them to build strong representations?

![](images/14241084c6d5c138e8cdc9d41757e61b3e2545a70a84e303016141fd97469302.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Layer"] --> B["Hidden Layer"]
    B --> C["Output Layer"]
    style A fill:#f9f,stroke:#333
    style C fill:#bbf,stroke:#333
```
</details>

# Encoder-Decoders

Good parts of decoders and encoders?   
What's the best way to pretrain them?

![](images/d35fdbc0bdb462af671dc380d36a4dbb8853dbf5e9f97005996d7d843ac9c112.jpg)

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
    DB[" "] --> DJ
    DB --> CK[" "]
    DB --> DL
    DB --> DK
    DB --> DL
    DB --> CK
    DB --> DL
    DB --> DK
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DW
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> DN
    DB --> BN
    DB --> BN
    DB --> BN
    DB --> BN
    DB --> BN
    DB --> BN
    DB --> BN
    DB --> BN
    DB --> BN
    DB --> BN
    DB --> BN
```
</details>

# Decoders

Language models! What we've seen so far.   
Nice to generate from; can't condition on future words

# BERT

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). Bert: Pre-training of deep bidirectional transformers for language understanding. NAACL.

Google citation: 127375

![](images/55bacc5d85e885412adb1347c0a9bf1f3f4dd8455a18907f4a3b72d62b27f21c.jpg)

<details>
<summary>text_image</summary>

NLP
BERT、GPT
Transformer
Attention
</details>

Suggested reading: The Illustrated BERT, ELMo, and co.

of text (books, wikipedia..etc).

![](images/f99549907f764b3f9064934485084d739ec7571ee5149739a3eaa751dc8af979.jpg)

<details>
<summary>text_image</summary>

Model:
BERT
Dataset:
WIKIPEDIA
Die freie Enzyklopädie
Objective:
Predict the masked word
(langauge modeling)
</details>

labeled dataset.

![](images/3bae6d9e876f5c9dbd90ae6965bebdf912a3288c818f67fa6cb7a066dbf65390.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Classifier"] -->|75% Spam, 25% Not Spam| B["Model: pre-trained in step #1"]
    B --> C["BERT"]
    C --> D["Email message"]
    D --> E["Buy these pills"]
    D --> F["Win cash prizes"]
    D --> G["Dear Mr. Atreides, please find attached..."]
    H["Class"] --> I["Spam"]
    H --> J["Spam"]
    H --> K["Not Spam"]
```
</details>

![](images/a7d22db7e94b6112f9669724ada88711b4ce0f9206f12a9583b4f5143d2b3d9b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph_Pre-training["Pre-training"]
        A1["NSP"] --> B1["BERT"]
        A2["Mask LM"] --> B1
        A3["Mask LM"] --> B1
        B1 --> C1["C"]
        B1 --> C2["T₁"]
        B1 --> C3["..."]
        B1 --> C4["Tₙ"]
        B1 --> C5["T_[SEP"]]
        B1 --> C6["T₁'"]
        B1 --> C7["..."]
        B1 --> C8["Tₘ'"]
        B1 --> C9["Tₘ'"]
    end

    subgraph_Fine-Tuning["Fine-Tuning"]
        D1["MNLI"] --> E1["NER"]
        D2["SQuAD"] --> E2["SQuAD"]
        D3["BERT"] --> E3["BERT"]
        D4["Question"] --> E4["E_[CLS"]]
        D5["Paragraph"] --> E5["E_1"]
        D6["Question Answer Pair"] --> E6["E_N"]
        D7["Question Answer Pair"] --> E7["E_[SEP"]]
        D8["Question Answer Pair"] --> E8["E_1'"]
        D9["Question Answer Pair"] --> E9["E_M'"]
    end

    style Pre-training fill:#f9f,stroke:#333
    style Fine-Tuning fill:#bbf,stroke:#333
```
</details>

Pretraining with encoders only! But encoders get bidirectional context, so we can’t do language modeling!

replace some fraction of words in the input with a special [MASK] token; predict these words. Masking 15% words randomly.

Replace input word with [MASK] 80% of the time.   
Replace input word with a random token 10% of the time.   
• Leave input word unchanged 10% of the time (but still predict it!).

![](images/118b731e9ae5b5d3a78b64bb6691e1cf24bf576fcff82648e27a2edc44fd55a5.jpg)

<details>
<summary>bar_stacked</summary>

| Position | Aardvark (%) | Improvisation (%) | Zyzzyva (%) |
| -------- | ------------ | ----------------- | ----------- |
| 1        | 0.1          | 10                | 0           |
| 2        | 0.1          | 10                | 0           |
| 3        | 0.1          | 10                | 0           |
| 4        | 0.1          | 10                | 0           |
| 5        | 0.1          | 10                | 0           |
| 6        | 0.1          | 10                | 0           |
| 7        | 0.1          | 10                | 0           |
| 8        | 0.1          | 10                | 0           |
| ...      | ...          | ...               | ...         |
| 512      | ...          | ...               | ...         |
| Randomly mask 15% of tokens | 1            | 1                 | 1           |
| Randomly mask 15% of tokens | 2            | 2                 | 2           |
| Randomly mask 15% of tokens | 3            | 3                 | 3           |
| Randomly mask 15% of tokens | 4            | 4                 | 4           |
| Randomly mask 15% of tokens | 5            | 5                 | 5           |
| Randomly mask 15% of tokens | 6            | 6                 | 6           |
| Randomly mask 15% of tokens | 7            | 7                 | 7           |
| Randomly mask 15% of tokens | 8            | 8                 | 8           |
| Randomly mask 15% of tokens | ...          | ...               | ...         |
| Input    | ...          | ...               | ...         |
| Note: Input values are not explicitly labeled; they are estimated based on the code execution.
</details>

# Ideas for Pretraining BERT: Masking

replace some fraction of words in the input with a special [MASK] token; predict these words.

$$
\begin{array}{l} h _ {1}, \dots , h _ {T} = \operatorname{Encoder} (w _ {1}, \dots , w _ {T}) \\ y _ {i} \sim A h _ {i} + b \\ \end{array}
$$

If ????� is the masked version of $x ,$ we will learn

$$
p _ {\theta} (x | \tilde {x})
$$

via the masked Language Model.

![](images/f7d56bd6ef66fc63f73d5eeb938b85130f5429b3fd378ada130743a12b26a069.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph Input Layer
        I["Input Layer I"] --> H1["[M"]]
        H1 --> H2["to"]
        H2 --> H3["the"]
        H3 --> H4["[M"]]
    end
    subgraph Hidden Layer
        H1 --> H5["[M"]]
        H5 --> H6["to"]
        H6 --> H7["the"]
        H7 --> H8["[M"]]
    end
    subgraph Output Layer
        H5 --> H9["[M"]]
        H9 --> H10["to"]
        H10 --> H11["the"]
        H11 --> H12["[M"]]
    end
    subgraph Storage Layer
        H9 --> H13["[M"]]
        H13 --> H14["to"]
        H14 --> H15["the"]
        H15 --> H16["[M"]]
    end
    I -->|went| A["Input Layer A,b"]
    H1 -->|went| B["Input Layer b"]
    H2 -->|went| C["Input Layer c"]
    H3 -->|went| D["Input Layer d"]
    H4 -->|went| E["Input Layer e"]
    H5 -->|went| F["Input Layer f"]
    H6 -->|went| G["Input Layer g"]
    H7 -->|went| H["Input Layer h"]
    H8 -->|went| I["Input Layer i"]
    H9 -->|went| J["Input Layer j"]
    H10 -->|went| K["Input Layer k"]
    H11 -->|went| L["Input Layer l"]
    H12 -->|went| M["Input Layer m"]
    H13 -->|went| N["Input Layer n"]
    H14 -->|went| O["Input Layer o"]
    H15 -->|went| P["Input Layer p"]
    H16 -->|went| Q["Input Layer q"]
    H17 -->|went| R["Input Layer r"]
    H18 -->|went| S["Input Layer s"]
    H19 -->|went| T["Input Layer t"]
    H20 -->|went| U["Input Layer u"]
    H21 -->|went| V["Input Layer v"]
    H22 -->|went| W["Input Layer w"]
    H23 -->|went| X["Input Layer x"]
    H24 -->|went| Y["Input Layer y"]
    H25 -->|went| Z["Input Layer z"]
    H26 -->|went| AA["Input Layer a"]
    H27 -->|went| AB["Input Layer b"]
    H28 -->|went| AC["Input Layer c"]
    H29 -->|went| AD["Input Layer d"]
    H30 -->|went| AE["Input Layer e"]
    H31 -->|went| AF["Input Layer f"]
    H32 -->|went| AG["Input Layer g"]
    H33 -->|went| AH["Input Layer h"]
    H34 -->|went| AI["Input Layer i"]
    H35 -->|went| AJ["Input Layer j"]
    H36 -->|went| AK["Input Layer k"]
    H37 -->|went| AL["Input Layer l"]
    H38 -->|went| AM["Input Layer m"]
    H39 -->|went| AN["Input Layer n"]
    H40 -->|went| AO["Input Layer o"]
```
</details>

# Ideas for Pretraining BERT: Two Sentences Task

To make BERT better at handling relationships between multiple sentences, the pretraining process includes an additional task: Given two sentences (A and B), is B likely to be the sentence that follows A, or not?

![](images/3261b76ede733bdf3e4dcf071ac7aa75fb1d3a4767937b0878955ae25058d673.jpg)

<details>
<summary>bar_stacked</summary>

| Input | Tokenized Input | Percentage |
|-------|-----------------|----------|
| Input | Sentence A      | 1%       |
| Input | Sentence B      | 99%      |
</details>

# Ideas for Pretraining BERT: Two Sentences Task

To make BERT better at handling relationships between multiple sentences, the pretraining process includes an additional task: Given two sentences (A and B), is B likely to be the sentence that follows A, or not?

The pretraining input to BERT was two separate contiguous chunks of text:   
![](images/9581b8228eec4be5ceb9bfa581379f3242166a7ce61f9c1227718172160c481b.jpg)

<details>
<summary>other</summary>

| Input | [CLS] | my | dog | is | cute | [SEP] | he | likes | play | ##ing | [SEP] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Token Embeddings | E[CLS] | Emy | Edog | Eis | Ecute | E[SEP] | Ehe | Elikes | Eplay | En-ing | E[SEP] |
| Segment Embeddings | EA | EA | EA | EA | EA | EA | EB | EB | EB | EB | EB |
| Position Embeddings | E0 | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 | E9 | E10 |
</details>

Two models were released:

·BERT-base: 12 layers,768-dim hidden states,12 attention heads,110 millon params.   
· BERT-large: 24layers,1024-dim hidden states,16 attention heads,340 millon params.

Trained on:

BooksCorpus (800 million words)   
English Wikipedia (2,500 million words)

Pretraining is expensive and impractical on a single GPU.

BERT was pretrained with 64 TPU chips for a total of 4 days.   
(TPUs are special tensor operation acceleration hardware)

Finetuning is practical and common on a single GPU

"Pretrain once, finetune many times."

BERT was massively popular and hugely versatile; finetuning BERT led to new state-ofthe-art results on a broad range of tasks.

QQP:Quora Question Pairs (detect paraphrase · questions)   
QNLI: natural language inference over question· answering data   
SST-2: sentiment analysis

CoLA: corpus of linguistic acceptability (detect whether sentences are grammatical.)

STS-B: semantic textual similarity

MRPC: microsoft paraphrase corpus   
RTE: a small natural language inference corpus

<table><tr><td>System</td><td>MNLI-(m/mm)392k</td><td>QQP363k</td><td>QNLI108k</td><td>SST-267k</td><td>CoLA8.5k</td><td>STS-B5.7k</td><td>MRPC3.5k</td><td>RTE2.5k</td><td>Average-</td></tr><tr><td>Pre-OpenAI SOTA</td><td>80.6/80.1</td><td>66.1</td><td>82.3</td><td>93.2</td><td>35.0</td><td>81.0</td><td>86.0</td><td>61.7</td><td>74.0</td></tr><tr><td>BiLSTM+ELMo+Attn</td><td>76.4/76.1</td><td>64.8</td><td>79.8</td><td>90.4</td><td>36.0</td><td>73.3</td><td>84.9</td><td>56.8</td><td>71.0</td></tr><tr><td>OpenAI GPT</td><td>82.1/81.4</td><td>70.3</td><td>87.4</td><td>91.3</td><td>45.4</td><td>80.0</td><td>82.3</td><td>56.0</td><td>75.1</td></tr><tr><td>BERTBASE</td><td>84.6/83.4</td><td>71.2</td><td>90.5</td><td>93.5</td><td>52.1</td><td>85.8</td><td>88.9</td><td>66.4</td><td>79.6</td></tr><tr><td>BERTLARGE</td><td>86.7/85.9</td><td>72.1</td><td>92.7</td><td>94.9</td><td>60.5</td><td>86.5</td><td>89.3</td><td>70.1</td><td>82.1</td></tr></table>

# Parameter-Efficient Fine-Tuning

Sparse Subnetworks   
Low-rank Composition

![](images/09a2a10ef43c0810fa0a3181db345c8182c5c62c1922227df65426ed8f4c365b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Processing Unit"] --> B["Model 1"]
    B --> C["Pixelated Output 1"]
    B --> D["Pixelated Output 2"]
    B --> E["Pixelated Output 3"]
    C --> F["Output Visualization"]
    D --> F
    E --> F
    F --> G["Output Visualization"]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bfb,stroke:#333
    style D fill:#ffb,stroke:#333
    style E fill:#fbb,stroke:#333
    style F fill:#fff,stroke:#333
    style G fill:#fff,stroke:#333
```
</details>

. During pruning,a fraction of the lowest-magnitude weights are removed   
The non-pruned weights are re-trained   
· Pruning for multiple iterations is more common (Frankle & Carbin,2019)

![](images/96ad2f47082a6ce3a6043b8b39a3aa0b5ec054d2cdd8537fe23ba66c584fb67f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Initial training"] -->|Pruning| B["Re-training"]
    B -->|Pruning| C["..."]
    C --> D["Re-training"]
    subgraph One-shot pruning
        E["One-shot nodes with connections"]
        F["One-shot nodes with connections"]
        G["One-shot nodes with connections"]
        H["One-shot nodes with connections"]
    end
    subgraph Iterative pruning
        I["Iterative nodes with connections"]
        J["Iterative nodes with connections"]
        K["Iterative nodes with connections"]
    end
```
</details>

# The Lottery Ticket Hypothesis

Dense,randomly-initialized models contain subnetworks("winning tickets") that一 when trained in isolation一reach test accuracy comparable to the original network in a similar number of iterations [Frankle& Carbin, 2019]

√ Sparse Subnetworks   
Low-rank Composition

![](images/d4d7d7b51ce9827e71e194a8d96cefcf5264af99fea0863e2dcc3b1027cb34f5.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Module"] --> B["Module 1"]
    B --> C["Component Unit"]
    C --> D["Output Module"]
    D --> E["Pixelated Output Module"]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bfb,stroke:#333
    style D fill:#ffb,stroke:#333
    style E fill:#dfd,stroke:#333
```
</details>

Assume we have a pre-trained autoregressive language model $P _ { \phi } ( y | x )$

· E.g., GPT based on Transformer

. Adapt this pretrained model to downstream tasks (e.g., summarization, NL2SQL, reading comprehension)

· Training dataset ofcontext-target pairs $\{ ( x _ { i } , y _ { i } ) \} _ { i = 1 , \dots , N }$

. During fullfine-tuning,we update $\phi _ { o }$ to $\phi _ { o } + \Delta \phi$ by following the gradient to maximize the conditional language modeling objective

$$
\max _ {\phi} \sum_ {(x, y)} \sum_ {t = 1} ^ {| y |} \log (P _ {\phi} (y _ {t} | x, y _ {<   t}))
$$

Hu, E. J., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., & Chen, W. LoRA: Low-Rank Adaptation of Large Language Models. In International Conference on Learning Representations, 2021.

Google citation: 12416

. For each downstream task,we learn a different set of parameters $\Delta \phi$

$| \Delta \phi | = | \phi _ { o } |$   
GPT-3 has a $\mid \phi _ { o } \mid$ of 175 billion   
· Expensive and challenging for storing and deploying many independent instances

Key idea: encode the task-specific parameter increment $\Delta \phi = \Delta \phi ( \Theta )$ by a smaller-sized set of parameters 0, $| \Theta | \ll | \phi _ { o }$

The task of finding $\Delta \phi$ becomes optimizing over 0

$$
\max _ {\Theta} \sum_ {(x, y)} \sum_ {t = 1} ^ {| y |} \log (P _ {\phi_ {o} + \Delta \phi (\Theta)} (y _ {t} | x, y _ {<   t}))
$$

Updates to the weights have a low“intrinsic rank" during adaptation (Aghajanyan et al.2020)   
$W _ { 0 } \in \mathbb { R } ^ { d \times k }$ : a pretrained weight matrix Constrain its update with a low-rank decomposition:

$$
W _ {0} + \Delta W = W _ {0} + \alpha B A
$$

where $B \in \mathbb { R } ^ { d \times r } , A \in \mathbb { R } ^ { r \times k } , r \ll \operatorname* { m i n } ( d , k )$

α is the tradeoff between pre-trained "knowledge"and task-specific “knowledge"   
Only A and B contain trainable parameters

![](images/ce39e2de60cf568d04971f7e2c77ddb74e73e86892aadf0048791c1572cb77cf.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["h"] --> B["Pretrained Weights W ∈ ℝ^{d×d}"]
    B --> C["B = 0"]
    C --> D["r"]
    D --> E["A = N(0, σ²)"]
    E --> F["d"]
    F --> G["x"]
    G --> H["Output"]
```
</details>

Few-shot learner: In-Context Learning   
Instruction Fine-tuning   
RLHF

# The blessings of scale

Altraining runs,estimated computing resources used

Floating-pointoperations,selectedsystems,bytype,logsale

![](images/0ae29a6e237f2e1ef5ac727b15f85208b47db18240440eb35a532d0cf0c39275.jpg)

<details>
<summary>scatter</summary>

| Model        | Value     |
| ------------ | --------- |
| PaLM (540B)  | ~10^24    |
| LaMDA        | ~10^23    |
| GPT-3        | ~10^23    |
| DALL-E       | ~10^22    |
| GPT-2        | ~10^22    |
| BERT-Large   | ~10^21    |
| NPLM         | ~10^18    |
| NetTalk      | ~10^16    |
| Neocognitron | ~10^15    |
| ADALINE      | ~10^14    |
| Theseus      | ~1        |
</details>

![](images/994b0018fe4b92baf8e73d118de2e765cac39f85a89acb86535d6a13dae3d3ab.jpg)

<100 Million

3 Billion

13 y.0. Human

BERT (2018)

30 Billion RoBERTa (2019)

200 Billion

1.4 Trillion

Chinchilla(2022)

\# tokens seen during training

# Math Problems

Wecan describe circles in thexy-plane using equations in terms ofxand y. Circleequationsquestionsrequireus to understand the connection between theseequationsandthe featuresof circles.

Forexample,theequation $( x + 2 ) ^ { 2 } + ( y - 3 ) ^ { 2 } = 4 ^ { 2 }$ is graphedin thecy-plane below.It isa circle withacenterat(-2,3)andaradiusof4.

# Coding Problems

```typescript
// Determine whether the sentiment of text is positive
// Use a web service
async function isPositive(text: string): Promise<boollean> {
    const response = await fetch(`http://text-processing.com/api/sentiment/`, {
    method: "POST",
    body: `text=${text Clark},
    headers: {
    "Content-Type": "application/x-www-form-urlencoded",
    },
    });
    const json = await response.json();
    return json.label === "pos";
} 
```

# Planning

Ineed to throwa dinner party for 6 people who are vegetarian. Can you suggest a 3-course menu with a chocolate dessert?

Sure,l can suggest a 3-course menu with a chocolate dessert for your vegetarian dinner party.Hereare some possible options:

· Starter:Wild Mushroom Tartlets with Onion Sauceor Vegan Popcorn Tofu Nuggets 2   
· Main: Vegan Butternut Squash Mac 2 or Vegetarian Three-Bean Chili   
· Dessert: Chocolate Lava Cake 4or Chocolate Pasta with Chocolate Hazelnut Cream Sauce, White Chocolate Shavings,and Fresh Berries4

I hope this helps you plan your party. Enjoy! O

Learn more:1.booths.co.uk+10 more

How do we get from

The Hong Kong Polytechnic University is located in

to

What can lhelp with?   
![](images/437f797cea7408214cbaed6db7cde8abc1888d823b37e832fc425112bb4af91b.jpg)

<details>
<summary>text_image</summary>

Message ChatGPT
+ Search ...
Create image Summarize text Make a plan Get advice More
</details>

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). Language models are few-shot learners. Advances in neural information processing systems, 33, 1877-1901.

Google citation: 43367

# GPT-3 (175B parameters; Brown et al., 2020)

Another increase in size (1.5B -> 175B)   
and data (40GB -> over 600GB)

Specify a task by simply prepending examples of the task before your example   
. Also called in-context learning, to stress that no gradient updates are performed when learning a new task (there is aseparate literature on few-shot learning with gradient updates)

![](images/fcdeae62989286b7c05c07eb461f2e318365a054c46636dd0da40c79c1414e81.jpg)

<details>
<summary>text_image</summary>

1 gaot => goat
2 sakne => snake
3 brid => bird
4 fsih => fish
5 dcuk => duck
6 cmihp => chimp
In-context learning
1 thanks => merci
2 hello => bonjour
3 mint => menthe
4 wall => mur
5 otter => loutre
6 bread => pain
In-context learning
</details>

# Zero-shot

In-Context Learning on SuperGLUE   
![](images/4e73569d974db2fe7c059412c77e76615e6c19acc58b85b5e0dda22ee8e2775d.jpg)

<details>
<summary>line</summary>

| Number of Examples in Context (K) | Value |
| --------------------------------- | ----- |
| 0                                 | 58    |
| 1                                 | 69    |
| 2                                 | 69    |
| 3                                 | 69    |
| 4                                 | 70    |
| 8                                 | 72    |
| 16                                | 73    |
| 32                                | 74    |
</details>

# One-shot

In-Context Learning on SuperGLUE   
![](images/41be1b5fd01475c96f98bd6035c29b5261f1800889e2abe73a643c05312f6f65.jpg)

<details>
<summary>line</summary>

| Number of Examples in Context (K) | Value |
| --------------------------------- | ----- |
| 0                                 | 58    |
| 1                                 | 69    |
| 2                                 | 69    |
| 3                                 | 69    |
| 4                                 | 70    |
| 8                                 | 72    |
| 16                                | 73    |
| 32                                | 74    |
</details>

# Few-shot

In-Context Learning on SuperGLUE   
![](images/84ea437c5c55122f17eb489b493539795117dc2baee5fe9cb3f2a5f483e18c8d.jpg)

<details>
<summary>line</summary>

| Number of Examples in Context (K) | Few-shot GPT-3 175B |
| --------------------------------- | ------------------- |
| 0                                 | 58                  |
| 1                                 | 69                  |
| 2                                 | 69                  |
| 3                                 | 69                  |
| 4                                 | 70                  |
| 8                                 | 72                  |
| 16                                | 73                  |
| 32                                | 74                  |
</details>

Zero/few-shot prompting   
```txt
Translate English to French:
sea otter => loutre de mer
peppermint => menthe poivrée
plush girafe => girafe peluche
cheese => 
```

Traditional fine-tuning   
```txt
1 sea otter => loutre de mer
    ↓
    gradient update
    ↓
1 peppermint => menthe poivrée
    ↓
    gradient update
    ↓
    • • •
    ↓
1 cheese => 
```

Some tasks seem too hard for even large LMs to learn through prompting alone.

Especially tasks involving richer, multi-step reasoning.

(Humans struggle at these tasks too!)

$$
\begin{array}{l} 1 9 5 8 3 + 2 9 5 3 4 = 4 9 1 1 7 \\ 9 8 3 9 4 + 4 9 3 8 4 = 1 4 7 7 7 8 \\ 2 9 3 8 2 + 1 2 3 4 7 = 4 1 7 2 9 \\ 9 3 8 4 7 + 3 9 2 9 9 = ? \\ \end{array}
$$

Solution: Change the prompt!!!

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., ... & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35, 24824-24837.

Google citation: 12853

# Standard Prompting

# Model Input

Q:Roger has 5 tennis balls.He buys2 more cans of tennis bals. Each can has 3 tennis balls. How many tennis balls does he have now?

A: The answer is 11.

Q: The cafeteria had 23 apples.If they used 20 to make lunch and bought6 more,how many apples do they have？

# Model Output

A: The answer is 27.

![](images/5c88e232645b91248b36a9adeec59fb4ed957611cd5820c5529cb1dcf9fa4f11.jpg)

# Chain-of-Thought Prompting

# Model Input

Q: Roger has 5 tennis balls.He buys2 more cans of tennis balls.Each can has3 tennis balls.Howmany tennis balls does he havenow?

A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 5 + 6 = 11. The answer is 11.

Q: The cafeteria had 23 apples.If they used 20 to make lunch and bought 6 more,how many apples do they have?

# Model Output

A: The cafeteria had 23 apples originally. They used 20 to make lunch. So they had 23 - 20 = 3. They bought 6 more apples, so they have 3 + 6 = 9. The answer is 9.

Middle school math word problems   
![](images/63f67456c1278b2749c0b4149d0ecc4f30060764923c5ff791d13c2e2105bf8f.jpg)

-— Standard prompung   
Chain-of-thought prompting   
Prior supervised best

Model scale (# parameters in billions)

# Model Input

Q: Roger has 5 tennis bals. He buys 2 more cans of tennis balls.Each can has 3 tennis balls.Howmany tennis balls does he have now?

A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 5 + 6 = 11. The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?

# Model Output

A: The cafeteria had 23 apples originally. They used 20 to make lunch. So they had 23 - 20 = 3. They bought6 more apples, so they have 3+6=9.The answer is 9.

Q: A juggler can juggle 16 bals. Half of the balls are golf balls,and half of the golf balls are blue. How many blue golf balls are there?

A: Let's think step by step. There are 16 balls in total. Half of the balls are golf balls. That means there are 8 golf balls. Half of the golf balls are blue.That means there are 4 blue golf balls.

<table><tr><td>No.</td><td>Category</td><td>Zero-shot CoT Trigger Prompt</td><td>Accuracy</td></tr><tr><td>1</td><td>LM-Designed</td><td>Let&#x27;s work this out in a step by step way to be sure we have the right answer.</td><td>82.0</td></tr><tr><td>2</td><td rowspan="4">Human-Designed</td><td>Let&#x27;s think step by step. (*1)</td><td>78.7</td></tr><tr><td>3</td><td>First, (*2)</td><td>77.3</td></tr><tr><td>4</td><td>Let&#x27;s think about this logically.</td><td>74.5</td></tr><tr><td>5</td><td>Let&#x27;s solve this problem by splitting it into steps. (*3)</td><td>72.2</td></tr><tr><td>6</td><td rowspan="5"><img src="images/df7201e4fe3dc10933d0db1c856320185ccec4ad7dab11f69b45a6fbfd0ad037.jpg"/></td><td>Let&#x27;s be realistic and think step by step.</td><td>70.8</td></tr><tr><td>7</td><td>Let&#x27;s think like a detective step by step.</td><td>70.3</td></tr><tr><td>8</td><td>Let&#x27;s think</td><td>57.5</td></tr><tr><td>9</td><td>Before we dive into the answer,</td><td>55.7</td></tr><tr><td>10</td><td>The answer is after the proof.</td><td>45.7</td></tr><tr><td>-</td><td></td><td>(Zero-shot)</td><td>17.7</td></tr></table>

WIKIPEDIA The Free Encyclopedia

![](images/8857d444ead129d5ead2c7417d45a0b92d1568021fe27a181f00f494f599e85c.jpg)

# Prompt engineering

文A 5 languages

Article

More

FromWikipedia,the free encyclopedia

Prompt engineering is a concept in artificial intelligence, particularly natural language processing (NLP). In prompt engineering, the description of the task is

# Prompt Engineerand Librarian

# Pros:

No finetuning needed, prompt engineering (e.g. CoT) can improve performance.

# Cons:

Limits to what you can fit in context   
Complex tasks will probably need gradient steps

Few-shot learner: In-Context Learning   
Instruction Fine-tuning   
RLHF

Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., ... & Lowe, R. (2022). Training language models to follow instructions with human feedback. Advances in neural information processing systems, 35, 27730-27744. Google citation: 13430

PROMPT Explain the moon landing to a 6 year old in a few sentences.

COMPLETIONGPT-3

Explain the theory of gravity to a 6 year old.

Explain the theory of relativity to a 6 year old in a few sentences.

Explain the big bang theory to a 6 year old.

Explain evolution to a 6 year old.

Language models are not aligned with user intent [Ouyang et al.\_2022]

Finetuning to the rescue!

# PROMPT

Explain the moon landing to a 6 year old in a few sentences.

# COMPLETION

# Human

A giant rocket ship blasted offrom Earth carrying astronauts to the moon. The astronauts landed their spaceship on the moon and walked around exploring the lunar surface. Then they returned safely back to Earth, bringing home moon rocks to show everyone.

Language models are not aligned with user intent [Ouyang et al.\_ 2022]

Finetuning to the rescue!

# The Modern Pretraining/Fine-tuning Paradigm

# Step1: Pretrain (on language modeling)

Lots of text; learn general things!

![](images/2e30df6d3817fe5224047e676dd6b7f2bfbe7ce34398af57e56724bbe4d67c6c.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Iroh"] --> B["goes"]
    B --> C["to"]
    C --> D["make"]
    D --> E["tasty"]
    E --> F["tea"]
    F --> G["END"]
    style A fill:#ff0000,stroke:#333
    style G fill:#ff0000,stroke:#333
    note1["(Transformer, LSTM, ++)"]
    note2["goes"] --> note1
    note3["to"] --> note2
    note4["make"] --> note3
    note5["tasty"] --> note4
    note6["tea"] --> note5
```
</details>

# Step 2: Finetune (on your task)

Not many labels; adapt to the task!

![](images/e023be971d580687afc96f745f2b6be2e1654554505e000c158ae7893b2cd7fc.jpg)

<details>
<summary>text_image</summary>

(Transformer, LSTM, ++ )
... the movie was ...
</details>

Pretraining can improve NLP applications by serving as parameter initialization.

Step 1: Pretrain (on language modeling)

Lots of text; learn general things!

![](images/25dc5bdf2b7ccb54cadf213d9c6ae7ec8421c948fe2c1cb16f57342a81483768.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["goes"] --> B["to"]
    B --> C["make"]
    C --> D["tasty"]
    D --> E["tea"]
    E --> F["END"]
    G["Iroh"] --> H["goes"]
    H --> I["to"]
    I --> J["make"]
    J --> K["tasty"]
    K --> L["tea"]
```
</details>

Step 2: Finetune (on many tasks)

Net many labels; adapt to the tasks!

![](images/82f713613ab46f8dad7c89714dbcbffdbd6f1e040dc8ba0290ac981184504e51.jpg)

<details>
<summary>text_image</summary>

Decoder
(Transformer, LSTM, ++ )
</details>

... the movie was...

Collect examples of (instruction,output) pairs across many tasks and finetune an LM

![](images/dfb31598624a11d5ed8e72e296ea2072fa81ac02f6a637e5b6008ea0531974bf.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Please answer the following question.<br>What is the boiling point of Nitrogen?"] --> B["Answer the following question by reasoning step-by-step.<br>The cafeteria had 23 apples. If they used 20 for lunch and bought 6 more, how many apples do they have?"]
    C["-320.4F"] --> D["The cafeteria had 23 apples originally. They used 20 to make lunch. So they had 23 - 20 = 3. They bought 6 more apples, so they have 3 + 6 = 9."]
    B --> E["Language model"]
    D --> E
```
</details>

Evaluate on unseen tasks

Q: Can Geoffrey Hinton have a conversation with George Washington? Give the rationale before answering.

Geoffrey Hinton isa British-Canadian computer scientist born in 1947.George Washingtondiedin 1799.Thus,they could not have had a conversation together.So the answer is"no".

[FLAN-T5; Chung et al., 2022]

![](images/c2bc77c8b23aa68385047202733d4105502ef52d1e8ca254788527f63d6501a9.jpg)  
(a) SUP-NATINST (this work)

![](images/9d5905e293596c6ad81211c30dadb770ba885fb2af23613fe191a0660e81775d.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Answer Generation"] --> B["Classification"]
    C["Mineral Text Modification"] --> D["Question Generation"]
    E["Answer Generation"] --> F["Classification"]
    G["Input"] --> A
```
</details>

(b) NATINST

![](images/2b405b38671d9b7502d395e2c3cae275c91900db8fa9bcce5b7a6a42e1cb6f79.jpg)

<details>
<summary>bubble</summary>

| Category | Value |
|---|---|
| QA Multiple Choice | 100 |
| QA Extractive | 85 |
| Blue and Fairness | 70 |
| QA Closed Book | 65 |
| Bond Options | 60 |
| Investment | 55 |
| Tax Classification | 50 |
| Real Estate | 45 |
| Housing & Other | 40 |
| Fundraising | 35 |
| Communication | 30 |
| Financial Services | 25 |
| Insurance | 20 |
</details>

(C) PROMPTSOURCE (TO subset)

![](images/1faa7ab7ee25891b5f330cbff37cc94575c77480e9cc5fb1ed6ad8fa26558e65.jpg)

<details>
<summary>bubble</summary>

| Category | Value |
|---|---|
| Summarization | 100 |
| Translation | 85 |
| Mac | 70 |
| Speech | 60 |
| Other | 55 |
| Social Work | 50 |
| Social Work (Other) | 45 |
| Other | 40 |
| Other | 35 |
| Other | 30 |
| Other | 25 |
| Other | 20 |
| Other | 15 |
| Other | 10 |
| Other | 5 |
| Other | 0 |
</details>

(d) FLAN

![](images/2c08b2b22b632268f2dff35b497637672e47ccf11a19be426066cfd6a28f5309.jpg)

<details>
<summary>bubble</summary>

| Category | Value |
|---|---|
| Generation | 100 |
| Enzyming | 35 |
| Close CA | 40 |
| Enzymation | 25 |
| Natural Species | 15 |
| Natural Species (Other) | 10 |
| Natural Species (Other) | 8 |
| Natural Species (Other) | 7 |
| Natural Species (Other) | 6 |
| Natural Species (Other) | 5 |
| Natural Species (Other) | 4 |
| Natural Species (Other) | 3 |
| Natural Species (Other) | 2 |
| Natural Species (Other) | 1 |
| Natural Species (Other) | 0.5 |
</details>

(e) INSTRUCTGPT   
Figure 2: Compared to other datasets, Sup-NATINsT covers a more diverse range of task types. InstructGPT reports a very coarse categorization of their task types. Bubble size represents the number of tasks ofeach type in log scale.

As is usually the case, data + model scale iskey for this to work!   
Super-Naturallnstructions dataset contains over 1.6K tasks, 3M+ examples

Classification,sequence tagging, rewriting, translation, QA..

Q: how do we evaluate such a model?

# Massive Multitask Language Understanding (MMLU)

[Hendrycks et al., 2021]

New benchmarks for measuring LM performance on 57 diverse knowledgeintensivetasks

![](images/2af6abf66f84f2f39e03017c6d14c441895da66329d333d009e63c7b1b1e23cd.jpg)

<details>
<summary>bar</summary>

| Field | GPT-3 | UnifiedQA |
| --- | --- | --- |
| Abstract Algebra | 45 | 42 |
| Anatomy | 68 | 58 |
| Astronomy | 72 | 65 |
| Business Ethics | 65 | 95 |
| Clinical Knowledge | 70 | 78 |
| College Biology | 68 | 60 |
| College Chemistry | 35 | 45 |
| College Comp Sci | 75 | 68 |
| College Mathematics | 60 | 55 |
| College Medicine | 75 | 65 |
| College Physics | 35 | 45 |
| Computer Security | 85 | 90 |
| Conceptual Physics | 65 | 70 |
| Econometrics | 55 | 45 |
| Electrical Engineering | 75 | 72 |
| Elementary Mathematics | 45 | 50 |
| Formal Logic | 40 | 35 |
| Global Facts | 60 | 55 |
| High School Biology | 75 | 80 |
| High School Chemistry | 50 | 55 |
| High School Comp Sci | 65 | 75 |
| High School European History | 80 | 90 |
</details>

# Astronomy

What is true for a type-Ia supernova?

A.This type occurs in binary systems.   
B.This type occurs in young galaxies.   
C. This type produces gamma-ray bursts.   
D. This type produces high amounts of X-rays.

# High School Biology

In a population of giraffes,an environmental change occurs that favors individuals that are tallest. As a result, more of the taller individuals are able to obtain nutrients and survive to pass along their genetic information. This is an example of

A. directional selection.   
B.stabilizing selection.   
C. sexual selection.   
D. disruptive selection

![](images/7c2de43722d160d72910bf4dde5fe65ea707d1960ab4ebcb719e09582497a9de.jpg)

<details>
<summary>line</summary>

| Model | Average (%) |
| --- | --- |
| RoBERTa-base 125M (fine-tuned) | 28 |
| UnifiedQA 11B | 50 |
| Gopher 280B (5-shot) | 60 |
| Chinchilla 70B (5-shot) | 68 |
| Flan-U-PaLM-540B | 73 |
| GPT-4 (few-shot) | 85 |
| Leeroo (5-shot) | 85 |
| Other models | Scatter points (approximate range) |
</details>

Rapid,impressive progress on challenging knowledge-intensive benchmarks

# Model input (Disambiguation QA)

Q: In the following sentences, explain the antecedent of the pronoun (which thing the pronoun refers to), or state that it is ambiguous.

Sentence: The reporter and the chef will discuss their favorite dishes.

Options:

(A) They will discuss the reporter's favorite dishes   
(B) They will discuss the chef's favorite dishes   
(C) Ambiguous

A: Let's think step by step.

# Before instruction finetuning

The reporter and the chef will discuss their favorite dishes.

The reporter and the chef will discuss the reporter's favorite dishes.

The reporter and the chef will discuss the chef's favorite dishes.

The reporter and the chef will discuss the reporter's and the chefs favorite dishes.

![](images/cb08aeef8c87209cc412c296817d2538abad5e7a980d3309ce268e02c4ab6526.jpg)

(doesn't answer question)

# Model input (Disambiguation QA)

Q: In the following sentences, explain the antecedent of the pronoun (which thing the pronoun refers to), or state that it is ambiguous.

Sentence: The reporter and the chef will discuss their favorite dishes.

Options:

(A) They willdiscuss the reporter's favorite dishes   
(B)They will discuss the chef's favorite dishes   
(C) Ambiguous

A: Let's think step by step.

# After instruction finetuning

The reporter and the chef will discuss their favorite dishes does not indicate whose favorite dishes they will discuss. So, the answer is (C).

![](images/cde97c00f66f222d22060f2a85a63dcf63d29970c6f64812cb52d5bff4383998.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Falcon"] --> B[" RWKV "]
    B --> C["PaLM 2 "]
    C --> D["Pythia"]
    D --> E["RedPajama-INCITE-Base"]
    E --> F["MPT-30B"]
    F --> G["MPT-7B Base"]
    G --> H["MPT-7B-StoryWriter-65k+"]
    H --> I["MPT-7B-Chat"]
    I --> J["StarCoderData"]
    J --> K["RedPajama-INCITE-Chat"]
    K --> L["XGen-7B"]
    L --> M["MPT-7B-Instruct"]
    C --> N["OpenLLaMA"]
    N --> O["RedPajama-INCITE-Base"]
    O --> P["MPT-7B-Chat"]
    P --> Q["OASST1"]
    Q --> R["databricks-dolly-15k"]
    R --> S["AmbiEnt"]
    S --> T["Sparks of AGI"]
    T --> U["BLOOM"]
    U --> V["The Stack"]
    V --> W["Roots"]
    W --> X["BloombergGPT"]
    X --> Y["Alpaca"]
    Y --> Z["GPT4All-j"]
    Z --> AA["LLaMA-Adapter"]
    AA --> AB["LLaMA"]
    AB --> AC["GPT4All"]
    AC --> AD["LLaMA"]
    AD --> AE["Self-Instruct"]
    AE --> AF["Flan-UL2"]
    AF --> AG["Bard"]
    AG --> AH["OpenAssistant"]
    AH --> AI["Koala"]
    AI --> AJ["GPT4All-j"]
    AJ --> AK["Baize"]
    AK --> AL["StableLM"]
    AL --> AM["OpenOrca-Preview1-13B"]
    AM --> AN["Llama 2"]
    AN --> AO["Orca"]
    AO --> AP["OpenOrca"]
    AP --> AQ["MPT-7B-Chat"]
    AQ --> AR["StarCoderData"]
    AR --> AS["RedPajama-INCITE-Chat"]
    AS --> AT["MPT-7B-Instruct"]
```
</details>

· The release of LlaMA led to open-source attempts to \`create'instruction tuning data

Generate instructions, input,and output from a LM [Wang et al., 2022]

Alpaca: fine-tuned from the LLaMA 7B model on 52K instruction-following examples

You don't need many samples to instruction tune (e.g., "LIMA: Less Is More for Alignment" Zhou et al., 2023)

![](images/b40ed74c16e3d9f6af556fe0a58fab0fb898cc80f8bce49537934d0ed1a4ed9b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Text-davinci-003"] --> B["Modified Self-instruct Instruction Generation"]
    C["175 Self-Instruct seed tasks"] --> B
    B --> D["52K Instruction-following examples"]
    D --> E["Supervised Finetuning"]
    E --> F["Alpaca 7B"]
    G["Example Seed Task"] --> H["Example Generated Task"]
    H --> I["Output: ... incorporating flexible components, such as moveable walls and furniture ..."]
    style A fill:#f9f,stroke:#333
    style C fill:#f9f,stroke:#333
    style G fill:#ccf,stroke:#333
    style H fill:#cfc,stroke:#333
    style I fill:#fcc,stroke:#333
```
</details>

<table><tr><td>Source</td><td>#Examples</td></tr><tr><td colspan="2">Training</td></tr><tr><td>Stack Exchange (STEM)</td><td>200</td></tr><tr><td>Stack Exchange (Other)</td><td>200</td></tr><tr><td>wikiHow</td><td>200</td></tr><tr><td>Pushshift r/WritingPrompts</td><td>150</td></tr><tr><td>Natural Instructions</td><td>50</td></tr><tr><td>Paper Authors (Group A)</td><td>200</td></tr></table>

![](images/42c608a737e30122ec55799263d85e4671769319a4888ddfa9f54e402bbe8ca0.jpg)

<details>
<summary>bar_stacked</summary>

| Model | LIMA wins (%) | Tie (%) | LIMA Loses (%) |
|---|---|---|---|
| Alpaca 65B | 53 | 21 | 26 |
| DaVinci003 | 44 | 21 | 35 |
| BARD (April) | 33 | 25 | 42 |
| Claude (April) | 24 | 22 | 54 |
| GPT-4 (April) | 18 | 25 | 57 |
</details>

Few-shot learner: In-Context Learning   
Instruction Fine-tuning   
RLHF

One limitation of instruction finetuning is obvious: it's expensive to colect ground-truth data for tasks.   
But there are other,subtler limitations too.Can you think of any?   
Problem 1: tasks like open-ended creative generation have no right answer.

Write me a story about a dog and her pet grasshopper.

Problem 2: language modeling penalizes alltoken-level mistakes equaly, but some errors are worse than others.   
Even with instruction finetuning, there a mismatch between the LM objective and the objective of "satisfy human preferences"!   
. Can we explicitly attempt to satisfy human preferences?

![](images/13f138e1cb93a7425fa7fecffe55c13129a5c94a167763f3890387bb5a87ec8b.jpg)

<details>
<summary>text_image</summary>

adventure
is a fantasy TV show END
LM
Avatar is a fantasy TV show
adventure
musical
show END
</details>

. Let's say we were training a language model on some task (e.g. summarization).   
For each LM sample s,imagine we had a way to obtain a human reward of that summary: R(s) ∈ R,higher is better.

SAN FRANCISCO, California (CNN) 一 A magnitude 4.2 earthquake shook the San Francisco ·· overturn unstable objects.

An earthquake hit San Francisco. There was minor property damage, but no injuries.

$$
R (s _ {1}) ^ {s _ {1}} = 8. 0
$$

The Bay Area has good weather but is prone to earthquakes and wildfires.

$$
R (s _ {2}) ^ {s _ {2}} = 1. 2
$$

. Now we want to maximize the expected reward of samples from our LM:

$$
\mathbb {E} _ {\hat {s} \sim p _ {\theta} (s)} [ R (\hat {s}) ]
$$

Note: for mathematical simplicity we're assuming only one "prompt"

# Reinforce Learning with Human Feedback Pipeline

Step1

Collect demonstration data, and train a supervised policy.

A promptis sampled fromour promptdataset.

Alabeler demonstrates the desired output behavior.

Thisdata isused to fine-tune GPT-3 with supervised learning.

![](images/545528a370f756ebb9e885e0c9a2295e075200a0a8c1e14daaec59e41b234f09.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Explain the moon landing to a 6 year old"] --> B["Some people went to the moon..."]
    B --> C["SFT"]
    C --> D["Document icon: document with crosshairs, file icons: paper, print, etc."]
```
</details>

Step2

Collect comparison data, and train a reward model.

Apromptand severalmodel outputsare sampled.

Alabelerranks the outputs from best toworst.

Thisdata isused to train our reward model.

![](images/e23b66bb7d738d876059a4c6de85b22a64a3d873121dccf5c87009b237aaaa55.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Explain the moon landing to a 6 year old"] --> B["A Explain gravity..."]
    A --> C["B Explain war..."]
    A --> D["C Moon is natural satellite of..."]
    A --> E["D People went to the moon..."]
    B --> F["RM"]
    C --> F
    D --> F
    E --> F
    F --> G["D > C > A = B"]
```
</details>

Step3

Optimize a policy against the reward model using reinforcement learning.

Anew prompt is sampled from thedataset.

The policy generates anoutput.

Therewardmodel calculatesa reward for the output.

Thereward is used toupdate the policy using PPO.

![](images/6f30e808acad3ce4e250b3dc60b01273633069e1836a9e2c4c12e37fefbaef8d.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Write a story about frogs"] --> B["PPO"]
    B --> C["Once upon a time..."]
    C --> D["RM"]
    D --> E["r_k"]
    E --> D
```
</details>

First step: instruction tuning!   
Second + third steps: maximize reward (but how??)

The field of reinforcement learning (RL) has studied these (and related) problems for many years now [Williams, 1992: Sutton and Barto, 1998]   
Circa 2013: resurgence of interest in RL applied to deep learning, game-playing [Mnih et al.,2013]   
But the interest in applying RL to modern LMs is an even newer phenomenon [Ziegler et al.,2019; Stiennon et al., 2020; Ouyang et al., 2022]. Why?

RL w/ LMs has commonly been viewed as very hard to get right (still is!)

Neweradvances in RLalgorithms thatwork for large neural models,including language models (e.g. PPO; [Schulman et al., 201Z])

![](images/0abd0c1c2ab1692c2f544b6f2525a14486014239c03cd3169b538704b3c8b4f6.jpg)

<details>
<summary>text_image</summary>

nature
THE INTERNATIONAL WEEKLY JOURNAL OF SCIENCE
LEARNING CURVE
Self-taught AI software
attains human-level
performance in video games
PACS 406.8.529
</details>

![](images/a67760c481e212507802fc55baaaee3f394354d6499dab42a3bc9dda77dd2f2c.jpg)

AlphaGo

![](images/00a08bcf8a4413a542baca654b50a411409ca87207843ac12612fe34b36a4ca0.jpg)

<details>
<summary>natural_image</summary>

Portrait of a man wearing a cap and white shirt, pointing with his finger (no visible text or symbols)
</details>

# LExplained

# in24Min

![](images/dba3a926e9d5ed41ff03160eb8edbb86a52533e513ee04984fafce49351b1e66.jpg)

<details>
<summary>natural_image</summary>

Two pixelated icons: a small robot and a globe, connected by curved arrows (no text or symbols)
</details>

https://www.youtube.com/watch?v=3vFISl7qMFI

RL-AlphaGo: https://www.youtube.com/watch?v=4PyWLgrt7YY

RL-ChatGPT and RLHF: https://www.youtube.com/watch?v=WMmGzx-jWvs&t=101s

How do we actually change our LM parameters $\theta$ to maximize this?

$$
\mathbb {E} _ {\hat {s} \sim p _ {\theta} (s)} [ R (\hat {s}) ]
$$

Let's try doing gradient ascent!

$$
\theta_ {t + 1} := \theta_ {t} + \alpha \nabla_ {\theta_ {t}} \mathbb {E} _ {\hat {s} \sim p _ {\theta_ {t} (s)}} [ R (\hat {s}) ]
$$

How do we estimate this expectation??

![](images/c4337577aedefd294c27f1b337952a1dd51db21356b015991a56dbad394d7772.jpg)

What if our reward function is nondifferentiable??

. Policy gradient methods in RL (e.g. REINFORCE; [Wiliams,1992]) give us tools for estimating and optimizing this objective.

We want to obtain

(defn.of expectation) (linearity of gradient)

$$
\nabla_ {\theta} \mathbb {E} _ {\hat {s} \sim p _ {\theta} (s)} [ R (\hat {s}) ] = \nabla_ {\theta} \sum_ {s} R (s) p _ {\theta} (s) = \sum_ {s} R (s) \nabla_ {\theta} p _ {\theta} (s)
$$

. Here we'll use a very handy trick known as the log-derivative trick.Let's try taking the gradient of log $p _ { \theta } ( s )$

$$
\nabla_ {\theta} \log p _ {\theta} (s) = \frac {1}{p _ {\theta} (s)} \nabla_ {\theta} p _ {\theta} (s) \quad \Rightarrow \quad \nabla_ {\theta} p _ {\theta} (s) = p _ {\theta} (s) \nabla_ {\theta} \log p _ {\theta} (s)
$$

(chain rule)

Plug back in:

This is an

$$
\sum_ {s} R (s) \nabla_ {\theta} p _ {\theta} (s) = \sum_ {s} p _ {\theta} (s) R (s) \nabla_ {\theta} \log p _ {\theta} (s)
$$

. Now we have put the gradient “inside" the expectation, we can approximate this objective with Monte Carlo samples:

$$
\nabla_ {\theta} \mathbb {E} _ {\hat {s} \sim p _ {\theta} (s)} [ R (\hat {s}) ] = \mathbb {E} _ {\hat {s} \sim p _ {\theta} (s)} [ R (\hat {s}) \nabla_ {\theta} \log p _ {\theta} (\hat {s}) ] \approx \frac {1}{m} \sum_ {i = 1} ^ {m} R (s _ {i}) \nabla_ {\theta} \log p _ {\theta} (s _ {i})
$$

This is why it's called "reinforcement learning": we reinforce good actions, increasing the chance they happen again.

Giving us the update rule:

$$
\begin{array}{l} \theta_ {t + 1} := \theta_ {t} + \alpha \frac {1}{m} \sum_ {i = 1} ^ {r} R (s _ {i})   \nabla_ {\theta_ {t}} \log p _ {\theta_ {t}} (s _ {i}) \\ \text {   is   a   lot   } \\ \text {   an   you   } \end{array}
$$

This is heavily simplified! There i more needed to do RL w/ LMs. Ca see any problems with this objective?

steps to minimize $p _ { \theta } ( s _ { i } )$

. Awesome: now for any arbitrary, non-differentiable reward function R(s),we can train our language model to maximize expected reward.   
Not so fast! (Why not?)   
Problem 1: human-in-the-loop is expensive!

· Solution: instead of directly asking humans for preferences, model their preferences as a separate (NLP) problem! [Knox and Stone,2009]

An earthquake hit San Francisco. There was minor property damage, but no injuries.

![](images/92b4cedb8af8bc6ec8ce46204334662d3047750a5de14777094042361417987e.jpg)

<details>
<summary>text_image</summary>

S₁
R(s₁) = 8.0
</details>

The Bay Area has good weather but is prone to earthquakes and wildfires.

$$
R (s _ {2}) ^ {s _ {2}} = 1. 2
$$

![](images/838d9127af477f4f2ff208ed332054bea127ecdf258d4442f91b53b9fed46fdc.jpg)

Train an LM $R M _ { \phi } ( s )$ to predict human preferences from an annotated dataset, then optimize for $R M _ { \phi }$ instead.

Problem 2: human judgments are noisy and miscalibrated!   
Solution: instead of asking for direct ratings, askfor pairwise comparisons, which can be more reliable [Phelps et al.,2015; Clark et al.,2018]

A 4.2 magnitude earthquake hit San Francisco, resulting in massive damage.

$$
S _ {3}
$$

$$
R (s _ {3}) = 4. 1? 6. 6? 3. 2?
$$

Problem 2: human judgments are noisy and miscalibrated!   
Solution:instead of asking fordirect ratings,askfor pairwise comparisons, which can be more reliable [Phelps et al., 2015; Clark et al., 2018]

An earthquake hit San Francisco. There was minor property damage, but no injuries.

V

A 4.2 magnitude earthquake hit San Francisco, resulting in massive damage.

V

The Bay Area has good weather but is prone to earthquakes and wildfires.

![](images/293ab9de180c276d2ec3ef69d0389f432ace8b556dd2930850302651e889e6aa.jpg)

<details>
<summary>bar</summary>

| Category | Value |
|---|---|
| The | ↑ |
| Bay | ↑ |
| Area | ↑ |
| ... | ↑ |
| ... | ↑ |
| wildfires | ↑ |
S1 | ↑ |
| 1.2 | ↑ |
</details>

S2

Bradley-Terry [1952] paired comparison model

$$
J _ {R M} (\phi) = - \mathbb {E} _ {(s ^ {w}, s ^ {l}) \sim D} \big [ \log \sigma (R M _ {\phi} (s ^ {w}) - R M _ {\phi} (s ^ {l})) \big ]
$$

"losing"

sample

sample

W should score higher than $s ^ { l }$

Evaluate RM on predicting outcome of held-out human judgments   
![](images/4e718f307829b0b432cefc0be368f8bfba1b81dd68333a11a6a831bf8403c3fa.jpg)  
[Stiennon et al., 2020]

Finally, we have everything we need:

A pretrained (possibly instruction-finetuned) $\mathsf { L } \mathsf { M } \ p ^ { P T } ( S )$   
· A reward model $R M _ { \phi } ( s )$ that produces scalar rewards for LM outputs,trained on a dataset of human comparisons   
· A method for optimizing LM parameters towards an arbitrary reward function.

Now to do RLHF:

· Initializea copy of the model $p _ { \theta } ^ { R L } ( s )$ ,with parameters $\theta$ we would like to optimize   
Optimize the following reward with RL:

$$
R (s) = R M _ {\phi} (s) - \underbrace {\beta \log \left(\frac {p _ {\theta} ^ {R L} (s)}{p ^ {P T} (s)}\right)} _ {\text {Pay a price when}} p _ {\theta} ^ {R L} (s) > p ^ {P T} (s)
$$

This isa penalty which prevents us from diverging too far from the pretrained model. In expectation,it is known as the Kullback-Leibler (KL) divergence between $p _ { \theta } ^ { R L } ( s )$ and $\mathcal { P } ^ { P T } ( s )$

![](images/1f834486caa09c35b85418f6f5718134b111212b2b8d6ec6c00a457223d80822.jpg)

<details>
<summary>line</summary>

| Model size | Human feedback | Supervised learning | p^PL(S) | p^IFT(S) | p^PT(S) | Pretrain only |
| ---------- | -------------- | ------------------- | ------- | -------- | ------- | ------------- |
| 1.3B       | 0.61           | 0.39                | -       | -        | -       | 0.23          |
| 2.7B       | 0.65           | 0.40                | -       | -        | -       | 0.31          |
| 6.7B       | 0.68           | 0.42                | -       | -        | -       | 0.29          |
| 12.9B      | 0.70           | 0.44                | -       | -        | -       | 0.36          |
</details>

# 30K Tasks

Step1

Collect demonstratjon data, and train a supervjsed policy.

Aprompt is sampled from our promptdataset.

A labeler demonstrates the desired output behavior.

This data is used to fine-tune GPT-3 with supervised learning.

![](images/5d0c91e9b710b2cb38e4f7600a7c37e235e238c8e8bc3720ca81e5819d58cc39.jpg)

Explain the moon landing toa 6 year old

![](images/0d819ecd7eb1b3d604034fca0007924ffd002379b7359688bca7fed3be3d0623.jpg)

Some people went to the moon...

![](images/5bc4a04d38f00e1270be8019cd385bd238c096c4fd6eb9d578e997f82ac923cc.jpg)

![](images/ecda7923db95d667392c59f4bffff1885b088a575ccb77de6a4a1d7d3e4a7651.jpg)

![](images/928967178a0e950207a3798e0d028d36f216e625460f486d2ee6556da0eebeec.jpg)

![](images/5d3622cfc16ea40e1413159c7ec64b0ef381d0ac6dda5bf3747b8364713462d5.jpg)

Step 2

Collect comparison data, and train a reward model.

A prompt and severalmodel outputs are sampled.

A labeler ranks the outputs from best to worst.

This data is used to train our reward model.

![](images/30d27c3df6bc62e57dee8290064e4800ab868e8d3bea5c657bc51b81d9286a6c.jpg)

Explain the moon landing toa 6year old

![](images/dee1c8baaf563d94fc707ca1502866a1a78bb9cbe5294831366ce11adb43a6e4.jpg)

Explain grawity..

![](images/016ff4e6d2e0d0396d7b6417bfff5ae89bf2d9afdf3eb1f807bc613fdc0c3aa9.jpg)

Explain war..

![](images/57bb7f120e84b4e3b1fe8e3d5a7b0630a92e9b5b1e3e758c4b01fac1470ab1f3.jpg)

satelite e..

![](images/b453ccd5a8e45b11f666599bb2eead269440996f0cf457d8d999cbcc8b7e4f77.jpg)

Pecple went to them.oon..

![](images/46fad800791cf0d2b9101b0037c44570c230ca964e310b39b8c8780a6ed2cdb7.jpg)

![](images/d7c8b33ffcfdad7226ac3d83201d32a78b57adc6ecba4441505eed6994f2a16e.jpg)

![](images/c7bd0a3dd853a064d1b920004e5f083345474d2f68dc3c30b3fadb44557d4561.jpg)

![](images/1e37dd656408b8da6a457117bec2cec6b0e32de13be60f01f956da86d83f3b7e.jpg)

![](images/db44e928959550a80df105d04cc6a8a9ba0431c0d2f5eb81fd2dc025fda9751b.jpg)

Step3

Optimize a policy against the reward model using reinforcement learning.

A new prompt is sampled from the dataset.

The policy generates an output.

The reward model calculatesa reward for the output.

Thereward is used to update the policy using PPO.

![](images/4cec9a75c1206cd96c1660ba588c4c797bfd33ff7960dea9e407a22b710c014e.jpg)

Write a story about frogs

![](images/213434d155c15710bd64853071ec38026c76270a6990b475e393d00d8787f8d1.jpg)

PPO   
![](images/9d31b55e7904c74f5cdb09d358653ef952c9ab613d5b4f04fa0d20b2cbf92b05.jpg)

![](images/01f8ff161258fc3de2d0416e18715e1a3b57cf721084e044ead8d9904b502456.jpg)

Once upon a time...

![](images/77366f701c2ccac7ecb5f7c0d7f711afe2a6b2cafd4f802b3896585ca6eb3ac0.jpg)  
RM

![](images/33969a9338f36dfb0e2ed7bad109c63ecaabf5cb6da529f3de6a260a5ae2d0ab.jpg)

![](images/38b2973f1c50ec0021ecb9361469a334ba16830c684b0430a22bf18bf3e1d4bb.jpg)

![](images/00743c660418f44a311c66eea61005386c10b8f3e352ac2b8e1b0c68fe04f92e.jpg)

# Tasks collected from labelers:

· Plain: We simply ask the labelers to come up with an arbitrary task, while ensuring the tasks had sufficient diversity.   
· Few-shot: We ask the labelers to come up with an instruction,and multiple query/response pairs for that instruction.   
· User-based: We had a number of use-cases stated in waitlist applications to the OpenAI API. We asked labelers to come up with prompts corresponding to these use cases.

<table><tr><td>Use-case</td><td>Prompt</td></tr><tr><td>Brainstorming</td><td>List five ideas for how to regain enthusiasm for my career</td></tr><tr><td>Generation</td><td>Write a short story where a bear goes to the beach, makes friends with a seal, and then returns home.</td></tr></table>

PROMPTWrite a short poem about a wise frog.

# COMPLETION

Write a short story in which a character has two different names.

Write a short story in which you try to get something back that you have lost.

Write a short story in which a character has a bad dream.

#

The frog is a symbol of wisdom

He knows all the secrets of the world

He is a master of disguise

And a great teacher of life

He is a symbol of transformation

And the bringer of change

He is the frog who has seen it all

And knows the meaning of it all

# ChatGPT: Optimizing Language Models for Dialogue

Note: OpenAl (and similar companies) are keeping more details secretabout ChatGPT training (including data, training parameters,model size) perhaps to keep a competitive edge...

# Methods

We trained this model using Reinforcement Learning from Human Feedback (RLHF),using the same methods as InstructGPT, but with slight differences in the data collection setup.We trained an initial model using supervised fine-tuning: human AI trainers provided conversations in which they played both sides-the user and an AI assistant.We gave the trainers access to model-written suggestions to help them compose their responses.We mixed this new dialogue dataset with the InstructGPT dataset,which we transformed into a dialogue format.

(lnstruction finetuning!)

# ChatGPT: Optimizing Language Models for Dialogue

Note: OpenAl (and similar companies) are keeping more details secret about ChatGPT training (including data, training parameters,model size) perhaps to keep a competitive edge...

# Methods

To create a reward model for reinforcement learning, we needed to collect comparison data, which consisted of two or more model responses ranked by quality. To collect this data, we took conversations that AI trainers had with the chatbot.We randomly selected a model-written message, sampled several alternative completions,and had AI trainers rank them. Using these reward models, we can fine-tune the model using Proximal Policy Optimization. We performed several iterations of this process.

(RLHF!)