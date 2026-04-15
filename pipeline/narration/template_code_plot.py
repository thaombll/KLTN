from model import gpt
from model.gpt import get_llm_response_sys
import matplotlib.pyplot as plt

def plot_bar(x, y, title="Bar Chart", xlabel="", ylabel=""):
    plt.figure()
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_trend(x, y, title="Trend Chart", xlabel="", ylabel=""):
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_scatter(x, y, title="Scatter Plot", xlabel="", ylabel=""):
    plt.figure()
    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

def plot_bubble(x, y, size, title="Bubble Chart", xlabel="", ylabel=""):
    plt.figure()
    plt.scatter(x, y, s=size)  # size controls bubble size
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

def plot_bar_line(x, bar_values, line_values, title="Bar + Line Chart", xlabel="", ylabel_bar="", ylabel_line=""):
    fig, ax1 = plt.subplots()

    ax1.bar(x, bar_values)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel_bar)

    ax2 = ax1.twinx()
    ax2.plot(x, line_values, marker='o')
    ax2.set_ylabel(ylabel_line)

    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()