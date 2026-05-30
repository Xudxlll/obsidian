# AMA 564 Deep Learning

# 2026 Spring

# Lecture

# Course Information

# Dr SHEN Guohao

TU713, Yip Kit Chuen Bldg.

guohao.shen@polyu.edu.hk

<table><tr><td rowspan="2"></td><td>Start Week</td><td>End Week</td><td>Day of Week</td><td>Start Time</td><td>End Time</td><td>Venue</td></tr><tr><td>1</td><td>13</td><td>Fri</td><td>12:30</td><td>15:20</td><td>SHA030</td></tr></table>

# Deep Neural Networks

Multi-Layer Perceptron   
Convolutional Neural networks   
Recurrent Neural Networks   
Transformer

# Learning Algorithms

Regression, classification   
Classification   
Generative Learning   
Vision   
Natural Language Processing

Backpropagation

Optimization

Overview of Training LLMs

<table><tr><td>Week</td><td>Date</td><td>Content</td></tr><tr><td>1</td><td>Jan 16</td><td>Multilayer Perceptrons I: History and Development</td></tr><tr><td>2</td><td>Jan 23</td><td>Multilayer Perceptrons II: Regression and Training</td></tr><tr><td>3</td><td>Jan 30</td><td>Backpropagation and Optimization</td></tr><tr><td>4</td><td>Feb 06</td><td>Computer Vision I: Convolution Neural Networks</td></tr><tr><td>5</td><td>Feb 13</td><td>Computer Vision II: Architectures and Training</td></tr><tr><td>6</td><td>Feb 27</td><td>Generative Models I: VAE</td></tr><tr><td>7</td><td>Mar 06</td><td>Generative Models II: GAN and others</td></tr><tr><td>8</td><td>Mar 13</td><td>Natural Language Processing I: Recurrent Neural Networks</td></tr><tr><td>9</td><td>Mar 20</td><td>Natural Language Processing II: Attention-based Models</td></tr><tr><td>10</td><td>Mar 27</td><td>Natural Language Processing III: Large Moldes and Training</td></tr><tr><td>11</td><td>Apr 03</td><td>General holiday (Good Friday)</td></tr><tr><td>12</td><td>Apr 10</td><td>Natural Language Processing IV: Fine-tuning and RLHF</td></tr><tr><td>13</td><td>Arp 17</td><td>Overall Course Review</td></tr></table>

# After this course, you will

Know different deep neural networks   
(can tell MLP, CNN, RNN, etc.)   
Understand how to train deep neural networks   
(backpropagation, optimization techniques)   
Apply or design algorithms for different learning tasks   
(regression, classification, generation; vision, natural language processing)   
Implement data analysis or learning task on python in practice   
(deep learning with PyTorch for conventional learning tasks)   
Know the key steps in building LLMs.

# Prerequisite

Linear Algebra   
Basic Calculus   
Probability and statistics   
Python Basics

# 13 Weeks

Lecture 2 hours each week Tutorial/Demo 1 hour each week   
Homework (30%) <= 3 Project (20%) 1   
Final (50%)

# References

1. Deep Learning. Goodfellow I., Bengio Y., Courville A. The MIT Press 2016.   
2. Deep Learning with Python. Francois Chollet with J. J. Allaire. Manning Publications Co.2018   
3. Foundations of Machine Learning. Mohri, M., Rostamizadeh, A., & Talwalkar, A. The MIT Press 2018.   
4. The Elements of Statistical Learning. Hastie, T.,Tibshirani, R, and Friedman, J. Springer 2009.   
5. Convex optimization: Algorithms and complexity. Bubeck, S. Now Publishers Inc.2015

Rubrics (Waiting for Approve from Department) 

<table><tr><td>Specific assessment methods/tasks</td><td>% weighting</td></tr><tr><td>Assignments</td><td>30%</td></tr><tr><td>Projects</td><td>20%</td></tr><tr><td>Midterm Test</td><td>None</td></tr><tr><td>Examination</td><td>50%</td></tr><tr><td>Total</td><td>100%</td></tr></table>

<table><tr><td>Grade Level</td><td>Cut-off</td></tr><tr><td>A-/A/A+</td><td>85</td></tr><tr><td>B-/B/B+</td><td>70</td></tr><tr><td>C-/C/C+</td><td>55</td></tr><tr><td>D/D+</td><td>40</td></tr><tr><td>F</td><td>&lt;40</td></tr></table>

# Programming

![](images/85fd1c89a6525ac91571dc1c01f745ed07be0a806d441fc566b0c1f59517a17d.jpg)

<details>
<summary>text_image</summary>

Machine Learning
War of Languages
Winner
Shield
julia
</details>

Source:https://www.codementor.io/@innat\_2k14/preferable-tools-for-machine-learning-python-matlab-r-jfozzpphz

In this course, we use Python.

# Programming

![](images/0555a45db44eb131c542a4bf90504faf09687408cc47e8b4a19cf7504299c7cd.jpg)

<details>
<summary>text_image</summary>

Keras
vs
TensorFlow
vs
PyTorch
</details>

Source: https://www.educba.com/keras-vs-tensorflow-vs-pytorch/

In this course, we use PyTorch.

# Programming

![](images/60e8fb7ed71c24fbcb698ab7d56cfdd41037f044e695e60282d483532a6f47f5.jpg)

# PyTorch

# https://pytorch.org/

![](images/bdc819b5ebbea2d1f97b121bf3780d8aa0a14601ac74d671ffeaf1d5fd411514.jpg)

# PyTorch

Get Started

Ecosystem <

Mobile

Blog

Tutorials

Docs<

Resources <

GitHub

Q

series better and thank you all who have made the 1-series so successful.

# Shortcuts

# PYTORCH 2.X: FASTER，MORE PYTHONIC AND AS DYNAMIC AS EVER

Today, we announce torch.compile,a feature that pushes PyTorch performance to new heights and starts the move for parts of PyTorch from C++ back into Python. We believe that this is a substantial new direction for PyTorch - hence we call it 2.0. torch.compile is a fully additive (and optional) feature and hence 2.0 is 100% backward compatible by definition.

Underpinning torch.compile are new technologies - TorchDynamo, AOTAutograd, PrimTorch and TorchInductor.

·TorchDynamo captures PyTorch programs safely using Python Frame Evaluation Hooks and is a significant innovation that was a result of 5 years of our R&D into safe graph capture   
· AOTAutograd overloads PyTorch's autograd engine as a tracing autodiff for generating ahead-of-time backward traces.   
· PrimTorch canonicalizes \~2oo0+ PyTorch operators down to a closed set of \~250 primitive operators that developers can taraet to build a

# Programming

# Tutorials: https://pytorch.org/tutorials

Tutorials > Welcome to PyTorch Tutorials

![](images/f1dd0a2c5596f655ceba5837a6339134f0da9dfde22c99ef9603094ed5db82e9.jpg)

# Learn the Basics

A step-by-step guide to buildinga complete ML workflow with PyTorch.

Getting Started

![](images/4a2a4638b91b140574c0d99364b73bdc6da9eacb7297d12f8ee33aaf7af0c099.jpg)

# Introduction to PyTorch on YouTube

# Learning PyTorch with Examples

![](images/bc15941e5448e75d92ab60a06af999b389ed735e3e004253a229ba4af7fc074a.jpg)

# Programming

# Helpful Documents:

# https://pytorch.org/docs/stable/index.html

PyTorch

Get Started

Ecosystem

Mobile

Blog

Tutorials

Resources <

GitHub

![](images/54869f358ba7e29e547262bc9231ab176db967c91ce8505e279148b0c717ccc0.jpg)

tensor

Community [+]

Developer Notes [+]

Language Bindings [+]

Python APl[-]

Docs > Search

# Searching..

· torch.jit.unsupported\_tensor\_ops (Python module,in TorchScript Unsupported Pytorch Constructs)   
· torch.masked.maskedtensor (Python module,in torch.masked)   
· torch.utils.tensorboard (Python module,in torch.utils.tensorboard)   
· torch.tensor (Python function,in torch.tensor)   
· torch.Tensor (Python class,in torch.Tensor)   
· Autograd mechanics

...rations that created

the data as you execute operations, giving you a directed acyclic graph

whose leaves are the input tensors and roots are the output tensors.

by tracing this graph from roots to leaves,you can automatically

compute the...

· Automatic differentiation package - torch.autograd

...ation of arbitrary scalar valued functions.it requires minimal

changes to the existing code- you only need to declare tensor s

for which gradients should be computed with the requires\_grad=true keyword.

as of now, we only support autograd...

C++

..le model modifications if needed (e.g. pulling out submodules)

# Tutorial

![](images/04702c8e4497b6fc16b093a3907cbaa1aa31c089f99db3f105217a2c1c547810.jpg)

<details>
<summary>text_image</summary>

jupyter
</details>

#

Personal or Course Project

![](images/14b1464789c7a58c66c871f948865217fdc3818af8275a0cf0936cb98a8705cb.jpg)

<details>
<summary>natural_image</summary>

Green circular logo with abstract grid pattern (no text or symbols)
</details>

ANACONDA

![](images/91d9ee5ab047c77f04f133b19626305d9cd3df9abd38a3412c32c0a56dd5c966.jpg)

<details>
<summary>text_image</summary>

PC
—
</details>

![](images/99985b07e47330d1946c574f1a4f4a6655787bca5ce8cb2d56e792bbf916776b.jpg)

<details>
<summary>natural_image</summary>

Abstract geometric diagram with a red curved line inside a polygonal structure (no text or symbols)
</details>

SPYDER

# 2023: A Big Year for Artificial Intelligence

![](images/87cdceceaf9ef778e5fca5fcd59df7190a13214ffd0f87e8fb4ed2cd0c716c2f.jpg)

<details>
<summary>text_image</summary>

ChatGPT
chat.openai.com/chat
Reset Thread
Light Mode
OpenAI Discord
Learn More
Log out
This causes the component to re-render, and the updated `count` value is displayed in the `p` element.
I hope this helps! Let me know if you have any other questions.
Can you add App.tsx that uses this component?
Sure! Here's an example of an `App` component that uses the `Counter` component from the previous example:
import React from 'react';
import Counter from './Counter';
function App() {
    return (
        <div>
            <Counter />
        </div>
    );
}
In this example, the `App` component simply renders the `Counter` component. When the `Counter` component is rendered, it will display a button and a paragraph that shows the current count. When the button is clicked, the `Counter` component will update its state and re-render, showing an updated count in the paragraph.
Free Research Preview: ChatGPT is optimized for dialogue. Our goal is to make AI systems more natural to interact with, and your feedback will help us improve our systems and make them safer.
</details>

<table><tr><td><img src="images/73c2877224250f5c68a111b6afad1dfdf910cf0e09f0a07d38bbb5f8b3d4aac7.jpg"/></td><td>ChatGPT</td><td><img src="images/55b65fdffd397a33ce1a0d38121b58cd56b1b86b0de911089f58a7b4c39e2069.jpg"/></td><td>Claude</td><td><img src="images/6424f4b31b65004b3bf565610e15dcd3ef33041bb24020a76da4b500c828ef83.jpg"/></td><td>Gemini</td></tr><tr><td><img src="images/4c832966fc064e16b9b4b72da246c46f61e3f4dd6a92a36ca45d7e3e144ee61d.jpg"/></td><td>Meta</td><td><img src="images/fbb562e182d67088df89c65fb42c6572ff21209508b624e447273486a741d6af.jpg"/></td><td>DeepSeek</td><td><img src="images/835d037645114ad50dc7878407a2fcbccb43ce075742ec2f2553ba13226546cf.jpg"/></td><td>Perplexity</td></tr><tr><td><img src="images/33e68a410a273ce67f50fdb6fd703df2b2ded5b68a49494ae9c48d6f8ac0601f.jpg"/></td><td>Midjourney</td><td><img src="images/7db031771be930824b6b983e7c5c0d7b418e000b57c49a86336d094f7bd7626d.jpg"/></td><td>Flux</td><td><img src="images/e8349d1fe2a4bfc23d911efd33fd40f24acc17b25ecad2b70d4f2337bfa4c654.jpg"/></td><td>Ideogram</td></tr><tr><td><img src="images/e2ac535d90b7023e2ab4a012ac13ca780f96e430f4633f56fa77432d99eb4ea3.jpg"/></td><td>Runway</td><td><img src="images/5116c777604551b184b25ddcfefada93faad4a1ac1a6134491542b5b8855977c.jpg"/></td><td>Luma</td><td><img src="images/b552b5ab492f6ecb8d918c3395d12825307c806d14a280c712539705570ceb32.jpg"/></td><td>Grok</td></tr></table>

# ARTIFICIAL INTELLIGENCE VSMACHINE LEARNING VS DEEP LEARNING

# O Artificial Intelligence

Development of smart systems and machines that can cary out tasks that typically require human intelligence

# 0 Machine Learning

Creates algorithms that can learn from data and make decisions based on patterns observed Require human intervention when decision is incorrect

# ③ Deep Learning

Uses an artificial neural network to reach accurate conclusions without human intervention

![](images/1338fc8bb405335245b14ccd56140a651a35769c7974c3bc2110c26a803f7b60.jpg)

Source: https://www.scs.org.sg/articles/machine-learning-vs-deep-learning

Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning.

