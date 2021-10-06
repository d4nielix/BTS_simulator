import matplotlib.pyplot as plt
from Generator import Generator


def main():
    test = Generator()
    testplot = [test.rndzeroone(0.6) for _ in range(100000)]
    plt.hist(testplot, bins=50)
    plt.show()

if __name__ == '__main__':
    main()