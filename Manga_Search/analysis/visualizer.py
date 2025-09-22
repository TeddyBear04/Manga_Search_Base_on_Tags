import matplotlib.pyplot as plt

def plot_bar(data, title, xlabel, ylabel):
    data.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
