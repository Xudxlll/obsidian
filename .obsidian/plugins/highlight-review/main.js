const { Plugin, ItemView, Notice, MarkdownRenderer, TFile } = require('obsidian');

const VIEW_TYPE = 'highlight-review-view';
const FIELD_LABELS = {
  highlight: 'Highlight 本身',
  sentence: '所在英文句子',
  translationSentence: '所在句子的中文译文',
  comment: 'HiNote comment 解释',
  source: '来源链接'
};
const RATINGS = { again: 1, hard: 2, good: 3, easy: 4 };
const DEFAULT_SETTINGS = {
  defaultFrontMode: 'translationSentence',
  defaultBackMode: 'sentence',
  newCardsPerDay: 20,
  reviewsPerDay: 100
};

module.exports = class HighlightReviewPlugin extends Plugin {
  async onload() {
    this.data = normalizeData(await this.loadData());
    this.registerView(VIEW_TYPE, leaf => new HighlightReviewView(leaf, this));
    this.addRibbonIcon('layers', 'Highlight Review', () => this.openView('review'));
    this.addCommand({ id: 'open-review', name: 'Open review', callback: () => this.openView('review') });
    this.addCommand({ id: 'open-manager', name: 'Open card manager', callback: () => this.openView('manage') });
    this.addCommand({ id: 'sync-current-note', name: 'Sync cards from current note highlights', callback: () => this.syncCurrentNote(true) });
    this.addCommand({ id: 'sync-all-hinote', name: 'Sync cards from all HiNote highlights', callback: () => this.syncAll(true) });
  }

  async savePluginData() { await this.saveData(this.data); }

  async openView(mode = 'review', extraState = {}) {
    // Always open SRS in the main workspace. Do not reuse an existing sidebar leaf:
    // Obsidian keeps sidebar views alive, and reusing leaves[0] pins the review UI
    // back into the narrow right sidebar.
    const leaf = this.app.workspace.getLeaf('tab');
    await leaf.setViewState({ type: VIEW_TYPE, active: true, state: { mode, ...extraState } });
    this.app.workspace.revealLeaf(leaf);
  }

  getActiveFile() { return this.app.workspace.getActiveFile(); }

  async syncCurrentNote(showNotice = false) {
    const file = this.getActiveFile();
    if (!file) return new Notice('没有当前笔记');
    const count = await this.syncFile(file.path);
    if (showNotice) new Notice(`Highlight Review: 已同步 ${count} 张卡片`);
    this.refreshViews();
  }

  async syncAll(showNotice = false) {
    const mapping = await this.readHiNoteMapping();
    let total = 0;
    for (const sourcePath of Object.keys(mapping)) total += await this.syncFile(sourcePath);
    if (showNotice) new Notice(`Highlight Review: 已同步 ${total} 张卡片`);
    this.refreshViews();
  }

  async readHiNoteMapping() {
    try {
      const raw = await this.app.vault.adapter.read('.hinote/metadata/file-mapping.json');
      return (JSON.parse(raw).mapping) || {};
    } catch (e) { return {}; }
  }

  async readHiNoteHighlights(sourcePath) {
    const mapping = await this.readHiNoteMapping();
    const jsonName = mapping[sourcePath] || toSafeFileName(sourcePath);
    try {
      const raw = await this.app.vault.adapter.read(`.hinote/highlights/${jsonName}`);
      return JSON.parse(raw).highlights || {};
    } catch (e) { return {}; }
  }

  async syncFile(sourcePath) {
    const sourceFile = this.app.vault.getAbstractFileByPath(sourcePath);
    if (!(sourceFile instanceof TFile)) return 0;
    const source = await this.app.vault.read(sourceFile);
    const translationPath = await this.findTranslationPath(source, sourcePath);
    const translationFile = translationPath ? this.app.vault.getAbstractFileByPath(translationPath) : null;
    const translation = translationFile instanceof TFile ? await this.app.vault.read(translationFile) : '';
    const highlights = await this.readHiNoteHighlights(sourcePath);
    const sourceParas = getArticleParagraphs(source);
    const transParas = getArticleParagraphs(translation);
    let count = 0;

    for (const [highlightId, h] of Object.entries(highlights)) {
      const context = buildCardContext(h, source, sourceParas, transParas, sourcePath);
      const id = stableCardId(sourcePath, highlightId);
      const old = this.data.cards[id] || {};
      const base = {
        id,
        sourcePath,
        translationPath,
        highlightId,
        frontMode: this.data.settings.defaultFrontMode,
        backMode: this.data.settings.defaultBackMode,
        frontOverride: '',
        backOverride: '',
        due: Date.now(),
        stability: 0,
        difficulty: 0,
        reps: 0,
        lapses: 0,
        lastReview: 0,
        history: [],
        created: Date.now()
      };
      // 手动覆盖、复习历史、字段选择都来自 old；自动字段来自 context 并可随同步更新。
      const card = Object.assign(base, old, context, { sourcePath, translationPath, highlightId, updated: Date.now() });
      this.data.cards[id] = card;
      count++;
    }
    await this.savePluginData();
    return count;
  }

  async findTranslationPath(source, sourcePath) {
    const m = source.match(/中文译文：\s*\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/);
    const candidates = [];
    if (m) candidates.push(resolveWikiPath(m[1]));
    candidates.push(sourcePath.replace(/\.md$/i, ' - 中文译文.md'));
    for (const c of candidates) {
      const withExt = c.endsWith('.md') ? c : c + '.md';
      if (this.app.vault.getAbstractFileByPath(withExt)) return withExt;
      const basename = withExt.split('/').pop().replace(/\.md$/i, '');
      const found = this.app.metadataCache.getFirstLinkpathDest(basename, sourcePath);
      if (found) return found.path;
    }
    return '';
  }

  getAllCards() { return Object.values(this.data.cards || {}); }
  getNewCards() { return this.getAllCards().filter(c => (c.reps || 0) === 0); }
  getDueReviewCards() {
    const now = Date.now();
    return this.getAllCards().filter(c => (c.reps || 0) > 0 && (c.due || 0) <= now).sort((a,b) => (a.due||0)-(b.due||0));
  }
  getDueCards() {
    const now = Date.now();
    return this.getAllCards().filter(c => (c.due || 0) <= now).sort((a,b) => (a.due||0)-(b.due||0));
  }
  getTodayStats() {
    const key = todayKey();
    if (!this.data.dailyStats || this.data.dailyStats.date !== key) {
      this.data.dailyStats = { date: key, newLearned: 0, reviewed: 0 };
    }
    return this.data.dailyStats;
  }
  getProgress() {
    const stats = this.getTodayStats();
    const settings = this.data.settings;
    const dueReviews = this.getDueReviewCards();
    const newCards = this.getNewCards().filter(c => (c.due || 0) <= Date.now()).sort((a,b) => (a.created||0)-(b.created||0));
    const remainingReviews = Math.max(0, Number(settings.reviewsPerDay || 0) - (stats.reviewed || 0));
    const remainingNew = Math.max(0, Number(settings.newCardsPerDay || 0) - (stats.newLearned || 0));
    return { stats, dueReviews, newCards, remainingReviews, remainingNew };
  }
  getStudyCards() {
    const p = this.getProgress();
    return [
      ...p.dueReviews.slice(0, p.remainingReviews),
      ...p.newCards.slice(0, p.remainingNew)
    ];
  }

  getAutoCardText(card, side, modeOverride) {
    const mode = modeOverride || (side === 'front' ? card.frontMode : card.backMode);
    if (mode === 'source') return `From: [[${card.sourcePath}]]`;
    return card[mode] || '';
  }
  getCardText(card, side) {
    const override = side === 'front' ? card.frontOverride : card.backOverride;
    if (override && override.trim()) return override;
    return this.getAutoCardText(card, side);
  }

  async updateCard(card) { this.data.cards[card.id] = card; await this.savePluginData(); this.refreshViews(); }
  async deleteCard(id) { delete this.data.cards[id]; await this.savePluginData(); this.refreshViews(); }
  async updateSettings(settings) {
    this.data.settings = Object.assign({}, this.data.settings, settings);
    await this.savePluginData();
    this.refreshViews();
  }

  async reviewCard(card, ratingName) {
    const now = Date.now();
    const rating = RATINGS[ratingName] || 3;
    const wasNew = (card.reps || 0) === 0;
    const previousDue = card.due || now;
    const elapsedDays = card.lastReview ? Math.max(0, (now - card.lastReview) / 86400000) : 0;
    const next = scheduleFsrsLike(card, rating, elapsedDays, now);
    Object.assign(card, next, {
      reps: (card.reps || 0) + 1,
      lapses: (card.lapses || 0) + (rating === 1 ? 1 : 0),
      lastReview: now,
      history: [ ...(card.history || []), { t: now, rating, previousDue, nextDue: next.due, stability: next.stability, difficulty: next.difficulty } ].slice(-200)
    });
    const stats = this.getTodayStats();
    if (wasNew) stats.newLearned = (stats.newLearned || 0) + 1;
    else stats.reviewed = (stats.reviewed || 0) + 1;
    await this.updateCard(card);
  }

  refreshViews() {
    this.app.workspace.getLeavesOfType(VIEW_TYPE).forEach(leaf => leaf.view && leaf.view.render && leaf.view.render());
  }
};

