from manim import *

class CreateCircle(Scene):
	def construct(self):
		t = Text('작동 방식\n\n1. Noise 제거\n2. Convolution 윤곽선 추출\n3. 그래프 점 유도')
		t.to_edge(UP)
		
		self.play(Write(t))