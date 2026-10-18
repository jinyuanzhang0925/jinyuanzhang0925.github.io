# 右郁石

记录编程、学习与日常。个人网站从 `Jeremy-zjy/Jeremy-zjy.github.io` 迁入，保留 22 篇已发布文章、原始日期及原有文章 URL。

新版采用米白与蓝色、中文衬线大标题和简洁的阅读布局。设计参考 GeekPlux 的排版方向，页面与样式独立编写。

## 本地运行

需要 Python 3.9 或更新版本。无需 Node.js、Hexo 或数据库。

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py
python scripts/check_site.py
python -m http.server 4173 --directory dist
```

打开 `http://localhost:4173/`。`dist/` 为可直接托管的静态网站，不提交到仓库。

## 写文章

在 `content/posts/` 新建 Markdown 文件，例如 `2026-10-18-hello.md`：

```yaml
---
title: 新的记录
date: '2026-10-18'
url: /2026/10/18/hello/
tags:
  - 随笔
categories: []
---

正文从这里开始。
```

`url` 必须是 `/年/月/日/文章名/`。不要改动旧文章的 `url`，已有外部链接依赖这些地址。提交到 `main` 后，GitHub Actions 自动构建、校验和部署。

## 修改网站

| 内容 | 文件 |
| --- | --- |
| 名称、描述、站点地址、社交链接 | `site.json` |
| 首页正文 | `templates/home.html` |
| 关于页面 | `templates/about.html` |
| 导航与页脚 | `templates/layout.html` |
| 颜色、字体与响应式布局 | `assets/style.css` |
| 搜索与深色模式 | `assets/site.js` |
| 构建与自动生成索引 | `build.py` |

搜索、话题、RSS、站点地图与文章目录由构建器生成。文章与导航在关闭 JavaScript 时仍可阅读。包含数学公式的文章会按需从 jsDelivr 加载固定版本的 MathJax；除此之外没有外部脚本、字体或统计请求。

## GitHub Pages

目标仓库：`jinyuanzhang0925/jinyuanzhang0925.github.io`。

在仓库 **Settings → Pages → Source** 选择 **GitHub Actions**，使用 `.github/workflows/pages.yml`。默认地址为 `https://jinyuanzhang0925.github.io/`。

自定义域名切换的具体说明见 `MIGRATION.md`。完成域名绑定后，将 `site.json` 的 `url` 改为实际的 HTTPS 域名，重新构建，确保 canonical、RSS 与 sitemap 使用一致的地址。

## 迁移来源与校验

`migration-manifest.json` 列出了全部 22 篇文章、旧路径及旧发布 HTML 的 SHA-256。导入以旧仓库 `master` 发布分支为准，因为 `hexo` 源码分支少了 5 篇文章，部分正文也较旧。`scripts/migrate_legacy.py` 仅用于一次性导入，不参与日常构建；运行它需要额外安装脚本头部标注的转换工具。

旧仓库代码许可证保留在 `LICENSE`。旧文中已有的第三方引用与署名保持原状。
