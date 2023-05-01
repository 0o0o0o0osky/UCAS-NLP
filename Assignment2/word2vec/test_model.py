import gensim

# 加载模型
model = gensim.models.Word2Vec.load('model')

# 获取词汇测试
# words = model.wv.index_to_key
# print(words)

# 获取词向量
# print(model.wv['青年'])

# 输出最相近的10个词
most_similar = model.wv.similar_by_word('中科院')

for i in range(10):
    print(most_similar[i][0], most_similar[i][1])
