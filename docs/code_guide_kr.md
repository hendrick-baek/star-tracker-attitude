# 코드 가이드 – Star Tracker 자세추정 시뮬레이션 프로젝트

이 문서는 프로젝트 코드 구조, 각 모듈의 개발 시점(Day), 그리고 주요 함수의 **역할 / 입력 / 출력 / 사용 목적**을 정리한 개발 가이드 문서이다.

목적은 다음과 같다.

- 프로젝트 코드 구조 이해
- 알고리즘 구현 흐름 정리
- 캡스톤 발표 및 보고서 참고 자료
- 이후 코드 확장 및 유지보수 지원

---

# 1. 프로젝트 개요

본 프로젝트는 **Star Tracker 기반 우주선 자세추정 시스템**을 시뮬레이션으로 구현하고 성능을 분석하는 것을 목표로 한다.

구현된 주요 기능은 다음과 같다.

- 3차원 회전 수학
- Quaternion 자세 표현
- Wahba 문제 해결
- Davenport q-method
- TRIAD 알고리즘
- QUEST 알고리즘
- 별 분포 시뮬레이션
- 센서 Field-of-View 모델
- 별 밝기(Magnitude) 필터링
- 측정 노이즈 모델링
- Monte Carlo 성능 분석
- 결과 시각화 그래프

---

# 2. 좌표계 및 회전 규약

본 프로젝트는 다음 회전 관계를 사용한다.

b = R r

의미

r : 관성좌표계(Inertial frame) 별 방향 벡터  
b : 위성 Body frame / 카메라 frame 벡터  
R : Inertial → Body 회전 행렬

모든 알고리즘과 함수는 이 규약을 기준으로 작성되어 있다.

---

# 3. 코드 흐름
rotations
↓
quaternion
↓
wahba
↓
triad
↓
quest
↓
star_field
↓
star_tracker_sensor
↓
star_tracker_simulator
↓
monte_carlo

Star Field 생성
        ↓
센서 모델 적용 (FOV + magnitude)
        ↓
Body frame 변환
        ↓
노이즈 추가
        ↓
vector pair 생성
        ↓
TRIAD / QUEST
        ↓
자세 추정
        ↓
오차 계산
        ↓
Monte Carlo 분석

---

# 4. 개발 진행 단계 (Day 기준)

---

# Day 1

회전 행렬 기본 검증 구현

내용

- 회전 행렬 직교성 검증
- determinant = 1 확인
- 벡터 norm 보존 확인

파일

rotations.py  
day1_rotation_check.ipynb

---

# Day 2

Axis-angle 회전 및 Rodrigues 공식 구현

파일

rotations.py

목적

일반적인 회전 생성 기능 구현

---

# Day 3

Quaternion 수학 구현

파일

quaternion.py

구현 함수

normalize(q)  
conjugate(q)  
multiply(q1,q2)  
rotate_vector(q,v)  
quat_to_rot(q)

목적

Quaternion 기반 자세 표현 및 벡터 회전 구현

---

# Day 4

Wahba 문제 해결 알고리즘 구현

파일

wahba.py

---

## build_B()

입력

b_vectors : (N,3) Body frame 벡터  
r_vectors : (N,3) Inertial frame 벡터  

출력

B : (3,3)

역할

Wahba 문제의 정렬 행렬 생성

B = Σ aᵢ bᵢ rᵢᵀ

---

## build_K()

입력

B : (3,3)

출력

K : (4,4)

역할

Davenport q-method에서 사용하는 K 행렬 생성

---

## solve_wahba()

입력

b_vectors  
r_vectors  

출력

q_opt : (4,)

역할

Wahba 문제의 최적 quaternion 계산

과정

1 B 행렬 생성  
2 K 행렬 생성  
3 eigenvalue 계산  
4 최대 eigenvalue의 eigenvector 선택  

---

## solve_wahba_rotation()

입력

b_vectors  
r_vectors  

출력

R : (3,3)

역할

Quaternion 결과를 회전행렬로 변환

내부 동작

q = solve_wahba(...)  
R = quat_to_rot(q).T

Transpose는 프로젝트 회전 규약을 맞추기 위해 필요하다.

---

# Day 5

