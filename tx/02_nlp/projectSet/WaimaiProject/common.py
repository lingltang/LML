import os

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class SimpleNetWork(nn.Module):
    def __init__(self,vocab_size=100,embedding_size=128,n_class=2):
        super(SimpleNetWork,self).__init__()
        self.vocab_size = vocab_size # 词汇大小
        self.embedding_size = embedding_size # 每个单词转换成的词向量大小
        self.n_class = n_class # 分类数目
        self.emb_layer = nn.Embedding(num_embeddings=self.vocab_size,embedding_dim=self.embedding_size)
        # self.linear = nn.Linear(self.vocab_size,self.embedding_size)
        self.classify_layer = nn.Sequential(
            nn.Linear(self.embedding_size, 512),
            nn.ReLU(),
            nn.Linear(512,256),
            nn.ReLU(),
            nn.Linear(256,128),
            nn.ReLU(),
            nn.Linear(128, self.n_class)
            # nn.Softmax()
        )

    def forward(self,x,length):
        '''
               前向过程
        NOTE:
            N表示样本数目，T表示每个样本序列长度
        :param x: 特征属性,形状为:[N,T],全部为单词id
        :param length: 样本的长度信息[N]
        :return: 置信度
        '''
        # 1、单词id转换 [N,T] -> [N,T,E]
        # x = F.one_hot(x,self.vocab_size)
        # x = x.to(torch.float32)
        # x = self.linear(x)
        x = self.emb_layer(x)

        # 2、将每个样本的T个时刻向量合并为一个向量值
        N,T,_ = x.shape
        msk = torch.zeros(N,T)
        for i , _l in enumerate(length):
            msk[i,:_l] = 1
        mask = msk[..., None]
        x = x*mask # [N,T,E]
        x = torch.sum(x,dim=1) / length.to(x.dtype)[...,None] # [N,E]
        # print(x.size())
        return self.classify_layer(x)

class MetricAccuracy(nn.Module):
    def __init__(self):
        super(MetricAccuracy, self).__init__()

    def forward(self, pred_score, target):
        """
        计算准确率
        :param pred_score: [N,C]预测N个样本属于C个类别的置信度
        :param target: [N]N个样本的真实类别标签下标id
        :return:
        """
        pred = torch.argmax(pred_score, dim=1).to(target.dtype)
        corr = torch.eq(pred, target).to(torch.float32)
        acc = torch.mean(corr)
        return acc

def export_script(model, example_inputs, output_path):
    model = model.cpu().eval()
    # 为什么要定example_inputs参数？-->再进行结构转换的时候，需要执行一遍模型的预测
    script_model = torch.jit.trace(model, example_inputs)
    _dir = os.path.dirname(output_path)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    script_model.save(output_path)

if __name__ == '__main__':
    network = SimpleNetWork()
    _x = torch.randint(1,5,(3,5)).to(torch.int64)
    _x[1,3:] = 0

    _length = torch.tensor([5,4,5])
    _t = network(_x,_length)
    print(_t)


class LstmNetWork(nn.Module):
    def __init__(self, vocab_size=100, embedding_size=128, n_class=2):
        super(LstmNetWork, self).__init__()
        self.vocab_size = vocab_size  # 词汇大小
        self.embedding_size = embedding_size  # 每个单词转换成的词向量大小
        self.n_class = n_class  # 分类数目
        self.emb_layer = nn.Embedding(num_embeddings=self.vocab_size, embedding_dim=self.embedding_size)
        self.lstm = nn.LSTM(
            input_size=self.embedding_size,# 每个时刻，输入向量维度大小
            hidden_size=self.embedding_size,# 每个时刻，输出向量维度大小
            num_layers=2,# LSTM层数
            batch_first=True# True表示输入结构为[N,T,E],False为[T,N,E]
        )
        self.classify_layer = nn.Sequential(
            nn.Linear(self.embedding_size, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, self.n_class)
            # nn.Softmax()
        )

    def forward(self, x, length):
        '''
               前向过程
        NOTE:
            N表示样本数目，T表示每个样本序列长度
        :param x: 特征属性,形状为:[N,T],全部为单词id
        :param length: 样本的长度信息[N]
        :return: 置信度
        '''
        # 1、单词id转换 [N,T] -> [N,T,E]
        # x = F.one_hot(x,self.vocab_size)
        # x = x.to(torch.float32)
        # x = self.linear(x)
        x = self.emb_layer(x)

        # 使用LSTM提取每个时刻的输出向量
        output,_ = self.lstm(x)
        x = output
        # 2、将每个样本的T个时刻向量合并为一个向量值
        N, T, _ = x.shape
        msk = torch.zeros(N, T)
        for i, _l in enumerate(length):
            msk[i, :_l] = 1
        mask = msk[..., None]
        x = x * mask  # [N,T,E]
        x = torch.sum(x, dim=1) / length.to(x.dtype)[..., None]  # [N,E]
        # print(x.size())
        return self.classify_layer(x)