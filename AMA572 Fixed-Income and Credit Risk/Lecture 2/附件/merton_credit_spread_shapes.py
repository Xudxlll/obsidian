"""从讲义 3.2 的债券定价公式绘制期限结构；在 vault 根目录运行本脚本。"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import log_ndtr

OUT = Path(__file__).resolve().parent
D, R, SIGMA = 100.0, 0.03, 0.25
TAU = np.geomspace(1e-5, 20, 7000)

def spread(v, tau):
    """s(0,T) = -log[B(0,T)/(D exp(-rT))]/T，返回年化小数。"""
    d1 = (np.log(v / D) + (R + SIGMA**2 / 2) * tau) / (SIGMA * np.sqrt(tau))
    d2 = d1 - SIGMA * np.sqrt(tau)
    # 两个正项用 logaddexp 合并，避免先计算看涨期权再相减造成消减误差。
    log_q = np.logaddexp(np.log(v / D) + R * tau + log_ndtr(-d1), log_ndtr(d2))
    return np.maximum(-log_q / tau, 0)

left, right = spread(130, TAU) * 1e4, spread(80, TAU) * 1e4
peak = int(left.argmax())
assert 0 < peak < len(TAU) - 1
assert np.all(np.diff(left[:peak + 1]) >= -1e-6)
assert np.all(np.diff(left[peak:]) <= 1e-6)
assert np.all(np.diff(right) < 0)
assert left[0] < 1e-6
assert np.isclose(spread(80, np.array([1e-6]))[0] * 1e-6, np.log(100 / 80), rtol=1e-5)

plt.rcParams.update({
    'font.family': ['Arial Unicode MS', 'DejaVu Sans'],
    'font.size': 11, 'axes.unicode_minus': False,
    'svg.fonttype': 'path', 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.labelcolor': '#273548', 'text.color': '#273548',
    'xtick.color': '#526174', 'ytick.color': '#526174',
})
fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.7))
fig.subplots_adjust(left=.085, right=.975, bottom=.20, top=.76, wspace=.31)
fig.suptitle('Merton 模型：两种信用利差期限结构', fontsize=20, fontweight='bold', y=.965)
fig.text(.5, .875, r'$t=0,\quad D=100,\quad r=3\%,\quad \sigma_V=25\%$' + '（无股息；示例参数，非市场数据）', ha='center', fontsize=11)
colors = ['#197E96', '#BD6034']
for ax, y, c in zip(axes, [left, right], colors):
    ax.plot(TAU, y, color=c, lw=2.8)
    ax.set_xlim(0, 20)
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.set_xlabel(r'剩余期限 $\tau=T-t$（年）', labelpad=10)
    ax.set_ylabel(r'信用利差 $s(0,T)$（基点 / 年）', labelpad=9)
    ax.grid(axis='y', alpha=.22)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color('#A9B4C2')

ax = axes[0]
ax.set_title(r'（i）$D<V(0)$：驼峰形', loc='left', fontsize=14, pad=17)
ax.set_ylim(0, 250)
ax.set_yticks([0, 50, 100, 150, 200, 250])
ax.plot(0, 0, 'o', color=colors[0], ms=5, clip_on=False)
ax.annotate(r'$\tau\to0^+:\ s(0,T)\to0$', xy=(.04, 1), xytext=(3.6, 40), fontsize=11,
            arrowprops=dict(arrowstyle='->', color=colors[0], lw=1.3))
ax.plot(TAU[peak], left[peak], 'o', color=colors[0], ms=5)
ax.annotate(f'峰值约 {left[peak]:.0f} bp\n期限约 {TAU[peak]:.2f} 年',
            xy=(TAU[peak], left[peak]), xytext=(7.1, 205), fontsize=11,
            arrowprops=dict(arrowstyle='->', color=colors[0], lw=1.3), va='center')
ax.text(.97, .06, r'$V(0)=130>D=100$', transform=ax.transAxes, ha='right', color=colors[0])

ax = axes[1]
ax.set_title(r'（ii）$D>V(0)$：单调下降', loc='left', fontsize=14, pad=17)
ax.set_ylim(0, 3000)
ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000])
# 用曲线顶部的延续箭头表达发散，不把无穷大误画成一个有限值。
ix = np.flatnonzero(right < 3000)[0]
ax.annotate('', xy=(TAU[ix] * .92, 3100), xytext=(TAU[ix] * 1.13, 2660),
            arrowprops=dict(arrowstyle='->', color=colors[1], lw=2), annotation_clip=False)
ax.text(4.0, 2630, r'$\tau\to0^+:\ s(0,T)\to+\infty$', fontsize=12, color=colors[1])
ax.annotate('期限越短，利差越高', xy=(2, float(spread(80, np.array([2.]))[0] * 1e4)),
            xytext=(6, 1630), fontsize=11,
            arrowprops=dict(arrowstyle='->', color=colors[1], lw=1.3))
ax.text(.97, .20, r'$V(0)=80<D=100$', transform=ax.transAxes, ha='right', color=colors[1])
fig.text(.5, .045, '按讲义 3.2 公式计算；1 bp = 0.01%。两图纵轴刻度不同；右图上方截断表示利差趋于无穷大。', ha='center', fontsize=10, color='#526174')
for ext in ['png', 'svg']:
    fig.savefig(OUT / f'Merton信用利差_两种期限结构.{ext}', dpi=200, facecolor='white')
plt.close(fig)
print(f'验证通过：左图先升后降，峰值 {left[peak]:.2f} bp（{TAU[peak]:.3f} 年）；右图严格递减；短期极限符合讲义。')
