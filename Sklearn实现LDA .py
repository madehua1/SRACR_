import jieba
import numpy as np
# import pyLDAvis
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy
import codecs
import json
import time
# import pyLDAvis.sklearn
# from gensim import corpora
# from gensim.models import LdaModel
# from gensim.corpora import Dictionary


'''
需允许loader2函数生成课程about提取词文件
'''
# def loader2():
#     with open('../File processing/课程about部分.txt', 'r', encoding="utf-8") as f1:
#         while True:
#             document = f1.readline()
#             if not document:
#                 break;
#             document_cut = jieba.cut(document)
#             result = ' '.join(document_cut)
#             # print(result)
#             with open('./课程about部分.json', 'a+', encoding="utf-8") as f2:
#                 f2.write(result)
#                 f2.close()
#
# loader2()
# print('*'*100)
#
starttime = time.time()
'''
读取ChineseStopWords.txt文件中的停用词，写入stopwords.txt文件，然后将stopwords.txt中的停用词复制到stopwords列表中
'''
with open('./cn_stopwords.txt', 'r', encoding="utf-8") as f:
    lines = f.readlines()
    f.close()

stopwords = []
for l in lines:
    stopwords.append(l.strip())


ress = []
def res_2():
    with open('./课程text提取词.json', 'r', encoding="utf-8") as f:
        while True:
            document = f.readline()
            if not document:
                break;
            ress.append(document)
    vector = TfidfVectorizer(stop_words=stopwords,dtype=np.float32)
    tfidf = vector.fit_transform(ress)
    return ress, vector , tfidf
ress, vector , tfidf = res_2()

wordlist = vector.get_feature_names()#获取词袋模型中的所有词


# tf-idf矩阵 元素a[i][j]表示j词在i类文本中的tf-idf权重
weightlist = tfidf.toarray()


#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for遍历某一类文本下的词语权重
def print_2():
    for i in range(len(ress)):
        print("-------第res%d段文本的词语tf-idf权重------"%i)
        for j in range(len(wordlist)):
            if wordlist[j] in ress[i]:
                print(wordlist[j], weightlist[0][j])


corpus_2 = ress
cntVector = CountVectorizer(stop_words=stopwords,dtype=np.float64,max_features=1000,max_df=0.5,min_df=3)
cntTf = cntVector.fit_transform(corpus_2)


vocs = cntVector.get_feature_names()
numpy.set_printoptions(threshold=None)
endtime1 = time.time()
K = 10
print('花费的时间为%s'%round((endtime1-starttime),3))
lda = LatentDirichletAllocation(n_components=K, max_iter=10,
                                learning_method='batch',
                                learning_offset=50,
                                random_state=0)

docres = lda.fit_transform(cntTf)
docres = np.array(docres)
# docres = docres.tolist()


tt_matrix = lda.components_
id = 0
for tt_m in tt_matrix:
    tt_dict = [(name, tt) for name, tt in zip(vocs, tt_m)]
    tt_dict = sorted(tt_dict, key=lambda x: x[1], reverse=True)
    # 打印权重值大于0.6的主题词：
    # tt_dict = [tt_threshold for tt_threshold in tt_dict if tt_threshold[1] > 0.6]
    # 打印每个类别前5个主题词：
    tt_dict = tt_dict[:20]
    # print('主题%d:' % (id), tt_dict)
    with open('../File processing/主题词K%d.json'%K, 'a+', encoding="utf-8") as f:
        tt_dict = json.dumps(tt_dict,ensure_ascii=False)
        f.write(tt_dict+'\n')
    id += 1

np.savetxt(fname='../File processing/course_lda_%d.txt'%K,X=docres,fmt="%.6f",delimiter='\t')
print(lda.perplexity(cntTf))


#
# pyLDAvis.enable_notebook()
# pyLDAvis.sklearn.prepare(lda, cntTf, cntVector)


