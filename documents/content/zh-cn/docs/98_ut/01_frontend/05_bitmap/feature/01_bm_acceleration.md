---
title: Shield-Bitmap Cache
categories: [bitmap 技术细节]
tags: [香山, Bitmap, 技术细节]
weight: 2
---


##   Shield-Bitmap Cache 性能加速 
 当访问一个物理地址   (PA)   时，硬件通过查找  Shield-XS  Bitmap    数据结构中对应的位置来确定该页是否具有安全属性。  

 查找安全属性的物理地址计算公式如下：  

 即  **Shield-Bitmap 访问地址 = MBMC.BMA + PA [XLEN-1：12+log  <sub>2</sub>(XLEN/8)]**  

 随后用选出对应该   4KB   页的权限。如果对应比特位为    1   ，则表示该页具有安全属性，只能被安全敏感型负载访问；如果为    0   ，则表示该页不具有安全属性，可以被非安全敏感型负载访问。  



##### Shield-XS 直接从内存中读取安全属性

![](../../feature01_1.png)

开启Shield-XS 隔离之后，CPU 内部发起的任何一笔访存操作，都需要对标记安全属性的存储空间发起访问，从内存中获取安全属性的延迟过长，使得系统的性能变差。

为了Shield-XS 隔离带来的性能损失，利用了程序的局部性，增加了Shield-Bitmap Cache, 

当任何一笔访存需要获取安全属性时，优先从Shield-Bitmap Cache 中读取，只有Shield-Bitmap Cache Miss时，才会发起访存请求。
#####  Shield-XS优先从Shield-BitMap Cache中读取安全属性
![](../../feature01_2.png)

