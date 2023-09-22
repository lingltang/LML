import copy

import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset, DataLoader


def get_vocab_mappint(path):
    '''
    :param path:
    :return:
    '''
    df = pd.read_csv(path)
    words = {
        'PAD': 0,# 填充单词
        'UNK': 1,# 未知单词
        'NUM': 2,# 数字
        'PDT': 3 # 标点符号
    }
    index = 4 # 初始index
    for text in df['review']:
        for word in list(text):
            if word in words:
                continue
            words[word] = index
            index+=1
    return words

class WaiMaiDataset(Dataset):
    def __init__(self,word2index,data_path=r'waimai.csv'):
        super(WaiMaiDataset,self).__init__()
        self.word2index = word2index
        self.pad_idx = self.word2index["PAD"]
        xs,ys,lengths = self._preprocess_data(data_path)
        self.xs = xs
        self.ys = ys
        self.lengths = lengths

    def _split_text(self,text):
        ids = []
        for word in list(text):
            word = word.strip()# 去除空格
            if len(word) == 0:
                continue
            if word in ['.',',','?','!',';',':','。','，','？','！','；','：','+','-','*','\\','/']:
                ids.append(self.word2index['PDT'])
            elif word in ['1','2','3','4','5','6','7','8','9','0']:
                ids.append(self.word2index['NUM'])
            else:
                ids.append(self.word2index.get(word,self.word2index['UNK']))
        return ids
    def _preprocess_data(self,data_path):
        df = pd.read_csv(data_path)
        df = df[['label','review']]
        xs = []
        ys = []
        lengths = []
        for value in df.values:
            ys.append(int(value[0]))
            words = self._split_text(value[1])
            xs.append(words)
            lengths.append(len(words))
        return xs,ys,lengths

    def __len__(self):
        return len(self.xs)

    def __getitem__(self, item):
        return self.xs[item],self.ys[item],self.lengths[item]

    def collate_fn(self,data):
        '''
        :param data:
        :return:
        '''
        ys = []
        lengths = []
        max_length = -1
        for _,y_,l_ in data:
            ys.append(y_)
            lengths.append(l_)
            if l_>max_length:
                max_length = l_
        xs = []
        for x,_,l_ in data:
            x = copy.deepcopy(x)
            if l_ < max_length:
                x.extend([self.pad_idx] * (max_length-l_))
            xs.append(x)
        return torch.tensor(xs),torch.tensor(ys),torch.tensor(lengths)



if __name__ == '__main__':
    # wd = WaiMaiDataset()
    data_path = r'waimai.csv'
    wordsMap = get_vocab_mappint(data_path)
    wd = WaiMaiDataset(wordsMap)
    trainloader = DataLoader(
        wd,
        batch_size=4,
        shuffle=True,
        num_workers=0,
        prefetch_factor=2,
        collate_fn=wd.collate_fn
    )
    for d in trainloader:
        print(d)
        break