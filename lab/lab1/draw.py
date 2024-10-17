import numpy as np
import matplotlib.pyplot as plt

def draw_time(times, h_num):
    fig = plt.figure(dpi=600)
    ax = fig.add_subplot(111)
    ax.plot(h_num, times)
    ax.set_xlabel('Number of Hash Functions')
    ax.set_ylabel('Running Time (s)')
    ax.set_title('Running Time vs. Number of Hash Functions')
    plt.show()


def draw_sim(sims, h_num):
    fig = plt.figure(dpi=600)
    ax = fig.add_subplot(111)
    ax.plot(h_num, sims)
    ax.set_xlabel('Number of Hash Functions')
    ax.set_ylabel('Jaccard Similarity with Naive Method')
    ax.set_title('Correctness vs. Number of Hash Functions')
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.1%}'.format(x) for x in vals])
    plt.show()
