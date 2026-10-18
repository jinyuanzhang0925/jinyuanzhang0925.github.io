# 网站迁移记录

迁移目标：`jinyuanzhang0925/jinyuanzhang0925.github.io`。域名：`zhangjinyuan.top`。

## 已完成的内容迁移

- 从旧仓库 `master` 分支恢复 22 篇实际发布的文章。
- 全部转换为 Markdown，保留文章标题、日期和原始 URL。
- `hexo` 分支仅有 17 篇且正文不是全部最新，因此以发布版本为准。
- Java 代码从旧主题的行号表格中恢复为标准代码块。
- 恢复旧分类和标签，并合并为新版的话题浏览入口。
- 原 `/archives/`、年月归档、`/categories/` 和翻页地址自动跳转到新版归档。
- 所有内部链接和锚点经过构建后校验。
- 修正 3 处原文已损坏的链接格式。

完整清单在 `migration-manifest.json`，每篇包含来源 HTML 的 SHA-256。

## 原站遗留情况

- `leetcode279` 原本没有正文，保留该文章与 URL，并显示空记录说明。
- `自动打卡` 的两张图片使用了无效的 Windows 路径，发布分支中也没有这些图片；保留文字说明，不显示破图。
- 两篇不同日期的文章原名都为“Java学习笔记2”，按原文保留，日期和 URL 可区分。
- `test`、`test1` 仍保存在完整归档中；首页展示有实际正文的文章。
- 旧友链、书影音、聚宝盒等栏目主要是主题模板或占位内容；原始文件保存在本地 `legacy-site/source/`，未扩展为新版功能。

## 代码简化

旧 `hexo` 分支共有 9,398 个跟踪项，其中 `node_modules` 就有 8,674 个。新版只保留 Markdown 文章、HTML 模板、一个 CSS、一个 JS、构建与检查脚本，以及两项构建依赖。

旧仓库与本地 `legacy-site/` 保留原始文件。新站使用独立、干净的提交历史；迁移不删除旧仓库，不转移原 Issues、Stars 或 Pull Requests。

## 自定义域名切换（2026-10-18）

- 新站已通过 GitHub Actions 发布到新账号的仓库。
- 在新账号 Settings → Pages 完成 `zhangjinyuan.top` 的 TXT 所有权验证。验证同时释放了旧账号的 Pages 域名绑定，无需删除旧仓库。
- 新仓库 Pages 自定义域名已设为 `zhangjinyuan.top`。
- 阿里云根域名 `@` 的旧 A 记录 `192.30.252.153` 已替换为 GitHub Pages 官方的四个地址：`185.199.108.153`、`185.199.109.153`、`185.199.110.153`、`185.199.111.153`。
- `www` 原有“境外 CNAME → jeremy-zjy.github.io”和“默认 A → 192.30.252.153”两条线路，均已改为 CNAME → `jinyuanzhang0925.github.io`。
- DNS TTL 保持 10 分钟。保留 `_github-pages-challenge-jinyuanzhang0925` TXT 记录，以维持域名验证。
- `site.json` 已改为 `https://zhangjinyuan.top`，供 canonical、RSS 和 sitemap 使用。
- GitHub DNS 检查通过，HTTPS 证书已签发，已开启 Enforce HTTPS；正式域名的 HTTPS 首页访问正常。
- 已验证中文旧文章 URL、站内搜索、含 22 篇文章的线上 RSS，以及 320px 手机宽度下的数学公式（无整页横向溢出）。

GitHub 官方文档：

- [验证域名与释放旧绑定](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
- [管理自定义域名](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
