#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import imdb
import random

###构造测试数据
testdata={(1, 2): 16.26183032322955, (1, 3): 48.68488359732031, (1, 4): 13.496744289321981, (1, 5): 11.430391423003446, (1, 6): 31.27786112448655, (2, 3): 79.85777093511635, (2, 4): 125.44216788770242, (2, 5): 38.88085052229449, (2, 6): 16.26183032322955, (3, 4): 13.37420454100194, (3, 5): 72.7142585036562, (3, 6): 356.5528838529134, (4, 5): 16.777015405582574, (4, 6): 18.09299518596166, (5, 6): 59.04720157419786}
# keys=[]
# for i in range(10,20):
#     for j in range(10,20):
#         if i!=j:
#
#             if (i, j) not in keys:
#                 value=1/(random.random()/10)+0.001
#                 newrecord={(i,j):value}
#                 testdata=dict(testdata,**newrecord)
#                 newrecord2 = {(i+100, j+100): value}
#                 testdata = dict(testdata, **newrecord2)
#                 keys.append((i, j))
#                 keys.append((j, i))
# print testdata


def NearestDistanceMethod(records,Gnum):
    """
    参数说明：
    records:传入的数据字典，这里每一个键值对代表一条记录
    Gnum:最后需要生成的分类个数

    1.主要变量名说明：
    Gconts:存放各分类的规则方法的字典，关键字为分类名称，值为该分类方法;
    Gids:当前分类规则下，各个分类的类别名称组成的列表;
    Gnum:设定的预期分类类别个数;
    GNewid:新合并的分类名称;
    MinValueKey:当前分类下，距离最近的两分类组成的元组;
    MinValueKey0:当前分类下，距离最近的两分类组成的元组下，元组的第一项值，这里应该是一个分类名称;
    MinValueKey0:当前分类下，距离最近的两分类组成的元组，元组的第二项值，这里应该是分分类名称;

    2.返回的结果：分别由分类名称和分类规则组成的Gnum个键值对的字典
    """

    ###生产初始的各分类及分类规则键值对组成的字典Gconts
    ###生产初始的分类名称组成的列表Gids
    Gconts = {}
    Gids=[]
    keys=records.keys()
    for key in keys:
        Gids+=list(key)
        for Gcont in list(key):
            Gconts[Gcont]=Gcont
    Gids = list(set(Gids))


    ###如下过程表示使用最小距离法聚类分析的过程
    i=0
    while len(Gids)>Gnum:
        i+=1
        GNewid = 'g' + str(i)
        ##获得值为最小的关键字，即为某两个分类组成的元组
        MinValueKey=min(records, key=records.get)
        ##从分类数据字典中删除值最小的键值对
        del records[MinValueKey]

        ###合并成为新的分类
        MinValueKey0 = MinValueKey[0]
        MinValueKey1 = MinValueKey[1]
        # print MinValueKey0,MinValueKey1

        if isinstance(MinValueKey0,str):
            Gconts0=Gconts[MinValueKey0]
            del Gconts[MinValueKey0]
        else:
            Gconts0=[MinValueKey0]
        if isinstance(MinValueKey1,str):
            Gconts1 = Gconts[MinValueKey1]
            del Gconts[MinValueKey1]
        else:
            Gconts1 = [MinValueKey1]

        newrules=list(set(Gconts0+Gconts1))
        newGconts={GNewid:newrules}
        Gconts=dict(Gconts,**newGconts)

        ##从分类名称列表中移除已经合并的两个分类名称
        Gids.remove(MinValueKey0)
        Gids.remove(MinValueKey1)

        ##计算新的分类与其他分类的距离，并更新records的数据，即删除旧的分类与其他分类的距离的键值对，新增新的分类与其他分类的距离的键值对
        ##更新分类名称列表Gids
        for Gid in Gids:
            recordsKeys=records.keys()
            # print recordsKeys
            PossibleKeys=[(MinValueKey0,Gid),(Gid,MinValueKey0),(MinValueKey1,Gid),(Gid,MinValueKey1)]
            NeedDelKeys=list(set(recordsKeys) & set(PossibleKeys))

            if NeedDelKeys!=[]:
                Gvalue=records.get(NeedDelKeys[0])
                for NeedDelKey in NeedDelKeys:
                    del records[NeedDelKey]
                    if NeedDelKey in records.keys():
                        GVvalue=records.get(NeedDelKey)
                        if Gvalue>GVvalue:
                            Gvalue=GVvalue


                records[(GNewid,Gid)]=Gvalue
        Gids.append(GNewid)
        # print Gids

    ##剔除Gconts中旧分类及分类规则键值对
    for key,value in Gconts.items():
        if isinstance(key,str):
            for oldG in value:
                del Gconts[oldG]

    return Gconts




if __name__ == '__main__':
    imformaldb = imdb.IMReadDB("123.56.138.94", 3307, "ebook", "4titbrVcvnP6LSFA", "ebook_con")
    imstatisticaldb = imdb.IMReadDB("182.92.184.14", 3306, "cx_fujun", "fjfjie%mysql3", "ds_read")
    selectsql='SELECT book_id,SUM(read_uv) FROM ds_read.prd_bid_d WHERE stat_day>20161219 GROUP BY book_id'
    resluts=imstatisticaldb.selectdb(selectsql)
    resluts=[(int(reslut[0]),int(reslut[1]))for reslut in resluts]

    tagsdict={}
    for result in resluts:
        selectsql='SELECT tag_id FROM ebook_con.con_tag_content WHERE content_id=%d'%result[0]
        tagids=imformaldb.selectdb(selectsql)
        for tagid in tagids:
            tagdictkey=int(tagid[0])
            if tagdictkey not in tagsdict.keys():
                tagsdict[tagdictkey]=int(result[1])
            else:
                tagsdict[tagdictkey] += int(result[1])

    # print tagdict.values()
    sorted_tags = sorted(tagsdict.iteritems(), key=lambda x: x[1], reverse=True)
    print sorted_tags
    for sorted_tag in sorted_tags[::50]:
        tagid=sorted_tag[0]
        selectsql='SELECT * FROM public_db.con_tag_relatedvalue WHERE tag2_id=%s or tag1_id=%s'%(tagid,tagid)
        resluts=imformaldb.selectdb(selectsql)
        tagvalateddict={}
        for reslut in resluts:
            newtagvalateddit={(int(reslut[0]),int(reslut[1])):float(reslut[2])}
            tagvalateddict=dict(tagvalateddict,**newtagvalateddit)


    # print tagvalateddict




    result=NearestDistanceMethod(tagvalateddict,10)

    print result