class HighlightReviewView extends ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.mode = 'review';
    this.current = null;
    this.flipped = false;
    this.editingCardId = '';
    this.focusedEditor = 'front';
  }
  getViewType() { return VIEW_TYPE; }
  getDisplayText() { return 'Highlight Review'; }
  getIcon() { return 'layers'; }
  async setState(state, result) {
    this.mode = state.mode || this.mode;
    this.editingCardId = state.cardId || this.editingCardId || '';
    await super.setState(state, result);
    this.render();
  }
  async onOpen() { this.render(); }

  render() {
    const root = this.containerEl.children[1];
    root.empty(); root.addClass('hfsrs-root');
    const toolbar = root.createDiv('hfsrs-toolbar');
    toolbar.createEl('button', { text: '复习' }).onclick = () => { this.mode = 'review'; this.current = null; this.flipped = false; this.render(); };
    toolbar.createEl('button', { text: '管理卡片' }).onclick = () => { this.mode = 'manage'; this.editingCardId = ''; this.render(); };
    toolbar.createEl('button', { text: '同步当前笔记' }).onclick = () => this.plugin.syncCurrentNote(true);
    toolbar.createEl('button', { text: '同步全部高亮' }).onclick = () => this.plugin.syncAll(true);
    const all = this.plugin.getAllCards();
    const progress = this.plugin.getProgress();
    toolbar.createSpan({ cls: 'hfsrs-muted', text: `总卡片 ${all.length}｜到期复习 ${progress.dueReviews.length}｜新卡 ${progress.newCards.length}` });

    if (this.mode === 'manage') this.renderManager(root, all);
    else if (this.mode === 'edit') this.renderSingleEditor(root);
    else this.renderReview(root);
  }

  renderProgress(root) {
    const p = this.plugin.getProgress();
    const s = this.plugin.data.settings;
    const box = root.createDiv('hfsrs-progress');
    box.createSpan({ text: `今日新学 ${p.stats.newLearned || 0} / ${s.newCardsPerDay}` });
    box.createSpan({ text: `今日复习 ${p.stats.reviewed || 0} / ${s.reviewsPerDay}` });
    box.createSpan({ text: `队列剩余 ${this.plugin.getStudyCards().length}` });
  }

  renderReview(root) {
    root.createEl('h2', { text: 'Highlight Review 复习' });
    this.renderProgress(root);
    this.renderSettings(root);
    const queue = this.plugin.getStudyCards();
    if (!this.current || !this.plugin.data.cards[this.current.id] || !queue.some(c => c.id === this.current.id)) {
      this.current = queue[0] || null; this.flipped = false;
    }
    if (!this.current) {
      root.createDiv('hfsrs-card').createEl('p', { text: '今天没有可复习卡片，或已达到每日新学/复习上限。' });
      return;
    }
    const card = this.current;
    const meta = root.createDiv('hfsrs-muted');
    const kind = (card.reps || 0) === 0 ? '新卡' : '复习卡';
    meta.createSpan({ text: `${kind} · ${card.highlight || ''} · reps ${card.reps || 0} · due ${new Date(card.due).toLocaleString()}` });
    const box = root.createDiv('hfsrs-review-box markdown-rendered');
    MarkdownRenderer.render(this.app, this.plugin.getCardText(card, this.flipped ? 'back' : 'front'), box, card.sourcePath || '', this);
    const actions = root.createDiv('hfsrs-review-actions');
    actions.createEl('button', { text: this.flipped ? '显示正面' : '显示背面' }).onclick = () => { this.flipped = !this.flipped; this.render(); };
    actions.createEl('button', { text: '编辑这张卡' }).onclick = () => { this.mode = 'edit'; this.editingCardId = card.id; this.render(); };
    if (this.flipped) {
      [['again','Again'], ['hard','Hard'], ['good','Good'], ['easy','Easy']].forEach(([key,label]) => {
        actions.createEl('button', { cls: 'hfsrs-rating', text: `${label} · ${previewInterval(card, key)}` }).onclick = async () => {
          await this.plugin.reviewCard(card, key);
          this.current = null; this.flipped = false; this.render();
        };
      });
    }
  }

  renderSettings(root) {
    const details = root.createEl('details', { cls: 'hfsrs-settings' });
    details.createEl('summary', { text: '每日上限设置' });
    const row = details.createDiv('hfsrs-settings-row');
    row.createEl('label', { text: '每日新学' });
    const newInput = row.createEl('input');
    newInput.type = 'number'; newInput.min = '0'; newInput.value = String(this.plugin.data.settings.newCardsPerDay || 0);
    row.createEl('label', { text: '每日复习' });
    const reviewInput = row.createEl('input');
    reviewInput.type = 'number'; reviewInput.min = '0'; reviewInput.value = String(this.plugin.data.settings.reviewsPerDay || 0);
    row.createEl('button', { text: '保存上限' }).onclick = async () => {
      await this.plugin.updateSettings({
        newCardsPerDay: Math.max(0, Number(newInput.value || 0)),
        reviewsPerDay: Math.max(0, Number(reviewInput.value || 0))
      });
      new Notice('已保存每日上限');
    };
  }

  renderManager(root, cards) {
    root.createEl('h2', { text: '卡片管理' });
    root.createEl('p', { cls: 'hfsrs-muted', text: '点击“编辑”会进入单卡编辑页。手动覆盖内容会在后续同步时保留。' });
    cards.sort((a,b)=>(b.updated||0)-(a.updated||0)).forEach(card => {
      const item = root.createDiv('hfsrs-list-item');
      const title = item.createDiv('hfsrs-card-title');
      title.createEl('h3', { text: card.highlight || '(empty)' });
      title.createSpan({ cls: 'hfsrs-pill', text: (card.reps || 0) === 0 ? '新卡' : `reps ${card.reps}` });
      item.createEl('div', { cls: 'hfsrs-muted', text: card.sourcePath || '' });
      const preview = item.createDiv('hfsrs-list-preview');
      preview.setText(cleanMd(this.plugin.getCardText(card, 'front')).slice(0, 160));
      const actions = item.createDiv('hfsrs-toolbar');
      actions.createEl('button', { text: '编辑' }).onclick = () => { this.mode = 'edit'; this.editingCardId = card.id; this.render(); };
      actions.createEl('button', { text: '今天复习' }).onclick = async () => { card.due = Date.now(); await this.plugin.updateCard(card); };
    });
  }

  renderSingleEditor(root) {
    const card = this.plugin.data.cards[this.editingCardId];
    if (!card) {
      root.createDiv('hfsrs-card').createEl('p', { text: '找不到这张卡。' });
      return;
    }
    const top = root.createDiv('hfsrs-toolbar');
    top.createEl('button', { text: '返回复习' }).onclick = () => { this.mode = 'review'; this.render(); };
    top.createEl('button', { text: '返回卡片列表' }).onclick = () => { this.mode = 'manage'; this.editingCardId = ''; this.render(); };
    this.renderCardEditor(root, card, true);
  }

  renderCardEditor(root, card) {
    const wrap = root.createDiv('hfsrs-card'); wrap.id = `hfsrs-${card.id}`;
    const title = wrap.createDiv('hfsrs-card-title');
    title.createEl('h2', { text: card.highlight || '(empty)' });
    title.createSpan({ cls: 'hfsrs-pill', text: card.sourcePath || '' });
    wrap.createEl('p', { cls: 'hfsrs-muted', text: '编辑框默认显示当前实际卡片文字。保存时，如果内容不同于自动生成内容，会保存为手动覆盖；以后同步不会覆盖它。' });

    const grid = wrap.createDiv('hfsrs-grid');
    grid.createEl('label', { text: '正面字段' });
    const frontSel = makeSelect(grid, card.frontMode || 'translationSentence');
    grid.createEl('label', { text: '背面字段' });
    const backSel = makeSelect(grid, card.backMode || 'sentence');
    grid.createEl('label', { text: '正面内容' });
    const frontTa = grid.createEl('textarea'); frontTa.value = this.plugin.getCardText(card, 'front');
    grid.createEl('label', { text: '背面内容' });
    const backTa = grid.createEl('textarea'); backTa.value = this.plugin.getCardText(card, 'back');

    frontTa.addEventListener('focus', () => { this.focusedEditor = 'front'; });
    backTa.addEventListener('focus', () => { this.focusedEditor = 'back'; });

    const getAuto = (side) => {
      const mode = side === 'front' ? frontSel.value : backSel.value;
      return this.plugin.getAutoCardText(card, side, mode);
    };
    frontSel.onchange = () => { if (!frontTa.value.trim() || frontTa.value === this.plugin.getCardText(card, 'front')) frontTa.value = getAuto('front'); renderLivePreview(); };
    backSel.onchange = () => { if (!backTa.value.trim() || backTa.value === this.plugin.getCardText(card, 'back')) backTa.value = getAuto('back'); renderLivePreview(); };

    grid.createEl('label', { text: '中文候选' });
    const candidatesBox = grid.createDiv('hfsrs-candidates');
    const candidates = (card.translationCandidates && card.translationCandidates.length ? card.translationCandidates : [card.translationSentence].filter(Boolean)).slice(0, 6);
    if (!candidates.length) candidatesBox.createDiv('hfsrs-muted').setText('没有找到中文候选句。');
    candidates.forEach((candidate, idx) => {
      const c = candidatesBox.createDiv('hfsrs-candidate');
      c.createDiv('hfsrs-candidate-text').setText(`${idx + 1}. ${candidate}`);
      c.createEl('button', { text: '填入正面' }).onclick = () => { frontTa.value = candidate; this.focusedEditor = 'front'; renderLivePreview(); };
      c.createEl('button', { text: '填入背面' }).onclick = () => { backTa.value = candidate; this.focusedEditor = 'back'; renderLivePreview(); };
    });

    grid.createEl('label', { text: '自动字段' });
    const fieldsPreview = grid.createDiv('hfsrs-field-preview');
    MarkdownRenderer.render(this.app, `**Highlight**：${card.highlight || ''}\n\n**英文句子**：${card.sentence || ''}\n\n**中文译文**：${card.translationSentence || ''}\n\n**Comment**：${card.comment || ''}`, fieldsPreview, card.sourcePath || '', this);

    const previewWrap = wrap.createDiv('hfsrs-preview-grid');
    const frontPreview = previewWrap.createDiv('hfsrs-preview-card markdown-rendered');
    const backPreview = previewWrap.createDiv('hfsrs-preview-card markdown-rendered');
    const renderLivePreview = () => {
      frontPreview.empty(); backPreview.empty();
      frontPreview.createEl('h4', { text: '正面预览' });
      backPreview.createEl('h4', { text: '背面预览' });
      MarkdownRenderer.render(this.app, frontTa.value, frontPreview, card.sourcePath || '', this);
      MarkdownRenderer.render(this.app, backTa.value, backPreview, card.sourcePath || '', this);
    };
    frontTa.addEventListener('input', renderLivePreview);
    backTa.addEventListener('input', renderLivePreview);
    renderLivePreview();

    const actions = wrap.createDiv('hfsrs-toolbar');
    actions.createEl('button', { text: '保存' }).onclick = async () => {
      card.frontMode = frontSel.value;
      card.backMode = backSel.value;
      const frontAuto = getAuto('front');
      const backAuto = getAuto('back');
      card.frontOverride = frontTa.value.trim() && frontTa.value !== frontAuto ? frontTa.value : '';
      card.backOverride = backTa.value.trim() && backTa.value !== backAuto ? backTa.value : '';
      card.updated = Date.now();
      await this.plugin.updateCard(card);
      new Notice('已保存卡片');
      this.mode = 'review';
      this.render();
    };
    actions.createEl('button', { text: '正面恢复自动生成' }).onclick = () => { frontTa.value = getAuto('front'); renderLivePreview(); };
    actions.createEl('button', { text: '背面恢复自动生成' }).onclick = () => { backTa.value = getAuto('back'); renderLivePreview(); };
    actions.createEl('button', { text: '重置为今天复习' }).onclick = async () => { card.due = Date.now(); await this.plugin.updateCard(card); };
    actions.createEl('button', { text: '删除' }).onclick = async () => { if (confirm('删除这张卡？')) { await this.plugin.deleteCard(card.id); this.mode = 'manage'; this.render(); } };
  }
}

