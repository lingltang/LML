import os

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from projectSet.data import commonWaimai
from projectSet.WaimaiProject import common


def training():
    data_path = '../data/waimai.csv'
    output_dir = '../data/output'
    model_dir = os.path.join(output_dir,'model')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    batch_size = 64
    lr = 0.01

    # 模型持久化
    original_model = None
    names = os.listdir(model_dir)
    if len(names):
        names.sort()
        path = os.path.join(model_dir, names[-1])
        original_model = torch.load(path)

    # 数据提取
    if original_model is not None:
        word_2_index = original_model['word2index']
    else:
        word_2_index = commonWaimai.get_vocab_mappint(data_path)
    trainset = commonWaimai.WaiMaiDataset(word_2_index,data_path=data_path)
    trainloader = DataLoader(
        trainset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
        prefetch_factor=2,
        collate_fn=trainset.collate_fn
    )

    # 定义可视化输出
    writer = SummaryWriter(output_dir,'summary')
    model = common.SimpleNetWork(vocab_size=len(word_2_index),embedding_size=128,n_class=2)
    loss_fn = nn.CrossEntropyLoss()
    train_op = optim.SGD(params=model.parameters(),lr=lr)
    acc_fn = common.MetricAccuracy()
    writer.add_graph(model,[torch.randint(0,100,(4,35)),torch.randint(0,100,(4,))])

    if original_model is not None:
        model.load_state_dict(original_model['model'])

    # 3. 模型的训练
    best_eval_acc = None
    total_epochs = 100
    train_step, test_step = 0, 0
    for epoch in range(total_epochs):
        # 模型训练
        model.train()  # 模型进入训练模式
        train_accs, train_losss = [], []
        for batch, (_xs, _ys, _lengths) in enumerate(trainloader):
            _xs = _xs.to(torch.int64)
            _ys = _ys.to(torch.int64)

            # b. 前向过程
            train_op.zero_grad()  # 将优化器涉及到的所有参数对应的梯度重置为0
            _y = model(_xs,_lengths)  # 模型的前向推理, [N,2]表示N个样本分别属于两个类别的置信度
            loss_ = loss_fn(_y, _ys)  # 计算损失

            # 计算准确率
            _yi = torch.argmax(_y, dim=1)
            _acc2 = acc_fn(_y, _ys)

            # c. 反向过程
            loss_.backward()  # 基于损失计算涉及到的所有参数的梯度值
            train_op.step()  # 参数更新
            print(f"train epoch:{epoch}/{total_epochs} batch:{batch} "
                  f"loss:{loss_.item():.3f} accuracy:{_acc2:.3f}")
            writer.add_scalar('train_loss', loss_.item(), global_step=train_step)
            writer.add_scalar('train_acc', _acc2.item(), global_step=train_step)
            train_step += 1
            train_losss.append(loss_.item())
            train_accs.append(_acc2.item())

        # 当前epoch的可视化指标保存
        eval_acc = np.mean(train_accs)
        writer.add_scalars('acc', {'train': np.mean(train_accs)}, global_step=epoch)
        writer.add_scalars('loss', {'train': np.mean(train_losss)}, global_step=epoch)

        # 模型持久化-->torch.save:可以持久化任意对象，因为底层就是通过pickle来进行二进制数据输出的
        # torch.save(model, os.path.join(root_dir, f"model_{epoch:04d}.pt"))
        if best_eval_acc is None or eval_acc > best_eval_acc:
            torch.save(
                {
                    'model':model.state_dict(),
                    'word2index':word_2_index,
                    'best_eval_acc':eval_acc
                }, os.path.join(model_dir, f"model_{epoch:04d}.pt")
            )
            best_eval_acc = eval_acc

    # NOTE: 不要忘记进行关闭操作
    writer.close()

def to_jit_model(path,output_dir):
    '''
    :param path:
    :param output_dir:
    :return:
    '''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    original_model = torch.load(path)
    word_2_index = original_model['word2index']

    model = common.SimpleNetWork(vocab_size=len(word_2_index), embedding_size=128, n_class=2)
    model.load_state_dict(original_model['model'])

    # 模型转换为jit模式
    common.export_script(
        model,
        (torch.randint(0,100,(4,35)),torch.randint(0,100,(4,))),
        os.path.join(output_dir,'model.pt')
    )
    torch.save(word_2_index,os.path.join(output_dir,'word2index.pkl'))


if __name__ == '__main__':
    # training()
    # to_jit_model(
    #     r'../data/output/model/model_0099.pt',
    #     r'./output-jit-model/final'
    # )
    model = torch.jit.load(r'./output-jit-model/final/model.pt')
    print(model)