---
title: hexo+github搭建博客
date: '2019-01-19'
url: /2019/01/19/hexo-github搭建博客/
tags: []
categories: []
---

# 序

搭建博客的过程教程很多，我也是参照网上的教程搭建的博客。搭建博客已经过去半年了，但是自己这么久却没有写这篇博文，多说无益，希望能从这篇博客开始先记录hexo博客的问题以及解决方法然后能坚持下去将自己所学所见记录下来，也作为自己生活学习的一个监督和记录。

## 搭建步骤：

1. GitHub创建个人仓库（名称与用户名一致）
2. git安装，绑定github密钥

   > git config –global user.name “你的GitHub用户名”  
   > git config –global user.email “你的GitHub注册邮箱”

   生成ssh密钥文件：

   > ssh-keygen -t rsa -C “你的GitHub注册邮箱”

   打开[GitHub_Settings_keys](https://github.com/settings/keys) 页面，新建new SSH Key

3. 安装node.js，npm
4. 安装hexo：

   > npm install -g hexo-cli

   博客初始化：

   > hexo init blog

   查看本地localhost是否成功
5. 修改.yml站点配置文件，绑定github
6. 绑定域名  
    在blog\source下新建CNAME文件（无文件名）,例如：  
    XXX.top  
    域名解析：建立CNAME解析，主机名分别为@和www，对应值都是你的 Github 个人主页地址
7. 最后hexo g,hexo d,就ok辣。

## 命令介绍

npm install hexo -g #安装Hexo  
npm update hexo -g #升级  
hexo init #初始化博客  
hexo n “我的博客” == hexo new “我的博客” #新建文章  
hexo g == hexo generate #生成  
hexo s == hexo server #启动服务预览  
hexo d == hexo deploy #部署  
hexo server #Hexo会监视文件变动并自动更新，无须重启服务器  
hexo server -s #静态模式  
hexo server -p 5000 #更改端口  
hexo server -i 192.168.1.1 #自定义 IP  
hexo clean #清除缓存，若是网页正常情况下可以忽略这条命令

## 踩过的坑

首先第一次搭建完成后，遇到了61行date的问题 ，一直没有解决，所以我选择了再次搭建，并且将此过程记录了下来。

1. 使用hexo命令显示无效

**注意需要在blog文件下进行操作**  
**还有congig.yml 空格问题基本新手都会犯**  
2. 执行hexo命令出现ERROR  
**npm install 即可**  
3. 前面都没有问题到了hexo d时候连接不上git  
**所以不应用http 应该使用git**  
4. 本地命令成功 但是localhost:访问不到网址  
**大概率是端口占用了**  
5. 本地可以访问但是用户名加github.io无法访问  
**注意库名与用户名一致!!!**  
6. 下载主题出现代理的问题  
 **查询是否使用代理：**  
 >git config –global http.proxy

```
**取消代理：**  

>git config --global --unset http.proxy
```

7. ERROR Process failed: about/index.md  
   TypeError: Cannot read property ‘utcOffset’ of null  
   折腾了半天发现原来站点的配置文件的timezone也就是时区必须要和主题的的配置文件一直，把这两个文件下的timezone都设为Asia/Shanghai就解决了
8. Cannot GET/xxx  
   查看index.html文件是否还在，可以参考[这个](https://www.jianshu.com/p/af83fc73e525)

附加功能：

---

### 1.打赏

1. 准备支付宝和微信二维码
2. 在_config.yml中配置图片
   > reward_comment: 坚持原创技术分享，您的支持将鼓励我继续创作！  
   > wechatpay: /images/wechat.jpg  
   > alipay: /images/aipay.png
3. wechat.jpg、alipay.png图片放入themes/next/source/images(主题配置)中
4. （解决文字闪烁问题）修改next/source/css/_common/components/post/post-reward.styl，注释wechat:hover和alipay:hover
