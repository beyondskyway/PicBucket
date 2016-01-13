PicBucket
============

基于七牛和SAE开发的图床

示例网站：[PicBucket](http://weiboxb.sinaapp.com/)
New: [PicBucket](http://weiboxb.sinaapp.com/bucket)

---

## 概述
>该小项目起源于本人写博客有时发现之前的图片链接会失效，或者不同网站发布图片链接不能共用，鉴于目前七牛和SAE的免费额度足够个人图床使用，所以决定搭建一个自己的图床。

* 基于flask框架，部署于SAE，七牛JS-SDK(包含Plupload插件)用于上传并保存图片文件，KVDB数据库
* 简化七牛JS-SDK（上传，预览，加载）到一个页面，采用瀑布流式布局（Blockits）
* 响应式布局，可兼容PC端和移动端（chrome）

![样式](http://7ximdq.com1.z0.glb.clouddn.com/1445326252487)

---

## 功能简介
* 七牛JS-SDK基本功能：上传，预览，水印，旋转，缩放等（部分已被隐藏）
* 按上传时间倒序，瀑布流布局，自动加载更多
* 长图底部波浪线，隐藏超出部分
* 封装sae的KVDB方便调用

---

## 安装和运行
* 安装flask相关环境
* 创建SAE的Python应用并上传代码，启用KVDB
* 创建七牛空间获取access-key，secret-key和domain-url
* 修改config.py文件中的配置信息（access-key，secret-key，domain-url，bucket-name）

---
## 修改历史
* 2015-06-09：调整移动端和PC端样式(主要改动上传和预览，采用响应式布局)
* 2105-07-06：重写上传文件UI，添加删除文件，附加标题、描述，修复图片重叠问题，修改PC端和移动端显示，修复移动端部分浏览器无法选择图片问题
* 2015-01-30：尽量使用Material Design重写

## 说明
1. flask相关可直接看[flask快速上手](http://dormousehole.readthedocs.org/en/latest/quickstart.html#)
2. 七牛上传仔细查阅[七牛Python官方文档](http://developer.qiniu.com/docs/v6/sdk/python-sdk.html)
3. 瀑布流插件[Blockits](http://www.inwebson.com/jquery/blocksit-js-dynamic-grid-layout-jquery-plugin/)详情
