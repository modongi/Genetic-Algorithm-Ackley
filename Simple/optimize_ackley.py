"""
设计遗传算法优化阿克莱函数，求解的问题是在-32<=x1,x2<=32上求一下函数的极小值
y = -a * exp(-b*sqrt(sum1/d)) -exp(sum2/d) + a + exp(1);
"""
from GA import GA
import matplotlib.pyplot as plt

fig = plt.figure()
y_array = []
x_array = []
x1_best = None
x2_best = None

test = GA(0.3, 0.1)
test.initpopulation()
for i in range(test.generation):
    test.next_generation()
    generation, answer, score = test.get_what_we_need()
    x1_best, x2_best = answer
    print(f'迭代次数：{i}  优化值：{str(score)}')
    x_array.append(i + 1)
    y_array.append(score)
    pass

plt.plot(x_array, y_array)
print(f'最优解(x1, x2)：({x1_best}, {x2_best})')
print(f'最小值是：{test.ackleyFitnessFunc(x1_best, x2_best)}')
plt.xlabel('Generations')
plt.ylabel('Optimal Ackley Function Value')
plt.show()
