import codecs
import json




'''


实体id文件的构造       每一行均为课程的id+数字序号
'''
with codecs.open(r'C:\Code\PycharmProjects\MOOCCube\entities\course2.json', 'r', encoding="utf-8") as f:
    entitiesid = []
    i = 0
    for line in f.readlines():
        line = json.loads(line,strict=False)
        entitiesid.append(line['id'])
        i1 = str(i)
        entitiesid.append(i1)
        i += 1
with codecs.open(r'C:\Code\PycharmProjects\MOOCCube\entities\teacher.json', 'r', encoding="utf-8") as f:
    for line in f.readlines():
        line = json.loads(line)
        entitiesid.append(line['id'])
        i1 = str(i)
        entitiesid.append(i1)
        i += 1

with codecs.open(r'C:\Code\PycharmProjects\MOOCCube\entities\school.json', 'r', encoding="utf-8") as f:
    for line in f.readlines():
        line = json.loads(line)
        entitiesid.append(line['id'])
        i1 = str(i)
        entitiesid.append(i1)
        i += 1






with codecs.open(r'C:\Code\PycharmProjects\PLTM\元组和实体构建\实体id.json', 'w', encoding="utf-8") as f:
    for j in range(len(entitiesid)):
        f.write(entitiesid[j]+'\t')
        if j%2!=0:
            f.write('\n')



relationsid = ['讲授','0','发布','1']
with codecs.open(r'C:\Code\PycharmProjects\PLTM\元组和实体构建\关系id.json', 'w', encoding="utf-8") as f:
    for j in range(len(relationsid)):
        f.write(relationsid[j]+'\t')
        if j%2!=0:
            f.write('\n')
