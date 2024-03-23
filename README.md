# BIliBili_dataGet

------

<p align="center"><img src="./img/img_1.png" style="margin； 0 auto"/></p>



本项目为Stupid_Cat 不想看论文摸鱼时解决压力的产物，用于消磨自己的时间以及复习数据库知识以及编程能力。


1. 本项目遵守 CC-BY-NC 4.0 协议，禁止一切商业使用，如需转载请注明作者 ID
2. **请勿滥用，本项目仅用于学习和测试！请勿滥用，本项目仅用于学习和测试！请勿滥用，本项目仅用于学习和测试！**
3. 本库用于获取Bilibili的视频的评论以及收藏夹、历史记录等数据，用于数据分析及数据挖掘的学习和参考
4. 利用本项目提供的接口、文档等造成不良影响及后果与本人无关

# 依赖包引用

使用前请确保已经安装了以下第三方包：

- requests
- retrying
- pandas
- pymysql
- urllib

- hashlib

# 接口文档

------

## Spider 类

| 参数    | 类型      | 必要性 | 备注 |
| ------- | --------- | ------ | ---- |
| cookies | json/dict | 必要   |      |

#### get_Comment_tocsv

| 参数 | 类型 | 必要性 | 备注 |
| ---- | ---- | ------ | ---- |
| bvs  | list | 必要   |      |

会将每个视频的数据以.csv格式存放到Commnet文件夹中

#### get_Comment_to_DataBase

| 参数 | 类型       | 必要性 | 备注                                                 |
| ---- | ---------- | ------ | ---------------------------------------------------- |
| toDB | SpidertoDB | 必要   | 一个SpidertoDB实例，需要进行实例化配置数据库基础功能 |
| bvs  | list       | 必要   | bv号的列表                                           |

会在配置的数据库在中建一个bilibilicomment表将数据存入表中

bilibilicomment表结构

| 键        | 类型      | 备注     |
| --------- | --------- | -------- |
| TITLE     | CHAR(50)  | NOT NULL |
| UPNAME    | CHAR(40)  | NOT NULL |
| TIME      | TIMESTAMP |          |
| UNAME     | CHAR(24)  |          |
| LIKECOUNT | BIGINT    |          |
| COMMENTS  | TEXT      |          |

get_bangumidata

静态方法

参数 ：无

生成.csv文件 返回B站番剧排行榜top50

#### get_Search_videos

| 参数          | 类型   | 必要性 | 备注                                         |
| ------------- | ------ | ------ | -------------------------------------------- |
| keyword       | string | 必要   | *keyword:**关键字 查询的视频标题 默认为原神* |
| *search_type* | string | 非必要 | 搜索目标类型默认为video                      |
| *order*       | string | 非必要 | *结果排序方式*                               |
| *page*        | int    | 非必要 | 页码                                         |

*return:list->[BV**号，标题，播放量，**UP**主**ID**，视频地址**]*

#### get_upvideo_bv

| 参数     | 类型 | 必要性 | 备注                                    |
| -------- | ---- | ------ | --------------------------------------- |
| *mid*    | int  | 必要   | *up**主的**id**号 视频空间连接上的数字* |
| page     | int  | 非必要 | *起始投稿页*                            |
| max_page | int  | 非必要 | *最大页*                                |

*return:* *返回一个**list(list)->[[**视频标题**,**视频**BV**号**,**视频评论数**,**视频播放量**]*,[**视频标题**,**视频**BV**号**,**视频评论数**,**视频播放量**]]

#### history_title_get

| 参数       | 类型 | 必要性 | 备注                        |
| ---------- | ---- | ------ | --------------------------- |
| data_count | int  | 必要   | *爬取多少数据 最大为**2000* |

在个人信息文件夹下生成一个.csv文件  返回历史记录的数据   数据包括视频标题 tag kid bvid



#### favlist_title_get

参数：无

在个人信息文件夹下生成一个.csv文件  返回默认收藏夹的数据数据包括视频标题 tag kid bvid



#### Cookies_name_get

获取Cookies所对的用户id

返回用户名

## SpidertoDB类

该类用于创建一个数据库对象 使得一次实例化就可以完成任务需要多长对数据库请求连接

| 参数     | 类型   | 必要性 | 备注       |
| -------- | ------ | ------ | ---------- |
| database | string | 必要   | 数据库名称 |
| user     | string | 必要   | 用户名     |
| password | string | 必要   | 密码       |
| host     | string | 必要   | 服务器     |

#### __sql_toDB_judge

私有方法 用于执行数据库sql语句

| 参数 | 类型   | 必要性 | 备注    |
| ---- | ------ | ------ | ------- |
| sql  | string | 必要   | SQL语句 |

#### insert_toDB

插入数据到表中

| 参数   | 类型   | 必要性 | 备注                                        |
| ------ | ------ | ------ | ------------------------------------------- |
| title  | string | 必要   |                                             |
| upname | string | 必要   |                                             |
| row    | dict   | 必要   | jsondata解析出来的一行评论                  |
| type   | string | 非必要 | 用于确定是否为根评论 当type为root时是根评论 |

#### create_table

当数据库中没有BiliBilicomment表时创建BiliBilicomment表

#### delete_Redundant_data

*TODO:* *去除重复数据* *SQL**语句条件判断错误把我的表给清空了 暂时搁置阿**(´**。＿。｀**)*

