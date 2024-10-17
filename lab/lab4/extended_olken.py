from sampling import Sampling
import copy
import time


class ExtendedSampling(Sampling):
    def __init__(self, db_file, popular_user_file, twitter_user_file):
        super(ExtendedSampling, self).__init__(db_file, popular_user_file, twitter_user_file)

    def extended_olken(self, h, popular_save_file, twitter_save_file, join_order):
        W = []
        pu_tuple, tu_tuple = self.load_frequency(popular_save_file, twitter_save_file)
        max_pu_frequency, max_tu_frequency = max(pu_tuple.values()), max(tu_tuple.values())
        t_hevy_len = 0
        p_heavy_len = 0
        t_light_len = 0
        p_light_len = 0
        t_light_frequency = h
        p_light_frequency = h
        t_cnt = self.conn.execute("SELECT source, COUNT(*) FROM Twitter_user GROUP BY source")
        p_cnt = self.conn.execute("SELECT source, COUNT(*) FROM Popular_user GROUP BY source")
        t_cnt_dict = {}
        p_cnt_dict = {}
        for r in t_cnt:
            t_cnt_dict[r[0]] = r[1]
        for r in p_cnt:
            p_cnt_dict[r[0]] = r[1]
        for k, t in tu_tuple.items():
            if t < h:
                t_light_len += t_cnt_dict[k]
            else:
                t_hevy_len += t_cnt_dict[k]
        for k, t in pu_tuple.items():
            if t < h:
                p_light_len += p_cnt_dict[k]
            else:
                p_heavy_len += p_cnt_dict[k]
        pu_frequencies = [max_pu_frequency, p_light_frequency]
        tu_frequencies = [max_tu_frequency, t_light_frequency]
        pu_table_lengths = [p_heavy_len, p_light_len]
        tu_table_lengths = [t_hevy_len, t_light_len]
        fr = self.conn.execute("SELECT COUNT(*) FROM " + join_order[0])
        first_length = None
        for result in fr:
            first_length = result[0]
        other_order = join_order[1:len(join_order)]
        w = self.combined_method(other_order, pu_frequencies,
                                 pu_table_lengths, tu_frequencies, tu_table_lengths)
        W.append({self.t0: w * first_length})
        for i in range(len(join_order) - 2):
            W_set = {}
            ts = self.conn.execute("SELECT * FROM " + join_order[i])
            other_order = join_order[i + 2:len(join_order)]
            w = self.combined_method(other_order, pu_frequencies,
                                     pu_table_lengths, tu_frequencies, tu_table_lengths)
            for j, result in enumerate(ts):
                if result[1] in t_cnt_dict:
                    first_length = t_cnt_dict[result[1]]
                else:
                    first_length = 0
                W_set[(result[0], result[1])] = w * first_length
            W.append(W_set)

        ts = self.conn.execute("SELECT * FROM " + join_order[len(join_order) - 2])
        W_set = {}
        for result in ts:
            if result[1] in t_cnt_dict:
                first_length = t_cnt_dict[result[1]]
            else:
                first_length = 0
            W_set[(result[0], result[1])] = first_length
        W.append(W_set)

        ts = self.conn.execute("SELECT * FROM " + join_order[len(join_order) - 1])
        W_set = {}
        for result in ts:
            W_set[(result[0], result[1])] = 1
        W.append(W_set)
        self.W = W
        return W

    def sample(self, sample_num, relations, h, popular_save_file, twitter_save_file):
        if self.W is None:
            W = self.extended_olken(h, popular_save_file, twitter_save_file, relations)
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

    def combined_method(self, table_names, pu_frequencies,
                        pu_table_lengths, tu_frequencies, tu_table_lengths):
        W = 0
        for i in range(2 ** len(table_names)):
            length = []
            frequency = []
            k = str(bin(i))[2:]
            if len(k) < len(table_names):
                for _ in range(len(table_names) - len(k)):
                    k = str(0) + k
            for j, table_name in enumerate(table_names):
                if table_name == "Twitter_user":
                    length.append(tu_table_lengths[int(k[j])])
                    frequency.append(tu_frequencies[int(k[j])])
                else:
                    length.append(pu_table_lengths[int(k[j])])
                    frequency.append(pu_frequencies[int(k[j])])

            ob = self.olken_bound(frequency)
            agmb = self.agm_bound(length)
            if ob > agmb:
                W = agmb
            else:
                W = ob
        return W

    @staticmethod
    def load_frequency(popular_user_file, twitter_user_file):
        pu_tuple = {}
        tu_tuple = {}
        with open(popular_user_file, "r", encoding="utf8") as f:
            for line in f:
                a, b = line.strip().split()
                pu_tuple[int(a)] = int(b)
        with open(twitter_user_file, "r", encoding="utf8") as f:
            for line in f:
                a, b = line.strip().split()
                tu_tuple[int(a)] = int(b)
        return pu_tuple, tu_tuple

    @staticmethod
    def agm_bound(lengths):
        bound = lengths[len(lengths) - 1]
        min_num = float("inf")
        if len(lengths) > 2:
            for i in range(1, len(lengths) - 1):
                if min_num > lengths[i]:
                    min_num = lengths[i]
            bound *= min_num
        return bound

    @staticmethod
    def olken_bound(frequency):
        bound = 1.
        for fre in frequency:
            bound *= fre
        return bound
