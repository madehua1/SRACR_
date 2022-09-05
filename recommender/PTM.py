import random
import time
import numpy as np
import codecs
import json
import matplotlib.pyplot as plt
from recommender import  util_functions,LinUCB

def staPTM(recommendN,studentsN,studentsstart,students):
    PTMAccumulateRegretMean = []
    for  i in range(recommendN):
        AccumulateRegret = []
        for studentid in range(studentsstart,studentsstart + studentsN):
            AccumulateRegret.append(students[studentid].PTMAccumulateRegret[i])
        mean = np.sum(AccumulateRegret)
        PTMAccumulateRegretMean.append(mean)
    return PTMAccumulateRegretMean


alpha = 0.2
d = 60
start = time.time()
PoolSize = 40
studentsN = 100
recommendN = 500
studentsstart = 90
epochs = 1
PTMMask = 'PTM'                           #唯一标识
courseNumberMin = 2
courseNumberMax = 10


courseId = util_functions.courseIdRead()
def run():
    coursesPool = util_functions.coursesPoolRead1(d)
    PTM = LinUCB.N_LinUCBAlgorithm(d, alpha, 1, init='zero')  # 推荐模型构建  选择特征维度为20，探索因子为0.7，A初始值为单位阵
    students = util_functions.studentRead(courseNumberMin,courseNumberMax)
    for studentid in range(studentsstart,studentsstart + studentsN):
        reward = util_functions.studentReward(students[studentid], courseId)
        coursesPool1 = util_functions.studentCoursesPool_Generate(students[studentid], reward, coursesPool,
                                                                  PoolSize=PoolSize)
        PTMAccumulateRegret = []  # LinUCB算法存储每个学生的累计悔值
        start = time.time()
        for i in range(recommendN):
            '''
            完成PTM一次推荐
            '''
            PTMCoursePicked = PTM.decide(coursesPool1,studentid)           #推荐课程
            reward1 = [r + np.random.normal(0, 0.1) for r in reward]
            r1 = reward1[PTMCoursePicked.id]
            students[studentid].updateRegret6(util_functions.find(reward1) - r1)             #更新学生的悔值
            PTMAccumulateRegret.append(sum(students[studentid].PTMRegret))
            PTM.updateParameters(PTMCoursePicked,r1,studentid)             #更新推荐模
            end = time.time()
            students[studentid].PTMAccumulateRegret = PTMAccumulateRegret
        print("向第%d个学生推荐花费的" % studentid + "cost time: %s" % (round((end - start), 3)))

    PTMAccumulateRegretMean = staPTM(recommendN,studentsN,studentsstart,students)
    PTMAccumulateRegretMean = np.array(PTMAccumulateRegretMean)
    with codecs.open('C:\Code\PycharmProjects\PLTM\推荐结果\%sstudentsN(%d)recommendN(%d)studentstart(%d)CN%d-%dPoolSize%dd(%d)alpha(%f)'
                     % (PTMMask, studentsN, recommendN, studentsstart,courseNumberMin,courseNumberMax,PoolSize, d, alpha), mode='a+',
            encoding='utf-8') as file:
        PTMAccumulateRegretMean = json.dumps(PTMAccumulateRegretMean.tolist())
        file.write(PTMAccumulateRegretMean+'\n')
        print("写入完成")


for j in range(3):
    alpha = 0.2
    d = 100
    print(d,alpha)
    for i in range(epochs):
        run()

