# AMA 564 Deep Learning

# 2026 Spring

# Lecture 12

# 30K Tasks

Step1

Collect demonstratjondata, and traina supervised policy.

Apromptis sampledfromour promptdataset.

![](images/88d5ccb75117cb21c1471688cc268292c13134f2d5d841f58f532ba9e610dfd6.jpg)

Explain the moon landing toa6year old

![](images/709bde8ca866c8f46e824a97a100445c9ffbb2dc765fb431f8cefe559df99573.jpg)

Some people went to themoon...

![](images/2bb084cbecb014f6472ca2f9bc9f5b79e230185686fa35044db8ad28b46a977e.jpg)

![](images/1493afeb3f1c8b22115ed685e6d8595127e2294072b9f002868951ca0f46d9bb.jpg)

Alabeler demonstratesthe desired output behavior.

Thisdata isused to fine-tune GPT-3 with supervised learning.

Step2

Collect comparisondata, andtrainarewardmodel.

Apromptand severalmodel outputsare sampled.

Alabelerranks the outputs from best to worst.

This data is used totrain our reward model.

![](images/01484ecc625bad81bfe1b2ced068b2c03b837fe544222e2f14be28a2f828c85c.jpg)

Explain themoon landing toa6year old

![](images/9f9a13e84e1e2c15ada6777f2c36a91243d3e1ae74eae6d111e8ff96777ef229.jpg)

Explaingraity.

![](images/039fe20ec68bf3f914993205c89dea312a72d649b88880aad5e76b1ace115d1f.jpg)

Explain war

![](images/52aa1be37b16f6d5e8988edd83721f101aa4fd166b5dc7446c64f198bcdeabd6.jpg)

Meanis natural

![](images/f7b4864be980cfb693a1feca71d96844944c4037c8d21ea4abce0df8e1e26e9a.jpg)

Pecple went to themocn.

![](images/8d02a36d2d10b1ce412539137266b22b2400acf6340430ec6a715a454e15cbc7.jpg)

![](images/61b8b66f061a197ace83476164b2eab33be7e8c4873e8176e60d32be30a64021.jpg)

![](images/e7624145662528549b11fdb652dcddcc4f8bf657a88376ac6ebdfef112b390b4.jpg)

![](images/e580ad2c96ab09d3547bbde5aa32995fb570e48f450008c77aacf26dd445a682.jpg)

![](images/e468a6196c0e3ce5cb74bbfa0cd9be9c5beed95c31b22fe142930037cba7c9d1.jpg)

Step3

Optimizeapolicyagainst therewardmodel using reinforcementlearning.

Anewprompt issampledfrom thedataset.

Thepolicy generates anoutput.

![](images/482f0c26c2c44430c2332abb3725982055520317dbe198dfa92c2c5947e788cd.jpg)

Write astory about frogs

![](images/12a620bf131e8851d2154284aa87dbb79a36f38566ac9d7fe1a6a57432ccddaf.jpg)

PPO   
![](images/1909c2da9c40aa8e68738e315f5059508e6ff8de0e8607733241077ceba26096.jpg)

![](images/a6876dc81aaac89d914d13ef282b79991afdb774c602420c39fc7ed20482191c.jpg)

Onceuponatime...

![](images/29e701d9c1926651589e7e10db3d2ce739b5dfde4fb4eda6e1272d756ef248ad.jpg)  
RM

![](images/7692379f2dd68b17777c2fcbc87bae8a936e6c3c6f4135b78ba5795bbba2c402.jpg)

![](images/30e07718f05c5cd6f24d7f58dc5f2464d40bc22e11ecbf313fe4e2bc2bc4bf73.jpg)

![](images/7ab54acda22170b34b0ac6f7a32e06e5eb1282d1e587d2c887147ac5f9ffd3bf.jpg)

Thereward model calculatesa rewardfor theoutput.

Thereward is usedtoupdate thepolicy using PPO.

How do we actually change our LM parameters $\theta$ to maximize this?

$$
\mathbb {E} _ {\hat {s} \sim p _ {\theta} (s)} [ R (\hat {s}) ]
$$

· Let's try doing gradient ascent!

$$
\theta_ {t + 1} := \theta_ {t} + \alpha \nabla_ {\theta_ {t}} \mathbb {E} _ {\hat {s} \sim p _ {\theta_ {t} (s)}} [ R (\hat {s}) ]
$$

How do we estimate this expectation??

![](images/84c52118d9e6bd3035d2560a19cd9f5f5003e74fb609c17fd06e6d2e6f255782.jpg)

What if our reward function is nondifferentiable??

Policy gradient methods in RL (e.g., REINFORCE;[Wiliams,1992]) give us tools for estimating and optimizing this objective.

We want to obtain

