const { Plugin } = require("obsidian");

module.exports = class DockStatusBarToRightSidebarPlugin extends Plugin {
  async onload() {
    this.rightSplit = null;
    this.resizeObserver = new ResizeObserver(() => this.updateStatusBarWidth());

    this.registerEvent(
      this.app.workspace.on("layout-change", () => this.watchRightSidebar())
    );
    this.registerDomEvent(window, "resize", () => this.watchRightSidebar());

    this.watchRightSidebar();
    window.setTimeout(() => this.watchRightSidebar(), 500);
  }

  onunload() {
    this.resizeObserver?.disconnect();
    document.body.style.removeProperty("--docked-status-bar-width");
  }

  watchRightSidebar() {
    const nextRightSplit = document.querySelector(".workspace-split.mod-right-split");

    if (nextRightSplit === this.rightSplit) {
      this.updateStatusBarWidth();
      return;
    }

    this.resizeObserver.disconnect();
    this.rightSplit = nextRightSplit;

    if (this.rightSplit) {
      this.resizeObserver.observe(this.rightSplit);
    }

    this.updateStatusBarWidth();
  }

  updateStatusBarWidth() {
    if (!this.rightSplit) return;

    const width = this.rightSplit.getBoundingClientRect().width;
    if (width > 0) {
      document.body.style.setProperty(
        "--docked-status-bar-width",
        `${Math.round(width)}px`
      );
    }
  }
};
