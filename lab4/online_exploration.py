from sampling import Sampling
import random
from scipy.stats import norm
import copy
import time


class OnlineExplorationSampling(Sampling):
    def __init__(self, db_file, popular_user_file, twitter_user_file):
        super(OnlineExplorationSampling, self).__init__(db_file, popular_user_file, twitter_user_file)

    def random_walk(self, random_walk_time, relations):
        walk_time = [{self.t0: random_walk_time}]
        walks = []
        records = {}
        rt = self.conn.execute("SELECT source, destination FROM Twitter_user")
        rt_tuples = []
        for result in rt:
            rt_tuples.append(result)
        rt_len = len(rt_tuples)
        records["Twitter_user"] = rt_tuples
        rp = self.conn.execute("SELECT source, destination FROM Popular_user")
        rp_tuples = []
        for result in rp:
            rp_tuples.append(result)
        rp_len = len(rp_tuples)
        records["Popular_user"] = rp_tuples
        for order in relations:
            times = {}
            for record in records[order]:
                times[record] = 0
            walk_time.append(times)
        for i in range(random_walk_time):
            walk = [self.t0]
            u = []
            for j in range(len(relations)):
                if j == 0:
                    sample = random.choice(records[relations[j]])
                    walk_time[j + 1][sample] += 1
                    walk.append(sample)
                    if relations[j] == "Twitter_user":
                        u.append(rt_len)
                    else:
                        u.append(rp_len)
                else:
                    p = "select " + relations[j] + ".source, " + relations[j] + ".destination" + " from " + \
                        relations[j] + " where " + str(walk[-1][1]) + "=" + relations[j] + ".source"
                    tt = self.conn.execute(p)
                    s = []
                    for t in tt:
                        s.append(t)
                    if len(s) == 0:
                        u.append(0)
                        break
                    sample = random.choice(s)
                    walk_time[j + 1][sample] += 1
                    walk.append(sample)
                    u.append(len(s))
            walks.append([walk, u])
        return walk_time, walks, records

    @staticmethod
    def wander_join_estimator(walks, record, i, alpha, ):
        Y = 0.
        n = 0
        sigma = 0.
        ls = []
        for walk, u in walks:
            if len(walk) < i + 2:
                continue
            if record == walk[i + 1]:
                k = 1.
                for j in range(i + 1, len(u)):
                    k *= u[j]
                Y += k
                n += 1
                ls.append(k)
        Y /= n
        for k in ls:
            sigma += (k - Y) ** 2
        sigma /= (n - 1)
        epsilon = sigma ** 0.5 * norm.ppf((alpha + 1) / 2, loc=0, scale=1) / n ** 0.5
        return Y + epsilon

    def dynamic_programming(self, W, record, join_order, i):
        p = "select " + join_order[i + 1] + ".source, " + join_order[i + 1] + ".destination" + " from " + \
            join_order[i + 1] + \
            " where " + str(record[1]) + "=" + join_order[i + 1] + ".source"
        tt = self.conn.execute(p)
        w = 0
        for result in tt:
            w += W[0][result]
        return w

    def online_exploration(self, threshold, join_order, random_walk_time, alpha):
        walk_time, walks, whole_records = self.random_walk(random_walk_time, join_order)
        W = []
        W_set = {}
        for result in whole_records[join_order[-1]]:
            W_set[result] = 1
        W.append(W_set)

        for i in range(len(join_order) - 2, -1, -1):
            W_set = {}
            wander_set = []
            pro_list = []
            pro_set = set({})
            for result in whole_records[join_order[i]]:
                if walk_time[i + 1][result] > threshold:
                    wander_set.append(result)
                else:
                    pro_list.append(result)
                    pro_set.add((-1, result[1]))
            set_num = {}
            for result in wander_set:
                W_set[result] = self.wander_join_estimator(walks, result, i, alpha)
            for result in pro_set:
                set_num[result] = self.dynamic_programming(W, result, join_order, i)
            for result in pro_list:
                W_set[result] = set_num[(-1, result[1])]
            W = [W_set] + W
        W = [{self.t0: self.wander_join_estimator(walks, self.t0, -1, alpha)}] + W
        self.W = W
        return W

    def sample(self, sample_num, join_order, threshold, random_walk_time, alpha):
        if self.W is None:
            W = self.online_exploration(threshold, join_order, random_walk_time, alpha)
        else:
            W = copy.deepcopy(self.W)
        i = 0
        S = None
        start_time = time.process_time()
        while i < sample_num:
            S = self.chain_join_sample(join_order, W)
            if S is not None:
                i += 1
        end_time = time.process_time()
        return end_time - start_time
