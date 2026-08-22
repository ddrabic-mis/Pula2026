import math

A=3.5
B=4.5
print("zaokruženo A:", round(A+0.0001))
print("zaokruženo B:", round(B+0.0001))
print("Zaokruženo na najbliži niži cijeli broj A:", math.floor(A))
print("Zaokruženo na najbliži niži cijeli broj B:", math.floor(B))
print("Zaokruženo na najbliži viši cijeli broj A:", math.ceil(A))
print("Zaokruženo na najbliži viši cijeli broj B:", math.ceil(B))