function normalizeData(raw) {
  const data = Object.assign({ cards: {}, settings: {}, dailyStats: null }, raw || {});
  data.cards = data.cards || {};
  data.settings = Object.assign({}, DEFAULT_SETTINGS, data.settings || {});
  if (!data.dailyStats || typeof data.dailyStats !== 'object' || !data.dailyStats.date) {
    data.dailyStats = { date: todayKey(), newLearned: 0, reviewed: 0 };
  }
  return data;
}
function todayKey() {
  const d = new Date();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${m}-${day}`;
}
function makeSelect(parent, value) {
  const sel = parent.createEl('select');
  Object.entries(FIELD_LABELS).forEach(([v, label]) => sel.createEl('option', { value: v, text: label }));
  sel.value = value;
  return sel;
}

function toSafeFileName(p) { return p.replace(/[\/\\:*?"<>|]/g, '_').replace(/\s+/g, '_').toLowerCase() + '.json'; }
function stableCardId(sourcePath, highlightId) { return `hfsrs-${hash(sourcePath + '|' + highlightId)}`; }
function hash(s) { let h = 2166136261; for (let i=0;i<s.length;i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h>>>0).toString(16); }
function resolveWikiPath(link) { return link.endsWith('.md') ? link : link + '.md'; }

function stripFrontmatter(md) { return (md || '').replace(/^---[\s\S]*?---\s*/,''); }
function getArticleParagraphs(md) {
  const body = stripFrontmatter(md || '');
  return body.split(/\n\s*\n/).map((raw, idx) => ({ raw, idx, clean: cleanMd(raw) }))
    .filter(p => isProseParagraph(p.clean));
}
function cleanMd(s) {
  return (s || '').replace(/<mark[^>]*>([\s\S]*?)<\/mark>/g, '$1')
    .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, '$2').replace(/\[\[([^\]]+)\]\]/g, '$1')
    .replace(/^>\s*/gm, '').replace(/^[#*\s-]+$/gm, '').replace(/\*\*/g,'').replace(/\*/g,'').trim();
}
function isProseParagraph(s) {
  if (!s || s.length < 20) return false;
  if (/^#+\s/.test(s) || /^Finance & economics/i.test(s)) return false;
  if (/^(中文译文|英文原文)：/.test(s)) return false;
  return /[.!?。！？]/.test(s);
}
function markToBold(s) { return (s || '').replace(/<mark[^>]*>([\s\S]*?)<\/mark>/g, '**$1**').replace(/\n+/g, ' ').replace(/\s+/g, ' ').trim(); }
function sentenceSplitEn(p) { return markToBold(p).split(/(?<=[.!?])\s+(?=[A-Z“"(])/).filter(Boolean); }
function sentenceSplitZh(p) { const m = cleanMd(p).match(/[^。！？]+[。！？]?/g); return (m || [cleanMd(p)]).map(x=>x.trim()).filter(Boolean); }
function containsHighlight(raw, h) {
  const text = (h.text || '').replace(/\*\*$/,'');
  if (!text) return false;
  return cleanMd(raw).includes(text) || raw.includes(text);
}
function buildCardContext(h, source, sourceParas, transParas, sourcePath) {
  let pIndex = sourceParas.findIndex(p => containsHighlight(p.raw, h));
  if (pIndex < 0 && typeof h.position === 'number') {
    const before = source.slice(0, h.position);
    const rawParaStart = before.lastIndexOf('\n\n');
    const rawParaEnd = source.indexOf('\n\n', h.position);
    const raw = source.slice(rawParaStart < 0 ? 0 : rawParaStart, rawParaEnd < 0 ? source.length : rawParaEnd);
    pIndex = sourceParas.findIndex(p => p.raw === raw || cleanMd(p.raw) === cleanMd(raw));
  }
  const sourcePara = sourceParas[pIndex] ? sourceParas[pIndex].raw : '';
  const sentences = sentenceSplitEn(sourcePara);
  const highlightText = (h.text || '').replace(/\*\*$/,'');
  const sentenceIndex = Math.max(0, sentences.findIndex(s => cleanMd(s).includes(highlightText)));
  let sentence = sentences[sentenceIndex] || markToBold(sourcePara) || `**${h.text || ''}**`;
  if (!sentence.includes('**') && highlightText) sentence = boldFirst(sentence, highlightText);
  const comment = ((h.comments || []).map(c => c.content || '').join('\n\n')).trim();
  const meaningSeed = inferMeaningFromComment(comment);
  const candidates = buildTranslationCandidates(transParas, pIndex, sentenceIndex, sentence, comment, meaningSeed);
  let translationSentence = candidates[0] || '';
  const meaning = inferMeaning(comment, translationSentence) || meaningSeed;
  if (meaning) translationSentence = boldFirst(translationSentence, meaning);
  const markedCandidates = candidates.map(c => {
    const m = inferMeaning(comment, c) || meaningSeed;
    return m ? boldFirst(c, m) : c;
  });
  return { highlight: h.text || '', sentence, translationSentence, translationCandidates: uniqueStrings(markedCandidates), comment, source: `From: [[${sourcePath}]]` };
}
function buildTranslationCandidates(transParas, pIndex, sentenceIndex, sentence, comment, meaningSeed) {
  const rows = [];
  const entityTokens = extractEntityTokens(sentence);
  for (let pi = Math.max(0, pIndex - 1); pi <= Math.min(transParas.length - 1, pIndex + 1); pi++) {
    const zhSentences = sentenceSplitZh(transParas[pi] ? transParas[pi].raw : '');
    zhSentences.forEach((zh, si) => {
      let score = 0;
      if (pi === pIndex) score += 20; else score += 8;
      score += Math.max(0, 10 - Math.abs(si - sentenceIndex) * 3);
      if (meaningSeed && zh.includes(meaningSeed)) score += 28;
      for (const token of entityTokens) if (zh.includes(token)) score += 8;
      const commentWords = extractCommentChineseWords(comment).filter(w => zh.includes(w));
      score += Math.min(20, commentWords.length * 3);
      if (zh.length >= 15 && zh.length <= 120) score += 4;
      rows.push({ zh, score });
    });
  }
  return rows.sort((a,b) => b.score - a.score).map(r => r.zh).filter(Boolean);
}
function extractEntityTokens(sentence) {
  const s = sentence || '';
  const tokens = [];
  const dict = [
    ['AI','AI'],
    ['artificial intelligence','人工智能'],
    ['China','中国'],
    ['Chinese','中国']
  ];
  dict.forEach(([en, zh]) => { if (new RegExp(en, 'i').test(s)) tokens.push(zh); });
  const nums = s.match(/\d+(?:,\d+)*(?:\.\d+)?\s*(?:%|m|mn|million|bn|billion)?/gi) || [];
  nums.forEach(raw => {
    const n = raw.trim();
    const compact = n.replace(/,/g, '').replace(/\s+/g, '');
    tokens.push(compact);
    const m = compact.match(/^(\d+(?:\.\d+)?)(m|mn|million|bn|billion)$/i);
    if (m) {
      const value = parseFloat(m[1]);
      const unit = m[2].toLowerCase();
      if (Number.isFinite(value)) {
        if (unit === 'm' || unit === 'mn' || unit === 'million') tokens.push(String(value * 100) + '万');
        if (unit === 'bn' || unit === 'billion') tokens.push(String(value * 10) + '亿');
      }
    }
  });
  return uniqueStrings(tokens);
}
function extractCommentChineseWords(comment) {
  const words = new Set();
  (comment.match(/[\u4e00-\u9fff]{2,8}/g) || []).forEach(seg => {
    for (let len = 2; len <= Math.min(4, seg.length); len++) {
      for (let i = 0; i <= seg.length - len; i++) words.add(seg.slice(i, i + len));
    }
  });
  const bad = /^(这里|意思|可以|理解|原句|不是|而是|这个|表达|常见|搭配|报道|语境|英文|中文)$/;
  return [...words].filter(w => !bad.test(w));
}
function boldFirst(s, term) {
  if (!s || !term || s.includes(`**${term}**`)) return s;
  return s.replace(term, `**${term}**`);
}
function inferMeaningFromComment(comment) {
  if (!comment) return '';
  const bolds = [...comment.matchAll(/\*\*([^*\n]{1,40})\*\*/g)].map(m => m[1]);
  for (const b of bolds) {
    const parts = b.split(/[\/／,，、;；\s]+/).map(x => x.replace(/^(指|是|表示|这里|不是|而是)/,'').trim()).filter(Boolean);
    for (const p of parts) if (/^[\u4e00-\u9fff]{2,8}$/.test(p)) return p;
  }
  const m = comment.match(/(?:指|表示|而是|意思是)\s*\*\*?([\u4e00-\u9fff][\u4e00-\u9fff\s\/／、，,]{1,30})\*\*?/);
  if (m) return m[1].split(/[\s\/／、，,]+/).find(x => x.length >= 2 && x.length <= 8) || '';
  return '';
}
function inferMeaning(comment, zh) {
  if (!comment || !zh) return '';
  const preferred = inferMeaningFromComment(comment);
  if (preferred && zh.includes(preferred)) return preferred;
  const candidates = new Set();
  const cjk = comment.match(/[\u4e00-\u9fff]{2,8}/g) || [];
  cjk.forEach(seg => { for (let len=2; len<=4; len++) for (let i=0; i<=seg.length-len; i++) { const sub = seg.slice(i,i+len); if (zh.includes(sub)) candidates.add(sub); } });
  const bad = /^(这里|意思|可以|理解|法院|企业|员工|人工|智能|杭州|中国|原句|不是|而是|这个|表达)$/;
  return [...candidates].filter(x => !bad.test(x)).sort((a,b)=>a.length-b.length)[0] || '';
}
function uniqueStrings(arr) {
  const out = [];
  const seen = new Set();
  for (const x of arr || []) {
    const key = cleanMd(x);
    if (!key || seen.has(key)) continue;
    seen.add(key); out.push(x);
  }
  return out;
}
function scheduleFsrsLike(card, rating, elapsedDays, now) {
  let s = card.stability || 0;
  let d = card.difficulty || 5;
  if (!card.reps) {
    const init = {1: 0.02, 2: 0.25, 3: 1, 4: 3}[rating];
    return { stability: init, difficulty: clamp(6 - rating, 1, 10), due: now + init * 86400000 };
  }
  const r = s > 0 ? Math.exp(Math.log(0.9) * elapsedDays / s) : 0;
  if (rating === 1) {
    s = Math.max(0.02, Math.min(1, s * 0.45)); d = clamp(d + 1.2, 1, 10);
  } else if (rating === 2) {
    s = Math.max(0.25, s * (1.15 + (1-r) * 0.6)); d = clamp(d + 0.3, 1, 10);
  } else if (rating === 3) {
    s = Math.max(1, s * (2.0 + (1-r) * 1.2)); d = clamp(d - 0.15, 1, 10);
  } else {
    s = Math.max(3, s * (3.2 + (1-r) * 1.8)); d = clamp(d - 0.45, 1, 10);
  }
  const maxDays = 36500;
  return { stability: s, difficulty: d, due: now + Math.min(s, maxDays) * 86400000 };
}
function previewInterval(card, key) {
  const next = scheduleFsrsLike(card, RATINGS[key], card.lastReview ? Math.max(0, (Date.now()-card.lastReview)/86400000) : 0, Date.now());
  const days = (next.due - Date.now()) / 86400000;
  if (days < 1/24) return `${Math.max(1, Math.round(days*24*60))}m`;
  if (days < 1) return `${Math.round(days*24)}h`;
  if (days < 30) return `${Math.round(days)}d`;
  if (days < 365) return `${Math.round(days/30)}mo`;
  return `${Math.round(days/365)}y`;
}
function clamp(x,a,b){ return Math.max(a, Math.min(b, x)); }
