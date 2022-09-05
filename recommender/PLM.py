import random
import time
import numpy as np
import codecs
import json
import matplotlib.pyplot as plt
from recommender import  util_functions,LinUCB

def staPLM(recommendN,studentsN,studentsstart,students):
    PLMAccumulateRegretMean = []
    for  i in range(recommendN):
        AccumulateRegret = []
        for studentid in range(studentsstart,studentsstart + studentsN):
            AccumulateRegret.append(students[studentid].PLMAccumulateRegret[i])
        mean = np.sum(AccumulateRegret)
        PLMAccumulateRegretMean.append(mean)
    return PLMAccumulateRegretMean


alpha = 0.2
k = 400
p = 30
start = time.time()
PoolSize = 40
studentsN = 100
recommendN = 500
studentsstart = 90
epochs = 1
PLMMask = 'PLM'                           #唯一标识
courseNumberMin = 2
courseNumberMax = 10


courseId = util_functions.courseIdRead()
def run():
    coursesPool = util_functions.coursesPoolRead2(k, p)
    PLM = LinUCB.N_LinUCBAlgorithm(p, alpha, 1, init='zero')  # 推荐模型构建  选择特征维度为20，探索因子为0.7，A初始值为单位阵
    students = util_functions.studentRead(courseNumberMin,courseNumberMax)
    for studentid in range(studentsstart,studentsstart + studentsN):
        reward = util_functions.studentReward(students[studentid], courseId)
        coursesPool1 = util_functions.studentCoursesPool_Generate(students[studentid], reward, coursesPool,
                                                                  PoolSize=PoolSize)
        PLMAccumulateRegret = []  # LinUCB算法存储每个学生的累计悔值
        start = time.time()
        for i in range(recommendN):
            '''
            完成PLM一次推荐
            '''
            PLMCoursePicked = PLM.decide(coursesPool1,studentid)           #推荐课程
            reward1 = [r + np.random.normal(0, 0.1) for r in reward]
            r1 = reward1[PLMCoursePicked.id]
            students[studentid].updateRegret5(util_functions.find(reward1) - r1)             #更新学生的悔值
            PLMAccumulateRegret.append(sum(students[studentid].PLMRegret))
            # print(PLMCoursePicked.id,util_functions.find(reward1) - r1)
            PLM.updateParameters(PLMCoursePicked,r1,studentid)             #更新推荐模型
            end = time.time()
            students[studentid].PLMAccumulateRegret = PLMAccumulateRegret
        print("向第%d个学生推荐花费的" % studentid + "cost time: %s" % (round((end - start), 3)))

    PLMAccumulateRegretMean = staPLM(recommendN,studentsN,studentsstart,students)
    PLMAccumulateRegretMean = np.array(PLMAccumulateRegretMean)
    with codecs.open('C:\Code\PycharmProjects\PLTM\推荐结果\%sstudentsN(%d)recommendN(%d)studentstart(%d)CN%d-%dPoolSize%dk(%d)alpha(%f)'
                     % (PLMMask, studentsN, recommendN, studentsstart,courseNumberMin,courseNumberMax ,PoolSize, k, alpha), mode='a+',
            encoding='utf-8') as file:
        PLMAccumulateRegretMean = json.dumps(PLMAccumulateRegretMean.tolist())
        file.write(PLMAccumulateRegretMean+'\n')


for j in range(10):
    alpha = 0.4
    k = 350
    print(k,p,alpha)
    for i in range(epochs):
        run()
        # k += 50