![](images/85c0cd0b9361d243bdf2816315d64bbcf750d4dc66001c3007de68961d58af30.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Layer"] --> B["Hidden Layer 1"]
    A --> C["Hidden Layer 2"]
    A --> D["Hidden Layer 3"]
    A --> E["Hidden Layer 4"]
    A --> F["Hidden Layer 5"]
    B --> G["Output Layer"]
    C --> G
    D --> G
    E --> G
    F --> G
    style A fill:#f9f,stroke:#333
    style G fill:#bbf,stroke:#333
```
</details>

Source: https://www.tibco.com/reference-center/what-is-a-neural-network

Deep Learning utilizes Artificial Neural Networks

A Three Wave Development of Deep Learning (Deep learning. Goodfellow, Bengio & Courville.)   
![](images/1cb31e70ca4c610b0d5c06b7d3d16fb39d5a07f49c7dc90294443b292118f12c.jpg)

<details>
<summary>line</summary>

| Model | Year | Value |
| --- | --- | --- |
| Mathematical model of neurons | 1943 | - |
| Single Layer Perceptron | 1958 | - |
| Cannot solve XOR problems | 1969 | - |
| Back propagation | 1976 | - |
| Multilayer Perceptron | 1986 | - |
| CNN & LeNet | 1997 | - |
| RNN LSTM | 1997 | - |
| Overwhelmed by SVM | 2006 | - |
| Deep belief network & deep learning | 2006 | - |
| Stacked Auto-Encoder | 2006 | - |
| GoogLeNet, GAN VGGNet, R-CNN | 2012 | - |
| ImageNet AlexNet DroupOut, ReLU | 2012 | - |
| BatchNormalization, Faster R-CNN, ResNet, FCN, UNet, YOLO, SSD | 2014 | - |
| Mask R-CNN, RetinaNet AlphaGo | 2017 | - |
| AlphaZero, GNN | 2019 | - |
</details>

Source: “Application of deep learning in ecological resource research: Theories, methods, and challenges”

Milestones   
![](images/c8ae3def04a24035b0a61317042768b4aa59f97dc10e9dcd1d322128e1a4f8e9.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["1940: Electronic Brain"] --> B["1943: Electronic Brain"]
    B --> C["1950: Perceptron"]
    C --> D["1957: Golden Age"]
    D --> E["1960: ADALINE"]
    E --> F["1969: XOR Problem"]
    F --> G["1986: Multi-layered Perceptron (Backpropagation)"]
    G --> H["1995: SVM"]
    H --> I["2006: Deep Neural Network (Pretraining)"]
    
    subgraph Time Periods
        J["S. McCulloch - W. Pitts"] --> K["F. Rosenblatt"]
        K --> L["B. Widrow - M. Hoff"]
        L --> M["M. Minsky - S. Papert"]
        M --> N["D. Rumelhart - G. Hinton - R. Williams"]
        N --> O["V. Vapnik - C. Cortes"]
        O --> P["G. Hinton - S. Ruslan"]
    end
    
    subgraph Legend
        Q["X AND Y"] --> R["+1 +2 X"]
        R --> S["+1 +2 X"]
        S --> T["+1 +2 X"]
        T --> U["+1 +2 X"]
        U --> V["+1 +2 X"]
        V --> W["+1 +2 X"]
        W --> X["+1 +2 X"]
        X --> Y["+1 +2 X"]
        Y --> Z["+1 +2 X"]
        Z --> AA["+1 +2 X"]
        AA --> AB["+1 +2 X"]
        AB --> AC["+1 +2 X"]
        AC --> AD["+1 +2 X"]
        AD --> AE["+1 +2 X"]
        AE --> AF["+1 +2 X"]
        AF --> AG["+1 +2 X"]
        AG --> AH["+1 +2 X"]
        AH --> AI["+1 +2 X"]
        AI --> AJ["+1 +2 X"]
        AJ --> AK["+1 +2 X"]
        AK --> AL["+1 +2 X"]
        AL --> AM["+1 +2 X"]
        AM --> AN["+1 +2 X"]
        AN --> AO["+1 +2 X"]
        AO --> AP["+1 +2 X"]
        AP --> AQ["+1 +2 X"]
        AQ --> AR["+1 +2 X"]
        AR --> AS["+1 +2 X"]
        AS --> AT["+1 +2 X"]
        AT --> AU["+1 +2 X"]
        AU --> AV["+1 +2 X"]
        AV --> AW["+1 +2 X"]
        AW --> AX["+1 +2 X"]
        AX --> AY["+1 +2 X"]
        AY --> AZ["+1 +2 X"]
        AZ --> BA["+1 +2 X"]
        BA --> BB["+1 +2 X"]
        BB --> BC["+1 +2 X"]
        BC --> BD["+1 +2 X"]
        BD --> BE["+1 +2 X"]
        BE --> BF["+1 +2 X"]
        BF --> BG["+1 +2 X"]
        BG --> BH["+1 +2 X"]
        BH --> BI["+1 +2 X"]
        BI --> BJ["+1 +2 X"]
        BJ --> BK["+1 +2 X"]
        BK --> BL["+1 +2 X"]
        BL --> BM["+1 +2 X"]
        BM --> BN["+1 +2 X"]
        BN --> BO["+1 +2 X"]
        BO --> BP["+1 +2 X"]
        BP --> BQ["+1 +2 X"]
        BQ --> BR["+1 +2 X"]
        BR --> BS["+1 +2 X"]
        BS --> BT["+1 +2 X"]
        BT --> BU["+1 +2 X"]
        BU --> BV["+1 +2 X"]
        BV --> BW["+1 +2 X"]
        BW --> BX["+1 +2 X"]
        BX --> BY["+1 +2 X"]
        BY --> BZ["+1 +2 X"]
        BZ --> CA["+1 +2 X"]
        CA --> CB["+1 +2 X"]
        CB --> CC["+1 +2 X"]
        CC --> CD["+1 +2 X"]
        CD --> CE["+1 +2 X"]
        CE --> CF["+1 +2 X"]
        CF --> CG["+1 +2 X"]
        CG --> CH["+1 +2 X"]
        CH --> CI["+1 +2 X"]
        CI --> CJ["+1 +2 X"]
        CJ --> CK["+1 +2 X"]
        CK --> CL["+1 +2 X"]
        CL --> CM["+1 +2 X"]
        CM --> CN["+1 +2 X"]
        CN --> CO["+1 +2 X"]
        CO --> CP["+1 +2 X"]
        CP --> CQ["+1 +2 X"]
        CQ --> CR["+1 +2 X"]
        CR --> CS["+1 +2 X"]
        CS --> CT["+1 +2 X"]
        CT --> CU["+1 +2 X"]
        CU --> CV["+1 +2 X"]
        CV --> CW["+1 +2 X"]
        CW --> CX["+1 +2 X"]
        CX --> CY["+1 +2 X"]
        CY --> CZ["+1 +2 X"]
        CZ --> DA["+1 +2 X"]
        DA --> DB["+1 +2 X"]
        DB --> DC["+1 +2 X"]
        DC --> DD["+1 +2 X"]
        DD --> DE["+1 +2 X"]
        DE --> DF["+1 +2 X"]
        DF --> DG["+1 +2 X"]
        DG --> DH["+1 +2 X"]
        DH --> DI["+1 +2 X"]
        DI --> DJ["+1 +2 X"]
        DJ --> DK["+1 +2 X"]
        DK --> DL["+1 +2 X"]
        DL --> DJ
    end
```
</details>

Source: http://beamlab.org/deeplearning/2017/02/23/deep\_learning\_101\_part1.html

# The first Neuron 1943

MP Neuron

![](images/de259b5ec2ca9869f7dfbb58a14599bd101ac80905f169b62430e4cc4a0a86a0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    x1["x₁"] --> y["ŷ"]
    x2["x₂"] --> y["ŷ"]
    xn["xₙ"] --> y["ŷ"]
    y["ŷ"] --> x1
    y["ŷ"] --> x2
    y["ŷ"] --> xn
```
</details>

$$
\hat {y} = 1 \text {   if   } \sum_ {i = 1} ^ {n} x _ {i} \geq b
$$

$$
\hat {y} = 0 \text {   otherwise }
$$

![](images/3f51a4cf7d51c085e097836166954de41c8c3c3bc0265420e9f207d9670c9470.jpg)

Boolean inputs

![](images/4808912e359ce3cb7032b79145ddd0d930515afe99b5fe08a30fe4fe83ddae15.jpg)

Linear

![](images/7fb4c5f0ba3d670f8654606c7d5b04567547d5af3c47f6569f6d017bc9472410.jpg)

Inputsare notweighted

![](images/ecd720f2d1037eb98909a35bda010a9427b1e0802f3d97a2427c049f284c23a1.jpg)

Adjustable threshold

McCulloch-Pitts Neuron

![](images/2efc0a35c34d372ce8f0985863eed27995a8b1b09799d7b31ea8cb054e940042.jpg)

<details>
<summary>natural_image</summary>

Portrait of an elderly man with a beard and mustache, wearing formal attire (no visible text or symbols)
</details>

Warren McCulloch (Neuroscientist)

![](images/ce88881625c30cfce82b194fb6adb5e6965a55cb1932aa7908650a3b7c6d53ec.jpg)

<details>
<summary>natural_image</summary>

Black-and-white portrait of a man wearing glasses and a tie (no visible text or symbols)
</details>

Walter Pitts (Logician)

# The first wave: 1940s-1960s

One of the very first ideas in machine learning and artificial intelligence

![](images/1df07934c57c2cf113dbb6d8b345c752f0a370cfde76114e0926a51421c2caa2.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["x₁"] --> B["w₁ⱼ"]
    C["x₂"] --> D["w₂ⱼ"]
    E["x₃"] --> F["w₃ⱼ"]
    G["..."] --> H["..."]
    I["xₙ"] --> J["wₙⱼ"]
    B --> K["Σ"]
    D --> K
    F --> K
    H --> K
    J --> K
    K --> L["net input netⱼ"]
    L --> M["φ"]
    M --> N["oⱼ activation"]
    M --> O["θⱼ threshold"]
    style K fill:#f9f,stroke:#333
    style M fill:#ccf,stroke:#333
```
</details>

Rosenblatt’s perceptron

• Date back to 1940s   
• Could recognize letters and numbers   
Repeated promises of “True AI” that were unfulfilled

"[The perceptron is] the embryo of an electronic computer that [the Navy] expects will be able to walk, talk, see, write, reproduce itself and be conscious of its existence."

\- Frank Rosenblatt, 1958

![](images/24718bf46d179cc2d751415297bff983cc69755c339d47b5728f26fb6b3d8448.jpg)

<details>
<summary>text_image</summary>

abc
perceptron
▲ ○ □
</details>

# Frank Rosenblatt

(July 11,1928 – July 11,1971)

American psychologist

“Father of deep learning”

(Tappert, Charles C. (2019).

"Who Is the Father of Deep Learning?”)

The first wave: 1940s-1960s

# BRACEYOURSELVES

![](images/a5d845f5eb5469be83d37867e6b1aaa0df8d1a149bc78ef8fb9335b9d89bf485.jpg)

<details>
<summary>text_image</summary>

AI WINTER IS
COMING
</details>

memegenerator.net

# The first AI Winter 1969

![](images/1f0d244a298411a34a780cdba85f9863c97e6e2e4cddde5b18338a049fedb747.jpg)

<details>
<summary>natural_image</summary>

Black-and-white photo of two men smiling and conversing in front of a bookshelf (no visible text or symbols)
</details>

Marvin Minsky (left) and Seymour Papert (right) in 1971.

Cynthia Solomon/Courtesy of MIT

Source:https://www.npr.org/sections/ed/2016/08/05/488669276/remembering-athinker-who-thought-about-thinking

They proved that perceptron can't even solve the XOR problem.   
End Rosenblatt’s research on perceptrons when he was only 41 years old.   
Kills research on neural nets for the next 15-20 years.

![](images/8311e96c8f41fdf3190e2e9432c5924c0e991464361e53448a3c75c62065dfc6.jpg)

<details>
<summary>text_image</summary>

Expanded Edition
Perceptrons
Marvin L. Minsky
Seymour A. Papert
</details>

The book “Perceptron”

# The first AI Winter 1969

![](images/927a410857616a1d1ac5543ba5bfdbf0ee21f1f1bd370a74e93eb7f674b7eedd.jpg)  
Source:https://etaxfree.xyz/index.php?route=product/category&cid=28&cname=xor+deep+learning

Linear Classifier can not do XOR.

# eep Learning HistoryThe Backpropagandists Emerge 1986

![](images/09163664a6c0d76feefb332c7eb4da9201ab45cc93aa8596c266beab85f131ac.jpg)

<details>
<summary>natural_image</summary>

Portrait engraving of a 19th-century man in formal attire (no text or symbols visible)
</details>

George Boole

2 November 1815 – 8 December 1864

Mathematician

Logician

![](images/d0575f65b5affa716f00c180e2f260a15d714a66be644eae709d411e1d23bd83.jpg)

<details>
<summary>natural_image</summary>

Portrait of a man with gray hair wearing a sweater over a collared shirt, standing in front of a bookshelf (no visible text or symbols)
</details>

Geoffrey Hinton

born 6 December 1947

Cognitive psychologist

and computer scientist

Great-great-grandson

# eep Learning HistoryThe Backpropagandists Emerge 1986

Along with David Rumelhart and Ronald Williams, Hinton published a paper entitled “Learning representations by backpropagating errors”.   
Neural nets with many hidden layers could be effectively trained by a relatively simple procedure.   
Additional layers endowed the network with the ability to learn nonlinear functions.

Disputes: Firstly published in1970 by Finnish master student Seppo Linnainmaa.

![](images/8b03b23b5a5780fdf986524f8b51e1c536b3273ec32a6b44dfc7f063df5d8e05.jpg)

<details>
<summary>natural_image</summary>

Portrait of a man with gray hair wearing a sweater over a collared shirt, standing in front of a bookshelf (no visible text or symbols)
</details>

Geoffrey Hinton

born 6 December 1947 Cognitive psychologist and computer scientist

# eep Learning HistoryThe Backpropagandists Emerge 1986

Neural Network - Backpropagation   
![](images/542fa07c44ef6ccc832c5b0f2c8bc39916685ecede9d8d3e5263afb180ec0b21.jpg)

MLK

MAKINGAISIMPLE

![](images/1d36bac315050af151202872b5a9e2d5390fe7098a61d0a872b46e4b52ae4f37.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Input Layer
        X1_1["X1"] --> N11["N11"]
        X1_2["X1"] --> N12["N12"]
        X1_3["X1"] --> N13["N13"]
    end

    subgraph Hidden Layer
        N11 --> N21["N21"]
        N12 --> N22["N22"]
        N13 --> N23["N23"]
    end

    subgraph Output Layer
        oP["o/P"] --> N21
        oP --> N22
        oP --> N23
    end

    X1_1 --> N11
    X1_2 --> N12
    X1_3 --> N13
    N11 --> N21
    N12 --> N22
    N13 --> N23
    oP --> N21
    oP --> N22
    oP --> N23
```
</details>

@ machinelearningknowledge.ai

eep Learning HistoryThe Convolutional network & LeNet 1998   
![](images/bdfd8ec847c98642d75b0ba45dfb19e337b4c15d762b518a6ecdddf65f600e60.jpg)

<details>
<summary>text_image</summary>

384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
384
</details>

A project which was speared headed by Yann Lecun at AT&T Bell Labs.   
LeNet-5 on MNIST data.   
Source:http://yann.lecun.com/exdb/lenet/dancing384.html

![](images/00852f6eda2d210c54350ba9f371949da3a3df47ef9a47c8447ca78e6ad23109.jpg)

<details>
<summary>natural_image</summary>

Portrait of a man wearing glasses and a dark polo shirt, with blurred background lighting (no text or symbols visible)
</details>

Yann LeCun   
born 8 July 1960 French computer scientist A founding father of convolutional nets

# The second AI Winter 1990s

The Network approach didn’t scale to larger problems.   
By the 90s the support vector machine (SVM) became the method of choice, and neural nets were moved back into storage.

![](images/693edb00febd132eda0ec8e0f5062d70f2bb269e8463008e0684e038eafa9869.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input Points"] --> B["Kernel"]
    B --> C["Decision Surface with Red Squares"]
    style A fill:#f9f,stroke:#333
    style C fill:#bbf,stroke:#333
    note right of C Decision Surface
```
</details>

![](images/b091ee27ef2b0c4c8eb788a81ad8f19cf663f62eb75f7afa5b236a327eb2db66.jpg)

<details>
<summary>text_image</summary>

x \u00b7 f(x)
Decision
boundary
</details>

Support Vector Machines   
Source: Support Vector Machine vs. Random Forest for Remote Sensing Image Classification: A Meta-analysis and systematic review. Mohammadreza Sheykhmousa and Masoud Mahdianpari.

# Rebranding as ‘Deep Learning’ 2006

Hinton once again declared that he knew how the brain works.   
Unsupervised pretraining of "deep belief nets" allowed for large and deeper models.

![](images/33cca4ba2bc31c24e98cec06ec0ef2f1b3967d7c85283c5c95179fda8759ad6a.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Deep Belief Network"] --> B["h1"]
    A --> C["h2"]
    A --> D["h3"]
    B --> E["x"]
    C --> F["x"]
    D --> G["x"]
    H["RBM"] --> I["h1"]
    H --> J["h2"]
    H --> K["h3"]
    L["RBM"] --> M["h1"]
    L --> N["h2"]
    L --> O["h3"]
    P["RBM"] --> Q["x"]
    P --> R["x"]
    S["RBM"] --> T["x"]
    S --> U["x"]
    V["RBM"] --> W["x"]
    V --> X["x"]
```
</details>

Source:https://www.toptal.com/machine-learning/an-introduction-to-deep-learningfrom-perceptrons-to-deep-networks

# The breakthrough 2012

In 2010, a large database known

as Imagenet containing millions of labelled images was created and published by Fei-Fei Li’s group at Stanford.

This database was coupled with the annual LSVRC, where contestants would build computer vision models, submit their predictions, and receive a score based on how accurate they were.

# ImageNet Challenge

# IMAGENET

1,000 object classes (categories).   
Images: 1.2M train ○100k test.

![](images/50f8b43f996901b68dadeb612eb47a996e7d76f1e548a3e78a579b30a9d8c1ba.jpg)

<details>
<summary>text_image</summary>

mite
mite
black widow
cockroach
tick
starfish
container ship
lifeboat
amphibian
fireboat
drilling platform
motor scooter
go-kart
moped
bumper car
golfcart
leopard
jaguar
cheetah
snow leopard
Egyptian cat
grille
mushroom
cherry
Madagascar cat
convertible
grille
pickup
beach wagon
fire engine
agaric
mushroom
jelly fungus
gill fungus
dead-man's-fingers
dalmatian
grape
elderberry
ffordshire bullterrier
currant
squirrel monkey
spider monkey
titi
indri
howler monkey
</details>

![](images/e74ed33d4bbb827342b0515623a956dec3a13cb67704ec2640b83a968fa5b624.jpg)

<details>
<summary>natural_image</summary>

Portrait of a smiling woman with shoulder-length brown hair wearing a patterned scarf, outdoors with blurred background (no text or symbols visible)
</details>

# Fei-Fei Li

Computer Science Department at Stanford University Co-Director of Stanford’s Human-Centered AI Institute

Homepage: https://profiles.stanford.edu/fei-fei-li/

# Winners of ILSVRC

ImageNet Large Scale Visual Recognition Challenge (ILSVRC) winners   
![](images/b053e0f70cef77dbaacbedce8ac38317bd7074f1e845cb29fc367fa30bc11d78.jpg)

<details>
<summary>bar_line</summary>

| Study | Value | Layer Count (Layers) |
| :--- | :--- | :--- |
| Lin et al | 28.2 | 1 |
| Sanchez & Perronnin | 25.8 | 1 |
| Krizhevsky et al (AlexNet) | 16.4 | 8 |
| Zeiler & Fergus | 11.7 | 8 |
| Simonyan & Zisserman (VGG) | 7.3 | 19 |
| Szegedy et al (GoogLeNet) | 6.7 | 22 |
| He et al (ResNet) | 3.6 | 152 |
| Shao et al | 3 | 152 |
| Hu et al (SENet) | 2.3 | 152 |
| Russakovsky et al | 5.1 | - |
shallow
</details>

Source: https://kjhov195.github.io/2020-02-10-CNN\_architecture\_2/

# ep Learning HistoryThe hardware GPUs can help

ILSVRC GPU Usageand Winning error rate   
![](images/4f27001dec649732d1a5147709e5db7a6c845e3c237d480d841ceba11b86ddd0.jpg)

<details>
<summary>bar_line</summary>

| Year | Number of entries using GPUs | Winning error % |
| ---- | ---------------------------- | --------------- |
| 2010 | 0                            | 28%             |
| 2011 | 0                            | 26%             |
| 2012 | 4                            | 16%             |
| 2013 | 60                           | 12%             |
| 2014 | 110                          | 7%              |
</details>

Here is a graph showing the error rate on Imagenet over time, note the precipitous drop in 2012 and the huge uptick in teams using GPUs.

# The breakthrough 2012

Number of Al papers on Scopus by subcategory (1998-2017)

Source: Elsevier

![](images/2b43e813e0a76065311dfe3a60c7c2cb6c39ae882a9fa8febb98ea63b06c8d87.jpg)

<details>
<summary>line</summary>

| Year | Machine Learning and Probabilistic Reasoning | Neural Networks | Computer Vision | Search and Optimization | NLP and Knowledge Representation | Fuzzy Systems | Planning and Decision Making | Total |
|------|-----------------------------------------------|-----------------|-----------------|--------------------------|----------------------------------|---------------|------------------------------|-------|
| 2000 | ~3,000                                        | ~4,000          | ~3,500          | ~2,500                   | ~2,000                           | ~1,500        | ~1,000                       | ~8,000 |
| 2005 | ~10,000                                       | ~8,000          | ~7,500          | ~5,000                   | ~4,500                           | ~3,500        | ~2,500                       | ~22,000 |
| 2010 | ~16,000                                       | ~13,000         | ~14,500         | ~6,500                   | ~6,000                           | ~5,500        | ~3,500                       | ~38,000 |
| 2015 | ~25,000                                       | ~18,000         | ~22,500         | ~8,500                   | ~7,500                           | ~6,500        | ~4,500                       | ~48,000 |
| 2020 | ~33,000                                       | ~28,000         | ~24,500         | ~9,500                   | ~8,500                           | ~7,500        | ~5,500                       | ~62,000 |
</details>

Neural networks are the second best way to do almost anything.

--J.S. Denker

# Development of Deep Learning 2013

![](images/f9a24acac10dc8c0378cee34fb55b40ec7b81db4030fabbc54cd786c3571c8f4.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input x"] --> B["Encoder qφ(z|x)"]
    B --> C["z"]
    C --> D["Decoder pθ(x|z)"]
    D --> E["x̂"]
    F["For AE"] --> C
    G["For VAE"] --> H["z ~ N(μz, Σz)"]
    H --> I["Σz"]
    I --> J["μz"]
    I --> K["z"]
    J --> L["Output"]
    K --> L
```
</details>

# Variational Auto-encoder

Auto-Encoding Variational Bayes (2013). Diederik P Kingma, Max

Welling. https://arxiv.org/abs/1312.6114.

Cited by 24417

Developing of Deep Learning 2014   
![](images/1ddde2afdb994d554c82790af8f9a60bd82bc1bccdc6e3eb0deef79b2475c37f.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Real faces"] --> C["Discriminator"]
    B["Random noise"] --> C
    D["Generator"] --> E["Generated faces"]
    C --> F["Fake"]
    C --> G["Real"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style D fill:#cfc,stroke:#333
    style C fill:#fcc,stroke:#333
    style E fill:#cff,stroke:#333
```
</details>

# Generative Adversarial Networks

Generative Adversarial Networks (2014). Ian J. Goodfellow, Jean

Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil

Ozair, Aaron Courville, Yoshua Bengio. https://arxiv.org/abs/1406.2661.

Cited by 53250

# 2018 Turing Award

![](images/f84854d9251606c303c95a71dda39077305e517e8d4063642093dfee0fdd20ff.jpg)

<details>
<summary>text_image</summary>

Yoshua Bengio
</details>

![](images/2a46c13a39b91acbd23e6503e125e0b315fc8bb1d16ff2a136859962859db6c8.jpg)

<details>
<summary>text_image</summary>

Geoffrey Hinton
</details>

![](images/1b32c1623be5eb159a797d7c82eb2382c31327df25f12027f720bf9c07f0c2ea.jpg)

<details>
<summary>text_image</summary>

Yann LeCun
</details>

Fathers of the Deep Learning Revolution Receive ACM A.M. Turing Award.

Bengio, Hinton and LeCun Ushered in Major Breakthroughs in Artificial Intelligence

# 2022 OpenAI ChatGPT

![](images/d97d0162301be7c2481f1b82d6ec3687ca9896daa00ce08faebe28ac446d9cc3.jpg)

<details>
<summary>natural_image</summary>

Abstract geometric pattern composed of interlocking curved lines forming a symmetrical design (no text or symbols)
</details>

# Step 1

Collect demonstration data and trainasupervised policy.

A prompt is sample from our prompt dataset.

A labeler demonstrates the desired output behavior.

This data is used to fine-tune GPT-3.5 with supervised learning.

![](images/d745688d45059e499f9483e04430844cff49db236a63f60713716db2785cb5bb.jpg)

Explainreinforcement learning toa6yearold.

![](images/98cc7c58dcf99713b5130edbf22d6783734f43d138c27b162bca9b8e6740fb1f.jpg)

We give treats and punishments to teach..

![](images/70967a501c23655931d08bd89745b8d01e2aa886d827e816a1ce47f5de3aefb8.jpg)

![](images/7227578ec01adfe282a744ee16692d2e41000498eacfeceb78a2edd31af816b0.jpg)

![](images/3af65822977558559475d44b270665fa7d736749814155f33f95f9b11e075cae.jpg)

# Step2

Collect comparison data and traina reward model.

A prompt and several model outputs are sampled.

A labeler ranks the outputs from best to worst.

This data is used to train our reward model.

![](images/13c2a615c37ae32d5ae933a06d81fcee4aef74fe1d4d4483a8058ddd28fad733.jpg)

Explainreinforcement learning toa6yearold.

Inreinforcement learning,.the agentis...

Explain reasrcis..

In machine lesrning..

D

We ghro trezts and punishment8 to taach

![](images/90d2b4ed02f8e8bcb22d4a54ea9b8daeeb5fa01f8e431f16d14c4667aaa31f32.jpg)

D>C>A>B

![](images/720fd57188045dc7992a84838d365cda80ea2766e038665024c2c57570d51684.jpg)

RM

![](images/e2d80878e295da96c28b2caa04dcd4d9bfc7816935571cb99a3c208558e7b57b.jpg)

D>C>A>B

# Step3

Optimizea policy against the reward model using the PPO reinforcement learning algorithm.

A new prompt is sampled from the dataset.

The PPO model is initialized from the supervised policy.

The policy generates an output.

The reward model calculates a reward for the output.

The reward is used to update the policy using PPO.

![](images/7cabc6b2fe093f5b1c59f7d91ea29b45f689fa491fa6c996d5c2c65bc551798a.jpg)

Write astory about otters.

PPO

![](images/3307765255c7ba46beae3a650e4a519f2e7a2f0068888e6e4beaabb0d214c55d.jpg)

Ipon a time...

Rm

![](images/92c1a9eb0b72e513db04a093e87a0aa86f9638322d6c62f07f8c19e4b6cdf25b.jpg)

rk

# 2024 Nobel Prize

![](images/ca4b409500c641efa941bf5d78fc90a35a2af0d840a46aaec8c32e65d306a464.jpg)

<details>
<summary>text_image</summary>

THE NOBEL PRIZE
IN PHYSICS 2024
Illustrations: Niklas Elmehed
</details>

John J.Hopfield

"forfoundational discoveriesandinventions thatenablemachinelearning withartificial neural networks"

THEROYALSWEDISHACADEMY OFSCIENCES

![](images/7cd4e3de593acd348db3c84c3380402062af4892dd638c07ca4c8b4cba6a6eed.jpg)

<details>
<summary>text_image</summary>

THE NOBEL PRIZE
IN CHEMISTRY 2024
Illustrations: Niklas Elmehed
</details>

David Baker

"forcomputational protein design"

Demis Hassabis

"forprotein structureprediction"

THEROYALSWEDISHACADEMY OFSCIENCES

# 2025 Turing Award

![](images/68c1a8faa09df986fecd9804a352abef6fa4ec487ccd5abb97cdd85690b511ef.jpg)

<details>
<summary>text_image</summary>

Andrew Barto
</details>

![](images/2bb458418a23087fa5f58e16f776c7db5553eb4f28a3c48d3cb90bb1335a0380.jpg)

<details>
<summary>text_image</summary>

Richard Sutton
</details>

Computing Power (GPU, TPU,…)   
![](images/c77786a96d44bb067efaaf4143d439cee8062f7172593d02bc107248801a13ba.jpg)

<details>
<summary>natural_image</summary>

Two electronic devices: a Tesla TESLA processor with green leads and a multi-chamber circuit board (no visible text or symbols)
</details>

GPU and TPU

Open Source Tools   
![](images/23b41ac849e4e165cd7945d8bd6934f3e9082a57ff3d8bc9b89998849722ca90.jpg)

PYTORCH

![](images/0acb1972d7ed3dbcad2deb90ddbf9eb33c3c2c39f980a394336830564ba54a8d.jpg)

Microsoft

CNTK

![](images/44c6eb9761db75859c6fe8bc7e9beed52dc1fb762752bcaed22c1dd165a2464e.jpg)

Caffe2

gensim

spaCy

dmlc

mxnet

theano

Big Data   
![](images/ac1ba9364dea7d56c95853db9e3d79bfb2ec40f82170e19db5d98ea57681a783.jpg)

<details>
<summary>text_image</summary>

BIG DATA
InterviewBit
</details>

# Regression

![](images/cfaf3612bc9c2cac43173d0e049a5d0f606d23f5644d65d0a2a905fc32b8c3f1.jpg)

<details>
<summary>scatter</summary>

| x    | y      |
|------|--------|
| 0.00 | 0.90   |
| 0.05 | 0.60   |
| 0.10 | 0.30   |
| 0.15 | 0.10   |
| 0.20 | -0.10  |
| 0.25 | -0.30  |
| 0.30 | -0.50  |
| 0.35 | -0.70  |
| 0.40 | -0.90  |
| 0.45 | -1.10  |
| 0.50 | -1.30  |
| 0.55 | -1.50  |
| 0.60 | -1.70  |
| 0.65 | -1.90  |
| 0.70 | -2.10  |
| 0.75 | -2.30  |
| 0.80 | -2.50  |
| 0.85 | -2.70  |
| 0.90 | -2.90  |
| 0.95 | -3.10  |
| 1.00 | -3.30  |
</details>

Least squares regression, quantile regression, robust regression…

# Image recognition

![](images/784208701800f2c9353ea6b59080575d9abe77a3667764a51def4aa48316f734.jpg)

[Krizhevsky 2012] 

<table><tr><td>汗洪焕浑鉴束娇门</td><td>汉宏忠混手诚嚼圭</td><td>夯弘唤豁伎殓揽兮</td><td>龙红疾浩祭拣锭钦津</td><td>脱喉蒙伙剖捡矫襟</td><td>壞侯焕火悸旨凭紧</td><td>嚎猴渔获济俭脚铆</td><td>豪毗宜或寄剪伎仗</td><td>毫厚幻感寂减角谨</td><td>郁候荒霍计萍泛进</td></tr></table>

[Ciresan et al. 2013]

![](images/e35e6526b435758ccb1657358b0e1d537fb536c2b819f7505e0e38949dda6b8e.jpg)

<details>
<summary>text_image</summary>

person : 0.992
horse : 0.993
person : 0.979
car : 1,000
dog : 0.967
</details>

![](images/adfe285e6988cd733f5d75a5ce7471aec40d873afead70fc1cb30dbd02b23c64.jpg)

<details>
<summary>text_image</summary>

bus : 0.996
person : 0.736
</details>

![](images/2d4a4a2766b0debcf1e24a5ca40bf63cf36a55e72beb2d732838bb1a22a59176.jpg)

<details>
<summary>text_image</summary>

dog : 0.994
cat : 0.982
</details>

![](images/501c1d4d3a9d17225a0c60e963dcaf607dcdc1d56d0b0bbd098f56c959808855.jpg)

<details>
<summary>text_image</summary>

boat : 0.970
person : 0.982
person : 0.983
person : 0.925
person : 0.989
Lickety Split
</details>

[Faster R-CNN-Ren 2015]

![](images/185d131ce0d7833598c2ae20df887550fed448d49587d30c35a693ba007cb076.jpg)

<details>
<summary>natural_image</summary>

Street scene with purple and blue carpet, green human figures, yellow directional signs, and trees (no readable text or symbols)
</details>

[NVIDIA dev blog]

# Vision

![](images/7d4d819ce849ce9197725a1b9acea2d3602c0f9d2ad3910a695dc5550559aabf.jpg)

<details>
<summary>natural_image</summary>

Medical professional examining a patient's arm with a digital device (no visible text or symbols)
</details>

[Stanford 2017]   
![](images/bc513632a8dfd0c41d6dd9ee955d5346e467f827aa08792f89d71df022d28bbb.jpg)

<details>
<summary>text_image</summary>

1.04
1.22
1.33
0.78
1.33
1.26
0.99
</details>

Figure1.Illumination andPoseinvariance.

[FaceNet- Google 2015]

![](images/80020039492058df9bb7d7c2102b9ea02572f55b561584e2dbbe3fff7f314a47.jpg)

<details>
<summary>natural_image</summary>

Microscopic tissue sections showing glandular structures with labeled regions (no text or symbols present)
</details>

(d) benign

![](images/674d66a853ab8849e7f38d1b5cf5c3b51b07de4b93778795a63ca70e3fb92a51.jpg)

<details>
<summary>natural_image</summary>

Microscopic tissue images showing cellular structures with blue and green markers, no visible text or symbols
</details>

(e) benign

![](images/77bd91d075e264e3c766a0a3f42594d212b9dcd3ce1e07fe5a0394d8bc79dffe.jpg)

<details>
<summary>natural_image</summary>

Microscopic tissue sections showing cellular structures with green and blue markers, no visible text or labels
</details>

(f) malignant   
[Nvidia Dev Blog 2017]

![](images/652a6f9f8191cd1325c05f6eb88c2a712293c861e22a2bf2d64fbc7f9053089e.jpg)

<details>
<summary>natural_image</summary>

Grid of nine facial face images with dot patterns, no visible text or symbols
</details>

[Facial landmark detection CUHK 2014]

# Generative models for image

![](images/4c4f55e0fa0c815f28e70a29ee69f306ffe665084424735e17d10a5030533267.jpg)

<details>
<summary>natural_image</summary>

Grid of 20 diverse male and female face portraits in various styles and colors (no text or symbols visible)
</details>

Sampled celebrities [Nvidia 2017]

![](images/c4565bdc51633dcfe19ed19e79ec42293466b688ad0eecc99d2fcff55b915b1b.jpg)

<details>
<summary>text_image</summary>

Text
description
This bird is
blue with white
and has a very
short beak
This bird has
wings that are
brown and has
a yellow belly
A white bird
with a black
crown and
yellow beak
This bird is
white, black,
and brown in
color, with a
brown beak
The bird has
small beak,
with reddish
brown crown
and gray belly
This is a small,
black bird with
a white breast
and white on
the wingbars.
This bird is
white black and
yellow in color,
with a short
black beak
Stage-I
images
Stage-II
images
</details>

# Image Translation

![](images/283f763e7de62603790d6dec636aea837d5d259fad4238a5c885f6b3e0d91759.jpg)

<details>
<summary>natural_image</summary>

Surreal artwork depicting mythological creatures and a giant creature in a fantasy, ornate setting (no text or symbols)
</details>

[DeepDream 2015]

![](images/5fcd520594b7b8d7727da6ef732c1a9ef2f27b232b9c6a9e7300c55faa584eb0.jpg)

[Gatys 2015]   
original   
![](images/a5109ccf5eabfa61cd6a3e7f5527298a14195fac389d44dd32e61bce28454e37.jpg)

<details>
<summary>natural_image</summary>

Illustration of a person in traditional embroidered attire with ornate headdress and floral background (no text or symbols)
</details>

bicubic   
(21.59dB/0.6423)   
![](images/4bb696308fe0b6fb2dc3f8903c140f61c047d6e9867be926602ecf2881b204c8.jpg)

<details>
<summary>natural_image</summary>

Illustration of a person in traditional ethnic attire with floral background (no text or symbols)
</details>

SRResNet   
(23.44dB/0.7777)   
![](images/3c174281406c948ed86546fdd089e863102d19c6dfda5fe751a71fb626643918.jpg)

<details>
<summary>natural_image</summary>

Illustration of a person in traditional attire with floral headwear, seated outdoors with autumn foliage in the background (no text or symbols visible)
</details>

SRGAN   
(20.34dB/0.6562)   
![](images/7f8c17bb452b1d25d179c360c54dfb6d1e450d1fa9904dfbc949d374a29f5273.jpg)

<details>
<summary>natural_image</summary>

Illustration of a person in traditional attire with embroidered headdress, seated outdoors with floral background (no text or symbols)
</details>

[Ledig 2016]

![](images/a2b2d800dbda11bbb688b3bead41d9e523e250d10acf789a49091a17a608f299.jpg)

<details>
<summary>natural_image</summary>

Illustration of a person in traditional embroidered attire with ornate headdress, seated outdoors with autumn foliage in background (no text or symbols)
</details>

Image Translation   
![](images/7eba857ebde656d80e4bd7afb5f39aeadff8e9022a036245f5be02160c446bbe.jpg)

<details>
<summary>text_image</summary>

Input
Old Eng.
Sheep Dog
Husky
German
Shepherd
Corgi
Input
Husky
Corgi
</details>

Figure 4:Dog breed translation results.   
![](images/38ac0b783ebfb853113aac28ead53884b501539fa7e93014b6dd09712dc21c14.jpg)

<details>
<summary>text_image</summary>

Input
Cougar
Cheetah
Leopard
Lion
Tiger
Input
Leopard
</details>

Figure 5:Cat species translation results.

[Liu et al., 2017]

Speech to Text   
![](images/8e15c262f7251621690055eede32aea2859e6018175df5112d9a75ab4d4ae220.jpg)

● Convolution Layer

Recurrent Layer

O Fully Connected Layer

![](images/f4ab59bffd3981d53a03c28177f5d2b82246a718b96d936c151732b7bf3eed46.jpg)

<details>
<summary>natural_image</summary>

Abstract circular graphic with flowing wave patterns in blue and pink tones (no text or symbols)
</details>

Hey Siri

![](images/ef94edc0b6b158d188ea7656f026d2d6c3fccbb42efdecbaba8c467c00555ceb.jpg)

<details>
<summary>natural_image</summary>

Abstract graphic with blue and gray shapes, no text or symbols present
</details>

![](images/f03e6f7260fd0866b25192b41779bd4f687f7d03e5f4080247554c86a4667cd9.jpg)

<details>
<summary>natural_image</summary>

Green square icon with two white speech bubbles (no text or symbols)
</details>

[Baidu 2014]

# Natural Language Processing

ENGLISH

Translate   
![](images/04565095689a754cd40e19d4b22c1bdbec9ea6f9150f6477fffc755fcc69f06f.jpg)

<details>
<summary>text_image</summary>

Italian Chinese French English - detected
English Spanish French Translate
deep learning
13/5000
l'apprentissage en profondeur
</details>

KOREAN

JAPANESE

![](images/1553b95bc2d591d4ec660411a796b08af01e5af1213a81079fe06b7df74c4969.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Top Left"] --> B["Red Node"]
    A --> C["Blue Node"]
    A --> D["Orange Node"]
    B --> E["Bottom Right"]
    C --> E
    D --> E
    E --> F["Bottom Left"]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bfb,stroke:#333
    style D fill:#ffb,stroke:#333
    style E fill:#fbb,stroke:#333
```
</details>

deep, leaming

[Google Translate System - 2016]   
![](images/06581f22d97c4f2b0d00074c3834cc003afb8858571bfc221e22f80966fb4ddf.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["+"] --> B["0"]
    A --> C["+"]
    B --> D["0"]
    C --> E["0"]
    D --> F["The"]
    D --> G["0"]
    G --> H["first"]
    G --> I["fifteen"]
    G --> J["minutes"]
    C --> K["0"]
    C --> L["0"]
    L --> M["were"]
    L --> N["dry"]
    E --> O["0"]
    E --> P["0"]
    P --> Q["the"]
    P --> R["0"]
    P --> S["end"]
    E --> T["0"]
    E --> U["I"]
    U --> V["0"]
    V --> W["really"]
    W --> X["+"]
    X --> Y["enjoyed"]
    X --> Z["0"]
    X --> AA["the"]
    X --> AB["lecture"]
```
</details>

[Socher 2015]

# Natural Language Processing

![](images/4af0fa5806768bffd6d81c1cc2a10bbc68f066d9d32e972c89d7ee299e9f3b67.jpg)

SalitKulla

Hev.Wynton Marsalis is playing thisweekend.Do you havea preference between Saturdayand Sunday?

-S

![](images/1891b191bbacd2fe6514bfccb137cec00416e7a4e3df8616fda8dd9d92c745ca.jpg)

![](images/1703e430138e906781aa76db3f381ff2262b71f1c68ef9de6da9dd810aea1165.jpg)

[Google Inbox Smart Reply]

![](images/99e5ddeee2951c864fc7c9bd1a136a39f87d982f30fc7a5e0ed701f91d328835.jpg)

<details>
<summary>natural_image</summary>

Black circular Amazon coffee ear with green head cover and 'amazon' logo on front (no additional text or symbols)
</details>

[Amazon Echo/Alexa]

# Natural Language Processing

![](images/9e6d31c9b7162e4d244976846fc110c6eb199ee18994b126354c02d381ebb986.jpg)

<details>
<summary>text_image</summary>

OpenAI
CHATGPT
GiP
</details>

OpenAI ChatGPT is going to make Google Obsolete for Programmers

Source: https://www.youtube.com/watch?v=Ih1FxMGfUtU

![](images/4d3a1b073756b1bd27e233a0c437eacf95cb084d0953cc2989fb48b16ddf56fc.jpg)

GPT-4.1 (2025-04-14)

![](images/569af347776b4dd2797391b1950f99c8e80533dd10e0012cf1032649524c0189.jpg)

GPT-4.1-mini (2025-04-14)

![](images/8f94b471d49c8eeb4f6418d20b0bd5c335510bac6f0ce78144f5de21ebc84b31.jpg)

GPT-5 (2025-08-07)

![](images/e80e4b3126e95b8a747c2cb94339272968ac3f791d1d18e5f81d0fdfbdc023d5.jpg)

GPT-5-mini (2025-08-07)

![](images/bb2304926863eccaf97cb91748cc6ba54ae5f5f401edf2f1241d31e67a787d99.jpg)

Gemini 2.5 Pro (GA)

![](images/a8fa84172fddab5b5e03dfce5713087011aebad42ba7222aeae7b20f32af1519.jpg)

Gemini 2.5 Flash (GA)

![](images/1350065130e2d858954f2975b4e6c394b2c788ceba6c2707b2da363713a10ff7.jpg)

Qwen3-235B-A22B-Thinking-2507

![](images/a4bbd9b0dddbae10831e42d3f8acaa05517c0147a18d2fc67ec6f3c17ab16e2b.jpg)

Free

![](images/6b6da9f44b61cb6115bb29c041db3b92b1f86b2abde9eaa4cba9a832b036427a.jpg)

Qwen2.5-VL-72B-Instruct

![](images/73aaa7f8a3a48994eb1e222b59dddc35205175a9dd6c738897ffe982981b1aa4.jpg)

Free

![](images/f194a87b50a39106bfc00632b3f3e35ee25cb79eed7984021b535771932672f2.jpg)

DeepSeek-R1-0528 (Azure Al Foundry)

![](images/9e27ccac490f997001939f2e56d0e20e51a2e6c20f3d649f1fb659af375dfba2.jpg)

DeepSeek-R1-0528 (Alibaba Cloud Bailian)

Generative models for Audio   
![](images/809c666e56d3d35f49f481031e092369bbfe97e0418820644707bd7340daffb2.jpg)

<details>
<summary>other</summary>

| Input | Hidden Layer | Output |
|-------|--------------|--------|
| 1     | 0            | 0      |
| 2     | 0            | 0      |
| 3     | 0            | 0      |
| 4     | 0            | 0      |
| 5     | 0            | 0      |
| 6     | 0            | 0      |
| 7     | 0            | 0      |
| 8     | 0            | 0      |
| 9     | 0            | 0      |
| 10    | 0            | 0      |
| 11    | 0            | 0      |
| 12    | 0            | 0      |
| 13    | 0            | 0      |
| 14    | 0            | 0      |
| 15    | 0            | 0      |
| 16    | 0            | 0      |
| 17    | 0            | 0      |
| 18    | 0            | 0      |
| 19    | 0            | 0      |
| 20    | 0            | 0      |
| 21    | 0            | 0      |
| 22    | 0            | 0      |
| 23    | 0            | 0      |
| 24    | 0            | 0      |
| 25    | 0            | 0      |
| 26    | 0            | 0      |
| 27    | 0            | 0      |
| 28    | 0            | 0      |
| 29    | 0            | 0      |
| 30    | 0            | 0      |
| 31    | 0            | 0      |
| 32    | 0            | 0      |
| 33    | 0            | 0      |
| 34    | 0            | 0      |
| 35    | 0            | 0      |
| 36    | 0            | 0      |
| 37    | 0            | 0      |
| 38    | 0            | 0      |
| 39    | 0            | 0      |
| 40    | 0            | 0      |
| 41    | 0            | 0      |
| 42    | 0            | 0      |
| 43    | 0            | 0      |
| 44    | 0            | 0      |
| 45    | 0            | 0      |
| 46    | 0            | 0      |
| 47    | 0            | 0      |
| 48    | 0            | 0      |
| 49    | 0            | 0      |
| 50    | 0            | 0      |
| Note: The actual values for Hidden Layer and Output are not provided in the code. The actual values are represented by the dots on the vertical axis.
</details>

Sound generation with WaveNet [DeepMind 2017]

Which one do you think is generated?

![](images/ea4f43ab09a564e9f8be882930c272842b91005a639ecb0e5df101f592a7bf0d.jpg)

![](images/b760dcf4305f925f0fa5dbebf91c47820da58beef048cf11d6d3c77b7a9b3c7f.jpg)

Tacotron 2 Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram

# Vision + NLP

![](images/40e3ee97b650f487dae3de32894cd951353f40ee8c3efe7dc768d67d402f0146.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Is the mustache real?"] --> B["GRU"]
    B --> C["q"]
    C --> D["τ"]
    D --> E["Wq"]
    D --> F["Wc"]
    D --> G["Wc"]
    D --> H["Wc"]
    D --> I["Wc"]
    D --> J["Wc"]
    D --> K["Wc"]
    D --> L["Wc"]
    D --> M["Wc"]
    D --> N["Wc"]
    D --> O["Wc"]
    D --> P["Wc"]
    D --> Q["Wc"]
    D --> R["Wc"]
    D --> S["Wc"]
    D --> T["Wc"]
    D --> U["Wc"]
    D --> V["Wc"]
    D --> W["Wc"]
    D --> X["Wc"]
    D --> Y["Wc"]
    D --> Z["Wc"]
    D --> AA["Wc"]
    D --> AB["Wc"]
    D --> AC["Wc"]
    D --> AD["Wc"]
    D --> AE["Wc"]
    D --> AF["Wc"]
    D --> AG["Wc"]
    D --> AH["Wc"]
    D --> AI["Wc"]
    D --> AJ["Wc"]
    D --> AK["Wc"]
    D --> AL["Wc"]
    D --> AM["Wc"]
    D --> AN["Wc"]
    D --> AO["Wc"]
    D --> AP["Wc"]
    D --> AQ["Wc"]
    D --> AR["Wc"]
    D --> AS["Wc"]
    D --> AT["Wc"]
    D --> AU["Wc"]
    D --> AV["Wc"]
    D --> AW["Wc"]
    D --> AX["Wc"]
    D --> AY["Wc"]
    D --> AZ["Wc"]
    D --> BA["Wc"]
    D --> BB["Wc"]
    D --> BC["Wc"]
    D --> BD["Wc"]
    D --> BE["Wc"]
    D --> BF["Wc"]
    D --> BG["Wc"]
    D --> BH["Wc"]
    D --> BI["Wc"]
    D --> BJ["Wc"]
    D --> BK["Wc"]
    D --> BL["Wc"]
    D --> BM["Wc"]
    D --> BN["Wc"]
    D --> BO["Wc"]
    D --> BP["Wc"]
    D --> BQ["Wc"]
    D --> BR["Wc"]
    D --> BS["Wc"]
    D --> BT["Wc"]
    D --> BU["Wc"]
    D --> BV["Wc"]
    D --> BW["Wc"]
    D --> BX["Wc"]
    D --> BY["Wc"]
    D --> BZ["Wc"]
    D --> CA["Wc"]
    D --> CB["Wc"]
    D --> CC["Wc"]
    D --> CD["Wc"]
    D --> CE["Wc"]
    D --> CF["Wc"]
    D --> CG["Wc"]
    D --> CH["Wc"]
    D --> CI["Wc"]
    D --> CJ["Wc"]
    D --> CK["Wc"]
    D --> CL["Wc"]
    D --> CM["Wc"]
    D --> CN["Wc"]
    D --> CO["Wc"]
    D --> CP["Wc"]
    D --> CQ["Wc"]
    D --> CR["Wc"]
    D --> CS["Wc"]
    D --> CT["Wc"]
    D --> CU["Wc"]
    D --> CV["Wc"]
    D --> CW["Wc"]
    D --> CX["Wc"]
    D --> CY["Wc"]
    D --> CZ["Wc"]
```
</details>

[VQA-Mutan 2017]

![](images/72c8c0db4324d67e358078217eb439e2cc38b78de22ef1d7dd104b340fa0177c.jpg)

<details>
<summary>natural_image</summary>

Man playing acoustic guitar with strings, wearing a T-shirt and jeans (no visible text or symbols)
</details>

"man in black shirt isplaying guitar."

![](images/28c094adbbe8292a2ea7db6e41760ae31f2a812fb791985687c8b757565292bf.jpg)

<details>
<summary>natural_image</summary>

Construction worker in safety gear operating machinery on a worksite (no visible text or symbols)
</details>

"construction worker in orange safety vest is working on road."

![](images/2735e00f7c295ee72d7656ed8106546d9a853012ca6859518038b6d154d628e5.jpg)

<details>
<summary>natural_image</summary>

A woman and a baby sitting on a red surface with a colorful LEGO building (no text or symbols visible)
</details>

"two young girlsare playing with

![](images/e9c49e67cd73e341c5edca9faf33fd66d92749829060d2195ca37bdf4aa00744.jpg)

<details>
<summary>natural_image</summary>

Person performing a mid-air acrobatic trick over a lake, with no visible text or symbols.
</details>

"boy is doing backflip on wakeboard."   
[Karpathy2015]

# Vision + NLP

an armchair in the shape of an avocado [..]

![](images/94bcc7ae7414b38e859c3695df8ef12fcccffbe36a8ee16ba9d5a2fa2c419cd4.jpg)

<details>
<summary>natural_image</summary>

Five modern green armchairs with yellow covers, arranged in a row (no text or symbols visible)
</details>

TEXTPROMPT

a store front that has the word 'openai' written on it [.]

AI-GENERATEDIMAGES   
![](images/e20edf80a37e6e7f38e8bbb2796757efdb7dbf188ad61c605f93b42bd238e8b9.jpg)

<details>
<summary>text_image</summary>

OPENAI
OPENAI
OPENAI
OPENAI
OPENAI
</details>

Open-AI GPT-3, or DALL-E: https://openai.com/blog/dall-e/

# Genomics

1.High-throughput experiments   
![](images/cc66b5c2b6f091f0ba8509c5dae468d865edab2ab03f6102ee6fa0b04d4a0802.jpg)  
PBM

![](images/1af60b06ced35f2bbc6512229ea791befd39cc1cd08ef641f46feacf67946641.jpg)  
SELEX

![](images/342a281215e8445f4471a935c1b6ee2bd2780e94ce194108106a2703f75334a3.jpg)  
ChIP/CLIP

2.Massivelyparalleldeep learning   
![](images/566d67c87a002470e79b05517497564d0634407dccfd1287766cd757248bcc35.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Large-scale data sets"] --> B["GPU server"]
    B --> C["Automatic model training"]
    C --> D["New motifs"]
    C --> E["Prediction network"]
    D --> F["DeepBind models"]
    E --> F
```
</details>

3.Community needs   
![](images/d63bd3551bc7138e6f11552241231acbdabf42b192e73bbcff0d1c71405e1f46.jpg)  
Generegulation

![](images/a7ebd1a6aff27cf9a062e61ac6f958d5847fd97a4633f8869ceab0bf884c6225.jpg)  
Precision medicine

![](images/b6c4cd5394ecc105708e0f46a03543273e0c4e07e65ba733cb7e99bd05ff1e40.jpg)  
Detect binding sites

[Deep Genomics 2017]   
![](images/742baa0a1e9c8b2d1854a466bdfc54ea4ef00d1c80d1f38fab872c6dbe3f0ad6.jpg)

![](images/0d2560400d88f1d876a80402923e9390fe80c7e104b615ed7e32a910e078a86d.jpg)

<details>
<summary>natural_image</summary>

3D protein structure visualization with alpha helices and beta sheets in blue and green (no labels or text)
</details>

T1037 /6vr4  
90.7 GDT   
(RNA polymerase domain)

![](images/b2b65cab2fb700a1eb96984b41f18c8c3ede2d654ad5874b2185950d58c7c4db.jpg)

<details>
<summary>natural_image</summary>

3D protein structure diagram with blue and green secondary structure elements (no labels or text)
</details>

T1049 /6y4f  
93.3 GDT   
(adhesin tip)

AlphaFold by DeepMind

Experimental result   
Computational prediction

# Chemistry Physics

![](images/25d77717c7089f7e3459e2f9fda72ace56eded5ca629a3c617fb45927c03c419.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["SMILES input"] --> B["c1ccccc1"]
    B --> C["ENCODER Neural Network"]
    C --> D["CONTINUOUS MOLECULAR REPRESENTATION (Latent Space)"]
    D --> E["f(z)"]
    E --> F["PROPERTY PREDICTION"]
    F --> G["SMILES output"]
    G --> H["c1ccccc1"]
    H --> I["ENCODER Neural Network"]
    I --> J["CONTINUOUS MOLECULAR REPRESENTATION (Latent Space)"]
    J --> K["PROPMENT PREDICTION"]
```
</details>

[G6mez-Bombarelli 2016]

![](images/58024372f3b0f263ce8c50459ea360a7b4b067ba0839e4bb4b6c9afa28596401.jpg)

<details>
<summary>natural_image</summary>

Three-panel image showing a mushroom cloud with a red pagoda on top, each with smoke and shadow (no text or symbols)
</details>

[Tompson 2016]   
![](images/8c814a0f5d182e3a9e209fb6365af60d76763c3f19e83c6cc7ffd4cfdb8590bf.jpg)

<details>
<summary>natural_image</summary>

3D rendered image of a red arch structure with shadow figure, no text or symbols visible
</details>

Finite element simulator accelerated (\~100 fold) by a 3D convolutional network

# Deep Learning for AI

![](images/fda39c44a92e4ae6074f89ebb360497d3d14e7d7eda6f3c8c28c82c1e0413ddc.jpg)

<details>
<summary>text_image</summary>

ALPHAGO
00:10:29
AlphaGo
Google DeepMind
LEE SEDOL
00:01:00
</details>

![](images/4a407fb6b1b8c1c9836b546e722ebc05b1d702cd453063349d1e38e6fff8417b.jpg)

<details>
<summary>text_image</summary>

w 20/30/0, b 8/40/2
</details>

A10: English Opening   
![](images/e2c898038d5a0bd8bb455ee5e76d079c6f74b51b51f5e28094d5cec7caac9a56.jpg)

<details>
<summary>line</summary>

| Time | Value |
|------|-------|
| 0:00 | 6%    |
| 2:00 | 12%   |
| 4:00 | 19%   |
| 6:00 | 12%   |
| 8:00 | 12%   |
</details>

[Deepmind AlphaGo／Zero 2017]

![](images/cf804818e233ce7d30b0908a2c81dcd7bcd8dfbac6ec4046b05e4feec52c1770.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Image"] --> B["Convolution"]
    B --> C["Convolution"]
    C --> D["Fully connected"]
    D --> E["Fully connected"]
    E --> F["No input"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#cfc,stroke:#333
    style D fill:#fcc,stroke:#333
    style E fill:#cff,stroke:#333
    style F fill:#ffc,stroke:#333
```
</details>

[Atari Games - DeepMind 2016]

![](images/f1db98d371da70f5ff91c5a6a3537f2ade307c2c8a4abc6ed875588a7ba6eeff.jpg)

<details>
<summary>text_image</summary>

TYPE
PLAYER
VISION
HEALTH
</details>

[Starcraft2 forAl research]

AlphaGo/Zero: Monte Carlo Tree Search, Deep Reinforcement Learning, self-play

# Won IMO Gold Medal 2025

![](images/dec82b3a706b8081ab7bb1048b069442dee8a5bdeb56768f26be58804226deed.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["IMO 2024\nFormal mathematics\nAlphaProof & AlphaGeometry"] --> B["IMO 2025\nInformal mathematics\nAdvanced Gemini with Deep Think"]
```
</details>

# Image editing by Gemini

![](images/bc134078e72c8fb09c3e8f4e62bcbc604bbe968835eb0cd4b1cce56d54c83c58.jpg)

<details>
<summary>natural_image</summary>

Two-panel image showing a person in an astronaut helmet, one with visible facial features and the other with a damaged face (no text or symbols)
</details>

Prompt: remove the helmet.

# Image editing by Gemini

![](images/c2a7086ca137e065d76c4f1265abc797edcf5c423c90f0a4d24594ebb48dd7bf.jpg)

<details>
<summary>natural_image</summary>

Two portrait photos of a woman with floral headpiece and red berries, set against blue background (no text or symbols)
</details>

Prompt: Change the head piece to something made from red flowers.

LAMBDA: A Large Model Based Data Agent   
![](images/f461efcfb840c88d85fa5546868f05de9077ecbdf5ed2103c49f9ad3fb206498.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["User"] --> B["Data"]
    B --> C["Large Language Models"]
    C --> D["LAMBDA"]
    D --> E["Knowledge Integration"]
    E --> F["Instructions"]
    F --> A
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#cfc,stroke:#333
    style D fill:#fcc,stroke:#333
    style E fill:#cff,stroke:#333
    style F fill:#ffc,stroke:#333
```
</details>

https://www.polyu.edu.hk/ama/cmfai/lambda.html

# Deep Neural Networks

# with

# motivating examples

An Example   
![](images/feca6e686f3844004605a22d6d443a8cb051439e475197fae0b33a41ee15eee1.jpg)

<details>
<summary>scatter</summary>

| x    | y    |
| ---- | ---- |
| 0.0  | -5.0 |
| 0.5  | -4.5 |
| 1.0  | -4.0 |
| 1.5  | -3.5 |
| 2.0  | -3.0 |
| 2.5  | -2.5 |
| 3.0  | -2.0 |
| 3.5  | -1.5 |
| 4.0  | -1.0 |
| 4.5  | -0.5 |
| 5.0  | 0.0  |
| 5.5  | 0.5  |
| 6.0  | 1.0  |
| 6.5  | 1.5  |
| 7.0  | 2.0  |
| 7.5  | 2.5  |
| 8.0  | 3.0  |
| 8.5  | 3.5  |
| 9.0  | 4.0  |
| 9.5  | 4.5  |
| 10.0 | 5.0  |
| 10.5 | 5.5  |
| 11.0 | 6.0  |
| 11.5 | 6.5  |
| 12.0 | 7.0  |
| 12.5 | 7.5  |
| 13.0 | 8.0  |
| 13.5 | 8.5  |
| 14.0 | 9.0  |
| 14.5 | 9.5  |
| 15.0 | 10.0 |
</details>

Least squares regression   
Data $( X _ { i } , Y _ { i } ) , i = 1 , \ldots , n .$   
To find a

$$
\boldsymbol {f} (\boldsymbol {x}; \alpha , \beta) = \boldsymbol {\beta} ^ {\prime} \boldsymbol {x} + \alpha
$$

such that

$$
\Sigma \big (Y _ {i} - f (X _ {i}) \big) ^ {2}
$$

is minimized over

$$
\begin{array}{c} \mathcal {F} = \{\boldsymbol {f} \colon \boldsymbol {f} (\boldsymbol {x}; \alpha , \beta) = \boldsymbol {\beta} ^ {\prime} \boldsymbol {x} + \alpha , \\ \boldsymbol {\alpha}, \boldsymbol {\beta} \in \mathbb {R} \} \end{array}
$$

The model $f ( x ; \pmb { \alpha } , \beta )$ is linear in the input ????.   
Simple, efficient, easy to compute.   
Not expressive, especially for nonlinear data.

An Example   
![](images/a228dfc12fd9374b98a47231950838038dddbeb7be6fd18658f5776319d8b7d7.jpg)

<details>
<summary>bar_line</summary>

| x      | y (red line) | y (blue dots) |
| ------ | ------------ | ------------- |
| -10.0  | 1.2          | 0.9           |
| -7.5   | 0.0          | -0.4          |
| -5.0   | -0.6         | -0.8          |
| -2.5   | 0.4          | 0.5           |
| 0.0    | 0.1          | -0.1          |
| 2.5    | -0.2         | -0.3          |
| 5.0    | 0.3          | 0.4           |
| 7.5    | 0.7          | 0.6           |
| 10.0   | -1.2         | -1.1          |
</details>

Data $( X _ { i } , Y _ { i } ) , i = 1 , \ldots , n .$   
To find a network

$$
f (x; \theta)
$$

such that

$$
\Sigma \left(Y _ {i} - f (X _ {i})\right) ^ {2}
$$

is minimized over

???? = {????: ???? ????; ???? ???????? ???? ???????????????? ???? ???????????????????????????? ???? ???? ???? ???? ???????? $\pmb { \theta } \in \mathbb { R } ^ { s } \}$

• The model ???? ????; ???? is a neural network parameterized by ????   
Can have many parameters, need training.   
• Very expressive, especially for high-dimensional nonlinear data.

# Mathematical Definition

# of

# Deep Neural Networks

# Feedforward Neural Networks (Multi-Layer Perceptrons)

• The architecture of a ${ \sf M L P }$ is expressed as a composition of a series of functions

$$
f _ {\theta} (x) = \mathcal {A} _ {L} \circ \sigma \circ \mathcal {A} _ {L - 1} \circ \sigma \circ \dots \circ \sigma \circ \mathcal {A} _ {1} (x), x \in \mathbb {R} ^ {d _ {0}}
$$

where

$$
\mathcal {A} _ {i} (x) = W _ {i} x + b _ {i}, \qquad x \in \mathbb {R} ^ {d _ {i - 1}}
$$

is the i-th linear transformation with

weight matrix $W _ { i } \in \mathbb { R } ^ { d _ { i } \times d _ { i - 1 } }$ and bias vector $b _ { i } \in \mathbb { R } ^ { d _ { i } }$ ,

and $\sigma$ is the activation function,

$\begin{array}{c} \mathsf { e . g . } , \qquad & { } \end{array}$

# Feedforward Neural Networks (Multi-Layer Perceptrons)

• The architecture of a MLP is expressed as a composition of a series of functions

$$
f _ {\theta} (x) = \mathcal {A} _ {L} \circ \sigma \circ \mathcal {A} _ {L - 1} \circ \sigma \circ \dots \circ \sigma \circ \mathcal {A} _ {1} (x), x \in \mathbb {R} ^ {d _ {0}}
$$

where

$$
\mathcal {A} _ {i} (x) = W _ {i} x + b _ {i}, \qquad x \in \mathbb {R} ^ {d _ {i - 1}}.
$$

Such MLP has ???? layers,

The input ???? is the 0-th layer and the output is the last layer.

$\begin{array} { r l } { h _ { i } ( x ) = } & { { } \circ \mathcal { A } _ { i } \circ \quad \circ \cdots \circ \quad \circ \mathcal { A } _ { 1 } ( x ) } \end{array}$ is the i-th layer, hidden layer.

The depth of the network $( L - 1 )$ , number of hidden layers.

• The width of the i-th layer is $d _ { i }$ . The width of the network is max $\{ d _ { 1 } , \dots , d _ { { L - 1 } } \}$   
• $\theta = ( W _ { 1 } , b _ { 1 } , \dots , W _ { L } , b _ { L } )$ collects all the parameters. Size of the network is # ????.

# Activation functions

$$
f _ {\theta} (x) = \mathcal {A} _ {L} \circ \sigma \circ \mathcal {A} _ {L - 1} \circ \sigma \circ \dots \circ \sigma \circ \mathcal {A} _ {1} (x), \qquad x \in \mathbb {R} ^ {d _ {0}}
$$

<table><tr><td>Sigmoid</td><td>Tanh</td><td>ReLU</td><td>Leaky ReLU</td></tr><tr><td> $g(z) = \frac{1}{1 + e^{-z}}$ </td><td> $g(z) = \frac{e^{z} - e^{-z}}{e^{z} + e^{-z}}$ </td><td> $g(z) = \max(0, z)$ </td><td> $g(z) = \max(\epsilon z, z)$ with  $\epsilon \ll 1$ </td></tr><tr><td><img src="images/1dc14c335d3c6b1374e8551b95615f313e5292a2d5c1776718bb383d1c0f40a5.jpg"/></td><td><img src="images/79ac8ae0408c8eba16614a06b9354f0c774282ea4655e68d851a58ead7b71cde.jpg"/></td><td><img src="images/0530a3d269fc4392a4b957db26206cdb060a30563706e929b21c872f22a8dc86.jpg"/></td><td><img src="images/0423443c37da3b1c8090368eb0501f2c8a085142260596a7ec0a031cc6ae51b4.jpg"/></td></tr></table>

An Activation functions is considered non-saturated if $\operatorname* { l i m } _ { x  \infty } \sigma ( x ) = \infty$ .

# Saturated Nonlinearity : Sigmoid, Tanh

Non-saturated Nonlinearity: Rectified Linear Unit (ReLU), Leaky ReLU

ReLU is a good default choice for most problems.

# Biological Neurons & Neurons in a Network

Impulses carried toward cell body   
![](images/d276f4d027b0d1b5bf5cdc8c212a5092a1e5ce0b37d69a3f7c4da3b390844af5.jpg)

<details>
<summary>text_image</summary>

dendrite
presynaptic terminal
axon
cell body
Impulses carried away
from cell body
</details>

This image by Felipe Perucho is licensed under CC-BY 3.0.

![](images/f525710bd9eb8881a967e6fc88edfdd390d806311f6347a355c9b632c64d10f4.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["x0"] --> B["w0"]
    C["axon from a neuron"] --> D["synapse"]
    E["w1x1"] --> F["cell body"]
    G["w2x2"] --> F
    F --> H["f"]
    I["dendrite"] --> J["Σ wi xi + b"]
    K["f"] --> L["f (Σ wi xi + b)"]
    M["activation function"] --> N["output axon"]
```
</details>

![](images/df21e9de85fe11aa214595837d2783dbda97a5cfeb136754ff06be6420d78932.jpg)

<details>
<summary>line</summary>

| x    | y     |
| ---- | ----- |
| -10  | 0.000 |
| -5   | 0.001 |
| 0    | 0.500 |
| 5    | 0.999 |
| 10   | 1.000 |
</details>

Sigmoid activation function $\frac { 1 } { 1 + e ^ { - x } }$

# Feedforward Neural Networks (Multi-Layer Perceptrons)

![](images/dd091486b15b3e8ab36b68addd2efb214af0de6a67fc2fba5c2096d31a451138.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    1 --> A
    2 --> A
    2 --> B
    3 --> A
    4 --> B
    4 --> C
    5 --> B
    5 --> C
    5 --> D
    6 --> B
    6 --> C
    7 --> D
    8 --> D
    9 --> D
```
</details>

![](images/0303381a0d77aeab9dddf7e8a8dc8ad8e18f0570a92e86f6ebc9d7036ff70646.jpg)

<details>
<summary>text_image</summary>

VS
</details>

![](images/2fc91380d9827102f1292f53632b95fe447de0823c1e99ca9fd7256771c5fbd6.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    1 --> A
    1 --> B
    1 --> C
    1 --> D
    2 --> A
    2 --> B
    2 --> C
    2 --> D
    3 --> A
    3 --> B
    3 --> C
    3 --> D
    4 --> A
    4 --> B
    4 --> C
    4 --> D
    5 --> A
    5 --> B
    5 --> C
    5 --> D
    6 --> A
    6 --> B
    6 --> C
    6 --> D
    7 --> A
    7 --> B
    7 --> C
    7 --> D
    8 --> A
    8 --> B
    8 --> C
    8 --> D
    9 --> A
```
</details>

Layers in MLP are fully connected

# Biological Neurons

# Neurons in a neural network:

![](images/1a26592bbb4f65a659739c6e23d8f814ed790500ec7a6888156b143beec49dac.jpg)

<details>
<summary>natural_image</summary>

Abstract illustration of branching yellow neural or vascular networks against a blue sky background (no text or symbols)
</details>

Complex connectivity

![](images/6e4759aa4e6bde5181ac501f8bfde82e4790a76be242ad03a8caac59520c9082.jpg)

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
        B1[" "] --> C10[" "]
    end

    style Input Layer fill:#f9f,stroke:#333
    style Output Layer fill:#ccf,stroke:#333
```
</details>

hidden layer 1 hidden layer 2

Layer structure

Fully connected

Computational efficient

Randomly wired neural networks generated by the classical Watts-Strogatz (WS) model: these three instances of random networks achieve (left-to-right)

79.1%, 79.1%, 79.0% classification accuracy on ImageNet under a similar computational budget to ResNet-50, which has 77.1% accuracy.

Randomly wired neural networks can also work!   
![](images/888568276bdf342a0daac8e50c49832bbc6c983a3c5d9fb5b2bdc87775c442d8.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph Layer1
        A1["conv₁"] --> B1["cluster"]
        A2["conv₁"] --> B2["cluster"]
        A3["conv₁"] --> B3["cluster"]
        A4["conv₁"] --> B4["cluster"]
        A5["conv₁"] --> B5["cluster"]
        A6["conv₁"] --> B6["cluster"]
        A7["conv₁"] --> B7["cluster"]
        A8["conv₁"] --> B8["cluster"]
        A9["conv₁"] --> B9["cluster"]
        A10["conv₁"] --> B10["cluster"]
        A11["conv₁"] --> B11["cluster"]
        A12["conv₁"] --> B12["cluster"]
        A13["conv₁"] --> B13["cluster"]
        A14["conv₁"] --> B14["cluster"]
        A15["conv₁"] --> B15["cluster"]
        A16["conv₁"] --> B16["cluster"]
        A17["conv₁"] --> B17["cluster"]
        A18["conv₁"] --> B18["cluster"]
        A19["conv₁"] --> B19["cluster"]
        A20["conv₁"] --> B20["cluster"]
        A21["conv₁"] --> B21["cluster"]
        A22["conv₁"] --> B22["cluster"]
        A23["conv₁"] --> B23["cluster"]
        A24["conv₁"] --> B24["cluster"]
        A25["conv₁"] --> B25["cluster"]
        A26["conv₁"] --> B26["cluster"]
        A27["conv₁"] --> B27["cluster"]
        A28["conv₁"] --> B28["cluster"]
        A29["conv₁"] --> B29["cluster"]
        A30["conv₁"] --> B30["cluster"]
        A31["conv₁"] --> B31["cluster"]
        A32["conv₁"] --> B32["cluster"]
        A33["conv₁"] --> B33["cluster"]
        A34["conv₁"] --> B34["cluster"]
        A35["conv₁"] --> B35["cluster"]
        A36["conv₁"] --> B36["cluster"]
        A37["conv₁"] --> B37["cluster"]
        A38["conv₁"] --> B38["cluster"]
        A39["conv₁"] --> B39["cluster"]
        A40["conv₁"] --> B40["cluster"]
        A41["conv₁"] --> B41["cluster"]
        A42["conv₁"] --> B42["cluster"]
        A43["conv₁"] --> B43["cluster"]
        A44["conv₁"] --> B44["cluster"]
        A45["conv₁"] --> B45["cluster"]
        A46["conv₁"] --> B46["cluster"]
        A47["conv₁"] --> B47["cluster"]
        A48["conv₁"] --> B48["cluster"]
        A49["conv₁"] --> B49["cluster"]
        A50["conv₁"] --> B50["cluster"]
        A51["conv₁"] --> B51["cluster"]
        A52["conv₁"] --> B52["cluster"]
        A53["conv₁"] --> B53["cluster"]
        A54["conv₁"] --> B54["cluster"]
        A55["conv₁"] --> B55["cluster"]
        A56["conv₁"] --> B56["cluster"]
        A57["conv₁"] --> B57["cluster"]
        A58["conv₁"] --> B58["cluster"]
        A59["conv₁"] --> B59["cluster"]
        A60["conv₁"] --> B60["cluster"]
        A61["conv₁"] --> B61["cluster"]
        A62["conv₁"] --> B62["cluster"]
        A63["conv₁"] --> B63["cluster"]
        A64["conv₁"] --> B64["cluster"]
        A65["conv₁"] --> B65["cluster"]
        A66["conv₁"] --> B66["cluster"]
        A67["conv₁"] --> B67["cluster"]
        A68["conv₁"] --> B68["cluster"]
        A69["conv₁"] --> B69["cluster"]
        A70["conv₁"] --> B70["cluster"]
        A71["conv₁"] --> B71["cluster"]
        A72["conv₁"] --> B72["cluster"]
        A73["conv₁"] --> B73["cluster"]
        A74["conv₁"] --> B74["cluster"]
        A75["conv₁"] --> B75["cluster"]
        A76["conv₁"] --> B76["cluster"]
        A77["conv₁"] --> B77["cluster"]
        A78["conv₁"] --> B78["cluster"]
        A79["conv₁"] --> B79["cluster"]
        A80["conv₁"] --> B80["cluster"]
        A81["conv₁"] --> B81["cluster"]
        A82["conv₁"] --> B82["cluster"]
        A83["conv₁"] --> B83["cluster"]
        A84["conv₁"] --> B84["cluster"]
        A85["conv₁"] --> B85["cluster"]
        A86["conv₁"] --> B86["cluster"]
        A87["conv₁"] --> B87["cluster"]
        A88["conv₁"] --> B88["cluster"]
        A89["conv₁"] --> B89["cluster"]
```
</details>

Xie S, Kirillov A, Girshick R, He K. Exploring randomly wired neural networks for image recognition. InProceedings of the IEEE/CVF International Conference on Computer Vision 2019 (pp. 1284-1293).

# Examples of Multi-Layer Perceptron (structure)

![](images/754a6017cfb89e6f387cacc15893e8fb6d52b3101455bfe1495edafd1d85b639.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Input Layer"] --> B["Hidden Layer"]
    C["Fully Connected (weights between) Layers"] --> D["Hidden Layer"]
    E["Input Layer"] --> F["Hidden Layer"]
    G["Fully Connected (weights between) Layers"] --> H["Hidden Layer"]
    I["Output Layer"] --> J["Hidden Layer"]
    style A fill:#f9f,stroke:#333
    style C fill:#f9f,stroke:#333
    style E fill:#f9f,stroke:#333
    style G fill:#f9f,stroke:#333
    style I fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style F fill:#bbf,stroke:#333
    style H fill:#bbf,stroke:#333
    style J fill:#bbf,stroke:#333
```
</details>

2-layer MLP with 1 hidden layer, depth = 1   
Network width = 6   
$\begin{array} { r l r } { \mathrm { ~ } } & { { } } & { = \left( 4 ^ { \ast } 6 + 6 \right) + \left( 6 ^ { \ast } 2 + 2 \right) = } \\ { \mathrm { ~ } } & { { } } & { = \left( 4 ^ { \ast } 6 + 6 \right) + \left( 6 ^ { \ast } 2 + 2 \right) = } \end{array}$   
$\begin{array} { r l } { \bullet } & { { } f _ { \theta } ( x ) = W _ { 2 } \pmb { \sigma } ( W _ { 1 } x + b _ { 1 } ) + b _ { 2 } } \end{array}$ ????

where $x \in \mathbb { R } ^ { 4 }$

$$
W _ {1} \in \mathbb {R} ^ {6 \times 4}, b _ {1} \in \mathbb {R} ^ {6},
$$

$$
W _ {2} \in \mathbb {R} ^ {2 \times 6}, b _ {2} \in \mathbb {R} ^ {2}.
$$

# Examples of Multi-Layer Perceptron (computation)

![](images/c5fc95f9c501eb1a524dac405ebfd85ddf276f6e9ab402fb50155eaf3d27c119.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    x1["x₁"] --> a1["a₁[1"]]
    x1 --> a2["a₂[1"]]
    x1 --> a3["a₃[1"]]
    x1 --> a4["a₄[1"]]
    x2["x₂"] --> a1
    x2 --> a2
    x2 --> a3
    x2 --> a4
    x3["x₃"] --> a1
    x3 --> a2
    x3 --> a3
    x3 --> a4
    a1 --> o["○"]
    a2 --> o
    a3 --> o
    a4 --> o
    o --> ŷ[ŷ]
```
</details>

$$
z _ {1} ^ {[ 1 ]} = w _ {1} ^ {[ 1 ] T} x + b _ {1} ^ {[ 1 ]}, a _ {1} ^ {[ 1 ]} = \sigma (z _ {1} ^ {[ 1 ]})
$$

$$
z _ {2} ^ {[ 1 ]} = w _ {2} ^ {[ 1 ] T} x + b _ {2} ^ {[ 1 ]}, a _ {2} ^ {[ 1 ]} = \sigma (z _ {2} ^ {[ 1 ]})
$$

$$
z _ {3} ^ {[ 1 ]} = w _ {3} ^ {[ 1 ] T} x + b _ {3} ^ {[ 1 ]}, a _ {3} ^ {[ 1 ]} = \sigma (z _ {3} ^ {[ 1 ]})
$$

$$
z _ {4} ^ {[ 1 ]} = w _ {4} ^ {[ 1 ] T} x + b _ {4} ^ {[ 1 ]}, a _ {4} ^ {[ 1 ]} = \sigma (z _ {4} ^ {[ 1 ]})
$$

$$
\widehat {\boldsymbol {y}} = \boldsymbol {w} _ {1} ^ {[ 2 ]} \cdot \boldsymbol {a} _ {1} ^ {[ 1 ]} + \boldsymbol {w} _ {2} ^ {[ 2 ]} \cdot \boldsymbol {a} _ {2} ^ {[ 1 ]} + \boldsymbol {w} _ {3} ^ {[ 2 ]} \cdot \boldsymbol {a} _ {3} ^ {[ 1 ]} + \boldsymbol {w} _ {4} ^ {[ 2 ]} \cdot \boldsymbol {a} _ {4} ^ {[ 1 ]} + \boldsymbol {b} _ {1} ^ {[ 2 ]}
$$

Different values of parameters (weights and bias) give different neural work.

Weights: $\begin{array} { r l r } { \boldsymbol { W } _ { 1 } = ( w _ { 1 } ^ { [ 1 ] } , w _ { 2 } ^ { [ 1 ] } , w _ { 3 } ^ { [ 1 ] } , w _ { 4 } ^ { [ 1 ] } ) } & { { } \boldsymbol { W } _ { 2 } = ( w _ { 1 } ^ { [ 2 ] } , w _ { 2 } ^ { [ 2 ] } , w _ { 3 } ^ { [ 2 ] } , w _ { 4 } ^ { [ 2 ] } ) } & { } \end{array}$ ????[

Biases: $b _ { 1 } = ( b _ { 1 } ^ { [ 1 ] } , b _ { 2 } ^ { [ 1 ] } , b _ { 3 } ^ { [ 1 ] } , b _ { 4 } ^ { [ 1 ] } ) \qquad b _ { 2 } = b _ { 1 } ^ { [ 2 ] }$ ????2 ???????? = ????1[2]

Examples of Multi-Layer Perceptron (programming)   
![](images/a730dc7bd38ffcb78efc41d3fdd73bdbd3eaf41fbd9035528b253bf2d1dff5a3.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Input Layer
        A1[" "] --> B1[" "]
        A2[" "] --> B2[" "]
        A3[" "] --> B3[" "]
    end
    subgraph Output Layer
        C1[" "] --> D1[" "]
        C2[" "] --> D2[" "]
        C3[" "] --> D3[" "]
    end
    style Input Layer fill:#f9f,stroke:#333
    style Output Layer fill:#ccf,stroke:#333
```
</details>

hidden layer 1 hidden layer 2

```python
# forward-pass of a 3-layer neural network:
f = lambda x: 1.0/(1.0 + np.exp(-x)) # activation function (use sigmoid)
x = np.random.randn(3, 1) # random input vector of three numbers (3x1)
h1 = f(np.dot(W1, x) + b1) # calculate first hidden layer activations (4x1)
h2 = f(np.dot(W2, h1) + b2) # calculate second hidden layer activations (4x1)
out = np.dot(W3, h2) + b3 # output neuron (1x1) 
```

# From shallow to deep

Shallow Neural Network   
![](images/d3410f43bc6e7061233ba76ee7b220a6b4b853572e999558508a4754b6223f83.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph Input Layer
        A1["Blue Node"] --> B1["Yellow Node"]
        A2["Blue Node"] --> B1["Yellow Node"]
        A3["Blue Node"] --> B2["Yellow Node"]
        A4["Blue Node"] --> B2["Yellow Node"]
        A5["Blue Node"] --> B3["Yellow Node"]
        A6["Blue Node"] --> B3["Yellow Node"]
    end
    subgraph Hidden Layer
        B1 --> C1["Green Node"]
        B2 --> C1["Green Node"]
        B3 --> C2["Green Node"]
        B4 --> C2["Green Node"]
        B5 --> C3["Green Node"]
    end
    subgraph Output Layer
        C1 --> D1["Green Arrow"]
        C2 --> D2["Green Arrow"]
        C3 --> D3["Green Arrow"]
    end
```
</details>

![](images/8217fbff120fb2e4084cbc6359836175dfe985969771821118a17bb8f7fb9a4e.jpg)  
Input Layer

Deep Neural Networks   
![](images/cbca4f71fa356a5ffd00c88fabd795a8f4e54753a840ee78bf3facd38827a038.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph Input Layer
        A1["Blue Node"] --> B1["Yellow Node"]
        A2["Blue Node"] --> B2["Yellow Node"]
        A3["Blue Node"] --> B3["Yellow Node"]
        A4["Blue Node"] --> B4["Yellow Node"]
        A5["Blue Node"] --> B5["Yellow Node"]
    end
    subgraph Hidden Layer
        C1["Yellow Node"] --> D1["Green Node"]
        C2["Yellow Node"] --> D2["Green Node"]
        C3["Yellow Node"] --> D3["Green Node"]
        C4["Yellow Node"] --> D4["Green Node"]
    end
    subgraph Output Layer
        E1["Green Node"] --> F1["Green Node"]
        E2["Green Node"] --> F2["Green Node"]
        E3["Green Node"] --> F3["Green Node"]
    end
```
</details>

![](images/e759cddad8d7016d4b2b6ee9ed5b1db1e7e980df0db58b2aa08a193d6af70990.jpg)  
Hidden Layer

![](images/e47288ba831457c3a92e0f7393c71cdcf1e61eecc48d31b18593814665a98fc3.jpg)  
Output Layer

From shallow to deep.

Do large Neural Networks overfit the data?

Underfit   
![](images/6bf237ae0077cbdc75bd69cf9188f65e929908dba240a4663e222c3515415c67.jpg)

<details>
<summary>scatter</summary>

| Output variable |
| --------------- |
| 0.5             |
| 1.2             |
| 1.8             |
| 2.3             |
| 2.7             |
| 3.1             |
| 3.5             |
| 4.0             |
| 4.5             |
| 5.0             |
| 5.5             |
| 6.0             |
| 6.5             |
| 7.0             |
| 7.5             |
| 8.0             |
| 8.5             |
| 9.0             |
| 9.5             |
</details>

Predictor variable

Optimal   
![](images/ed083b3321fe4cc1c93af1903e5c5521e92c1ab44c9198727f993188b206e931.jpg)

<details>
<summary>scatter</summary>

| Output variable |
| --------------- |
| 0.0             |
| 0.2             |
| 0.4             |
| 0.6             |
| 0.8             |
| 1.0             |
| 1.2             |
| 1.4             |
| 1.6             |
| 1.8             |
| 2.0             |
| 2.2             |
| 2.4             |
| 2.6             |
| 2.8             |
| 3.0             |
| 3.2             |
| 3.4             |
| 3.6             |
| 3.8             |
| 4.0             |
</details>

Predictor variable

Overfit   
![](images/15fac746e726322ac94a0d224add4dfdced0ff87a15ae77864863f3976dee5e6.jpg)

<details>
<summary>scatter</summary>

| Output variable |
| --------------- |
| 0               |
| 1               |
| 2               |
| 3               |
| 4               |
| 5               |
| 6               |
| 7               |
| 8               |
| 9               |
| 10              |
| 11              |
| 12              |
| 13              |
| 14              |
| 15              |
| 16              |
| 17              |
| 18              |
| 19              |
| 20              |
</details>

Predictor variable

Larger Neural Networks perform better on data with larger size   
![](images/9e77450146f579277c8f45537b5b1e9c34355b38e8361d89cafd69fbdd2922bf.jpg)  
Source: https://lilianweng.github.io/posts/2017-06-21-overview/

Neural networks are composited functions.

Neural networks can approximate other functions.

Neural networks can be expressive.

# Universality of Neural Networks (Arbitrary-width case)

Universal approximation theorem: Let $C ( X , Y )$ denote the set of continuous functions from $X$ to Y. Let $\sigma \in C ( \mathbb { R } , \mathbb { R } )$ . Note that $( \sigma \circ x ) _ { i } = \sigma ( x _ { i } )$ ，so $\sigma \circ x$ denotes $\sigma$ applied to each component of x.

Then $\sigma$ is not polynomial if andonly if for every $n \in \mathbb { N } , m \in \mathbb { N }$ , compact $K \subseteq \mathbb { R } ^ { n }$ $f \in C ( K , \mathbb { R } ^ { m } ) , \varepsilon > 0$ there exist $k \in \mathbb { N } , A \in \mathbb { R } ^ { k \times n } , b \in \mathbb { R } ^ { k } , C \in \mathbb { R } ^ { m \times k }$ such that

$$
\sup _ {x \in K} \| f (x) - g (x) \| <   \varepsilon
$$

where

$$
g (x) = C \cdot (\sigma \circ (A \cdot x + b))
$$

Any continuous functions defined on a compact set can be approximated arbitrarily well by a shallow neural network if the shallow neural network is arbitrarily wide.

# Universality of Neural Networks (Arbitrary-depth case)

Universal approximation theorem (L1 distance, ReLU activation, arbitrary depth, minimal width). For any Bochner-Lebesgue p-integrable function $f : \mathbb { R } ^ { n }  \mathbb { R } ^ { m }$ and any $\epsilon > 0$ there exists a fully-connected ReLU network F of width exactly $d _ { m } = \operatorname* { m a x } \{ n + 1 , m \}$ satisfying

$$
\int_ {\mathbb {R} ^ {n}} \| f (x) - F (x) \| ^ {p} \mathrm{d} x <   \epsilon .
$$

Moreover, there exists a function $f \in L ^ { p } ( \mathbb { R } ^ { n } , \mathbb { R } ^ { m } )$ and some $\epsilon > 0 .$ ,for which there is no fully-connected ReLU network of width less than $d _ { m } = \operatorname* { m a x } \{ n + 1 , m \}$ satisfying the above approximation bound.

Any continuous functions defined on a compact set can be approximated arbitrarily well by a fixed-width neural network if the neural network is arbitrarily deep.

Universality of Neural Networks   
![](images/58e12236ebbdcf8b11f4fb81d8ea563a3674af1cf2c8982dc7ceafe40e4b3a07.jpg)

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

![](images/cb20119b7efa3ece7dd15d130382e545a0e9fe4367e070550db6d91a93cfde04.jpg)

<details>
<summary>contour</summary>

| Class   | X Range | Y Range |
|---------|---------|---------|
| Class 1 | -10 to 0 | -10 to 0 |
| Class 1 | 0 to 5  | 0 to 5  |
| Class 1 | 5 to 10 | -5 to 0 |
| Class 1 | -10 to 0 | -10 to 0 |
| Class 2 | -10 to 0 | -10 to 0 |
| Class 2 | -5 to 0 | -5 to 0 |
| Class 2 | 0 to 5  | 0 to 5  |
| Class 2 | 5 to 10 | -5 to 0 |
| Class 2 | -10 to 0 | -10 to 0 |
</details>

![](images/58ce5a7938424fdd71fad8bb2dc0b0fae92b2aab95e5317601d16e1f5aca88f9.jpg)

<details>
<summary>area</summary>

| Region | X Range | Y Range |
|---|---|---|
| Class 1 | -10 to 0 | -10 to 3 |
| Class 1 | -5 to 0 | -5 to 0 |
| Class 1 | 0 to 5 | 0 to 3 |
| Class 1 | -10 to 0 | -10 to 3 |
| Class 2 | -10 to 0 | -10 to 3 |
| Class 2 | -5 to 0 | -5 to 0 |
| Class 2 | 0 to 5 | 0 to 3 |
| Class 2 | -10 to 0 | -10 to 3 |
The chart displays a single shaded region in the upper-right quadrant (Class 1) and below the lower-left quadrant (Class 1). The label 'Class 1' appears near the top-left corner, while 'Class 2' is on the right side.
</details>

![](images/b14e018d4be83df3d52949f7b0ea8990fff4046ac0d23d86eb2f238503862027.jpg)

<details>
<summary>area</summary>

| x    | Class 1 | Class 2 |
| ---- | ------- | ------- |
| -10  | -5      | -5      |
| -8   | 7       | -5      |
| -6   | -5      | -5      |
| -4   | 0       | -5      |
| -2   | 2       | -5      |
| 0    | 0       | -5      |
| 2    | 2       | -5      |
| 4    | -5      | -5      |
| 6    | 0       | -5      |
| 8    | 7       | -5      |
| 10   | -5      | -5      |
</details>

![](images/54a864d314ed7f9445ed5be509cc9212f7a033da9561e18a8b89878d913df2fb.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["∫"] --> B["∫"]
    A --> C["∫"]
    A --> D["∫"]
    B --> E["∫"]
    B --> F["∫"]
    C --> G["∫"]
    C --> H["∫"]
    D --> I["∫"]
    D --> J["∫"]
    style A fill:#fff,stroke:#000
    style B fill:#fff,stroke:#000
    style C fill:#fff,stroke:#000
    style D fill:#fff,stroke:#000
    style E fill:#fff,stroke:#000
    style F fill:#fff,stroke:#000
    style G fill:#fff,stroke:#000
    style H fill:#fff,stroke:#000
    style I fill:#fff,stroke:#000
    style J fill:#fff,stroke:#000
```
</details>

![](images/f91f6a8fc9aeea9452993950269c7135041666dacc6430fcc64546143f1c26db.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["∫"] --> B["∫"]
    A --> C["∫"]
    B --> D["∫"]
    B --> E["∫"]
    C --> F["∫"]
    C --> G["∫"]
    D --> H["∫"]
    D --> I["∫"]
    E --> J["∫"]
    E --> K["∫"]
    F --> L["∫"]
    F --> M["∫"]
    G --> N["∫"]
    G --> O["∫"]
    H --> P["∫"]
    H --> Q["∫"]
    I --> R["∫"]
    I --> S["∫"]
    J --> T["∫"]
    J --> U["∫"]
    K --> V["∫"]
    K --> W["∫"]
    L --> X["∫"]
    L --> Y["∫"]
    M --> Z["∫"]
    M --> AA["∫"]
    N --> AB["∫"]
    N --> AC["∫"]
    O --> AD["∫"]
    O --> AE["∫"]
```
</details>

![](images/3222479502550757d9021654935c4da26feed2fa5e019f4018c44c85c6d93f4d.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A[" "] --> B[" "]
    A --> C[" "]
    A --> D[" "]
    A --> E[" "]
    B --> F[" "]
    C --> G[" "]
    D --> H[" "]
    E --> I[" "]
    F --> J[" "]
    G --> K[" "]
    H --> L[" "]
    I --> M[" "]
    style A fill:#fff,stroke:#000
    style B fill:#fff,stroke:#000
    style C fill:#fff,stroke:#000
    style D fill:#fff,stroke:#000
    style E fill:#fff,stroke:#000
    style F fill:#fff,stroke:#000
    style G fill:#fff,stroke:#000
    style H fill:#fff,stroke:#000
    style I fill:#fff,stroke:#000
    style J fill:#fff,stroke:#000
    style K fill:#fff,stroke:#000
    style L fill:#fff,stroke:#000
    style M fill:#fff,stroke:#000
```
</details>

Neural networks can also approximate classification regions very well.

![](images/0f914a7cd127d8bbb5933e4fc93e93129402674a043725de7f518a7f2f509983.jpg)

<details>
<summary>bubble</summary>

| Model           | Operations [G-Ops] | Top-1 accuracy [%] |
| --------------- | ------------------ | ------------------ |
| Inception-v3    | 8                  | 76                 |
| ResNet-50       | 7                  | 73                 |
| ResNet-34       | 7                  | 73                 |
| ResNet-101      | 15                 | 78                 |
| ResNet-152      | 23                 | 78                 |
| VGG-16          | 30                 | 70                 |
| VGG-19          | 39                 | 70                 |
| ENet            | 2                  | 68                 |
| ResNet-18       | 3                  | 69                 |
| GoogLeNet       | 3                  | 69                 |
| BN-NIN          | 2                  | 62                 |
| BN-AlexNet      | 2                  | 55                 |
| AlexNet         | 2                  | 55                 |
</details>

Source: https://arxiv.org/pdf/1605.07678.pdf

Accuracy vs. operations, size ∝ parameters. Top-1 one-crop accuracy versus amount of operations required for a single forward pass. The size of the blobs is proportional to the number of network parameters; a legend is reported in the bottom right corner, spanning from 5×106 to 155×106 params. Both these figures share the same y-axis, and the grey dots highlight the centre of the blobs.

![](images/0288953bba1e71b53615721c5f57159496f706553de169c70b35460bac31f101.jpg)

<details>
<summary>bar</summary>

| Model         | Top-1 accuracy density [%/M-Params] |
| ------------- | ------------------------------------ |
| VGG-19        | 0.4                                  |
| VGG-16        | 0.4                                  |
| AlexNet       | 0.8                                  |
| BN-AlexNet    | 0.9                                  |
| ResNet-152    | 1.2                                  |
| ResNet-101    | 1.7                                  |
| Inception-v4  | 2.5                                  |
| ResNet-50     | 2.9                                  |
| Inception-v3  | 3.2                                  |
| ResNet-34     | 3.3                                  |
| ResNet-18     | 5.9                                  |
| BN-MIN        | 7.2                                  |
| GoogLeNet     | 9.8                                  |
| ENet          | 11.7                                 |
</details>

Accuracy per parameter vs. network. Information density (accuracy per parameters) is an efficiency metric that highlight that capacity of a specific architecture to better utilise its parametric space. Models like VGG and AlexNet are clearly oversized, and do not take fully advantage of their potential learning ability. On the far right, ResNet-18, BN-NIN, GoogLeNet and ENet (marked by grey arrows) do a better job at “squeezing” all their neurons to learn the given task, and are the winners of this section.

# Oh no! It seems too DEEP!!!!

![](images/947344fe1b2b3cd38f181790d8d99183bd2b0587aba6ee7b09f4b66c5a199a72.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    subgraph Layer1
        A1["●"] --> B1["○"]
        A2["..."] --> B1
        A3["○"] --> B1
        A4["..."] --> B1
    end
    subgraph Layer2
        B1 --> C1["○"]
        B1 --> C2["○"]
        B2["..."] --> C2
        B3["○"] --> C2
        B4["..."] --> C2
    end
    subgraph OutputLayer
        C1 --> D["○"]
        C2 --> D
        C3["..."] --> D
        C4["○"] --> D
        D --> E["○"]
    end
    style Layer1 fill:#f9f,stroke:#333
    style Layer2 fill:#bbf,stroke:#333
    style OutputLayer fill:#dfd,stroke:#333
```
</details>

# Next Time

How to use Deep Neural Networks to do regression?