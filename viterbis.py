# encoding=utf-8
# """
#
# Created on Thu Feb 16 19:28:39 2017
# 2017-4-2
#     ForwardBackwardAlg函数功能：实现前向算法
#     理论依据：李航《统计学习方法》
# 2017-4-5
#     修改了ForwardBackwardAlg函数名称为ForwardAlgo以及输出的alpha数组形式
#     完成了BackwardAlgo函数功能：后向算法
#     以及函数FBAlgoAppli：计算在观测序列和模型参数确定的情况下，
#     某一个隐含状态对应相应的观测状态的概率
# 2017-4-6
#     完成BaumWelchAlgo函数一次迭代
# 2017-4-7
#     实现维特比算法
# @author: sgp
# """

import numpy as np
from collections import deque


#
# def one_word_fre(O, pinyin_list, fre, word_table_inverse):
#     x = pinyin_list[O]
#     ans = []
#     for i in x:
#         ans.append((word_table_inverse[i], fre[i]))
#     sorted(ans, key=lambda s: s[1], reverse=True)
#
#     return ans

class Node(object):
    def __init__(self, hanzi_code):
        self.hanzi_code = hanzi_code
        self.prob = 0
        self.previous = None


def viterbi_algo(params, observations):
    layers = []

    for ob in observations:

        ob = params.encode_pinyin[ob]
        hanzis_code = params.pinyin2hanzi[ob]
        tmp = []
        for hanzi_code in hanzis_code:
            tmp.append(Node(hanzi_code))
        layers.append((tmp, ob))

    if len(observations) == 1:
        x = [(params.decode_hanzi[hanzi.hanzi_code], params.hanzi_fre[hanzi.hanzi_code]) for hanzi in layers[0][0]]
        sorted(x, key=lambda s: s[1], reverse=True)
        return x

    first_layer = layers[0][0]
    for hanzi in first_layer:
        hanzi.prob = params.hanzi_fre[hanzi.hanzi_code]

    previous_layer = first_layer
    for layer in layers[1:]:
        for hanzi in layer[0]:
            for previous_hanzi in previous_layer:
                t = previous_hanzi.prob * params.trans_mat[previous_hanzi.hanzi_code, hanzi.hanzi_code]
                if t > hanzi.prob:
                    hanzi.prob = t
                    hanzi.previous = previous_hanzi
            hanzi.prob *= params.gen_mat[hanzi.hanzi_code, layer[1]]
        previous_layer = layer[0]

    x = max(layers[-1][0], key=lambda s: s.prob)
    prob = x.prob
    hanzi_seq = str("")
    while x is not None:
        hanzi_seq += params.decode_hanzi[x.hanzi_code]
        x = x.previous
    hanzi_seq = hanzi_seq[::-1]
    ans = []
    ans.append((hanzi_seq, prob))
    return ans
