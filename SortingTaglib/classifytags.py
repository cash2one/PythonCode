#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lish'
import imdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
base_path='/home/lish/imread/chapcontent/'

IMOfficialDB=imdb.IMReadDB("192.168.0.34",3306,"ebook","ebook%$amRead")

def ClassifiedTags():
    selectsql='SELECT class_id FROM ebook_con.con_class WHERE class_id<60 and class_id<>0 and class_id<>11'
    results=IMOfficialDB.selectdb(selectsql)

    for result in results:
        classid=int(result[0])
        insertsql="""INSERT INTO public_db.tmp_con_tag (tag_id,tag_name,tag_frequency,class_id)
                    SELECT aa.tag_id,aa.tag_name,bb.num,bb.class_id FROM ebook_con.con_tag aa,
                    (SELECT a.tag_id,COUNT(*)num,b.class_id FROM ebook_con.con_tag_content a,
                    (SELECT book_id,book_name,book_tag,class_id FROM ebook_con.con_book WHERE class_id=%s)b
                    WHERE a.content_id=b.book_id GROUP BY a.tag_id)bb WHERE aa.tag_id=bb.tag_id ORDER BY bb.num desc limit 200"""%classid
        results=IMOfficialDB.insertdb(insertsql)


if __name__ == '__main__':
    ClassifiedTags()