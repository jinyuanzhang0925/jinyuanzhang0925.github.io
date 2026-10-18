---
title: hexo+github迁移电脑
date: '2021-04-04'
url: /2021/04/04/hexo-github迁移电脑/
tags: []
categories: []
---

# hexo个人博客迁移

从一台电脑上迁移至另外一台电脑

## 实现步骤

- 复制blog文件夹
- 在新的电脑上下载新的git和nodejs
- npm install
- 安装hexo,重新部署。

  ## 问题

  ### 1.nodejs版本过高

  下载低版本13.14。

  ### 2.Please make sure you have the correct access rights and the repository exists.（一般是公钥出问题）

1. > git config –global user.name “你的GitHub用户名”  
   > git config –global user.email “你的GitHub注册邮箱”
2. 删除.ssh文件夹（直接搜索该文件夹）下的known_hosts(手动删除即可，不需要git）
3. 生成ssh密钥文件：

   > ssh-keygen -t rsa -C “你的GitHub注册邮箱”
4. 打开[GitHub_Settings_keys](https://github.com/settings/keys%22) 页面，新建new SSH Key，把密钥复制上去。

   ### 3.遇见404问题

   [参考解决方法](https://www.jianshu.com/p/2349c763cc02?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation)
