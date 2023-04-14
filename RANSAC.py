import numpy as np
import matplotlib.pyplot as plt
import csv

def ransac_line_fitting(data, n_iterations, threshold, min_inliers):
  #변수 설정
  best_fit = None
  best_error = np.inf
  best_inliers = None
  
  for i in range(n_iterations):
    #랜덤으로 샘플 불러오기
    sample = data[np.random.choice(data.shape[0], 2, replace = False), :]
    #샘플 점 2개로 그래프 그리기
    x1, y1 = sample[0]
    x2, y2 = sample[1]
    a = (y2 - y1) / (x2- x1)
    b = y1 - a* x1
    #모든 점까지 그래프와의 거리 계산
    distance = np.abs(a * data[:, 0] - data[:, 1] + b) / np.sqrt(a**2 + 1)
    #threshold(기준)이하 거리 만족하는 점 개수
    inliers = data[distance < threshold]
    #inliers 개수가 큰 것을 새로운 best_fit으로 설정
    if len(inliers) >= min_inliers:
      error = np.sum(distance**2)
      if error < best_error:
        best_fit = (a, b)
        best_error = error
        best_inliers = inliers
  return best_fit, best_inliers

#csv 파일 불러오기
f = open('RANSAC_data.csv', 'r')
rdr = csv.reader(f)
_mydata = []

#_mydata에 csv파일 float형태로 저장
for line in rdr:
  x_data = float(line[0])
  y_data = float(line[1])
  _mydata.append([x_data, y_data])
f.close()
data = np.array(_mydata)

#model, inliers에 
model, inliers = ransac_line_fitting(data, n_iterations = 100, threshold = 1, min_inliers = 10)

#matplotlib 이용해 분산형 그래프 그리고 추세선 그래프 그리기
plt.scatter(data[:, 0], data[:, 1], label = "Data")
plt.scatter(inliers[:, 0], inliers[:, 1], label = "Inliers")
x_range = np.linspace(0, 10, 100)
plt.plot(x_range, model[0] * x_range + model[1], 'r', label = "RANSAC LINE")
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