(defn.of expectation） (linearity of gradient)

$$
\nabla_ {\theta} \mathbb {E} _ {\hat {s} \sim p _ {\theta} (s)} [ R (\hat {s}) ] = \nabla_ {\theta} \sum_ {s} R (s) p _ {\theta} (s) = \sum_ {s} R (s) \nabla_ {\theta} p _ {\theta} (s)
$$

Here we'lluse a very handy trick known as the log-derivative trick. Let's try taking the gradient of log $p _ { \theta } ( s )$

$$
\nabla_ {\theta} \log p _ {\theta} (s) = \frac {1}{p _ {\theta} (s)} \nabla_ {\theta} p _ {\theta} (s) \quad \Rightarrow \quad \nabla_ {\theta} p _ {\theta} (s) = p _ {\theta} (s) \nabla_ {\theta} \log p _ {\theta} (s)
$$

(chain rule)

This is an

Plug back in:

$$
\sum_ {s} R (s) \nabla_ {\theta} p _ {\theta} (s) = \sum_ {s} p _ {\theta} (s) R (s) \nabla_ {\theta} \log p _ {\theta} (s)
$$

Now we have put the gradient “inside" the expectation,we can approximate this objective with Monte Carlo samples:

$$
\nabla_ {\theta} \mathbb {E} _ {\hat {s} \sim p _ {\theta} (s)} [ R (\hat {s}) ] = \mathbb {E} _ {\hat {s} \sim p _ {\theta} (s)} [ R (\hat {s}) \nabla_ {\theta} \log p _ {\theta} (\hat {s}) ] \approx \frac {1}{m} \sum_ {i = 1} ^ {m} R (s _ {i}) \nabla_ {\theta} \log p _ {\theta} (s _ {i})
$$

This is why it's called "reinforcement learning": we reinforce good actions, increasing the chance they happen again.

Giving us the update rule:

$$
\begin{array}{l} \theta_ {t + 1} := \theta_ {t} + \alpha \frac {1}{m} \sum_ {i = 1} ^ {m} R (s _ {i})   \nabla_ {\theta_ {t}} \log p _ {\theta_ {t}} (s _ {i}) \\ \text {   is   a   lot   } \\ \text {   an   you   } \end{array}
$$

This is heavily simplified! There is more needed to do RL w/ LMs.Ca see any problems with this objective?

$p _ { \theta } ( s _ { i } )$

ke steps to minimize $p _ { \theta } ( s _ { i } )$

Awesome: now for any arbitrary, non-differentiable reward function R(s),we can train our language model to maximize expected reward.   
Not so fast!(Why not?)   
Problem 1: human-in-the-loop is expensive!

· Solution: instead of directly asking humans for preferences, model their preferences as a separate (NLP) problem![Knox and Stone,2009]

An earthquake hit San Francisco. There was minor property damage, but no injuries. The Bay Area has good weather but is prone to earthquakes and wildfires.

Train an LM $R M _ { \phi } ( s )$ predict human preferences from an annotated dataset, then optimize for $R M _ { \phi }$ instead.

![](images/c6e8ff33216b1bc81937a6136d6aed8b8b23c04cbf104b51f4f686d27c6c86ab.jpg)

<details>
<summary>text_image</summary>

S₁
R(s₁) = 8.0
</details>

$$
R (s _ {2}) ^ {s _ {2}} = 1. 2
$$

![](images/d466c559482b6525c28d0a722d526939c7cb41f6fb64c5968f489a49ce3826a2.jpg)

·Problem 2: human judgments are noisy and miscalibrated!   
Solution: instead of asking for direct ratings,ask for pairwise comparisons, which can be more reliable [Phelps et al.,2015; Clark et al.,2018]

A 4.2 magnitude earthquake hit San Francisco, resulting in massive damage.

$$
S _ {3}
$$

$$
R (s _ {3}) = 4. 1? \quad 6. 6? \quad 3. 2?
$$

. Problem 2: human judgments are noisy and miscalibrated!   
Solution: instead of asking for direct ratings,ask for pairwise comparisons, which can be more reliable [Phelps et al.,2015; Clark et al., 2018]

An earthquake hit San Francisco. There was minor property damage, but no injuries.

V

A 4.2 magnitude earthquake hit San Francisco, resulting in massive damage.

V

The Bay Area has good weather but is prone to earthquakes and wildfires.

![](images/a56a4efff49b307c2b2ef5a0a451f5fd85ef23feb3e0953a8453b98828d46079.jpg)

<details>
<summary>bar</summary>

| Category       | Value |
| -------------- | ----- |
| The            | 1.2   |
| Bay            | 1.2   |
| Area           | 1.2   |
| ...            | 1.2   |
| ...            | 1.2   |
| wildfires      | 1.2   |
</details>

S3

S2

Bradley-Terry [1952] paired comparison model

$$
J _ {R M} (\phi) = - \mathbb {E} _ {(s ^ {w}, s ^ {l}) \sim D} \big [ \log \sigma (R M _ {\phi} (s ^ {w}) - R M _ {\phi} (s ^ {l})) \big ]
$$

"losing"

sample

sW should score higher than $s ^ { l }$

Feedbackcomesaspreferencesovermodelsamples: $\mathcal { D } = \{ x ^ { i } , y _ { w } ^ { i } , y _ { l } ^ { i } \}$ Prompt Dispreferred response Preferred response

Bradley-Terry Model connects rewards to preferences:

$$
p (y _ {w} \succ y _ {l} \mid x) = \sigma (r (x, y _ {w}) - r (x, y _ {l}))
$$

Train the reward model by minimizing negative log likelihood:

$$
\mathcal {L} _ {R} (\phi , \mathcal {D}) = - \mathbb {E} _ {(x, y _ {w}, y _ {l}) \sim \mathcal {D}} \left[ \log \sigma (r _ {\phi} (x, y _ {w}) - r _ {\phi} (x, y _ {l})) \right]
$$

Now we have a reward model $r _ { \phi }$ that represents\* goodness according to humans

Now,learn a policy $\pi _ { \theta }$ achieving highrewardwhilestaying close to original model $\pi _ { \mathrm { r e f } }$

$$
\max _ {\pi_ {\theta}} \mathbb {E} _ {x \sim \mathcal {D}, y \sim \pi_ {\theta} (y | x)} [ r _ {\phi} (x, y) ] - \beta \mathbb {D} _ {\mathrm{KL}} [ \pi_ {\theta} (y | x) | | \pi_ {\text {ref}} (y | x) ]
$$

![](images/afef3777bc2fd0ac2cae9d2fac65c786a265712941caabf38fffd22671e0e482.jpg)

Sample from policy

![](images/b4e523eb1de2b73c46d26c9dd854aad63d1f29d99aaf1b11e5dc8c1b6db1ab6b.jpg)

Want high reward...

![](images/cfc3a2618683f7a334d48115dc7849da3c443de2d9091813af83ddc401d8b942.jpg)

...but keep KL to original model small!

![](images/bd0a76e9db5cc2bd6b9742ea39db56dde7deb8442cce9b350f8e90b9c64a6eae.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["User Query"] --> B["Policy LM π^RL θ_old"]
    B --> C["Experience Buffer"]
    C --> D["Value Model V_φ(s_t)"]
    D --> E["GAE"]
    E --> F["Policy LM π^RL θ"]
    F --> G["PPO-clip Loss"]
    G --> H["MSE Loss"]
    H --> I["Value Model V_φ(s_t)"]
    I --> J["Experience Buffer"]
    J --> K["Policy LM π^RL θ"]
    K --> L["Pretraining Data"]
    L --> M["Policy LM π^RL θ"]
    M --> N["GAE"]
    N --> O["Advantage Function"]
    N --> P["TD Error"]
    N --> Q["Return"]
    O --> R["π^RL_θ (at|st)"]
    P --> S["π^RL_θ (at|st)"]
    Q --> T["π^RL_θ (at|st)"]
    R --> U["π^RL_θ (at|st)"]
    S --> V["π^RL_θ (at|st)"]
    T --> W["π^RL_θ (at|st)"]
    U --> X["π^RL_θ (at|st)"]
    V --> Y["π^RL_θ (at|st)"]
    W --> Z["π^RL_θ (at|st)"]
    X --> AA["π^RL_θ (at|st)"]
    Y --> AB["π^RL_θ (at|st)"]
    Z --> AC["π^RL_θ (at|st)"]
    AA --> AD["π^RL_θ (at|st)"]
    AB --> AE["π^RL_θ (at|st)"]
    AC --> AF["π^RL_θ (at|st)"]
    AD --> AG["π^RL_θ (at|st)"]
    AE --> AH["π^RL_θ (at|st)"]
    AF --> AI["π^RL_θ (at|st)"]
    AG --> AJ["π^RL_θ (at|st)"]
    AH --> AK["π^RL_θ (at|st)"]
    AI --> AL["π^RL_θ (at|st)"]
    AJ --> AM["π^RL_θ (at|st)"]
    AK --> AN["π^RL_θ (at|st)"]
    AL --> AO["π^RL_θ (at|st)"]
    AM --> AP["π^RL_θ (at|st)"]
    AN --> AQ["π^RL_θ (at|st)"]
    AO --> AR["π^RL_θ (at|st)"]
    AP --> AS["π^RL_θ (at|st)"]
    AQ --> AT["π^RL_θ (at|st)"]
    AR --> AU["π^RL_θ (at|st)"]
    AS --> AV["π^RL_θ (at|st)"]
    AT --> AW["π^RL_θ (at|st)"]
    AU --> AX["π^RL_θ (at|st)"]
    AV --> AY["π^RL_θ (at|st)"]
    AW --> AZ["π^RL_θ (at|st)"]
```
</details>

Figure1:PPO workflow,depicting thesequential steps in thealgorithm's execution. The process beginswithsampling from the environment,followed bytheapplicationof GAE for improved advantage approximation. The diagram then illustrates the computation of various lossfunctions employed in PPO,signifyingthe iterative nature of the learning processand the policy updates derived from these losses.

Accelerate RLHF with Variance Increase   
Direct Preference Optimization

![](images/167f1b8e58a1b3674859b9555b88fa519e0841a596bb1700893862680873e456.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    q --> Policy["Policy Model"]
    Policy --> o
    o --> Reference["Reference Model"]
    o --> Reward["Reward Model"]
    o --> Value["Value Model"]
    Reference --> KL["⊕"]
    Reward --> KL
    Value --> KL
    KL --> r["r"]
    r --> GAE["GAE"]
    GAE --> A
    v --> Value
    v --> Reference
```
</details>

![](images/b9cedf21a556b7dce8327aa836360424533b4cdeb6f752614e056269e539edae.jpg)

<details>
<summary>text_image</summary>

Trained
Models
Frozen
Models
</details>

![](images/9979344313a1c6e8aba901abe80e8b0cda3758b8841671474391b07cfe7895be.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    q --> Policy["Policy Model"]
    Policy --> o1["o₁"]
    Policy --> o2["o₂"]
    Policy --> ...
    o2 --> Reference["Reference Model"]
    o2 --> Reward["Reward Model"]
    Reward --> r1["r₁"]
    Reward --> r2["r₂"]
    Reward --> ...
    r1 --> Group["Group Computation"]
    r2 --> Group
    ... --> Group
    R1 --> A1["A₁"]
    R2 --> A2["A₂"]
    ... --> A_G["A_G"]
    A1 --> KL["KL"]
    A2 --> KL
    AG["A_G"] --> KL
```
</details>

Fig. 3. Comparison of popular RL fine-tuning methods in RLHF

• GRPO has exhibited comparable performance with less computational cost compared to PPO.

[2] Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., ... & Guo, D. (2024). Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300.   
[3] Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R., ... & He, Y. (2025). Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948.

![](images/b781781ab4ecd67d888f04853f2a91fb7c8ec44c32af559e5214e4f795f7346a.jpg)

<details>
<summary>line</summary>

| train/global_step | GRPO  | PPO   |
| ----------------- | ----- | ----- |
| 0                 | -0.2  | -0.2  |
| 20                | 0.1   | 0.1   |
| 40                | 0.3   | 0.4   |
| 60                | 0.4   | 0.5   |
| 80                | 0.5   | 0.6   |
| 100               | 0.5   | 0.8   |
</details>

Fig. 4. Performance of PPO and GRPO during training process

GRPO has comparable performance compared to PPO at the beginning but suffers from slow training in the end.

GRPO has comparable performance compared to PPO at the beginning but suffers from slow training in the end.   
• Although GRPO needs less training resources, it suffers from its slow training in practice.   
• How to accelerate GRPO?

[2] Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., ... & Guo, D. (2024). Deepseekmath: Pushing the limits of mathematical [2]Shao,Z.,Wang，P.,ZuQ.,Xu，R.,Song,J.Bi,X,.,&GuoD.(2024).Deepseekmath:Pushing thelimitsofmathematical reasoning in open language models. arXiv preprint arXiv:2402.03300. reasoning in open language models. arXiv preprint arXiv:2402.03300. [3] Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R., ... & He, Y. (2025). Deepseek-r1: Incentivizing reasoning capability in [3]Guo,DangD,ZangHongJZang,RXuR&He.(25)Deepseek:ncentivingreasonngaiit llms via reinforcement learning. arXiv preprint arXiv:2501.12948. IIms via reinforcement learning. arXiv preprint arXiv:2501.12948. [4] Hou, Z., Du, P., Niu, Y., Du, Z., Zeng, A., Liu, X., ... & Dong, Y. (2024). Does RLHF Scale? Exploring the Impacts From Data, [4] Hou,Z,Du,P.,NiuY.,Du,Z,Zeng,A,Liu,X.,&DongY.(2024).DoesRLHFScaleExploringtheImpactsFromData Model, and Method. arXiv preprint arXiv:2412.06000. Model,and ethod.arXivpreprintarXiv:241206000. [5] Li, G., Lin, M., Galanti, T., Tu, Z., & Yang, T. (2025). DisCO: Reinforcing Large Reasoning Models with Discriminative Constrained [5]LiG,LinalantiuZngT(2).DisCOReinforingargeReasoingModelswithiscriminatieContrned Optimization. arXiv preprint arXiv:2505.12366. Optimization.arXiv preprint arXiv:2505.12366.

• Both accuracy and reward variance matter in RLHF training!

![](images/233afd383c5df1c936187048e1e6071e56742bcff7dcaf47e8d5bde80f96afb3.jpg)

<details>
<summary>text_image</summary>

Initial policy
</details>

Reward Model   
![](images/5796ce0e90d6471367c9bc266eeddcf2970de073b1cd072631250d82b853bc64.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["High"] --> B["Moderate"]
    B --> C["Low"]
```
</details>

Reward Variance   
![](images/0113b3b07abe4ead6225075ca8d3b348dcc8ab806812b815cfe72a93760ca61d.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["High"] --> B["Moderate"]
    B --> C["Low"]
```
</details>

Fig. 5. Illustration of the roles of accuracy and reward variance in RLHF

Theorem. For RLHF objective

$$
\mathbb {E} _ {\mathbf {x} \sim \mathcal {D}} \left[ \mathbb {E} _ {\mathbf {y} \sim \pi_ {\theta} (\cdot | \mathbf {y})} [ r (\mathbf {x}, \mathbf {y}) ] - \lambda D _ {\mathrm{KL}} \big (\pi_ {\theta} (\cdot | \mathbf {y}) | | \pi_ {\mathrm{ref}} (\cdot | \mathbf {y}) \big) \right]
$$

Given any $\gamma > 0$ , prompt $\mathbf { x } \in \mathcal X$ , the time it takes until

$$
\mathbb {E} _ {\mathbf {y} \sim \pi_ {\theta (t)} (\cdot | \mathbf {y})} [ r (\mathbf {x}, \mathbf {y}) ] \geq \mathbb {E} _ {\mathbf {y} \sim \pi_ {\theta (0)} (\cdot | \mathbf {y})} [ r (\mathbf {x}, \mathbf {y}) ] + \gamma
$$

is at least:

$$
\Omega \left(\mathbb {E} _ {\mathbf {x ^ {\prime}} \sim \mathcal {D}} \left[ \mathrm{Var} _ {\mathbf {y} \sim \pi_ {\theta (0)} (\cdot | \mathbf {x ^ {\prime}})} r (\mathbf {x ^ {\prime}}, \mathbf {y}) \right] ^ {- \frac {1}{3}}\right)
$$

Natural idea: accelerating by increasing $\begin{array} { r } { \mathbb { E } _ { \mathbf { x } ^ { \prime } \sim \mathcal { D } } \left[ \operatorname { V a r } _ { \mathbf { y } \sim \pi _ { \theta ( 0 ) } ( \cdot | \mathbf { x } ^ { \prime } ) } r ( \mathbf { x } ^ { \prime } , \mathbf { y } ) \right] ^ { - \frac { 1 } { 3 } } } \end{array}$

How to increase?

![](images/008b56bbd5743c4a867e630a41b53e9a353896391c6f1cfdd304a5d99292a5af.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Ex~D"] --> B["fixed"]
    C["Var y~πθ(0)(·|x)|r(x,y)"] --> D["adjust"]
    B --> A
    D --> C
    style A fill:#f9f,stroke:#333
    style C fill:#bbf,stroke:#333
    style B fill:#dfd,stroke:#333
    style D fill:#dfd,stroke:#333
```
</details>

Idea: adjust $r ( \mathbf { x } , \mathbf { y } )$ to increase Var $\mathbf { \dot { y } } { \sim } { \pi } _ { \boldsymbol { \theta } ( 0 ) } ( \mathbf { \cdot } | \mathbf { x } ) ^ { r } \mathbf { ( x , y ) }$ for each $\mathbf { x } \in \mathcal { D }$

![](images/c72ba73b79ec57ab4c64b03819a94340c851c53bfd7d454ce5258d020bf3c7b0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Dataset D"] --> B["Prompt x"]
    B --> C["Policy model πθ"]
    C --> D["Response group"]
    D --> E["y1"]
    D --> F["y2"]
    D --> G["..."]
    D --> H["Response yn"]
    E --> I["Reward r(x,y1)"]
    F --> J["Reward r(x,y2)"]
    G --> K["..."]
    H --> L["Reward r(x,yn)"]
    I --> M["r̃(x,y1)"]
    J --> N["r̃(x,y2)"]
    K --> O["r̃(x,yn)"]
    L --> P["r̃(x,yn)"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#cfc,stroke:#333
    style D fill:#fcc,stroke:#333
    style E fill:#cff,stroke:#333
    style F fill:#cff,stroke:#333
    style G fill:#cff,stroke:#333
    style H fill:#cff,stroke:#333
    style I fill:#ffc,stroke:#333
    style J fill:#ffc,stroke:#333
    style K fill:#ffc,stroke:#333
    style L fill:#ffc,stroke:#333
    style M fill:#ffc,stroke:#333
    style N fill:#ffc,stroke:#333
    style O fill:#ffc,stroke:#333
    style P fill:#ffc,stroke:#333
```
</details>

# Reward adjustment model

Objective: increase reward variance.   
Requirement 1: preserve reward boundness.   
Requirement 2: preserve reward expectation.   
Requirement 3: preserve relative preferences.

WLOG, suppose original reward model is ??: $\mathcal { X } \times \mathcal { Y }  [ m , M ]$ and ${ \bf y } _ { 1 } , { \bf y } _ { 2 } , \cdots , { \bf y _ { n } }$ are ordered such that

$$
r (\mathbf {x}, \mathbf {y} _ {1}) \geq r (\mathbf {x}, \mathbf {y} _ {2}) \geq \dots \geq r (\mathbf {x}, \mathbf {y} _ {n}).
$$

We propose a reward adjustment model.

$$
\max _ {\mathbf {z} \in \mathbb {R} ^ {n}} f (\mathbf {z}) := \sum_ {i = 1} ^ {n} p _ {i} z _ {i} ^ {2}
$$

$\begin{array} { r } { \mathrm { s . t . } m \leq z _ { i } \leq M \forall 1 \leq i \leq M , } \end{array}$ Boundedness

$$
\begin{array}{l} \sum_ {i = 1} ^ {n} p _ {i} z _ {i} = \sum_ {i = 1} ^ {n} p _ {i} r _ {i}, \\ z _ {i} \geq z _ {i + 1} \forall 1 \leq i \leq n - 1, \\ \end{array}
$$

where $p _ { i } = \pi _ { \theta ( 0 ) } ( \mathbf { y } _ { i } | \mathbf { x } )$ .

Suppose we have a solution $\mathbf { z } ^ { \ast }$ . Then the reward $r ( \mathbf { x } , \mathbf { y } _ { i } )$ is adjusted to $\tilde { r } ( \mathbf { x } , \mathbf { y } _ { i } ) = \mathbf { z } _ { i } ^ { * }$ .

![](images/57bef69f2807bc59ad5d121801c82c89c3df8285fb0fb69ed371fa8014154d6c.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Adjusting rewards over the response group"] --> B["Var_{y~πθ(·|x')} r̃(x', y) increase"]
```
</details>

Theorem 1. Let $\mathbf { x } \in \mathcal { D }$ be a given prompt and $\left\{ \mathbf { y } _ { 1 } , \mathbf { y } _ { 2 } , \cdots , \mathbf { y } _ { n } \right\} \subset { \mathcal { Y } }$ be the response group. If the reward $\left( { \tilde { r } } ( \mathbf { x } , \mathbf { y } _ { 1 } ) , { \tilde { r } } ( \mathbf { x } , \mathbf { y } _ { 2 } ) , \cdots , { \tilde { r } } ( \mathbf { x } , \mathbf { y } _ { n } ) \right)$ is a global optimal solution of the reward adjustment model, with $r _ { i } = r ( \mathbf { x } , \mathbf { y } _ { i } )$ and $p _ { i } = \pi _ { \theta } ( \mathbf { y } _ { i } | \mathbf { x } ) \forall i \in \{ 1 , 2 , \cdots , n \}$ , then the reward variance of policy model $\pi _ { \theta } ( \cdot | \mathbf { x } )$ over the response space can be increased for the prompt $\mathbf { x } \in \mathcal { D }$ .

Properties of the proposed reward adjustment model:

Non-convex optimization problem, usually NP-hard to solve.   
The feasible set is a bounded and non-empty polyhedral.

$$
\mathcal {P} := \{\mathbf {z} \in \mathbb {R} ^ {n} | \sum_ {i = 1} ^ {n} p _ {i} z _ {i} = \sum_ {i = 1} ^ {n} p _ {i} r _ {i}, m \leq z _ {i} \leq M \forall 1 \leq i \leq n, z _ {i} \geq z _ {i + 1} \forall 1 \leq i \leq n - 1 \}
$$

Objective function is convex.

• The global optimal solution is attained at one of the extreme points.

Lemma 1. Define a subset of extreme point set ?? as

$$
\mathcal {V} ^ {*} := \left\{\mathbf {v} \in \mathcal {V} | f (\mathbf {v}) = \max _ {\mathbf {v} ^ {\prime} \in \mathcal {V}} f (\mathbf {v} ^ {\prime}) \right\},
$$

then the point(s) in $\mathcal { V } ^ { \ast }$ are global solution(s) to the reward adjustment model.

The set of extreme points can be characterized.

# Lemma 2. The set of extreme points ?? of ?? is

$$
\mathcal {V} = \left\{\mathbf {v} = (v _ {1}, \dots v _ {n}) \in \mathcal {P} \left| \begin{array}{c} \exists 0 \leq k \leq l \leq n, m <   \alpha <   M \mathrm{s.t.} \\ v _ {1} = \dots = v _ {k} = M, \\ v _ {k + 1} = \dots = v _ {l} = \alpha , \\ v _ {l + 1} = \dots = v _ {n} = m, \\ \alpha = \frac {\sum_ {i = 1} ^ {n} p _ {i} r _ {i} - M \sum_ {i = 1} ^ {k} p _ {i} - m \sum_ {i = l + 1} ^ {n} p _ {i}}{\sum_ {i = k + 1} ^ {l} p _ {i}}. \end{array} \right. \right\}
$$

• Therefore, the extreme point $\mathbf { v } = ( v _ { 1 } , v _ { 2 } , \cdots , v _ { n } )$ has the following form.

![](images/fb113b56078655dc60ab1f1da219af2a673ef6f95f2140086e62d65741e4a452.jpg)

<details>
<summary>bar_stacked</summary>

| Segment | Value |
|---------|-------|
| v1      | M     |
| ...     | M     |
| vk      | α     |
| vk+1    | α     |
| ...     | α     |
| vl      | m     |
| vl+1    | m     |
| ...     | m     |
| vn      | m     |
</details>

Based on the special form, an $O ( n )$ solving algorithm is designed.

# Algorithms

Enumerate ?? from ?? to ??. (inner loop)

![](images/8756343bed8485de807707a0c02980ee60e78f90f968a418c7ae726225dbdc50.jpg)

<details>
<summary>text_image</summary>

k = 2
l = 3 →
</details>

![](images/18bbdf2e55b230473a43fa4a53ed91910ac7d2fa18c5e4df3d1a9acd9bf2aaac.jpg)

<details>
<summary>text_image</summary>

k = 2
l = 4 →
</details>

![](images/198d3f3266a7a9e2245da14cb665fba12a25c465b54288def187a5e09a6fa749.jpg)

<details>
<summary>text_image</summary>

k = 2
l = 5 →
</details>

Enumerate ?? from ?? to ??. (outer loop)

![](images/5aa98a8fd506a679b9bdebf5184d16271d1d412729e17688fba2a3dddafa1767.jpg)

<details>
<summary>text_image</summary>

k = 2 →
l = 3
</details>

![](images/f815c9d2eec80058efdd3182edd758cf0e98763ea195aa1cebe83dcae201c8c4.jpg)

<details>
<summary>text_image</summary>

k = 3 →
l = 4
</details>

![](images/6beaa131084e1d31dd56113a4d2c01f80fbdce0dc9ae46cf7620f44a5c0e9ee4.jpg)

<details>
<summary>text_image</summary>

k = 4 →
l = 5
</details>

• An $O ( n ^ { 2 } )$ algorithm to find the global optimal solution.

Algorithm 1 Enumeration search algorithm for   
1: Input: $p = (p_1, p_2, \cdots, p_n)$ with 0 < $p_i < 1$ . A sorted reward $r = (r_1, r_2, \cdots, r_n)$ . An upper bound M and a lower bound m.

2: Output: A optimal solution $z^*$ to (3) and the optimal objective value $f^*$ .

3: Initialization: $c = \sum_{i=1}^{n} p_i r_i$ , $z^* = r$ , $f^* = 0$ , $k^* = 0$ , $l^* = 0$ , $\alpha^* = 0$ .

4: for $k = 0, 1, \ldots, n$ do

5: for $l = k, k + 1, \ldots, n$ do

6: Compute $\alpha$ based on lemma 2.

7: Compute current objective value $\bar{f}$ based on c, M, m, p.

8: if $\bar{f} > f^*$ then

9: Set $f^* = \bar{f}$ , $k^* = k$ , $l^* = l$ , $\alpha^* = \alpha$ .

10: end if

11: end for

12: end for

13: Set $z_1^* = \cdots = z_{k^*}^* = M$ , $z_{k^*+1}^* = \cdots = z_{l^*}^* = \alpha^*$ , $z_{l^*+1}^* = \cdots = z_n^* = m$ .

14: return $z^* = (z_1^*, z_2^*, \cdots, z_n^*)$ and $f^*$

An $O ( n )$ search algorithm.   
• Search strategy: start search from two ends to the center.

$$
k = 0 \longrightarrow \qquad \qquad \qquad \qquad \qquad \longleftarrow l = n
$$

![](images/f39d51865e3ccd88669ab4e335a4c827eeabaab276bf1d179762db9e2a521586.jpg)

<details>
<summary>natural_image</summary>

A row of eight green rectangular blocks with black borders, no text or symbols present.
</details>

$$
k = 1 \longrightarrow \qquad \qquad \qquad \longleftarrow l = n
$$

![](images/822264fe3674f740d0f9353a3148ee050a9178d468a9f954221f58d3b1388ab2.jpg)

<details>
<summary>natural_image</summary>

Simple horizontal bar divided into two sections: red on the left and green on the right, with no text or symbols.
</details>

$$
k = 1 \longrightarrow \qquad \qquad \qquad \longleftarrow l = n - 1
$$

![](images/17ad10aa5c71c9356197d78690bc19a17af203aacf8ef94742bde29aae872597.jpg)

<details>
<summary>natural_image</summary>

Simple horizontal bar divided into three colored sections (red, green, blue) with no text or symbols
</details>

Once a solution becomes infeasible, all subsequent solutions along that search direction are infeasible.

Define $\begin{array} { r } { S _ { A } = \sum _ { i = 1 } ^ { k } p _ { i } , S _ { B } = \sum _ { i = k + 1 } ^ { l } p _ { i } , S _ { C } = \sum _ { i = l + 1 } ^ { n } p _ { i } } \end{array}$

Lemma 3. Suppose $k < l - 1$

$\begin{array} { r } { | \mathsf { f } M < \frac { c - M S _ { A } - m S _ { C } } { S _ { B } } , \mathsf { t h e n } \frac { c - M S _ { A } - m S _ { C } } { S _ { B } } < \frac { c - M ( S _ { A } + p _ { k + 1 } ) - m S _ { C } } { S _ { B } - p _ { k + 1 } } ; } \end{array}$ < ??−??????−??????, then

$\begin{array} { r } { \mathsf { I f } m > \frac { c - M S _ { A } - m S _ { C } } { S _ { B } } , \mathsf { t h e n } \frac { c - M S _ { A } - m S _ { C } } { S _ { B } } > \frac { c - M S _ { A } - m ( S _ { C } + p _ { l } ) } { S _ { B } - p _ { l } } . } \end{array}$ ??−??????−??????, then >

Once a solution becomes infeasible, all subsequent solutions along that search direction are infeasible.   
• Illustration:

![](images/7533478eae1dcdbfa7e09ea156917882c1a2836145c6a7ff056d851ccea36c1c.jpg)

<details>
<summary>text_image</summary>

k = 2
l = n - 1
</details>

$\textsf { f } k = 2 , l = n - 1$ is infeasible,

![](images/fcd7a6f9b7b22fd284442a7fe71b22c3e3e5b0b35649553bb029113834dd91bf.jpg)

<details>
<summary>text_image</summary>

k = 3 → l = n - 1
</details>

then $k \geq 3 , l = n - 1$ are all infeasible.

The objective function value exhibits a monotonically increasing trend if the solution is feasible.

# Lemma 5. Assume $m < \alpha < M$ .

$\begin{array} { r } { \vert \textsf { f } \frac { c - M ( S _ { A } + p _ { k + 1 } ) - m S _ { C } } { S _ { B } - p _ { k + 1 } } > m } \end{array}$ , then it can strictly increase the objective function value by setting $k = k + 1$ and ?? = ??;

$\begin{array} { r } { \mathsf { I f } \frac { c - M S _ { A } - m ( S _ { C } + p _ { l } ) } { S _ { B } - p _ { l } } < M } \end{array}$ ????−???? , then it can strictly increase the objective function value by setting ?? = ?? and ?? = ?? − 1.

The objective function value exhibits a monotonically increasing trend if the solution is feasible.   
• Illustration

![](images/2dbdb363dfaf7b222a1d6ed629e2548071bd8a709cb8ce1b1a08d882791a72be.jpg)

<details>
<summary>text_image</summary>

k = 0 → ← l = n
f₀
k = 1 → ← l = n
f₁
k = 1 → ← l = n - 1
f₂
</details>

If those three solutions are all feasible, then $f _ { 2 } > f _ { 1 } > f _ { 0 }$

One-pass search algorithm is an ??(??) algorithm. If the rewards are not sorted at first, then it will requires ??(??log??) to sort the rewards and probabilities.

Algorithm 2 One-pass search algorithm for (3)   
1: Input: $p = (p_1, p_2, \cdots, p_n)$ with $0 < p_i < 1$ . A sorted reward $r = (r_1, r_2, \cdots, r_n)$ . An upper bound M and a lower bound m.

2: Output: A optimal solution $z^*$ to (3) and the optimal objective value $f^*$ .

3: Initialization: $c = \sum_{i=1}^{n} p_i r_i$ , k = 0, l = n, iter = 0.

4: Define $C(0) = 0$ and compute the cumulative sums $C(i) = \sum_{j=1}^{i} p_j \quad 1 \leq i \leq n$ .

5: while iter < n do

6: Compute $S_A = C(k)$ , $S_C = C(n) - C(l)$ , $S_B = C(l) - C(k)$ .

7: if $S_B \leq 0$ then

8: Break.

9: end if

10: Set $\alpha = (c - MS_A - mS_C)/S_B$ . Compute objective $f = SA M^2 + S_B \alpha^2 + S_C m^2$ .

11: Set $f^* = f, k^* = k, l^* = l, flags = 0$ .

12: if k < l and $S_B - p_{k+1} > 0$ then

13: $\bar{\alpha} = \frac{c - (S_A + p_{k+1}) M - S_c m}{S_B - p_{k+1}}$ .

14: if $m \leq \bar{\alpha} \leq M$ then

15: $f_{new} = (S_A + p_{k+1}) M^2 + (S_B - p_{k+1}) \bar{\alpha}^2 + S_C m^2$ .

16: if $f_{new} > f^*$ then

17: $f^* = f_{new}, k^* = k + 1, l^* = l, flags = 1$ .

18: end if

19: end if

20: end if

21: if l > k and $S_B - p_l > 0$ then

22: $\bar{\alpha} = \frac{c - S_A M - (S_C + p_l)m}{S_B - p_l}$ .

23: if $m \leq \bar{\alpha} \leq M$ then

24: $f_{new} = S_A M^2 + (S_B - p_l) \bar{\alpha}^2 + (S_C + p_l) m^2$ .

25: if $f_{new} > f^*$ then

26: $f^* = f_{new}, k^* = k, l^* = l - 1, flags = 1$ .

27: end if

28: end if

29: end if

30: if flags = 1 then

31: k = k*, l = l*.

32: Continue.

33: else

34: Break.

35: end if

36: iter = iter + 1.

37: end while

38: Set $z_1^* = \cdots = z_{k^*}^* = M$ , $z_{k^*+1}^* = \cdots = z_{l^*}^* = \alpha$ , $z_{l^*+1}^* = \cdots = z_n^* = m$ .

39: return $z^* = (z_1^*, z_2^*, \cdots, z_n^*)$ and $f^*$

Search from the left side

Search from the right side

Integrate the reward adjustment model into the standard GRPO algorithm, resulting in the GRPOVI algorithm.   
• The responses are generated from the current policy model.   
• The corresponding probabilities are from the initial policy model.   
• The guarantee for reward variance increase can be easily derived.

Corollary 1. Let $\mathbf { x } \in \mathcal { D }$ be any given prompt. Assume that the responses $\left\{ \mathbf { y } _ { 1 } , \mathbf { y } _ { 2 } , \cdots , \mathbf { y } _ { n } \right\}$ are generated from the policy model $\pi _ { \theta ( t ) } ( \cdot | \mathbf { x } )$ . If the reward $\left( { \tilde { r } } ( \mathbf { x } , \mathbf { y } _ { 1 } ) , { \tilde { r } } ( \mathbf { x } , \mathbf { y } _ { 2 } ) , \cdots , { \tilde { r } } ( \mathbf { x } , \mathbf { y } _ { n } ) \right)$ is a global optimal solution of the reward adjustment model, with $r _ { i } = r ( \mathbf { x } , \mathbf { y } _ { i } )$ and $p _ { i } = \pi _ { \theta ( 0 ) } ( \mathbf { y } _ { i } | \mathbf { x } ) \forall i \in \{ 1 , 2 , \cdots , n \}$ , then the reward variance of policy model $\pi _ { \theta ( 0 ) } ( \cdot | \mathbf { x } )$ over the response space can be increased for the prompt $\mathbf { x } \in \mathcal { D }$ .

![](images/415bf992902f99cfce3293348c691c0d52a7129291faa2c990917996453301fc.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Dataset D"] --> B["Batch Db"]
    B --> C["Prompt x"]
    C --> D["Current policy model πθ(t)"]
    D --> E["y1"]
    D --> F["y2"]
    D --> G["..."]
    D --> H["yn"]
    E --> I["r(x,y1)"]
    F --> J["r(x,y2)"]
    G --> K["..."]
    H --> L["r(x,yn)"]
    I --> M["tilde{r}(x,y1)"]
    J --> N["tilde{r}(x,y2)"]
    K --> O["..."]
    L --> P["tilde{r}(x,yn)"]
    M & N --> Q["A1"]
    N --> R["A2"]
    O & P --> S["..."]
    Q & R & S --> T["An"]
    style D fill:#f9f,stroke:#333
    style E fill:#ccf,stroke:#333
    style F fill:#ccf,stroke:#333
    style G fill:#ccf,stroke:#333
    style H fill:#ccf,stroke:#333
    style I fill:#cfc,stroke:#333
    style J fill:#cfc,stroke:#333
    style K fill:#cfc,stroke:#333
    style L fill:#cfc,stroke:#333
    style M fill:#fcc,stroke:#333
    style N fill:#fcc,stroke:#333
    style O fill:#fcc,stroke:#333
    style P fill:#fcc,stroke:#333
    style Q fill:#ffc,stroke:#333
    style R fill:#ffc,stroke:#333
    style S fill:#ffc,stroke:#333
    style T fill:#ffc,stroke:#333
```
</details>

Update policy model

The pseudo code of GRPOVI algorithm.

Algorithm 3 GRPOVI: GRPO with reward variance increase   
1: Input: reference model $\pi_{ref}$ , reward model r, dataset D, group size n.
2: Output: policy model $\pi_{\theta(T)}$ .
3: Initialization: $\pi_{\theta(0)} = \pi_{\text{ref}}$ .
4: for step $t = 0, 1, \cdots, T$ do
5: Choose a batch $D_b$ from D.
6: Generate n responses $\{\mathbf{y}_i\}_{i=1}^n$ from $\pi_{\theta(t)}(\cdot|\mathbf{x})$ for each $x \in D_b$ .
7: Compute the probability $p_i = \pi_{\text{ref}}(\mathbf{y}_i|\mathbf{x})$ based on reference model $\pi_{ref}$ for each $i = 1, 2, \cdots, n$ .
8: Normalize the probabilities $p_i = \frac{p_i}{\sum_{i=1}^n p_i}$ .
9: Compute reward $r_i = r(\mathbf{x}, \mathbf{y}_i)$ for each $i = 1, 2, \cdots, n$ .
10: Sort $\{p_i\}_{i=1}^n$ and $\{r_i\}_{i=1}^n$ such that $r_1 \geq r_2 \geq \cdots \geq r_n$ .
11: Compute the adjusted rewards $\{\tilde{r}_i\}_{i=1}^n$ based on $\{p_i\}_{i=1}^n$ and $\{r_i\}_{i=1}^n$ (algorithm [1] or algorithm [2]).
12: Compute advantages in GRPO based on $\{\tilde{r}_i\}_{i=1}^n$ .
13: Update policy model $\pi_{\theta(t)}$ according to GRPO-based RLHF training method.
14: end for
15: return policy model $\pi_{\theta(T)}$

# Experiments

• The comparative experiment on the search algorithms.

<table><tr><td rowspan="2">Size n</td><td colspan="2">Enumeration search algorithm</td><td colspan="2">One-pass search algorithm</td></tr><tr><td>Optimal value  $f_1^*$ </td><td>Running time (s)</td><td>Optimal value  $f_2^*$ </td><td>Running time (s)</td></tr><tr><td>10</td><td>0.3918</td><td>0.0022</td><td>0.3918</td><td>0.0015</td></tr><tr><td>50</td><td>0.4260</td><td>0.0438</td><td>0.4260</td><td>0.0057</td></tr><tr><td>100</td><td>0.5159</td><td>0.1707</td><td>0.5159</td><td>0.0112</td></tr><tr><td>500</td><td>0.4970</td><td>4.2043</td><td>0.4970</td><td>0.0539</td></tr><tr><td>1000</td><td>0.4938</td><td>16.9763</td><td>0.4938</td><td>0.1106</td></tr><tr><td>5000</td><td>0.4919</td><td>408.9071</td><td>0.4919</td><td>0.5515</td></tr><tr><td>10000</td><td>0.4933</td><td>1659.4376</td><td>0.4933</td><td>1.0561</td></tr></table>

Table 1 Comparison of enumeration search algorithm (algorithm ) and one-pass search algorithm (algorithm) for solving )

• The experiment between original GRPO and GRPOVI algorithms on LLM RLHF training.

• Policy model: Pythia-1B   
• Reward model: GRM-Gemma-2-2B

![](images/344f0c867adea3ceaab7a808caed114e7ac5909f2c51e5218019f220ba0938f8.jpg)

<details>
<summary>line</summary>

| Checkpoints | GRPOVI  | GRPO    |
| ----------- | ------- | ------- |
| 1           | 0.0578  | 0.0568  |
| 2           | 0.0655  | 0.0640  |
| 3           | 0.0670  | 0.0648  |
| 4           | 0.0660  | 0.0635  |
| 5           | 0.0660  | 0.0610  |
| 6           | 0.0635  | 0.0598  |
| 7           | 0.0640  | 0.0612  |
| 8           | 0.0648  | 0.0612  |
</details>

(a) Performance on the training set.

![](images/bcffcc1b6118bed6a3928c979a6ee83f3e15f7f63fb8988b550ed859600ec19e.jpg)

<details>
<summary>line</summary>

| Checkpoints | GRPOVI  | GRPO    |
| ----------- | ------- | ------- |
| 1           | 0.0565  | 0.0558  |
| 2           | 0.0648  | 0.0635  |
| 3           | 0.0672  | 0.0640  |
| 4           | 0.0658  | 0.0627  |
| 5           | 0.0658  | 0.0607  |
| 6           | 0.0637  | 0.0593  |
| 7           | 0.0641  | 0.0607  |
| 8           | 0.0644  | 0.0602  |
</details>

(b) Performance on the test set.

• The experiment between original GRPO and GRPOVI algorithms on LLM RLHF training.

• Policy model: Pythia-1B   
• Reward model: GRM-Llama-3.2-3B

![](images/2c895d92aeb20caa53c687c7de19a013f581b4727eee24c0b0af6e96d9639c25.jpg)

<details>
<summary>line</summary>

| Checkpoints | GRPOVI  | GRPO    |
| ----------- | ------- | ------- |
| 1           | 0.056   | 0.0535  |
| 2           | 0.058   | 0.0542  |
| 3           | 0.058   | 0.0537  |
| 4           | 0.059   | 0.0538  |
| 5           | 0.059   | 0.0552  |
| 6           | 0.0595  | 0.0558  |
| 7           | 0.0602  | 0.0562  |
| 8           | 0.0608  | 0.0572  |
</details>

(a) Performance on the training set.

![](images/aa3022cc9787759a95343a7b8cd407b90c206005b836de8555c0f0263e12ff75.jpg)

<details>
<summary>line</summary>

| Checkpoints | GRPOVI  | GRPO    |
| ----------- | ------- | ------- |
| 1           | 0.055   | 0.0525  |
| 2           | 0.057   | 0.053   |
| 3           | 0.0575  | 0.053   |
| 4           | 0.058   | 0.0535  |
| 5           | 0.0585  | 0.0545  |
| 6           | 0.059   | 0.055   |
| 7           | 0.060   | 0.0555  |
| 8           | 0.060   | 0.0545  |
</details>

(b) Performance on the test set.

# Direct Preference Optimization

Feedbackcomesaspreferencesovermodelsamples: $\mathcal { D } = \{ x ^ { i } , y _ { w } ^ { i } , y _ { l } ^ { i } \}$ Prompt Dispreferred response Preferred response

Bradley-Terry Model connects rewards to preferences:

$$
p (y _ {w} \succ y _ {l} \mid x) = \sigma (r (x, y _ {w}) - r (x, y _ {l}))
$$

Train the reward model by minimizing negative log likelihood:

$$
\mathcal {L} _ {R} (\phi , \mathcal {D}) = - \mathbb {E} _ {(x, y _ {w}, y _ {l}) \sim \mathcal {D}} \left[ \log \sigma (r _ {\phi} (x, y _ {w}) - r _ {\phi} (x, y _ {l})) \right]
$$

Now we have a reward model $r _ { \phi }$ that represents\* goodness according to humans

Now,learn a policy $\pi _ { \theta }$ achieving highrewardwhilestaying close to original model $\pi _ { \mathrm { r e f } }$

$$
\max _ {\pi_ {\theta}} \mathbb {E} _ {x \sim \mathcal {D}, y \sim \pi_ {\theta} (y | x)} [ r _ {\phi} (x, y) ] - \beta \mathbb {D} _ {\mathrm{KL}} [ \pi_ {\theta} (y | x) | | \pi_ {\mathrm{ref}} (y | x) ]
$$

![](images/daf97c0fa39b1941b1dbb088ebb71a00e625aa14fe3ab069a68da4ecc7392da7.jpg)

Sample from policy

![](images/911c9dbecfb1444416459ffb43cae4f493930a333393e7e6598b837c5e243012.jpg)

Want high reward...

![](images/a70631e5fc50f2b297f428edca4265e6af9bf95cde6cc09bc967964d0606fcdf.jpg)

...but keep KL to original model small!

$$
\begin{array}{l} \max _ {\pi} \mathbb {E} _ {x \sim \mathcal {D}, y \sim \pi} [ r (x, y) ] - \beta \mathbb {D} _ {\mathrm{KL}} \overbrace {[ \pi (y | x) | | \pi_ {\mathrm{ref}} (y | x) ]} ^ {} (1) D _ {K L} [ \pi (y | x) | | \pi_ {\mathrm{ref}} (y | x) ] = \mathbb {E} _ {y \sim \pi (y | x)} \left[ \log \frac {\pi (y | x)}{\pi_ {\mathrm{ref}} (y | x)} \right] \\ \begin{array}{l} = \max _ {\pi} \mathbb {E} _ {x \sim \mathcal {D}} \mathbb {E} _ {y \sim \pi (y | x)} \left[ r (x, y) - \beta \log \frac {\pi (y | x)}{\pi_ {\text {ref}} (y | x)} \right] \\ = \min _ {\pi} \mathbb {E} _ {x \sim \mathcal {D}} \mathbb {E} _ {y \sim \pi (y | x)} \left[ \log \frac {\pi (y | x)}{\pi_ {\text {ref}} (y | x)} - \frac {1}{\beta} r (x, y) \right] \\ = \min _ {\pi} \mathbb {E} _ {x \sim \mathcal {D}} \mathbb {E} _ {y \sim \pi (y | x)} \left[ \log \frac {\pi (y | x)}{\pi_ {\text {ref}} (y | x) \exp \left(\frac {1}{\beta} r (x , y)\right)} \right] \end{array} \\ \end{array}
$$

$$
\begin{array}{r l} & \min _ {\pi} \mathbb {E} _ {x \sim \mathcal {D}} \mathbb {E} _ {y \sim \pi (y | x)} \left[ \log \frac {\pi (y | x)}{\pi_ {\mathrm{ref}} (y | x) \exp \left(\frac {1}{\beta} r (x , y)\right)} \right] \longrightarrow D _ {K L} \left[ \pi (y | x) \| \pi_ {\mathrm{ref}} (y | x) \exp \left(\frac {1}{\beta} r (x, y)\right) \right] \\ & \quad \frac {1}{Z (x)} \pi_ {\mathrm{ref}} (y | x) \exp \left(\frac {1}{\beta} r (x, y)\right) \\ & \quad = \min _ {\pi} \mathbb {E} _ {x \sim \mathcal {D}} \mathbb {E} _ {y \sim \pi (y | x)} \left[ \log \frac {\pi (y | x)}{\frac {1}{Z (x)} \pi_ {\mathrm{ref}} (y | x) \exp \left(\frac {1}{\beta} r (x , y)\right)} - \log Z (x) \right] \end{array} \tag {3}
$$

$$
\pi^ {*} (y | x) = \frac {1}{Z (x)} \pi_ {\mathrm{ref}} (y | x) \exp \left(\frac {1}{\beta} r (x, y)\right),
$$

$$
Z (x) = \sum_ {y} \pi_ {\mathrm{ref}} (y \mid x) \exp \left(\frac {1}{\beta} r (x, y)\right)
$$

$$
\pi_ {r} (y \mid x) = \frac {1}{Z (x)} \pi_ {\text { ref }} (y \mid x) \exp \left(\frac {1}{\beta} r (x, y)\right)
$$

![](images/7c5959fd2a89f0c5fc30ca4dadd8237b1a4e535e4b1ef641c0d7fa76f8bf950c.jpg)

$$
r (x, y) = \beta \log \frac {\pi_ {r} (y \mid x)}{\pi_ {\mathrm{ref}} (y \mid x)} + \beta \log Z (x).
$$

Therefore,

$$
r (x, y _ {2}) - r (x, y _ {1})
$$

$$
= \beta \log \frac {\pi_ {r} (y _ {2} | x)}{\pi_ {r e f} (y _ {2} | x)} + \beta \log Z (x)) - (\beta \log \frac {\pi_ {r} (y _ {1} | x)}{\pi_ {r e f} (y _ {1} | x)} + \beta \log Z (x))
$$

$$
= \beta \log \frac {\pi_ {r} (y _ {2} | x)}{\pi_ {r e f} (y _ {2} | x)} - \beta \log \frac {\pi_ {r} (y _ {1} | x)}{\pi_ {r e f} (y _ {1} | x)}
$$

$$
\frac {e ^ {A}}{e ^ {A} + e ^ {B}} = \frac {1}{1 + e ^ {B - A}} = \sigma (B - A)
$$

$$
r (x, y _ {2}) - r (x, y _ {1}) = \beta \log \frac {\pi_ {r} (y _ {2} | x)}{\pi_ {r e f} (y _ {2} | x)} - \beta \log \frac {\pi_ {r} (y _ {1} | x)}{\pi_ {r e f} (y _ {1} | x)}
$$

$$
p ^ {*} (y _ {1} \succ y _ {2} \mid x) = \frac {1}{1 + \exp \left(\beta \log \frac {\pi^ {*} (y _ {2} | x)}{\pi_ {\mathrm{ref}} (y _ {2} | x)} - \beta \log \frac {\pi^ {*} (y _ {1} | x)}{\pi_ {\mathrm{ref}} (y _ {1} | x)}\right)}
$$

$$
\mathcal {L} _ {\mathrm{DPO}} \left(\pi_ {\theta}; \pi_ {\text {ref}}\right) = - \mathbb {E} _ {(x, y _ {w}, y _ {l}) \sim \mathcal {D}} \left[ \log \sigma \left(\beta \log \frac {\pi_ {\theta} \left(y _ {w} \mid x\right)}{\pi_ {\text {ref}} \left(y _ {w} \mid x\right)} - \beta \log \frac {\pi_ {\theta} \left(y _ {l} \mid x\right)}{\pi_ {\text {ref}} \left(y _ {l} \mid x\right)}\right) \right]
$$

$$
\frac {\sigma^ {\prime} (u)}{\sigma (u)} = \frac {\sigma (u) * (1 - \sigma (u))}{\sigma (u)} = \sigma (- u)
$$

$$
\nabla_ {\theta} \mathcal {L} _ {\mathrm{DPO}} (\pi_ {\theta}; \pi_ {\text { ref }}) = - \mathbb {E} _ {(x, y _ {w}, y _ {l}) \sim \mathcal {D}} \left[ \frac {\sigma^ {\prime} (u)}{\sigma (u)} \nabla_ {\theta} (u) \right]
$$

$$
u = \beta \log \frac {\pi_ {\theta} (y _ {l} \mid x)}{\pi_ {\text { ref }} (y _ {l} \mid x)} - \beta \log \frac {\pi_ {\theta} (y _ {w} \mid x)}{\pi_ {\text { ref }} (y _ {w} \mid x)}
$$

![](images/bfaa3d9549a3d12a675561cbd0887ad8272c9a75420ceadbaf1f8a7557844d19.jpg)

$$
\nabla_ {\theta} \mathcal {L} _ {\mathrm{DPO}} (\pi_ {\theta}; \pi_ {\text { ref }}) =
$$

$$
\left. \right. - \mathbb {E} _ {\left(x, y _ {w}, y _ {l}\right) \sim \mathcal {D}} \left[ \beta \sigma \left(\beta \log \frac {\pi_ {\theta} \left(y _ {w} \mid x\right)}{\pi_ {\text { ref}} \left(y _ {w} \mid x\right)} - \beta \log \frac {\pi_ {\theta} \left(y _ {l} \mid x\right)}{\pi_ {\text { ref}} \left(y _ {l} \mid x\right)}\right)\left[ \nabla_ {\theta} \log \pi \left(y _ {w} \mid x\right) - \nabla_ {\theta} \log \pi \left(y _ {l} \mid x\right)\right]\right]
$$

Reinforcement Learning from Human Feedback (RLHF)   
![](images/d7a64210ede9992e7a8097056890a86bf8c1d0dbbad6c4f2e9eecc5527b09fdb.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["preference data"] --> B["maximum likelihood"]
    B --> C["reward model"]
    C --> D["label rewards"]
    D --> E["sample completions"]
    E --> F["LM policy"]
    F --> G["reinforcement learning"]
    style A fill:#f9f,stroke:#333
    style G fill:#bbf,stroke:#333
```
</details>

Direct Preference Optimization (DPO)   
![](images/76c6f2f65e88f0ebab88b44f32c088ff803e1cbab940113f6e9e5e37a0b5339b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["preference data"] --> B["×: &quot;write me a poem about the history of jazz&quot;"]
    B --> C["maximum likelihood"]
    C --> D["final LM"]
```
</details>

TL;DRSummarization Win Ratevs Reference   
![](images/97b59a8af21c8c4e0f0790c0c55339227c20d6ef9dc682e4c28ddbc48c297332.jpg)

<details>
<summary>line</summary>

| Sampling temperature | DPO    | PPO    | Preferred-FT | SFT    | GPT-J  | Best of 128 |
| -------------------- | ------ | ------ | ------------ | ------ | ------ | ----------- |
| 0.00                 | 0.62   | 0.58   | 0.38         | 0.40   | 0.06   | 0.42        |
| 0.25                 | 0.61   | 0.52   | 0.39         | 0.40   | 0.06   | 0.52        |
| 0.50                 | 0.60   | 0.40   | 0.41         | 0.38   | 0.10   | 0.58        |
| 0.75                 | 0.52   | 0.20   | 0.38         | 0.34   | 0.07   | 0.52        |
| 1.00                 | 0.40   | 0.08   | 0.36         | 0.28   | 0.06   | 0.48        |
</details>

You can replace the complex RL part with a very simple weighted MLEobjective   
Othervariants (KTO,IPO) now emerging too   
TL;DR summarization win rates vs.humanwritten summaries (GPT-4asa judge)

IMDb Sentiment Generation  
![](images/ff78e6c651b08afaff87e0a14bdeacf35ca3ee282ed7dcb01b5d1eaef18eac49.jpg)

1. Generate positive IMDB reviews from GPT2-XL   
2.Use pre-trained sentiment classifier as Gold RM   
3． Create preferences based on Gold RM   
4.Optimize with PPO and DPO

# Mistral

# 4Instruction Fine-tuning

WetrainMixtral-Instruct usingsupervisedfine-tuning (SFT)onaninstruction dataset followed by DirectPreferenceOptimization(DPO)[25]onapaired feedbackdataset.Mixtral-Instruct reachesa score of 8.30onMT-Bench[33](seeTable2),makingit thebest open-weightsmodelasofDecember 2023.Independent humanevaluationconductedbyLMSys isreported inFigure6and shows that Mixtral-InstructoutperformsGPT-3.5-Turbo，GeminiPro,Claude-2.1,andLlama27OBchat.

<table><tr><td>Model</td><td>Arena Elo rating</td><td>MT-bench (score)</td><td>License</td></tr><tr><td>GPT-4-Turbo</td><td>1243</td><td>9.32</td><td>Proprietary</td></tr><tr><td>GPT-4-0314</td><td>1192</td><td>8.96</td><td>Proprietary</td></tr><tr><td>GPT-4-0613</td><td>1158</td><td>9.18</td><td>Proprietary</td></tr><tr><td>Claude-1</td><td>1149</td><td>7.9</td><td>Proprietary</td></tr><tr><td>Claude-2.0</td><td>1131</td><td>8.06</td><td>Proprietary</td></tr><tr><td>Mixtral-8x7b-Instruct-v0.1</td><td>1121</td><td>8.3</td><td>Apache 2.0</td></tr><tr><td>Claude-2.1</td><td>1117</td><td>8.18</td><td>Proprietary</td></tr><tr><td>GPT-3.5-Turbo-0613</td><td>1117</td><td>8.39</td><td>Proprietary</td></tr><tr><td>Gemini Pro</td><td>1111</td><td></td><td>Proprietary</td></tr><tr><td>Claude-Instant-1</td><td>1110</td><td>7.85</td><td>Proprietary</td></tr><tr><td>Tulu-2-DPO-708</td><td>1110</td><td>7.89</td><td>AI2 ImpACT Low-risk</td></tr><tr><td>Yi-34B-Chat</td><td>1110</td><td></td><td>Yi License</td></tr><tr><td>GPT-3.5-Turbo-0314</td><td>1105</td><td>7.94</td><td>Proprietary</td></tr><tr><td>Llama-2-70b-chat</td><td>1077</td><td>6.86</td><td>Llama 2 Community</td></tr></table>

Figure6:LMSysLeaderboard.(Screenshot fromDec22,2023)Mixtral8x7BInstructvO1achievesanArena Eloratingof1121outperformingClaude-2.1(1117),allversionsofGP-3.5-Turbo(1117best),GeminiPro (1111),andLlama-2-7Ob-chat(1o77).Mixtraliscurrentlythebestopen-weightsmodelbyalargemargin.

# LLaMa3

# Instruction fine-tuning

Tofully unlock thepotential of ourpretrainedmodelsinchat usecases,we innovated onour approach toinstruction-tuningaswellOurapproachtopost-training isa combinationof supervised fine-tuning(SFT),rejection sampling,proximal policyoptimization (PPO),and directpreferenceoptimization(DPO).The quality of the prompts that areused in SFTand thepreferencerankingsthatare usedin PPOand DPO hasanoutsized influenceonthe performanceof alignedmodels.Someof ourbiggestimprovements inmodel qualitycame fromcarefullycuratingthisdataand performingmultiple rounds of qualityassuranceon annotationsprovided by human annotators.

Learning frompreferencerankings via PPO andDPoalso greatly improvedtheperformance ofLlama3onreasoningand coding tasks.Wefoundthatif youaskamodelareasoning question thatit struggles toanswer,themodel willsometimesproduce therightreasoning trace:Themodel knows howtoproducetherightanswer，butitdoesnotknowhowtoselect it.Training on preferencerankings enablesthemodel to learn howto select it.

![](images/9a0a5e2a34ddd7271fe94a3fe81ae403bc0612f209fcdb48a3044d2f5cc49a33.jpg)

<details>
<summary>bar</summary>

| Category | DPO | PPO |
|---|---|---|
| TL;DR (t=0) | 62 | 58 |
| TL;DR (t=0.25) | 61 | 53 |
| CNN/DailyMail (t=0) | 36 | 31 |
| CNN/DailyMail (t=0.25) | 32 | 23 |
</details>

DPO is trained only on the Reddit TL;DR feedback data.   
2. PPO uses a trained reward function and additional prompts for RL training.   
3. We evaluate the trained policies on OOD CNN/DailyMail news summarization task.

DPO fits an implicit reward function:

1. Is the DPO implicit reward as good as the explicit one?   
2． Does using a weaker optimizer,such as PPO provide a better solution (regularization).

# RewardBench:Evaluating Reward Models

Evaluatingthecapabilities,safetyandpitfallsofrewardmodels

# FEuArdbench

![](images/aca453998b751786367427c613af64ad0bac4f075f29dbfb5f16a871e31c0cee.jpg)

RewardBench Leaderboard

![](images/4712be9c9400db9bd84ad737e1525046ee4d4fb59af3fa1b097b21d05dd07996.jpg)

![](images/301fca38bd7d5afbfacb1149be71ae1798e9a6309297c1fd06fcd99fdc625607.jpg)

Seq.Classifiers

![](images/634f989114630966f0cebee51ff9f5b33062e0606f9859dd12de59b36d871a6c.jpg)

DPO

![](images/97848d7e1549d25742fc81560ae0ee441b07d6778da6f2fb912404ac73e022ee.jpg)

CustomClassifiers

![](images/b87982c20f8638d2d884784cbd7db59bfc30966f4a9f48c74f44c119d4f288f5.jpg)

Generative

![](images/14662529ca4df1d711adbacf3f8f0af4d091e80e567a8070d4f39e3b9c29cd2e.jpg)

Al2Experiments

![](images/fc5f32cc266932a525a2784f221c4dcfdf57a970836fbb3f5f2cd6e7829fa955.jpg)

Model

29

11

49

48

![](images/029cd7ee93ae0084ec3c2a45cdc17fec4a763599ccfdb6c510e9f07ef82cbb42.jpg)

Model Type

DPO

DPO

DPO

Seq.Classifier

Custom Classifier

Seq.Classifier

DPO

DPO

DPO

DPO

DPO

![](images/5cbcd5c228183488c46b790830b0b3980bb953880d4dec8f7e370299d5512ddc.jpg)

Score

68.75

68.21

81.55

83.62

55.01

56.14

73.35

![](images/1a2ea879512ce34a9617f400f4558a125670e0a898aa14a49534bb85a927ddc7.jpg)

Chat

53.6

81.6

99.4

95

72.9

38.8

91.6

![](images/dc5aa18c8f9e939ce52062468e6bf0c23aadb0e3773e80b34108e918efbbf5f7.jpg)

atHard

68.

65.

64

62.5

Safety

81.2

61

61.8

Reasoning

85.5

86.3

86.4

59.8

Prior Sets(0.5 weight)

DPO fits an implicit reward function:

1. Is the DPO implicit reward as good as the explicit one?   
2. Does using a weaker optimizer, such as PPO provide a better solution (regularization).

![](images/8a5e05ff08099ce616d6a96dfd0479fa92c6c851cbec327885cd9cbd5eb1f2b8.jpg)

![](images/40c4cc518460883913d5d98f7517ec22b18a5c10c8c175906bd0440fa8d48313.jpg)

![](images/e391c92705af8450602e34dc20da8a221a534362a531ccc79a8b9f0cc2ae9ca5.jpg)

<details>
<summary>bar_stacked</summary>

HH (β=0.05)
| Length | Dataset chosen | Dataset rejected | DPO (β=0.05, α=0.0) |
|---|---|---|---|
| 0-50 | 115 | 25 | 0 |
| 50-100 | 73 | 0 | 30 |
| 100-150 | 25 | 12 | 52 |
| 150-200 | 5 | 0 | 56 |
| 200-250 | 8 | 0 | 34 |
| 250-300 | 3 | 0 | 34 |
| 300-350 | 2 | 0 | 12 |
| 350-400 | 1 | 0 | 4 |
The chart displays the distribution of sample lengths for three models: Dataset chosen, Dataset rejected, and DPO (β=0.05, α=0.0). Vertical dashed lines indicate thresholds at approximately 75 and 150 length units.
</details>

![](images/e630ea72c595720a168ded9de78b1f79a56320dcfbfc1933264ff527a4c63b0a.jpg)

<details>
<summary>bar_stacked</summary>

TLDR (β=0.5)
| Length | Dataset chosen | Dataset rejected | DPO (β=0.5, α=0.0) |
|---|---|---|---|
| 0-10 | 0 | 0 | 2 |
| 10-20 | 5 | 10 | 0 |
| 20-30 | 35 | 25 | 0 |
| 30-40 | 68 | 12 | 0 |
| 40-50 | 102 | 5 | 78 |
| 50-60 | 0 | 0 | 47 |
| 60-70 | 0 | 0 | 17 |
| 70-80 | 0 | 0 | 6 |
| 80-90 | 0 | 0 | 3 |
| 90-100 | 0 | 0 | 2 |
</details>

![](images/c65b3da8c3cdce1558d1c9d85f981380a00651105aa7f403232abd3400284e55.jpg)

![](images/fead2eb390dc9639e384530cb4126cc0a26b262fd6ee7a53898d833248674d67.jpg)  
Disentangling Length from Qualityin Direct Preference Optimization,Park et.al.

DPO fits an implicit reward function:

1. Is the DPO implicit reward as good as the explicit one? YES   
2. Does using a weaker optimizer, such as PPO provide a better solution (regularization).   
NO