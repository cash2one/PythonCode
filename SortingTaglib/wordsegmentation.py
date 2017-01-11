#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'
import urllib2
import jieba,json
import imdb
from collections import Counter
import sys
sys.path.append("../")
sys.setdefaultencoding('utf-8')
IMOfficialDB=imdb.IMReadDB("123.56.138.94",3307,"ebook","4titbrVcvnP6LSFA")

##获取图书用于分词的内容
def segerateCont(bookid):
    introduceapi='http://readapi.imread.com/api/v1/book/introduce?bid=%s&spm=1.120.0.1&scm=1.320644'%bookid
    introducecont = urllib2.urlopen(introduceapi).read()
    introducecont = json.loads(introducecont)
    alltext = introducecont['book_brief']+introducecont['tag']
    chapterlistapi='http://readapi.imread.com/api/v1/book/chapterlist?bid=%s&page=1&page_size=200000&order_type=asc&vt=9'%bookid
    chapterlistcont = urllib2.urlopen(chapterlistapi).read()
    chapterlistjsoncont=json.loads(chapterlistcont)
    for para in chapterlistjsoncont['chapterList']:
        if int(para['feeType'])==0:
            chapterid=para['cid']
            # print chapterid
            chaptercontapi = 'http://readapi.imread.com/api/v2/chapter/2/%s/%s/index?auto_pay=0&cm=M3540030'%(bookid, chapterid)
            # print chaptercontapi
            chaptercontcont = urllib2.urlopen(chaptercontapi).read()
            chaptercontjsoncont=json.loads(chaptercontcont)
            # print chaptercontjsoncont,'??'
            chaptercont=chaptercontjsoncont['success']['content']
            chaptername=chaptercontjsoncont['success']['name']
            alltext+=chaptername+';'+chaptercont
    return alltext


def classifyTagslib(classid):
    selectsql="""SELECT aa.tag_id,aa.tag_name FROM ebook_con.con_tag aa,
                (SELECT a.tag_id,COUNT(*)num,b.class_id FROM ebook_con.con_tag_content a,
                (SELECT book_id,book_name,book_tag,class_id FROM ebook_con.con_book WHERE class_id=%s)b
                WHERE a.content_id=b.book_id GROUP BY a.tag_id)bb WHERE aa.tag_id=bb.tag_id ORDER BY bb.num desc limit 200"""%classid
    results=IMOfficialDB.selectdb(selectsql)
    tagslibdict={}
    for result in results:
        tagitems={result[1]:int(result[0])}
        tagslibdict=dict(tagslibdict,**tagitems)
    # tagslib=tagslibdict.values()
    return tagslibdict


def JiebaCut(bookid,tagslibdict):

    tagslib=tagslibdict.keys()
    cutcont=segerateCont(bookid)
    jieba.load_userdict("tagsweight")
    stopwords=[line.strip().decode('utf-8') for line in open('stopwords').readlines()]
    # tagslib=[line.strip().decode('utf-8') for line in open('tagsdict').readlines()]

    jieba_result =jieba.cut(cutcont)            #jieba.cut_for_search() 结巴分词搜索引擎模式,jieba.cut('xxxx',cut_all=True)全模式，默认精确模式
    words_cut= " ".join(jieba_result).split(' ')

    print u'程序处理中，请等待...'
    # ###剔除单个的字
    # word_lists = filter(lambda x: (not (len(x) <=1)),words_cut)
    # ###剔除停用词中的词语
    # word_lists = [word for word in word_lists if word not in stopwords]

    ###需要剔除数字，标点符号，字，停用词库.
    tagwords=[]
    for word in words_cut:
        # if word not in tagslib and len(word)>1 and word.isdigit()==False:
        if word in tagslib and word not in stopwords:
            tagwords+=[word]

    counts=Counter(tagwords).most_common(50)#从多到少返回一个有前n多的元素的列表，如果n被忽略或者为none，返回所有元素，相同数量的元素次序任意
    results=[(bookid,tagslibdict.get(count[0]),count[1]) for count in counts]

    # # print counts
    # for count in counts:
    #     print count[0],count[1]
    return results






if __name__ == '__main__':


    selectsql='SELECT class_id FROM ebook_con.con_class WHERE class_id<60 and class_id<>0'
    results=IMOfficialDB.selectdb(selectsql)

    for result in results[3:4]:
        classid=int(result[0])
        tagslibdict=classifyTagslib(classid)

        selectsql='SELECT book_id FROM ebook_con.con_book WHERE class_id=%s AND  book_status=1 and source_id=2'%classid
        results=IMOfficialDB.selectdb(selectsql)
        for result in results[1:2]:
            try:
                bookid=int(result[0])
                print '正在处理图书：%s！！'
                # cutcont='暗黑轻松的玩耍暗黑我好开心暗黑轻松搞定一切暗黑哈合适的弗拉索夫暗黑'
                results=JiebaCut(bookid,tagslibdict)
                # print results
                insertsql='INSERT INTO public_db.tmp_con_tag_content (book_id,tag_id,tag_frequency) VALUES (%s,%s,%s)'
                IMOfficialDB.insertdb(insertsql,results)
            except Exception,e:
                print e
