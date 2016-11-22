#coding: utf-8
import jieba
import jieba.analyse

jieba.load_userdict('./word.txt')

seg_list = jieba.cut('不生二孩的首要原因是教育费用太高,为何多数中国家庭不满足于义务教育?')
print ','.join(seg_list)


tags = jieba.analyse.extract_tags('不生二孩的首要原因是教育费用太高,为何多数中国家庭不满足于义务教育?', topK=10)
print ",".join(tags)
