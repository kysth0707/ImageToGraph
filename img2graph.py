import cv2 as cv
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import time

# IMG1 = cv.imread('./testimgs/5.png')[:, :, ::-1]  # BGR -> RGB 변환

# ======================== 기본 변수


# 점 몇 칸마다 찍을 지
dotLimitByDistance = 3

# 이미지 노이즈 지울 정도
IMG_THRESHOLD = 30

# 수축 팽창 할까요?
IMG_ERODE_DILLATE = False

# 블러 처리 할까요?
DO_BLUR = False


# 3x3 필터 정의
filter_ = np.array([[-1, 0, 1],
                    [-1, 0, 1],
                    [-1, 0, 1]])

filter_2 = np.array([[1, 0, -1],
                     [1, 0, -1],
                     [1, 0, -1]])

filter_3 = np.array([[1, 1, 1],
                    [0, 0, 0],
                    [-1, -1, -1]])

filter_4 = np.array([[-1, -1, -1],
                     [0, 0, 0],
                     [1, 1, 1]])

# 5x5 필터 정의
filter_mean = np.array([[1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1]])

# 평행이동 정의
affM1 = np.array([
	[1, 0, 0],
	[0, 1, +1]
], dtype = np.float32)

affM2 = np.array([
	[1, 0, 0],
	[0, 1, -1]
], dtype = np.float32)

affM3 = np.array([
	[1, 0, +1],
	[0, 1, 0]
], dtype = np.float32)

affM4 = np.array([
	[1, 0, -1],
	[0, 1, 0]
], dtype = np.float32)

# 그래프 점을 찍을 목록들
checkLength = 2
# checkList = [(x, y) for x in range(0, (checkLength-1)*2+1) for y in range(-checkLength, checkLength+1)]
checkList = [
	(0, 1),  (1, 1),
	(0, 0),  (1, 0),
	(0, -1), (1, -1),
]
checkList.remove((0, 0))


#========================= 이미지 변환


def convertImg(img):
	# 이미지 읽기
	gray_image = cv.cvtColor(img, cv.COLOR_RGB2GRAY)  # 흑백 이미지로 변환

	if DO_BLUR:
		gray_image = convolve2d(gray_image, filter_mean, mode='valid', boundary='fill', fillvalue=0) # 블러 처리

	# 각각의 필터로 컨볼루션 수행
	output1 = convolve2d(gray_image, filter_, mode='valid', boundary='fill', fillvalue=0)
	output2 = convolve2d(gray_image, filter_2, mode='valid', boundary='fill', fillvalue=0)
	output3 = convolve2d(gray_image, filter_3, mode='valid', boundary='fill', fillvalue=0)
	output4 = convolve2d(gray_image, filter_4, mode='valid', boundary='fill', fillvalue=0)

	# 절댓값을 더해 엣지 강도 계산
	output = np.abs(output1) + np.abs(output2) + np.abs(output3) + np.abs(output4)
	normalized_output = cv.normalize(output, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
	_, binary_output = cv.threshold(normalized_output, IMG_THRESHOLD, 1, cv.THRESH_BINARY)

	if IMG_ERODE_DILLATE:
		# 수축하고 팽창해서 더러운 점들 없애기
		kernel = np.ones((2, 2), np.uint8)

		changedImg1 = cv.erode(binary_output, kernel, iterations=1)
		changedImg2 = cv.dilate(changedImg1, kernel, iterations=1)
	else:
		changedImg2 = binary_output

	# 윤곽선 1픽셀을 남기기 위한 작업
	imgShape = (changedImg2.shape[1], changedImg2.shape[0])

	changedImg3 = cv.warpAffine(changedImg2, affM1, imgShape) + cv.warpAffine(changedImg2, affM2, imgShape) + cv.warpAffine(changedImg2, affM3, imgShape) + cv.warpAffine(changedImg2, affM4, imgShape)
	changedImg3 = np.where(changedImg3 > 0, 1, 0) - changedImg2

	# 점들 가져오기
	dotListY, dotListX = np.where(changedImg3 == 1)

	# 점들로 변환
	dotsDict = {k : True for k in sorted([(x, y) for x, y in zip(dotListX, dotListY)], key = lambda x : x[0])}

	allGraphDots = []

	while True:
		if len(dotsDict) == 0:
			break

		# dotsDict의 첫 데이터 고름
		dotX, dotY = next(iter(dotsDict))
		dotVector = (0, 0)

		dotPoses = [(dotX, dotY)]
		del dotsDict[(dotX, dotY)]

		addDot = 0
		while True:
			possibleNextPlus = [(xx, yy) for xx, yy in checkList if dotsDict.get((dotX + xx, dotY + yy))]
			# print(tmp)
			if len(possibleNextPlus) == 0:
				dotPoses.append((dotX, dotY))
				break
			
			# 여기서 다음 칸 고르기
			nextPlusPos = possibleNextPlus[0]

			dotX += nextPlusPos[0]
			dotY += nextPlusPos[1]

			del dotsDict[(dotX, dotY)]
			# dotsDict.pop((dotX, dotY))

			addDot += 1
			if addDot > dotLimitByDistance:
				dotPoses.append((dotX, dotY))
				addDot = 0
		
		if len(dotPoses) > 2:
			allGraphDots.append(dotPoses)

	AllDatas = []
	for data in allGraphDots:
		# graphX = []
		# graphY = []
		# for x, y in data:
		# 	graphX.append(x)
		# 	graphY.append(-y)
			# print(x, y)
		# break
		AllDatas.append(data)#(graphX, graphY))

	return AllDatas