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

## 自定义域名切换

先确认新账号 GitHub Pages 的默认地址可正常访问，再完成下列切换。

1. 如旧账号已验证该域名，需由域名所有者在新账号 **Settings → Pages** 按 GitHub 给出的 TXT 记录验证 `zhangjinyuan.top`。
2. 在旧仓库 **Settings → Pages** 移除 `zhangjinyuan.top` 的绑定。
3. 在新仓库 **Settings → Pages → Custom domain** 添加 `zhangjinyuan.top`。
4. 域名商中根域名 `@` 的 A 记录应指向 GitHub Pages 官方地址：`185.199.108.153`、`185.199.109.153`、`185.199.110.153`、`185.199.111.153`。若已为这些值，无需更改。
5. `www` 的 CNAME 改为 `jinyuanzhang0925.github.io`。本次环境解析到的旧值是 `jeremy-zjy.github.io`，需要在域名商核对。
6. 等待 GitHub DNS 检查、证书签发，启用 **Enforce HTTPS**。
7. 把 `site.json` 的 `url` 改为 `https://zhangjinyuan.top`，提交后自动重新部署。
8. 检查首页、一个中文旧文章 URL、搜索和 RSS。

当前本地网络的根域名解析经过代理，返回 `198.18.*` 合成地址，不能据此认定公网 A 记录；请以域名商配置或可信公网 DNS 查询为准。

GitHub 官方文档：

- [创建 GitHub Pages 站点](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [管理自定义域名](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
