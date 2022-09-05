import codecs
import json


'''

读取teacher-course.json文件，并添加’讲授‘关系，生成学校发布课程.json文件
'''
with codecs.open(r'C:\Code\PycharmProjects\MOOCCube\relations\teacher-course.json', 'r', encoding="utf-8") as f:
    TeacherCoureses = []
    for TeacherCourese in f.readlines():
        TeacherCourese = TeacherCourese.strip().split('\t')
        TeacherCourese.insert(1,'讲授')
        TeacherCoureses.append(TeacherCourese)

# with codecs.open(r'C:\Code\PycharmProjects\PLTM\元组和实体构建\老师讲授课程.json', 'w', encoding="utf-8") as f:
#     for j in range(len(TeacherCoureses)):
#         f.write("\t".join(TeacherCoureses[j]) + '\n')



'''

读取school-course.json文件，并添加‘发布’关系，生成学校发布课程.json文件
'''
with codecs.open(r'C:\Code\PycharmProjects\MOOCCube\relations\school-course.json', 'r', encoding="utf-8") as f:
    SchoolCoureses = []
    for SchoolCourese in f.readlines():
        SchoolCourese = SchoolCourese.strip().split('\t')
        SchoolCourese.insert(1,'发布')
        SchoolCoureses.append(SchoolCourese)

# with codecs.open(r'C:\Code\PycharmProjects\PLTM\元组和实体构建\学校发布课程.json', 'w', encoding="utf-8") as f:
#     for j in range(len(SchoolCoureses)):
#         f.write("\t".join(SchoolCoureses[j])+'\n')






'''

读取school-course.json，teacher-course.json文件，添加'发布'，'讲授'两种关系，生成三元组.json文件
'''
tuples = []
with codecs.open(r'C:\Code\PycharmProjects\MOOCCube\relations\teacher-course.json', 'r', encoding="utf-8") as f:
    for TeacherCourese in f.readlines():
        TeacherCourese = TeacherCourese.strip().split('\t')
        TeacherCourese.insert(1,'讲授')
        tuples.append(TeacherCourese)

with codecs.open(r'C:\Code\PycharmProjects\MOOCCube\relations\school-course.json', 'r', encoding="utf-8") as f:
    for SchoolCourese in f.readlines():
        SchoolCourese = SchoolCourese.strip().split('\t')
        SchoolCourese.insert(1,'发布')
        tuples.append(SchoolCourese)

with codecs.open(r'/元组和实体构建\三元组.json', 'w', encoding="utf-8") as f:
    for j in range(len(tuples)):
        f.write("\t".join(tuples[j])+'\n')













