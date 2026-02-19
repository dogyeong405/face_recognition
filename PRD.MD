# 얼굴인식 프로그램 작성

1. Camera 연동
2. Machine Learning 이용
- Hugging face 에서 모델 찾아서 이용
3. 파이썬 언어를 활용
4. 웹 대시보드 작성까지
5. github 사용, github issues 에 문서화 마일스톤

1. frontend
- 언어와 프레임워크는 react / Vite 활용하여 만들자.
- 얼굴 인식 : 컴퓨터의 카메라를 웹 브라우저에서 접근한다.
- 얼굴 등록 : 얼굴 + 이름으로 등록한다. (한글 깨짐문제 발생)
- 등록된 사람 목록 : 등록된 사람에 사진을 2개 이상 등록 가능하도록 한다.

2. backend
*(frontend 는 겉 껍데기 라면, backend 는 실제로 기능이 돌아가게 만드는 핵심)
- 언어와 프레임워크는 python + fastAIP 활용하여 만들자.
- Deep Learning 모델 (Insightface) 라이브러리를 활용해 전달받은 사진을 판독하고, 그 결과를 frontend 에 전달 해 준다.
- 등록하는 사진 학습결과, 사람 목록을 저장하고 불러오는 등 뒤쪽에서 이뤄지는 작업을 수행한다.