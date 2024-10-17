from sampling import Sampling
import copy
import time

class ExactWeightSampling(Sampling):
    def __init__(self, db_file, popular_user_file, twitter_user_file):
        super(ExactWeightSampling, self).__init__(db_file, popular_user_file, twitter_user_file)

    def exact_weight(self, relations):
        W = []
        for i in range(len(relations) - 1, -1, -1):  # 从后向前计算
            W_dict = {}  # 存放当前关系中所有元组的权值
            if i == len(relations) - 1:
                last_tuples = self.conn.execute("SELECT source, destination FROM " + relations[i])
                for t in last_tuples:
                    W_dict[t] = 1  # 最后一个关系中的元组权重为 1
                W.append(W_dict)
            else:
                next_dict = W[0]
                dest_dict = {}
                this_tuples = self.conn.execute("SELECT source, destination FROM " + relations[i])
                dests = self.conn.execute("SELECT DISTINCT destination FROM " + relations[i])
                for dest in dests:
                    query = "select " + relations[i + 1] + ".source, " + relations[i + 1] + \
                           ".destination" + " from " + relations[i + 1] + " where " + str(dest[0]) + \
                           "=" + relations[i + 1] + ".source"
                    dest_tuples = self.conn.execute(query)  # 从下一个关系中找到所有目标为 dest 的元组
                    w = 0
                    for t in dest_tuples:
                        w += next_dict[t]
                    dest_dict[dest[0]] = w  # dest-权重 键值对
                for t in this_tuples:
                    W_dict[t] = dest_dict[t[1]]  # 根据目标的权重赋值
                W = [W_dict] + W  # 头插
        w0 = sum(W[0].values())  # 计算权值和
        W = [{self.t0: w0}] + W
        self.W = W
        return W

    def sample(self, sample_num, relations):
        if self.W is None:
            W = self.exact_weight(relations)
        else:
            W = copy.deepcopy(self.W)
        i = 0
        S = None
        start_time = time.process_time()
        while i < sample_num:
            S = self.chain_join_sample(relations, W)
            if S is not None:
                i += 1
        end_time = time.process_time()
        return end_time - start_time
