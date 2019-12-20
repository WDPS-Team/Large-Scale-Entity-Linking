import matplotlib.pyplot as plt

dates = ["2019-12-11", "2019-12-12", "2019-12-13", "2019-12-14", "2019-12-15", "2019-12-16"]
p  = [0.0505, 0.0580, 0.1188, 0.2102, 0.2727, 0.2817]
r  = [0.1892, 0.1714, 0.3303, 0.3946, 0.3321, 0.3482]
f1 = [0.0798, 0.0867, 0.1748, 0.2743, 0.2995, 0.3115]

plt.plot(dates, p, label="Precision")
plt.plot(dates, r, label="Recall")
plt.plot(dates, f1, label="F1")
plt.title("Development Of Scores")
plt.xlabel("Date Of Measurement")
plt.ylabel("Value")
plt.legend(loc="upper left")
plt.show()
plt.close()
