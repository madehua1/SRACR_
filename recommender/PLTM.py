import random
import time
import numpy as np
import codecs
import json
import matplotlib.pyplot as plt
from recommender import  util_functions,LinUCB

def staPLTM(recommendN,studentsN,studentsstart,students):
    PLTMAccumulateRegretMean = []
    for  i in range(recommendN):
        AccumulateRegret = []
        for studentid in range(studentsstart,studentsstart + studentsN):
            AccumulateRegret.append(students[studentid].PLTMAccumulateRegret[i])
        mean = np.sum(AccumulateRegret)
        PLTMAccumulateRegretMean.append(mean)
    return PLTMAccumulateRegretMean


alpha = 0.2
k = 350
d = 60
p = 30
start = time.time()
PoolSize = 40
studentsN = 100
recommendN = 500
studentsstart = 90
epochs = 1
PLTMMask = 'PLTM'                           #唯一标识
courseNumberMin = 2
courseNumberMax = 10


courseId = util_functions.courseIdRead()
def run():
    coursesPool = util_functions.coursesPoolRead(k=k,p=p, d=d)
    students = util_functions.studentRead(courseNumberMin,courseNumberMax)
    PLTM = LinUCB.N_LinUCBAlgorithm(p+d, alpha, 1, init='zero')  # 推荐模型构建  选择特征维度为20，探索因子为0.7，A初始值为单位阵
    for studentid in range(studentsstart, studentsstart + studentsN):
        reward = util_functions.studentReward(students[studentid], courseId)
        coursesPool1 = util_functions.studentCoursesPool_Generate(students[studentid], reward, coursesPool,
                                                                  PoolSize=PoolSize)
        PLTMAccumulateRegret = []  # LinUCB算法存储每个学生的累计悔值
        start = time.time()
        for i in range(recommendN):
            '''
            完成PLTM一次推荐
            '''
            PLTMCoursePicked = PLTM.decide(coursesPool1, studentid)  # 推荐课程
            reward1 = [r + np.random.normal(0, 0.1) for r in reward]
            r1 = reward1[PLTMCoursePicked.id]
            students[studentid].updateRegret1(util_functions.find(reward1) - r1)  # 更新学生的悔值
            PLTMAccumulateRegret.append(sum(students[studentid].PLTMRegret))
            PLTM.updateParameters(PLTMCoursePicked, r1, studentid)  # 更新推荐模型

            end = time.time()
            students[studentid].PLTMAccumulateRegret = PLTMAccumulateRegret
        print("向第%d个学生推荐花费的" % studentid + "cost time: %s" % (round((end - start), 3)))

    PLTMAccumulateRegretMean = staPLTM(recommendN, studentsN, studentsstart, students)
    PLTMAccumulateRegretMean = np.array(PLTMAccumulateRegretMean)
    with codecs.open('C:\Code\PycharmProjects\PLTM\推荐结果\%sstudentsN(%d)recommendN(%d)studentstart(%d)CN%d-%dPoolSize%dk(%d)d(%d)alpha(%f)'
                     % (PLTMMask, studentsN, recommendN, studentsstart,courseNumberMin,courseNumberMax,PoolSize,k,d,alpha), mode='a+', encoding='utf-8') as file:
        PLTMAccumulateRegretMean = json.dumps(PLTMAccumulateRegretMean.tolist())
        file.write(PLTMAccumulateRegretMean + '\n')

for j in range(20):
    k = 350
    d = 30
    alpha = 1.2
    print(k,p,d,alpha)
    for i in range(epochs):
        run()





