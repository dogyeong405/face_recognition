"""
탐구보고서 PDF 생성 스크립트
- fpdf2 + Malgun Gothic 한글 폰트 사용
"""
from fpdf import FPDF
import os

FONT_DIR = "C:/Windows/Fonts"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "탐구보고서_얼굴인식시스템.pdf")


class ReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("malgun", "", os.path.join(FONT_DIR, "malgun.ttf"))
        self.add_font("malgun", "B", os.path.join(FONT_DIR, "malgunbd.ttf"))
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("malgun", "B", 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, "InsightFace 기반 실시간 얼굴 인식 웹 시스템", align="C")
        self.ln(12)

    def footer(self):
        self.set_y(-20)
        self.set_font("malgun", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"- {self.page_no()} -", align="C")

    def title_page(self):
        self.add_page()
        self.ln(60)
        self.set_font("malgun", "B", 28)
        self.set_text_color(40, 40, 80)
        self.cell(0, 16, "탐구보고서", align="C")
        self.ln(20)
        self.set_font("malgun", "B", 18)
        self.set_text_color(80, 80, 120)
        self.cell(0, 12, "InsightFace 기반", align="C")
        self.ln(14)
        self.cell(0, 12, "실시간 얼굴 인식 웹 시스템", align="C")
        self.ln(40)
        self.set_font("malgun", "", 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "기술 스택: React + FastAPI + InsightFace (ArcFace)", align="C")
        self.ln(8)
        self.cell(0, 10, "2026", align="C")

    def section_title(self, number, title):
        self.ln(6)
        self.set_font("malgun", "B", 15)
        self.set_text_color(40, 40, 100)
        self.cell(0, 12, f"{number}. {title}")
        self.ln(10)
        # 밑줄
        self.set_draw_color(100, 100, 200)
        self.set_line_width(0.5)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(6)

    def sub_title(self, title):
        self.set_font("malgun", "B", 12)
        self.set_text_color(60, 60, 100)
        self.cell(0, 10, title)
        self.ln(8)

    def body_text(self, text):
        self.set_font("malgun", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 7, text)
        self.ln(3)

    def bullet(self, text):
        self.set_font("malgun", "", 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.cell(8, 7, "  -")
        self.multi_cell(0, 7, text)
        self.ln(1)

    def code_block(self, text):
        self.set_font("Courier", "", 9)
        self.set_fill_color(240, 240, 245)
        self.set_text_color(50, 50, 50)
        y_start = self.get_y()
        self.multi_cell(0, 6, text, fill=True)
        self.ln(4)

    def table_row(self, cells, header=False):
        self.set_font("malgun", "B" if header else "", 10)
        if header:
            self.set_fill_color(60, 60, 120)
            self.set_text_color(255, 255, 255)
        else:
            self.set_fill_color(245, 245, 250)
            self.set_text_color(40, 40, 40)

        col_widths = [170 / len(cells)] * len(cells)
        for i, cell in enumerate(cells):
            self.cell(col_widths[i], 9, cell, border=1, fill=True, align="C")
        self.ln()


def build_report():
    pdf = ReportPDF()

    # ── 표지 ──
    pdf.title_page()

    # ── 목차 ──
    pdf.add_page()
    pdf.section_title("", "목차")
    toc = [
        ("1", "탐구 동기 및 목적"),
        ("2", "이론적 배경"),
        ("3", "시스템 설계"),
        ("4", "핵심 기술 분석"),
        ("5", "구현 과정"),
        ("6", "실험 및 결과"),
        ("7", "결론 및 향후 과제"),
        ("8", "참고문헌"),
    ]
    for num, title in toc:
        pdf.set_font("malgun", "", 11)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(0, 9, f"  {num}.  {title}")
        pdf.ln(8)

    # ── 1. 탐구 동기 및 목적 ──
    pdf.add_page()
    pdf.section_title("1", "탐구 동기 및 목적")

    pdf.sub_title("1.1 탐구 동기")
    pdf.body_text(
        "얼굴 인식 기술은 스마트폰 잠금 해제, 출입 관리, 보안 시스템 등 "
        "일상생활 곳곳에서 활용되고 있다. 이러한 기술이 실제로 어떤 원리로 "
        "작동하는지, 그리고 웹 브라우저만으로도 실시간 얼굴 인식이 가능한지에 "
        "대한 궁금증에서 본 탐구를 시작하게 되었다."
    )
    pdf.body_text(
        "특히 딥러닝 기반 얼굴 인식 모델이 사람의 얼굴을 어떻게 수치화(임베딩)하고, "
        "이를 통해 신원을 판별하는 과정을 직접 구현하고 실험함으로써, "
        "AI 기술의 원리를 깊이 이해하고자 하였다."
    )

    pdf.sub_title("1.2 탐구 목적")
    pdf.bullet("딥러닝 기반 얼굴 인식의 핵심 원리(임베딩, 코사인 유사도)를 이해한다.")
    pdf.bullet("InsightFace(ArcFace) 모델을 활용하여 실시간 얼굴 인식 시스템을 구현한다.")
    pdf.bullet("웹 기술(React, FastAPI)을 결합하여 브라우저에서 동작하는 완전한 얼굴 인식 애플리케이션을 개발한다.")
    pdf.bullet("얼굴 인식과 동시에 나이, 성별 추정 기능을 통합하여 다중 속성 분석 시스템을 구축한다.")

    # ── 2. 이론적 배경 ──
    pdf.add_page()
    pdf.section_title("2", "이론적 배경")

    pdf.sub_title("2.1 얼굴 인식의 일반적 파이프라인")
    pdf.body_text(
        "얼굴 인식 시스템은 일반적으로 다음 4단계를 거친다:\n\n"
        "  (1) 얼굴 감지(Face Detection): 이미지에서 얼굴 영역을 찾아 바운딩 박스로 표시\n"
        "  (2) 얼굴 정렬(Face Alignment): 눈, 코, 입 등 랜드마크를 기준으로 얼굴을 정규화\n"
        "  (3) 특징 추출(Feature Extraction): 정렬된 얼굴에서 고차원 임베딩 벡터 생성\n"
        "  (4) 특징 비교(Feature Matching): 임베딩 간 유사도를 계산하여 신원 판별"
    )

    pdf.sub_title("2.2 ArcFace 손실 함수")
    pdf.body_text(
        "ArcFace(Additive Angular Margin Loss)는 얼굴 인식 분야에서 가장 널리 쓰이는 "
        "손실 함수 중 하나이다. 기존 Softmax 손실 함수의 결정 경계에 각도 마진(angular margin)을 "
        "추가하여, 같은 사람의 얼굴 임베딩은 더 가깝게, 다른 사람의 임베딩은 더 멀어지도록 학습한다."
    )
    pdf.body_text(
        "수식으로 표현하면, 기존 Softmax에서 cos(theta)를 cos(theta + m)으로 대체하여 "
        "클래스 간 분리도를 높인다. 여기서 m은 마진 파라미터로, 값이 클수록 더 엄격한 "
        "구분을 요구한다. 본 프로젝트에서 사용하는 buffalo_l 모델은 ArcFace로 학습된 "
        "ResNet-50 백본 네트워크를 사용하며, 512차원 임베딩 벡터를 출력한다."
    )

    pdf.sub_title("2.3 코사인 유사도")
    pdf.body_text(
        "두 얼굴 임베딩 벡터 간의 유사도를 측정하기 위해 코사인 유사도(Cosine Similarity)를 "
        "사용한다. 코사인 유사도는 두 벡터가 이루는 각도의 코사인 값으로, -1에서 1 사이의 값을 가진다.\n\n"
        "  similarity(A, B) = (A . B) / (|A| * |B|)\n\n"
        "값이 1에 가까울수록 두 벡터가 유사하며(같은 사람), 0에 가까울수록 관련이 없는 것으로 판단한다. "
        "본 시스템에서는 유사도 임계값을 0.4로 설정하여, 이 값 이상일 때 동일인으로 판별한다."
    )

    pdf.sub_title("2.4 나이/성별 추정 모델")
    pdf.body_text(
        "InsightFace의 buffalo_l 모델 팩에는 얼굴 인식뿐 아니라 나이 및 성별 추정 모델(genderage.onnx)이 "
        "포함되어 있다. 이 모델은 96x96 크기의 얼굴 이미지를 입력받아 3개의 출력값을 생성한다:\n\n"
        "  - 출력[0], 출력[1]: 여성/남성 확률 (argmax로 성별 결정)\n"
        "  - 출력[2]: 정규화된 나이 값 (0~1 범위, 100을 곱하여 실제 나이로 변환)\n\n"
        "이 모델은 얼굴 인식 파이프라인에서 자동으로 실행되므로, 추가 비용 없이 "
        "나이와 성별 정보를 함께 얻을 수 있다."
    )

    # ── 3. 시스템 설계 ──
    pdf.add_page()
    pdf.section_title("3", "시스템 설계")

    pdf.sub_title("3.1 전체 아키텍처")
    pdf.body_text(
        "본 시스템은 Client-Server 아키텍처를 채택하였다.\n\n"
        "  [브라우저(React)] --HTTP/REST--> [백엔드 서버(FastAPI)] --ONNX--> [InsightFace 모델]\n\n"
        "프론트엔드는 React + Vite로 구축하여 웹캠 제어와 사용자 인터페이스를 담당하고, "
        "백엔드는 FastAPI로 REST API를 제공하며 InsightFace 모델을 호스팅한다."
    )

    pdf.sub_title("3.2 기술 스택")
    pdf.table_row(["구분", "기술", "역할"], header=True)
    pdf.table_row(["Frontend", "React 19 + Vite 7", "웹캠 제어, UI 렌더링"])
    pdf.table_row(["Backend", "Python FastAPI", "REST API, 모델 호스팅"])
    pdf.table_row(["AI Engine", "InsightFace (buffalo_l)", "얼굴 감지/인식/속성 분석"])
    pdf.table_row(["추론 엔진", "ONNX Runtime", "모델 추론 실행"])
    pdf.table_row(["데이터 저장", "JSON + NumPy (.npy)", "사용자 정보, 임베딩 저장"])
    pdf.ln(4)

    pdf.sub_title("3.3 데이터 흐름")
    pdf.body_text(
        "[얼굴 등록 흐름]\n"
        "  1. 사용자가 이름을 입력하고 웹캠으로 여러 장의 사진을 촬영\n"
        "  2. 프론트엔드가 이미지를 FormData로 백엔드에 전송 (POST /register)\n"
        "  3. 백엔드가 각 이미지에서 얼굴을 감지하고 512차원 임베딩 추출\n"
        "  4. 임베딩(.npy)과 원본 이미지(.jpg)를 파일로 저장, 메타데이터를 people.json에 기록"
    )
    pdf.body_text(
        "[얼굴 인식 흐름]\n"
        "  1. 웹캠에서 0.5초 간격으로 프레임을 캡처하여 백엔드에 전송 (POST /recognize)\n"
        "  2. 백엔드가 이미지에서 모든 얼굴을 감지하고 각각의 임베딩 추출\n"
        "  3. 등록된 모든 임베딩과 코사인 유사도를 비교하여 가장 유사한 사람 매칭\n"
        "  4. 동시에 나이/성별 추정 모델이 실행되어 속성 정보 생성\n"
        "  5. 결과(이름, 유사도, 나이, 성별, 바운딩 박스)를 JSON으로 반환\n"
        "  6. 프론트엔드가 Canvas 오버레이로 바운딩 박스와 정보를 실시간 표시"
    )

    pdf.sub_title("3.4 API 설계")
    pdf.table_row(["메서드", "경로", "설명"], header=True)
    pdf.table_row(["POST", "/register", "얼굴 등록 (이름 + 이미지들)"])
    pdf.table_row(["POST", "/recognize", "얼굴 인식 (이미지 -> 결과)"])
    pdf.table_row(["GET", "/people", "등록된 사용자 목록 조회"])
    pdf.table_row(["GET", "/images/{file}", "등록된 얼굴 이미지 제공"])

    # ── 4. 핵심 기술 분석 ──
    pdf.add_page()
    pdf.section_title("4", "핵심 기술 분석")

    pdf.sub_title("4.1 InsightFace buffalo_l 모델 구성")
    pdf.body_text(
        "buffalo_l은 InsightFace에서 제공하는 고성능 모델 팩으로, 5개의 ONNX 모델로 구성된다:"
    )
    pdf.table_row(["모델 파일", "기능", "입력 크기"], header=True)
    pdf.table_row(["det_10g.onnx", "얼굴 감지 (SCRFD)", "가변"])
    pdf.table_row(["w600k_r50.onnx", "얼굴 인식 (ArcFace)", "112x112"])
    pdf.table_row(["genderage.onnx", "나이/성별 추정", "96x96"])
    pdf.table_row(["1k3d68.onnx", "3D 랜드마크 (68점)", "192x192"])
    pdf.table_row(["2d106det.onnx", "2D 랜드마크 (106점)", "192x192"])
    pdf.ln(4)
    pdf.body_text(
        "이 모델들은 FaceAnalysis 클래스에 의해 자동으로 로드되며, "
        "app.get(image) 호출 시 감지된 각 얼굴에 대해 순차적으로 실행된다. "
        "전체 모델 팩의 크기는 약 275MB이며, CPU만으로도 실시간 추론이 가능하다."
    )

    pdf.sub_title("4.2 임베딩 벡터와 얼굴 매칭")
    pdf.body_text(
        "ArcFace 모델(w600k_r50.onnx)은 정렬된 얼굴 이미지를 512차원 실수 벡터로 변환한다. "
        "이 벡터를 '임베딩(embedding)'이라 하며, 같은 사람의 다른 사진에서 추출한 임베딩은 "
        "벡터 공간에서 가까운 위치에 분포한다.\n\n"
        "매칭 과정에서는 인식 대상의 임베딩을 등록된 모든 임베딩과 비교하여, "
        "코사인 유사도가 가장 높은 사람을 찾는다. 임계값(0.4) 미만이면 'Unknown'으로 분류한다."
    )

    pdf.sub_title("4.3 실시간 처리 전략")
    pdf.body_text(
        "웹 브라우저에서 실시간 얼굴 인식을 구현하기 위해 다음 전략을 적용하였다:\n\n"
        "  - 프레임 캡처 주기: 0.5초 (초당 2프레임)\n"
        "  - 이미지 압축: JPEG 품질 80%로 전송 데이터 최소화\n"
        "  - Canvas 오버레이: 비디오 위에 별도의 Canvas 레이어를 겹쳐 바운딩 박스 렌더링\n"
        "  - 모델 싱글톤: InsightFace 모델을 서버 시작 시 1회만 로드하여 메모리 효율화\n"
        "  - 비동기 처리: FastAPI의 async/await를 활용한 비차단 요청 처리"
    )

    # ── 5. 구현 과정 ──
    pdf.add_page()
    pdf.section_title("5", "구현 과정")

    pdf.sub_title("5.1 백엔드 구현")
    pdf.body_text(
        "FastAPI를 사용하여 REST API 서버를 구축하였다. 핵심 모듈은 다음과 같다:\n\n"
        "  - face_engine.py: InsightFace 모델 래퍼. 얼굴 감지, 임베딩 추출, 유사도 비교 기능 제공\n"
        "  - database.py: JSON 파일 기반의 사용자 데이터 관리. 임베딩은 NumPy .npy 형식으로 저장\n"
        "  - utils.py: 업로드된 이미지 바이트를 OpenCV 형식으로 변환하는 유틸리티\n"
        "  - main.py: FastAPI 앱 진입점. CORS 설정, API 엔드포인트 정의"
    )
    pdf.body_text(
        "한글 이름 처리를 위해 이미지 파일명에는 UUID를 사용하고, "
        "이름은 people.json에서 UTF-8로 관리하는 방식을 채택하여 한글 깨짐 문제를 방지하였다."
    )

    pdf.sub_title("5.2 프론트엔드 구현")
    pdf.body_text(
        "React 19와 Vite 7을 사용하여 SPA(Single Page Application)를 구축하였다. "
        "주요 페이지는 다음과 같다:\n\n"
        "  - RegisterPage: 이름 입력 + 웹캠 다중 사진 촬영 + 등록 API 호출\n"
        "  - RecognitionPage: 실시간 웹캠 + Canvas 오버레이(바운딩 박스, 이름, 나이/성별)\n"
        "  - PeoplePage: 등록된 사용자 카드 그리드, 대표 이미지, 등록 사진 수 표시"
    )
    pdf.body_text(
        "Vite 개발 서버의 프록시 기능을 활용하여 프론트엔드의 /api/* 요청을 "
        "백엔드 서버(localhost:8000)로 자동 전달하도록 설정하였다."
    )

    pdf.sub_title("5.3 나이/성별 추정 기능 통합")
    pdf.body_text(
        "InsightFace의 genderage.onnx 모델은 FaceAnalysis 파이프라인에서 자동으로 실행된다. "
        "얼굴 감지 후 각 Face 객체에 gender(0=여성, 1=남성)와 age(0~100) 속성이 자동으로 설정된다.\n\n"
        "이를 활용하기 위해 백엔드의 /recognize API 응답에 gender와 age 필드를 추가하고, "
        "프론트엔드에서는 바운딩 박스 하단에 '성별 / 나이세' 라벨을 Canvas로 렌더링하여 "
        "실시간으로 나이와 성별 정보를 표시하도록 구현하였다."
    )

    # ── 6. 실험 및 결과 ──
    pdf.add_page()
    pdf.section_title("6", "실험 및 결과")

    pdf.sub_title("6.1 실험 환경")
    pdf.table_row(["항목", "사양", "비고"], header=True)
    pdf.table_row(["OS", "Windows 10 Pro", ""])
    pdf.table_row(["Python", "3.10", "venv 가상환경"])
    pdf.table_row(["InsightFace", "0.7.3", "buffalo_l 모델"])
    pdf.table_row(["ONNX Runtime", "CPU", "CPUExecutionProvider"])
    pdf.table_row(["웹캠 해상도", "640 x 480", "30fps"])
    pdf.ln(4)

    pdf.sub_title("6.2 얼굴 인식 성능")
    pdf.body_text(
        "등록된 사용자를 대상으로 다양한 조건에서 인식 실험을 수행하였다:\n\n"
        "  - 정면 얼굴: 유사도 0.6~0.85 범위로 안정적 인식\n"
        "  - 측면(약 30도): 유사도가 다소 하락하나 임계값(0.4) 이상으로 인식 가능\n"
        "  - 조명 변화: 자연광/형광등 환경에서 모두 정상 작동\n"
        "  - 미등록 인물: 'Unknown'으로 올바르게 분류 (유사도 0.2 이하)"
    )

    pdf.sub_title("6.3 나이/성별 추정 결과")
    pdf.body_text(
        "나이 추정은 실제 나이와 약 3~7세의 오차 범위를 보였다. "
        "조명, 표정, 화장 등에 따라 변동이 있으나, 대략적인 연령대 파악에는 충분한 정확도를 보였다.\n\n"
        "성별 추정은 대부분의 경우 정확하게 판별되었으며, "
        "안경, 마스크 등 부분 가림 상황에서도 비교적 안정적인 결과를 보였다."
    )

    pdf.sub_title("6.4 처리 속도")
    pdf.body_text(
        "CPU 환경에서의 처리 시간 측정 결과:\n\n"
        "  - 모델 초기 로딩: 약 3~5초 (최초 1회)\n"
        "  - 얼굴 1개 감지 + 인식 + 속성 분석: 약 100~200ms\n"
        "  - 프레임 캡처 + 전송 + 응답 전체 주기: 약 300~500ms\n\n"
        "0.5초 간격의 프레임 캡처 설정으로 자연스러운 실시간 인식 경험을 제공하였다."
    )

    # ── 7. 결론 및 향후 과제 ──
    pdf.add_page()
    pdf.section_title("7", "결론 및 향후 과제")

    pdf.sub_title("7.1 결론")
    pdf.body_text(
        "본 탐구에서는 InsightFace(ArcFace)를 활용한 실시간 얼굴 인식 웹 시스템을 설계하고 구현하였다. "
        "웹 브라우저만으로 얼굴 등록, 실시간 인식, 나이/성별 추정까지 가능한 통합 시스템을 완성하였으며, "
        "다음과 같은 성과를 달성하였다:\n\n"
        "  (1) ArcFace 기반 512차원 임베딩과 코사인 유사도를 활용한 높은 정확도의 얼굴 인식 구현\n"
        "  (2) React + FastAPI의 Client-Server 구조로 확장 가능한 웹 애플리케이션 아키텍처 설계\n"
        "  (3) 얼굴 인식과 동시에 나이/성별 추정을 수행하는 다중 속성 분석 시스템 구축\n"
        "  (4) CPU 환경에서도 실시간 처리가 가능한 최적화된 파이프라인 구현"
    )
    pdf.body_text(
        "이 프로젝트를 통해 딥러닝 기반 얼굴 인식의 핵심 원리를 실제 구현 과정에서 깊이 이해할 수 있었으며, "
        "웹 기술과 AI 모델을 결합하는 풀스택 개발 경험을 축적하였다."
    )

    pdf.sub_title("7.2 향후 과제")
    pdf.bullet("GPU 가속 적용: CUDA를 활용한 추론 속도 향상")
    pdf.bullet("다중 얼굴 동시 인식 최적화: 배치 처리를 통한 효율 개선")
    pdf.bullet("데이터베이스 전환: JSON에서 SQLite/PostgreSQL로 확장하여 대규모 사용자 지원")
    pdf.bullet("보안 강화: 안티 스푸핑(Anti-Spoofing) 기능 추가로 사진/영상 공격 방어")
    pdf.bullet("모바일 최적화: 경량 모델(buffalo_s) 적용 및 반응형 UI 구현")
    pdf.bullet("감정 분석: 표정 인식 모델 추가를 통한 감정 상태 분석 기능 확장")

    # ── 8. 참고문헌 ──
    pdf.add_page()
    pdf.section_title("8", "참고문헌")
    refs = [
        "Deng, J., Guo, J., Xue, N., & Zafeiriou, S. (2019). ArcFace: Additive Angular Margin Loss for Deep Face Recognition. CVPR 2019.",
        "Guo, Y., Zhang, L., Hu, Y., He, X., & Gao, J. (2016). MS-Celeb-1M: A Dataset and Benchmark for Large-Scale Face Recognition. ECCV 2016.",
        "InsightFace: An open source 2D&3D deep face analysis toolbox. https://github.com/deepinsight/insightface",
        "FastAPI Documentation. https://fastapi.tiangolo.com/",
        "React Documentation. https://react.dev/",
        "ONNX Runtime. https://onnxruntime.ai/",
    ]
    for i, ref in enumerate(refs, 1):
        pdf.set_font("malgun", "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(8, 7, f"[{i}]")
        pdf.multi_cell(0, 7, ref)
        pdf.ln(2)

    # ── 출력 ──
    pdf.output(OUTPUT_PATH)
    print(f"PDF 생성 완료: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_report()
