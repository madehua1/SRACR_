import codecs
import time
import json
import numpy as np
import random
class Article():
    '''
    只有arm的序号和特征
    '''

    def __init__(self, aid, FV=None):
        self.id = aid
        self.featureVector = FV

class User:
    '''

    存储学生的id和奖励
    '''
    def __init__(self, uid, courseSelect,PLTMRegret=[],PLTMAccumulateRegret=[],greedyRegret=[],greedyAccumulateRegret=[],
                 UCBRegret=[],UCBAccumulateRegret=[],randomRegret=[],randomAccumulateRegret=[], PLMRegret=[],PLMAccumulateRegret=[],
                 PTMRegret=[], PTMAccumulateRegret=[]):
        self.uid = uid
        self.courseSelect = courseSelect
        self.PLTMRegret = PLTMRegret
        self.PLTMAccumulateRegret = PLTMAccumulateRegret
        self.greedyRegret = greedyRegret
        self.greedyAccumulateRegret = greedyAccumulateRegret
        self.UCBRegret = UCBRegret
        self.UCBAccumulateRegret = UCBAccumulateRegret
        self.randomRegret = randomRegret
        self.randomAccumulateRegret = randomAccumulateRegret
        self.PLMRegret = PLMRegret
        self.PLMAccumulateRegret = PLMAccumulateRegret
        self.PTMRegret = PTMRegret
        self.PTMAccumulateRegret = PTMAccumulateRegret
    def updateRegret1(self,regret):
        self.PLTMRegret.append(regret)
    def updateRegret2(self,regret):
        self.greedyRegret.append(regret)
    def updateRegret3(self,regret):
        self.UCBRegret.append(regret)
    def updateRegret4(self,regret):
        self.randomRegret.append(regret)
    def updateRegret5(self,regret):
        self.PLMRegret.append(regret)
    def updateRegret6(self,regret):
        self.PTMRegret.append(regret)


def find(t):
    max = -1000
    for i in range(len(t)):
        if (t[i]) > max:
            max = t[i]
    return max

'''

读取课程的特征向量（LDA和transe生成）,生成总体的coursesPool
'''
def coursesPoolRead(k=100,p=30,d=30):
    start = time.time()
    with codecs.open('C:\Code\PycharmProjects\PLTM\File processing\coursesIdTopic_%dPCA_%d.json'%(k,p), mode='r',
                     encoding='utf-8') as file1:
        courseVector1 = []
        lines = file1.readlines()
        for str in lines:
            dict = json.loads(str)
            courseVector1.append(dict['text'])
    with codecs.open('C:\Code\PycharmProjects\PLTM\File processing\coursesNumberd(%d).json' % d, mode='r',
                     encoding='utf-8') as file2:
        courseVector2 = []
        lines = file2.readlines()
        for str in lines:
            dict = json.loads(str)
            courseVector2.append(dict['vector'])
    i = 0
    for courseV1 in courseVector1:
        courseV1.extend(courseVector2[i])
        courseVector1[i] = courseV1
        i += 1
    courseVector = courseVector1
    courseVector = np.array(courseVector)
    end = time.time()
    # print("cost time1: %s" % (round((end - start), 3)))
    coursesPool = []
    for i in range(705):
        course = Article(i, courseVector[i])
        coursesPool.append(course)
    return coursesPool


def coursesPoolRead1(d=40):
    start = time.time()
    with codecs.open('C:\Code\PycharmProjects\PLTM\File processing\coursesNumberd(%d).json'%d, mode='r',
                     encoding='utf-8') as file1:
        courseVector = []
        lines = file1.readlines()
        for str in lines:
            dict = json.loads(str)
            courseVector.append(dict['vector'])
    courseVector = np.array(courseVector)
    end = time.time()
    # print("cost time1: %s" % (round((end - start), 3)))
    coursesPool = []
    for i in range(705):
        course = Article(i, courseVector[i])
        coursesPool.append(course)
    return coursesPool


def coursesPoolRead2(k=50,p=20):
    start = time.time()
    with codecs.open('C:\Code\PycharmProjects\PLTM\File processing\coursesIdTopic_%dPCA_%d.json'%(k,p), mode='r',
                     encoding='utf-8') as file1:
        courseVector = []
        lines = file1.readlines()
        for str in lines:
            dict = json.loads(str)
            courseVector.append(dict['text'])
    courseVector = np.array(courseVector)
    end = time.time()
    # print("cost time1: %s" % (round((end - start), 3)))
    coursesPool = []
    for i in range(705):
        course = Article(i, courseVector[i])
        coursesPool.append(course)
    return coursesPool





'''

读取所有学生选择的课程，以0，1形式在列表中存储,并生成推荐使用的学生对象
'''
def studentRead(courseNumberMin,courseNumberMax):
    start = time.time()
    with codecs.open(r'C:\Code\PycharmProjects\PLTM\File processing\userNumber%d-%d.json'%(courseNumberMin,courseNumberMax),
                mode='r',encoding='utf-8') as file2:
        lines = file2.readlines()

    coursesSelect = []
    for str in lines:
        dict = json.loads(str)
        coursesSelect.append(dict['course_order'])
    end = time.time()
    print("cost time: %s" % (round((end - start), 3)))
    students = []
    for i in range(len(coursesSelect)):
        student = User(i, coursesSelect[i], PLTMRegret=[], PLTMAccumulateRegret=[],
                       greedyRegret=[], greedyAccumulateRegret=[], UCBRegret=[], UCBAccumulateRegret=[],
                       randomRegret=[], randomAccumulateRegret=[],
                       PLMRegret=[], PLMAccumulateRegret=[],PTMRegret=[],PTMAccumulateRegret=[])  # 学生对象的id为整数，reward为列表
        students.append(student)

    return students

'''
读取课程的id
'''
def courseIdRead():
    courseId = []
    with open('C:\Code\PycharmProjects\MOOCCube\entities\course.json', mode='r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        line = json.loads(line)
        courseId.append(line['id'])
    return courseId

'''
得到学生对课程的真实反馈
'''
def studentReward(student,couseId):
    reward = [0] * 706
    i = 0
    for id in couseId:
        if id in student.courseSelect:
            reward[i] = 1
        i += 1
    return reward


'''

为每个学生生成对应的coursesPool
'''
def studentCoursesPool_Generate(student,reward,coursesPool,PoolSize=40):         #使正负反馈的比例为1：a
    courseSelectNumber = len(student.courseSelect)
    coursesSelect = []
    courseNotSelect = []
    for i in range(len(coursesPool)):
        if reward[i] == 1:
            coursesSelect.append(coursesPool[i])
        else:
            courseNotSelect.append(coursesPool[i])
    courseNotSelect = random.sample(courseNotSelect,PoolSize-courseSelectNumber)
    # coursesSelect.extend(courseNotSelect)
    courseNotSelect.extend(coursesSelect)
    coursesSelect = courseNotSelect
    return coursesSelect


