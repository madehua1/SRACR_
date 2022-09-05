import numpy as np


class LinUCBUserStruct:
    def __init__(self, featureDimension, lambda_, init="zero"):
        '''

        :param featureDimension: 特征维数
        :param lambda_: 矩阵A的初始值
        :param init: 初始用户兴趣
        '''
        self.d = featureDimension
        self.A = lambda_ * np.identity(n=self.d)
        self.b = np.zeros(self.d)
        self.AInv = np.linalg.inv(self.A)
        if (init == "random"):
            self.UserTheta = np.random.rand(self.d)
        else:
            self.UserTheta = np.zeros(self.d)
        self.time = 0

    def updateParameters(self, articlePicked_FeatureVector, click):
        '''

        :param articlePicked_FeatureVector: 选择的arm的feature
        :param click: 真实的reward
        :return: None
        '''
        self.A += np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector)
        self.b += articlePicked_FeatureVector * click
        self.AInv = np.linalg.inv(self.A)
        self.UserTheta = np.dot(self.AInv, self.b)
        self.time += 1

    def getTheta(self):
        '''

        :return: 用户的兴趣
        '''
        return self.UserTheta

    def getA(self):
        '''

        :return:返回A矩阵
        '''
        return self.A

    def getProb(self, alpha, article_FeatureVector):
        '''

        :param alpha: explore系数
        :param article_FeatureVector:arm的feature
        :return: arm的回报上置信
        '''
        if alpha == -1:
            alpha = alpha = 0.1 * np.sqrt(np.log(self.time + 1))
        mean = np.dot(self.UserTheta, article_FeatureVector)
        var = np.sqrt(np.dot(np.dot(article_FeatureVector, self.AInv), article_FeatureVector))
        pta = mean + alpha * var
        return pta

    def getProb_plot(self, alpha, article_FeatureVector):
        '''

        :param alpha: explore稀疏==系数
        :param article_FeatureVector: arm的feature
        :return: arm的上置信，回报的均值，回报的方差
        '''
        mean = np.dot(self.UserTheta, article_FeatureVector)
        var = np.sqrt(np.dot(np.dot(article_FeatureVector, self.AInv), article_FeatureVector))
        pta = mean + alpha * var
        return pta, mean, alpha * var


class Uniform_LinUCBAlgorithm(object):
    '''
    一个用户，多个arm
    '''

    def __init__(self, dimension, alpha, lambda_, init="zero"):
        '''

        :param dimension: 特征维数
        :param alpha: explore系数
        :param lambda_: 矩阵A的初始值
        :param init: 用户的初始兴趣
        '''
        self.dimension = dimension
        self.alpha = alpha
        self.USER = LinUCBUserStruct(dimension, lambda_, init)

        self.CanEstimateUserPreference = False
        self.CanEstimateCoUserPreference = True
        self.CanEstimateW = False
        self.CanEstimateV = False

    def decide(self, pool_articles, userID):
        '''

        :param pool_articles: 给定的arm pool
        :param userID: 给定的用户
        :return: 选择的arm
        '''
        maxPTA = float('-inf')
        articlePicked = None

        for x in pool_articles:
            x_pta = self.USER.getProb(self.alpha, x.contextFeatureVector[:self.dimension])
            if maxPTA <= x_pta:
                articlePicked = x
                maxPTA = x_pta
        return articlePicked

    def updateParameters(self, articlePicked, click, userID):
        '''

        :param articlePicked: 选择的arm
        :param click: 真实的回报
        :param userID: ？
        :return: None
        '''
        self.USER.updateParameters(articlePicked.contextFeatureVector[:self.dimension], click)



# ---------------LinUCB(fixed user order) algorithm---------------
class N_LinUCBAlgorithm:
    '''
    多个用户，多个arm
    '''

    def __init__(self, dimension, alpha, lambda_, init="zero"):  # n is number of users   ,init表示用户的兴趣向量的初始化方式
        self.users = {}
        self.dimension = dimension
        self.alpha = alpha
        self.lambda_ = lambda_
        self.init = init

        self.CanEstimateUserPreference = False
        self.CanEstimateCoUserPreference = True
        self.CanEstimateW = False
        self.CanEstimateV = False

    def decide(self, pool_articles, userID):
        '''

        :param pool_articles: 给定的arm pool
        :param userID: 给定用户
        :return: 选择的arm
        '''

        # 新用户初始化其参数
        if userID not in self.users:
            self.users[userID] = LinUCBUserStruct(self.dimension, self.lambda_, self.init)
        maxPTA = float('-inf')
        articlePicked = None

        for x in pool_articles:
            # x_pta = self.users[userID].getProb(self.alpha, x.contextFeatureVector[:self.dimension])
            x_pta = self.users[userID].getProb(self.alpha, x.featureVector[:self.dimension])
            # pick article with highest Prob
            if maxPTA < x_pta:
                articlePicked = x
                maxPTA = x_pta

        return articlePicked

    def getProb(self, pool_articles, userID):
        '''

        :param pool_articles: 所有的arm
        :param userID: 给定的用户
        :return: 用户对于所有arm的均值和方差列表
        '''
        means = []
        vars = []
        for x in pool_articles:
            x_pta, mean, var = self.users[userID].getProb_plot(self.alpha, x.contextFeatureVector[:self.dimension])
            means.append(mean)
            vars.append(var)
        return means, vars

    def updateParameters(self, articlePicked, click, userID):
        '''

        :param articlePicked: 选择的arm
        :param click: 真实回报
        :param userID: 用户
        :return: None
        '''
        # self.users[userID].updateParameters(articlePicked.contextFeatureVector[:self.dimension], click)
        self.users[userID].updateParameters(articlePicked.featureVector[:self.dimension], click)






