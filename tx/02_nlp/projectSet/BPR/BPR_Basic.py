import random
from collections import defaultdict
import numpy as np
from sklearn.metrics import roc_auc_score
import scores

'''
函数说明:BPR类（包含所需的各种参数）
'''


class BPR:
    user_count = 943  # 用户数
    item_count = 1682  # 项目数
    latent_factors = 20  # k个主题,k数
    lr = 0.01  # 步长α
    reg = 0.01  # 参数λ
    train_count = 10000  # 训练次数
    train_data_path = 'train.txt'  # 训练集
    test_data_path = 'test.txt'  # 测试集
    # U-I的大小
    size_u_i = user_count * item_count
    # 随机设定的U，V矩阵(即公式中的Wuk和Hik)矩阵
    U = np.random.rand(user_count, latent_factors) * 0.01
    V = np.random.rand(item_count, latent_factors) * 0.01
    biasV = np.random.rand(item_count) * 0.01
    # 生成一个用户数*项目数大小的全0矩阵
    test_data = np.zeros((user_count, item_count))
    print("test_data_type", type(test_data))
    # 生成一个一维的全0矩阵
    test = np.zeros(size_u_i)
    # 再生成一个一维的全0矩阵
    predict_ = np.zeros(size_u_i)

    # 通过文件路径，获取U-I数据
    def load_data(self, path):
        user_ratings = defaultdict(set)
        # 输入文件路径path
        with open(path, 'r') as f:
            for line in f.readlines():
                u, i = line.split(" ")
                u = int(u)
                i = int(i)
                user_ratings[u].add(i)
        return user_ratings  # 输出字典user_ratings，为包含U-I的键值对

    # 输出一个numpy.ndarray文件（n维数组）test_data,其中把含有反馈信息的数据置为1
    # 通过文件路径，获取测试集数据 获取测试集的评分矩阵
    def load_test_data(self, path):
        file = open(path, 'r')  # 测试集文件路径path
        for line in file:
            line = line.split(' ')
            user = int(line[0])
            item = int(line[1])
            self.test_data[user - 1][item - 1] = 1

    # 对训练集字典处理，更新分解后两个矩阵
    def train(self, user_ratings_train):
        for user in range(self.user_count):
            # 随机获取一个用户
            u = random.randint(1, self.user_count)  # 找到一个user
            # 训练集和测试集不是全都一样的,比如train有948,而test最大为943
            if u not in user_ratings_train.keys():
                continue
            # 从用户的U-I中随机选取1个Item
            i = random.sample(user_ratings_train[u], 1)[0]  # 找到一个item，被评分
            # 随机选取一个用户u没有评分的项目
            j = random.randint(1, self.item_count)
            while j in user_ratings_train[u]:
                j = random.randint(1, self.item_count)  # 找到一个item，没有被评分
            # 构成一个三元组（uesr,item_have_score,item_no_score)
            # python中的取值从0开始
            u = u - 1
            i = i - 1
            j = j - 1
            # BPR
            r_ui = np.dot(self.U[u], self.V[i].T) + self.biasV[i]
            r_uj = np.dot(self.U[u], self.V[j].T) + self.biasV[j]
            r_uij = r_ui - r_uj
            loss_func = -1.0 / (1 + np.exp(r_uij))
            # 更新2个矩阵
            self.U[u] += -self.lr * (loss_func * (self.V[i] - self.V[j]) + self.reg * self.U[u])
            self.V[i] += -self.lr * (loss_func * self.U[u] + self.reg * self.V[i])
            self.V[j] += -self.lr * (loss_func * (-self.U[u]) + self.reg * self.V[j])
            # 更新偏置项
            self.biasV[i] += -self.lr * (loss_func + self.reg * self.biasV[i])
            self.biasV[j] += -self.lr * (-loss_func + self.reg * self.biasV[j])

    # 得到预测矩阵/评分矩阵predict
    def predict(self, user, item):
        predict = np.mat(user) * np.mat(item.T)
        return predict

    # 主函数
    def main(self):
        # 获取U-I的{1:{2,5,1,2}....}数据
        user_ratings_train = self.load_data(self.train_data_path)
        # 获取测试集的评分矩阵

        self.load_test_data(self.test_data_path)
        for u in range(self.user_count):
            for item in range(self.item_count):
                if int(self.test_data[u][item]) == 1:
                    self.test[u * self.item_count + item] = 1
                else:
                    self.test[u * self.item_count + item] = 0
        # 训练
        for i in range(self.train_count):
            self.train(user_ratings_train)  # 训练10000次完成
        predict_matrix = self.predict(self.U, self.V)  # 将训练完成的矩阵內积
        # 预测
        self.predict_ = predict_matrix.getA().reshape(-1)  # .getA()将自身矩阵变量转化为ndarray类型的变量
        print("predict_new", self.predict_)
        self.predict_ = pre_handel(user_ratings_train, self.predict_, self.item_count)
        auc_score = roc_auc_score(self.test, self.predict_)
        print('AUC:', auc_score)
        # Top-K evaluation
        scores.topK_scores(self.test, self.predict_, 5, self.user_count, self.item_count)


# 对结果进行修正，即用户已经产生交互的用户项目进行剔除，只保留没有产生用户项目的交互的数据
def pre_handel(set, predict, item_count):
    # 确保推荐不是训练集中的正样本
    for u in set.keys():
        for j in set[u]:
            predict[(u - 1) * item_count + j - 1] = 0
    return predict


if __name__ == '__main__':
    # 调用类的主函数
    bpr = BPR()
    bpr.main()