from ctypes import *
import os

tasks = [
    'task1.c',
    'task2.c',
    'task3.c',
    'task4.c',
    'task5.c',
    'task6.c',
    'task7.c',
    'task8.c',
    'task9.c',
    'task10.c',
]

for task in tasks:
    os.system("gcc -o " + task.replace(".c", ".so") + " --shared -fPIC " + task)

