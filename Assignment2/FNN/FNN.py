import torch
import torch.nn as nn
import torch.optim as optim
import collections
import matplotlib.pyplot as plt
import numpy as np
import re

# 读取处理后的汉语语料
corpus = []
lines = []
with open('../cleaned.txt', 'r', encoding='GBK') as f:
    text = f.read()
    corpus = text.split()
    lines = text.strip().split('\n')
words_set = list(collections.OrderedDict.fromkeys(corpus).keys())

vocab_size = len(words_set)
# window size
C = 2

word_to_id = {word: i for i, word in enumerate(words_set)}
id_to_word = {word_to_id[word]: word for word in word_to_id}

skip_grams = []

for line in lines:
    line_words = re.split("[ ]+", line.strip())
    for idx in range(C, len(line_words) - C):
        # center word
        center = word_to_id[line_words[idx]]
        # context word idx
        context_idx = list(range(idx - C, idx)) + list(range(idx + 1, idx + C + 1))
        context = [word_to_id[line_words[i]] for i in context_idx]
        for w in context:
            skip_grams.append([center, w])

# 定义模型
class FNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(FNN, self).__init__()
        self.embed = nn.Embedding(vocab_size, embedding_dim)
        self.linear = nn.Linear(embedding_dim, vocab_size)
        """
        self.tanh = self.Tanh()
        """
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.embed(x)
        """
        x = self.tanh(x)
        """
        x = self.linear(x)
        x = self.softmax(x)
        return x


# 定义参数
embedding_dim = 10

# 初始化
device = torch.device('cpu')
model = FNN(vocab_size, embedding_dim).to(device)
# 损失函数
criterion = nn.CrossEntropyLoss()
# 优化
optimizer = optim.Adam(model.parameters(), lr=0.003)

# 训练模型
epochs = 50
batch_size = 10000
model.train()
loss_list = []
for epoch in range(epochs):
    for batch in range(0, len(skip_grams) - batch_size, batch_size):
        input = torch.tensor(skip_grams[batch:batch + batch_size][0]).long().to(device)
        output = torch.tensor(skip_grams[batch:batch + batch_size][1]).long().to(device)
        out = model(input)
        loss = criterion(out, output)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print("epoch: %d, batch: %d" % (epoch, batch))
    loss_list.append(loss)

# 绘制训练损失的折线图
y = plt.plot([y.detach().numpy() for y in loss_list])
plt.title('Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.savefig('training_loss.jpg')


# 获取词向量
word_vectors = model.embed.weight.data.numpy()

# 保存到本地
np.savetxt('word_vectors.csv', np.array(word_vectors), delimiter=',')