Wahba 알고리즘 노이즈 성능 검증

파일

phase1_noise_validation.py

내용

노이즈 수준에 따른 자세추정 오차 분석

---

# Day 6

Star Tracker 센서 모델 설계

내용

- Field of View 모델
- 별 밝기 필터링
- 센서 관측 모델 정의

---

# Day 7

별 분포 생성 및 가시성 계산

파일

star_field.py

---

## random_unit_vectors()

입력

N : 별 개수

출력

(N,3) 단위 벡터

목적

구면 위에 균일 분포하는 별 방향 생성

---

## spherical_cap_fraction()

입력

FOV half angle

출력

이론적 가시 별 비율

목적

FOV 이론 검증

---

## filter_fov_body()

입력

body frame 벡터  
boresight  
FOV

출력

FOV 내부 별

목적

센서 시야 내 별 필터링

---

# Day 7 센서 모델

파일

star_tracker_sensor.py

---

## assign_magnitude_uniform()

역할

별 밝기 값 생성

---

## apply_magnitude_cut()

입력

별 방향  
밝기  
magnitude limit

출력

관측 가능한 별

목적

센서 감도 모델링

---

# Day 8

Star Tracker 측정 시뮬레이터 구현

파일

star_tracker_simulator.py

---

## simulate_star_tracker_measurements()

입력

N_total : 전체 별 개수  
R_true : 실제 자세  
fov_deg : 시야각  
m_lim : 밝기 제한  
noise_sigma : 측정 노이즈

출력

r_visible  
b_measured

동작

1 별 생성  
2 회전 적용  
3 FOV 필터  
4 magnitude 필터  
5 노이즈 추가  

---

# Day 9

전체 파이프라인 자세추정

test_day9_attitude_estimation.py

과정

star simulation  
→ Wahba 추정  
→ 자세 오차 계산

---

# Day 10

TRIAD 알고리즘 구현

파일

triad.py

---

## solve_triad()

입력

r1 r2  
b1 b2  

출력

R

역할

두 벡터를 이용한 자세추정

수식

R = T_b T_rᵀ

특징

- 계산 빠름
- 노이즈에 취약

---

# Day 11

QUEST 알고리즘 구현

파일

quest.py

---

## solve_quest()

입력

vector pairs

출력

quaternion

목적

Wahba 문제를 Newton iteration으로 해결

---

## solve_quest_rotation()

출력

rotation matrix

---

# Day 12

Monte Carlo 성능 분석

파일

monte_carlo.py  
monte_carlo_extended.py  

---

## attitude_error_deg()

역할

두 회전 행렬 사이의 각도 오차 계산

---

## run_single_trial()

역할

한 번의 Star Tracker 시뮬레이션 실행

출력

visible star 수  
TRIAD error  
QUEST error  

---

## run_monte_carlo_noise_sweep()

역할

노이즈 수준 변화에 따른 성능 분석

---

# 5. 그래프 생성 코드

plot_day12_noise_sweep.py

그래프

noise vs mean error  
noise vs std error  
noise vs visible stars  

---

plot_day12_extended.py

그래프

error histogram  
error CDF  
star count vs error  
star count vs std  

---

# 6. 실행 방법

자세추정 테스트

python src/test_day9_attitude_estimation.py

---

TRIAD 테스트

python src/test_day10_triad.py

---

QUEST 테스트

python src/test_day11_quest.py

---

Monte Carlo 실행

python src/test_day12_monte_carlo.py

---

그래프 생성

python src/plot_day12_noise_sweep.py

python src/plot_day12_extended.py

---

# 7. 프로젝트 요약

본 프로젝트는 Star Tracker 기반 자세추정 시스템을 **완전한 시뮬레이션 환경으로 구현**하였다.

구현된 주요 구성 요소

- 별 분포 시뮬레이션
- 센서 모델
- Wahba 최적 해법
- TRIAD 알고리즘
- QUEST 알고리즘
- Monte Carlo 성능 분석
- 결과 시각화

이 구조는 실제 우주선 자세결정 연구에서 사용하는 시스템 구조와 유사하다.

추후 확장 가능 연구

- EKF 자세 필터
- 센서 융합
- 자기장 기반 항법
- 실제 센서 데이터 적용
