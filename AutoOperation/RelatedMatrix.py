#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import os

import imdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]

formaldb = imdb.IMReadDB("123.56.138.94",3307,"ebook","4titbrVcvnP6LSFA","ebook_con")


#图书对应的标签列表[tag1,tag2,..]
def BooksToTag(tagid):
    # selectsql = 'SELECT content_id,tag_id FROM ebook_con.con_tag_content where tag_id = %d'%tagid
    selectsql = 'SELECT book_id,tag_id FROM public_db.tmp_con_tag_content where tag_id = %d'%tagid
    results = formaldb.selectdb(selectsql)
    BooksToTag = []
    for result in results:
        bid = int(result[0])
        # tagid = int(result[1])
        BooksToTag.append(bid)
    return BooksToTag


#相关度公式
def RelatedFormula(tag1,tag2):
    Tag1ToBooks = BooksToTag(tag1)
    Tag2ToBooks = BooksToTag(tag2)
    Tag1InterTag2 = list(set(Tag1ToBooks) & set(Tag2ToBooks))
    # Tag1UnionTag2 = list(set(Tag1ToBooks) | set(Tag2ToBooks))
    if len(Tag1InterTag2)!=0:
        relatedvalue = float(len(Tag1InterTag2)) / min(len(Tag1ToBooks),len(Tag2ToBooks))
    else:
        relatedvalue=0
    return  relatedvalue

#用于计算两组或两个标签的相关度
def TagsRelatedDict(args1,args2):
    args1floag=isinstance(args1, list)
    args2floag=isinstance(args2, list)
    relatedDict = {}
    if args1floag and args2floag:
        tags1=args1
        tags2=args2
        for tag1 in tags1:
            for tag2 in tags2:
                if tag2 != tag1:
                    key1 = (tag1, tag2)
                    key2 = (tag2, tag1)
                    if key1 not in relatedDict.keys() and key2 not in relatedDict.keys():
                        relatedvalue=RelatedFormula(tag1, tag2)
                        addDict = {key1: relatedvalue}
                        relatedDict = dict(relatedDict, **addDict)
                    else:
                        continue
                else:
                    continue
    elif args2floag!=True and args1floag!=True:
        tag1=args1
        tag2=args2
        if tag2 != tag1:
            key1 = (tag1, tag2)
            key2 = (tag2, tag1)
            if key1 not in relatedDict.keys() and key2 not in relatedDict.keys():
                relatedvalue = RelatedFormula(tag1, tag2)
                addDict = {key1: relatedvalue}
                relatedDict = dict(relatedDict, **addDict)
    else:
        if args1floag!=True:
            tag1=args1
            tags2 = args2
        else:
            tag1 = args2
            tags2 = args1
        for tag2 in tags2:
            if tag2 != tag1:
                key1 = (tag1, tag2)
                key2 = (tag2, tag1)
                if key1 not in relatedDict.keys() and key2 not in relatedDict.keys():
                    # print tag1, tag2
                    relatedvalue = RelatedFormula(tag1, tag2)

                    if relatedvalue!=0:
                        print tag1, tag2,relatedvalue
                        addDict = {key1: relatedvalue}
                        relatedDict = dict(relatedDict, **addDict)

    return relatedDict



def main():

    selectsql = 'SELECT DISTINCT tag_id FROM ebook_con.con_tag_content'
    results = formaldb.selectdb(selectsql)
    tagids=[]
    for result in results:
        tagids.append(int(result[0]))

    # print tagids
    for tagid in tagids:
        result=TagsRelatedDict(tagid,tagids)
        relateddata=[]
        for key,value in result.items():
            # if value!=0.0:
                relateddata+=[key+tuple([str(value)])]
        if relateddata!=[]:
            insertsql='INSERT INTO public_db.con_tag_relatedvalue (tag1_id,tag2_id,relatedvalue) VALUES (%s,%s,%s)'
            formaldb.insertdb(insertsql,relateddata)
        # print relateddata


if __name__ == '__main__':
    main()
    # tagids=[10358,10359,10364,10426,10431,10592,10599,11913,12031,12033,12256,12273,12295,12506,13368,13506,13610,13612,13613]#,10312,13625,10268,10372,26601,10273,10379,27319,10322,13333,10315,18116,10264,17933,17757,20935,10412,12942,10656,13552,10227,13023,14066,10275,10321,13968,10358,18112,10640,10476,10434,10375,13203,10373,11405,10270,18508,13417,10639,28744,29161,10436,13921,28090,12144,19398,10238,10327,12792,10240,10431,10495,13755,12273,18628,10417,10446,10475,10449,10473,26224,10430,11460,33139,17868,10602,10641,13271,10277,10323,12136,12454,10282,10292,36026,26210,10301,10480,12858,10349,21652,13633,17007,17946,18559,19481,10317,10382,10592,10642]
    # print TagsRelatedDict(13203,10365)
    # print TagsRelatedDict(10429,10269)
    # print TagsRelatedDict(10429,tagids)
    # print TagsRelatedDict(13203,tagids)
    # print TagsRelatedDict(tagids,tagids)