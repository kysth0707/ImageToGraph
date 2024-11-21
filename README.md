# ImageToGraph

https://www.youtube.com/watch?v=HaDNDTrHa-c
![image](https://github.com/user-attachments/assets/c9861517-73df-4d0c-b8e5-56b9e80d88f8)

convolution -> graph

왜 굳이 convolution 적용시킨 걸 그래프 화?
1. 이미지 중 벡터처럼 화질 손실 최소화 가능

- 작동방식
1. 실시간 이미지 추출
2. 기호에 맞게 그래프의 특성 선택 + 노이즈 제거량 선택
3. Convolution 으로 외곽선 추출
4. 왼쪽부터 스캔하면서 그래프의 점들 추출
5. 이미지 시각화
6. 라그랑주 보간법으로 4점씩 연결하며 표현