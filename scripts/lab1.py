import numpy as np

#zadanie 1
array = np.random.randint(5, size=15)
print(array)
print(min(array))
print(max(array))
print(np.std(array))


#zadanie 2
array = np.random.rand(4,4)
print(np.sum(array, axis=0))
print(np.sum(array, axis=1))

#zadanie 3
array = np.arange(0, 25*3, 3).reshape(5,5)
print(array)
print(np.where((array % 2 == 0) & (array > 10 )))