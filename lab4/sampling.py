import sqlite3
import numpy as np
import os


class Sampling:
    def __init__(self, db_file, popular_user_file, twitter_user_file):
        self.t0 = (-1, -1)  # 起始虚拟元组
        self.conn = sqlite3.connect(db_file)
        self.W = None

    def chain_join_sample(self, relations, W):
        t = self.t0
        S = {self.t0}
        for i in range(len(relations)):
            wt = W[i][t]
            if i == 0:
                p = "select " + relations[i] + ".source, " + relations[i] + ".destination" + " from " + relations[i]
                tRi = self.conn.execute(p)
                tRI = self.conn.execute(p)
                WtRi = 0
                for result in tRi:
                    WtRi += W[i + 1][result]
            else:
                p = "select " + relations[i] + ".source, " + relations[i] + ".destination" + " from " + relations[i] + \
                    " where " + str(t[1]) + "=" + relations[i] + ".source"
                tRi = self.conn.execute(p)
                tRI = self.conn.execute(p)
                WtRi = 0
                for result in tRi:
                    WtRi += W[i + 1][result]

            W[i][t] = WtRi
            if wt != 0:
                reject_prob = 1 - WtRi / wt
            else:
                reject_prob = 0
            if np.random.rand() <= min(reject_prob, 0.5):
                return None
            num = np.random.rand()
            p = 0.
            sample = None
            for result in tRI:
                if WtRi != 0:
                    p += W[i + 1][result] / WtRi
                else:
                    p = 1
                if num < p:
                    sample = result
                    t = result
                    break
            if sample is not None:
                S.add(sample)
        return S
