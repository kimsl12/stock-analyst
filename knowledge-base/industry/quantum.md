---
updated: 2026-04-19
valid_until: 2026-05-19
category: industry
sub_category: science_tech
topic: quantum
sub_sectors:
  - 양자컴퓨팅
  - 양자통신
  - PQC(포스트양자암호)
  - 양자센서
sources:
  - NIST (FIPS 203/204/205, IR 8547, CNSA 2.0)
  - IBM Quantum Roadmap (Nighthawk/Kookaburra/Loon)
  - Google Quantum AI (Willow)
  - IonQ IR (FY2025 실적, FY2026 가이던스)
  - Quantinuum (Helios, IPO S-1)
  - QuEra Computing (Nature 2025, $230M 투자)
  - PsiQuantum ($1B+ Series E, 시카고+브리즈번)
  - D-Wave (QCI 인수, FY2025 $24.6M)
  - Rigetti (C-DAC 108큐빗, Novera)
  - PASQAL (SPAC $2B)
  - Infleqtion (INFQ, 2026.02 NYSE 상장)
  - NVIDIA Ising (양자 AI 모델, 2026.04.14)
  - Meta Engineering (PQC 마이그레이션 2026.04.16)
  - MarketsandMarkets, Grand View Research, Precedence Research, BCC Research, Fortune BI
  - GM Insights, IDTechEx (양자센서)
  - SpinQ, QuantumBasel (VC 투자 집계)
  - McKinsey, Gartner, Global Risk Institute
  - 과기정통부 양자과학기술 종합계획 (2026.01.29)
  - 전자신문, 이코노미사이언스
  - Riverlane, Iceberg Quantum, Nature, IEEE Spectrum, phys.org
  - ESA (Eagle-1 EuroQCI), Qubitrium (QubitCore CubeSat)
  - Palo Alto Networks, Cloudflare, SandboxAQ
confidence: high
last_synced_from_db: 2026-04-19
---

# Quantum Technology Knowledge Base

## CURRENT (2026-04-19)

---

### 1. 시장 규모 & 성장률

| 지표 | 수치 | 출처 |
|---|---|---|
| 글로벌 양자컴퓨팅 시장 2025 | $1.44B ~ $3.52B (정의 범위에 따른 편차) | [Precedence Research / MarketsandMarkets] |
| 글로벌 양자컴퓨팅 시장 2026E | $1.88B ~ $2.7B (Fortune BI $2.04B) | [Precedence / Fortune BI / MarketsandMarkets] |
| 양자컴퓨팅 소프트웨어 시장 2026E | $0.78B -> 2030E $1.68B (CAGR 21.2%) | [Research and Markets] |
| 글로벌 양자컴퓨팅 시장 2030E | $4.24B ~ $20.2B (CAGR 20.5~41.8%) | [Grand View / BCC $7.3B / TBRC $16.27B / M&M $20.2B] |
| 양자센서 시장 2025 | $860M | [GM Insights] |
| 양자센서 시장 2026E | $984M (+14.4% YoY) | [GM Insights] |
| 양자센서 시장 2032E | $2.28B (CAGR 14.99%) | [GM Insights / IDTechEx] |
| 양자 경제적 파급효과 2035E | $1T (총 경제적 임팩트) | [The Quantum Insider] |

**주의**: 양자컴퓨팅 시장 규모 추정치는 하드웨어/소프트웨어/서비스/컨설팅 포함 범위에 따라 최대 5배 차이. 중위 추정 $7~10B(2030)이 합리적.

---

### 2. 투자 & 펀딩

| 지표 | 수치 | 출처 |
|---|---|---|
| 글로벌 VC 투자 2025 (3Q 누적) | $3.77B (Q1만 $1.25B, 전년 Q1 대비 2배+) | [SpinQ / QuantumBasel] |
| 정부 투자 2025 (공시 누적) | $10B+ (일본 $7.4B, 스페인 $900M, 호주 $620M, 싱가포르 $222M) | [Qureca / SpinQ] |
| 중국 양자 누적 정부 투자 | $10B+ (국가양자정보과학연구소 단독) | [SpinQ / postquantum.com] |
| 한국 양자 투자 계획 (2035까지) | 3조원+ (민관 합동) | [과기정통부 종합계획 2026.01.29] |
| 한국 현재 정부 투자 진행 중 | 1,980억원 | [과기정통부] |
| 한국 양자산업펀드 | 2026년 본격 조성 | [과기정통부] |

---

### 3. 주요 기업 & 기술 현황

#### 3-1. 초전도 방식

| 기업 | 2026 현황 | 핵심 지표 |
|---|---|---|
| **IBM** | Kookaburra(2026): qLDPC 메모리+LPU 최초 통합 모듈. Nighthawk 양자우위 연말 목표 | 7,500 게이트/2026말, 2029 fault-tolerant 목표. Qiskit 1,300만 다운로드(개발자 선호 69%) [IBM Quantum] |
| **Google** | Willow 칩(2024.12) below-threshold 양자오류억제 최초 실증 | 105큐빗, 99.88% 2-qubit gate fidelity, surface code 1 논리큐빗 [Google Quantum AI] |
| **Rigetti** | C-DAC(인도) $8.4M 108큐빗 시스템 주문(H2 2026), Novera $5.7M Q1 출하 | FY2025 매출 $7.09M(-34% YoY), 주가 ~$17(1Y +111%). 99.9% 2-qubit gate fidelity [Rigetti / 24/7 Wall St] |

#### 3-2. 이온트랩 방식

| 기업 | 2026 현황 | 핵심 지표 |
|---|---|---|
| **IonQ** | FY2026 가이던스: 매출 $225~245M (중위 $235M, +81% YoY) | FY2025 $130M(+202%), Q4 $61.9M(+429%), RPO $370M. Q1 2026 가이던스 $48~51M. 주가 $35~40, 목표가 $67.67(+140%). Q1 실적 5/6 발표 [IonQ IR] |
| **Quantinuum** | Helios 상용 출시, IPO S-1 비공개 제출 | 98 all-to-all connected 물리큐빗에서 48논리큐빗(2:1 효율, 업계 최고). H2: QV 2^25(3,350만). $10B IPO, $20B+ 목표. 2026 후반 상장 예상 [Quantinuum / Bloomberg] |

#### 3-3. 중성원자 방식

| 기업 | 2026 현황 | 핵심 지표 |
|---|---|---|
| **QuEra** | 100논리큐빗 + 10,000+물리큐빗 (3세대) | $230M 투자(Google/NVIDIA/SoftBank). Tsim GPU 시뮬레이터(85큐빗 600ns/shot) [QuEra] |
| **PASQAL** | 10,000큐빗 시스템 도입 예정, SPAC 상장($2B) | 노벨상 Alain Aspect 창업, Fresnel 프로세서(루비듐) [PASQAL] |
| **Infleqtion** | 2026.02 NYSE 상장(INFQ) -- 중성원자 최초 IPO | 양자컴퓨팅+양자센싱 듀얼. NASA ISS 양자센싱 파트너십 [Infleqtion] |

#### 3-4. 양자어닐링

| 기업 | 2026 현황 | 핵심 지표 |
|---|---|---|
| **D-Wave** | QCI 인수($550M) 후 gate-model 2026 GA 목표 | FY2025 매출 $24.6M(+179% YoY). Q1 2026 YTD 수주 $32.8M(기록적). 현금 $884.5M. FAU $20M 계약 [D-Wave / Fast Company] |

#### 3-5. 광자 방식

| 기업 | 2026 현황 | 핵심 지표 |
|---|---|---|
| **PsiQuantum** | Series E $1B+ 유치, 시카고+브리즈번 2개 사이트 구축 | CEO Victor Peng 취임(2026.02, 전 AMD/Xilinx 사장). NVIDIA 파트너십. Airbus/Lockheed Martin 협력. 도쿄대/미쓰비시 NEDO 프로그램(20개사 80명). 밸류 ~$7B [PsiQuantum / IEEE Spectrum] |
| **Xanadu** | PennyLane 프레임워크 운영, 광자 양자컴퓨팅 | 오픈소스 QML 대표 라이브러리 [PennyLane] |

**미국 상장 양자 순수기업 6사**: IonQ(IONQ), D-Wave(QBTS), Rigetti(RGTI), Quantum Computing Inc(QUBT), Arqit(ARQQ), Infleqtion(INFQ)

---

### 4. 양자 오류보정 & Fault-Tolerant 진전

| 마일스톤 | 내용 | 출처 |
|---|---|---|
| NVIDIA Ising (2026.04.14) | 세계 최초 양자 교정+에러보정용 오픈소스 AI 모델. Ising Calibration(수일->수시간), Ising Decoding(PyMatching 대비 2.5x 빠르고 3x 정확). IonQ/IQM/Fermilab/ORNL 채택 | [NVIDIA Technical Blog] |
| IBM Kookaburra (2026) | 최초 qLDPC 메모리 + LPU 통합 양자 프로세서 모듈 | [IBM Quantum Blog] |
| 중간측정 없는 FTQC (2026.04) | 이온트랩에서 중간측정 없이 Grover 알고리즘 3 논리큐빗 실행 성공 | [phys.org] |
| 게이지 이론 QEC (2026.03) | gauge theory 기법으로 물리큐빗 수 대폭 절감 가능한 새 에러보정법 | [phys.org] |
| Google Willow below-threshold (2024.12) | 규모 확대 시 오류 기하급수 감소 최초 입증 (30년 난제) | [Google Quantum AI] |
| Quantinuum Helios 48 논리큐빗 (2025.11) | 2:1 물리-논리 큐빗 비율, break-even 초과 | [Quantinuum] |
| Iceberg Pinnacle (2026.02) | RSA-2048 해독 물리큐빗 100만에서 10만으로 10배 절감 | [Iceberg Quantum] |
| qLDPC 코드 확산 (2026) | IBM 전환(2024) 이후 타사 추종 중 | [Riverlane] |
| QEC 연구 폭증 | 2025년 120편 peer-reviewed 논문 (2024년 36편 대비 3.3배) | [Riverlane] |
| IQM Shor 2048-bit (2026.04.05) | 최초 게이트레벨 Shor 알고리즘 2048비트 키 컴파일 | [IQM / Fraunhofer FOKUS] |

**핵심 트렌드**: 개별 논리큐빗 시연에서 "1세대 FTQC 전체 시스템 구축"으로 전환. NVIDIA AI 모델 참여로 양자-AI 융합 가속.

---

### 5. PQC(포스트양자암호)

| 항목 | 내용 | 출처 |
|---|---|---|
| NIST 최종 표준 | ML-KEM(FIPS 203), ML-DSA(FIPS 204), SLH-DSA(FIPS 205) - 2024.08 최종 발표, 즉시 사용 가능 | [NIST] |
| 양자취약 알고리즘 폐기 | 2035까지 RSA/ECC 등 폐기 예정 (NIST IR 8547) | [NIST] |
| NSS 규정 준수 시한 | 2027.01 -- CNSA 2.0 국가안보시스템 PQC 전환 시한. 공급망으로 확산 | [NIST NCCoE / CNSA 2.0] |
| Meta PQC 마이그레이션 (2026.04.16) | Meta가 자사 PQC 전환 프레임워크/교훈 공개. 하이브리드 배포(ECDH+ML-KEM 병행) 사례 | [Meta Engineering Blog] |
| 기업 도입 현황 (2026) | Google Chrome ML-KEM 기본 활성화, AWS/Azure/MS PQC 구현, HSM 벤더 PQC 통합 | [Palo Alto / Cloudflare / SEALSQ] |
| PQC 인증서 | 2026년 최초 발급 예정 (기본값 아님) | [Cloudflare / HashiCorp] |
| RSA-2048 위협 시점 | 2030~2034 추정 (Gartner: 2029 unsafe / 2034 breakable) | [Gartner / GRI / RSA Blog] |
| 필요 자원 | ~4,000 논리큐빗 (각 수천 물리큐빗) | [TCG / Citi Institute] |
| Harvest Now Decrypt Later | 적대세력이 현재 암호문 수집 중 - PQC 전환 시급성의 근거 | [Citi Institute / Cisco] |

**변화 포인트**: "연구 주제"에서 "마이그레이션 계획 필수" 단계로 전환 완료 (2026). Meta 사례 공개로 대기업 PQC 전환 가속.

---

### 6. 양자통신 & 양자 인터넷

| 항목 | 내용 | 출처 |
|---|---|---|
| 중국 CN-QCN | 10,000+km / 145노드 캐리어급 양자통신 네트워크 | [postquantum.com] |
| Jinan-1 마이크로위성 | 12,900km QKD 실증 (베이징-남아공, 2025.03) | [Nature / ScienceDaily] |
| 지상->위성 양자 업링크 | 기존 다운링크만 가능하다는 인식 뒤집음 -- 더 저렴하고 실용적 글로벌 양자네트워크 가능 | [ScienceDaily 2025.12] |
| Qubitrium QubitCore (2026.04) | CubeSat 호환 양자 페이로드, BBM92 QKD 프로토콜 탑재, 상용 양자위성통신 첫걸음 | [The Quantum Insider] |
| 100km 양자 얽힘 분배 | USTC 2026.02 Nature: memory-memory 얽힘 100km (50km 장벽 돌파) | [Nature 2026.02] |
| 유럽 Eagle-1 QKD 위성 | 2026말~2027초 발사 목표, EuroQCI 범유럽 양자통신 인프라(27개국) | [ESA] |
| 캐나다 QEYSSat | 2026 발사 예정 | [CSA] |
| EPB-IonQ 양자네트워크 | Chattanooga 양자컴퓨팅+네트워크 통합 상용시설 (2026초 운영 개시) | [EPB / IonQ] |
| 한국 양자통신망 | 800km / 48노드 정부망 (2022 완료), SKT-IDQ 지분 협력 | [InsightKorea / SKT] |
| 독일 TD.QR | 양자중계기 프로젝트 2026.01 시작 (14개월) | [Innovation News Network] |

---

### 7. 양자센서

| 항목 | 수치/내용 | 출처 |
|---|---|---|
| 시장 규모 2026E | $984M (+14.4% YoY) | [GM Insights] |
| 시장 규모 2032E | $2.28B (CAGR 14.99%) | [GM Insights / IDTechEx] |
| 기술 성숙도 (TRL) | 원자시계 TRL 7-8(국방 실전배치), 자기계 TRL 6-7(상용 프로토타입), 중력계 TRL 5-6(전-상용 시험) | [TQI] |
| QuantumDiamonds | QD m.1 반도체 비파괴 검사 시스템 -- Eurofins EAG Labs 설치, 양자다이아몬드현미경으로 마이크론급 자기장 이미징 | [QuantumDiamonds / TQI] |
| Infleqtion-NASA | ISS 양자센싱 물리팩키지 업그레이드 -- 기록적 원자 집단 달성, 지구 모니터링/관성 항법 | [Infleqtion / NASA] |
| SandboxAQ AQNav | GPS 불필요 양자 자기장 항법 -- 미 공군과 새로운 마일스톤 달성 | [SandboxAQ / USAF] |
| 국방/군사 점유율 | 38% (정밀항법/타이밍/스텔스탐지) | [Mordor Intelligence] |
| 자동차 점유율 | 27% (자율주행 안전/항법) | [Fortune Business Insights] |
| 특허 활동 | 2015년 이후 4배 이상 증가 | [PatSnap] |
| 시장 드라이버 | 5G/6G 동기화, 자율주행 양자LiDAR, GPS-denied 국방, 반도체 검사 | [IDTechEx / GM Insights] |

---

### 8. 양자 클라우드 & 소프트웨어

| 플랫폼 | 하드웨어 접근 | 비고 |
|---|---|---|
| **AWS Braket** | IonQ, Rigetti, QuEra, IQM | 하드웨어 불가지론 최대 플랫폼 [AWS] |
| **Azure Quantum** | IonQ, Quantinuum, Rigetti, Atom Computing | QDK 2026.01 업데이트 (화학 알고리즘 게이트 수 획기적 감소) [Microsoft] |
| **IBM Qiskit Runtime** | IBM 자체 (Heron/Flamingo 등) | Qiskit 최대 커뮤니티, 1,300만 다운로드, 개발자 선호 69% [IBM] |

| 프레임워크 | 운영 | 특징 |
|---|---|---|
| **Qiskit** | IBM | 가장 광범위한 생태계, 글로벌 최다 채택 |
| **PennyLane** | Xanadu | QML(양자머신러닝) 대표, 자동미분 |
| **Cirq** | Google | 양자오류보정 프로토타입, 하드웨어 벤치마킹 |

---

### 9. 양자컴퓨팅 응용 현황 (2026)

| 분야 | 진행 상황 | 출처 |
|---|---|---|
| **금융** | HSBC/Vanguard-IBM 포트폴리오 최적화 파일럿, 옵션 가격결정, 사기탐지 | [IBM / SC Quantum] |
| **신약개발** | Google-Boehringer Ingelheim Cytochrome P450 양자시뮬레이션, 하이브리드 양자-고전 파이프라인 | [Nature / npj Drug Discovery] |
| **물류** | QAOA 30+노드 경로 최적화에서 고전 대비 우위 | [Meta Intelligence / SC Quantum] |
| **반도체 검사** | QuantumDiamonds QD m.1 비파괴 자기장 이미징(마이크론급) | [QuantumDiamonds / Eurofins EAG] |
| **항법** | SandboxAQ AQNav GPS-free 양자항법, 미 공군 실증 | [SandboxAQ] |
| **IBM 양자우위** | 2026말 quantum advantage 달성 예상, 커뮤니티 검증 대기 | [IBM] |

---

### 10. 한국 양자산업

| 항목 | 내용 | 출처 |
|---|---|---|
| **양자산업 육성법** | 2026년 시행 - 양자기술을 독립 산업영역으로 법제화 | [과기정통부] |
| **2035 목표** | 퀀텀칩 제조 세계1위 / 양자기업 2,000개 / 인력 1만명 | [과기정통부 종합계획 2026.01.29] |
| **투자 규모** | 민관 합동 3조원+ (2035까지), 현재 진행 1,980억원 | [대한민국 정책브리핑 / 과기정통부] |
| **2028 중간 목표** | 풀스택 양자컴퓨터(자체 기술 기반) 개발 완료 | [MBC 뉴스 / 과기정통부] |
| **양자클러스터** | 2026.07 지정 예정 | [ZDNet Korea] |
| **양자산업펀드** | 2026년 본격 조성 (벤처/스타트업 마중물) | [과기정통부] |
| **양자기술 협의체** | 삼성전자/LG전자/삼성디스플레이/코오롱(제조) + SKT/KT/LGU+(통신) + 삼성SDS/LG CNS/두산(IT) + 국민은행/신한(금융) + 한화/LIG(방산) | [전자신문] |
| **IonQ 한국 투자** | 공동연구센터 설립, 3년 $15M 투자 | [유니콘팩토리] |
| **인력 양성** | AI영재학교/양자대학원 활용, 연 100명 핵심인재 배출 | [과기정통부] |
| **국내 시장 전망** | 2031E 3,200억원 | [이코노미사이언스] |

#### 10-1. 한국 양자 관련주

| 종목 | 양자 관련 사업 | 비고 |
|---|---|---|
| SK텔레콤 | IonQ 협력, IDQ 지분, 양자암호 시험망 | 양자통신 대장주 |
| 드림시큐리티 | PQC 양자보안 | 암호 전문 |
| 코위버 | PTN/ROADM, 양자암호 통신망 연동 | SKT 양자망 참여 |
| 쏠리드 | 양자통신 인프라 | 통신장비 |
| 우리넷 | 양자통신 인프라 | 통신장비 |
| 옵티시스 | 양자 광학 부품 | 광학 전문 |
| 시큐브 | 양자보안 | 보안 |

---

### 11. 투자 지표 & ETF

| 지표 | 수치 | 출처 |
|---|---|---|
| QTUM ETF (Defiance) | YTD +6%, 1Y +62%, 경비율 0.4% | [Yahoo Finance / Defiance ETFs] |
| IonQ (IONQ) | $35~40 (2026.04 중순), 시총 ~$14B, 목표가 $67.67(+140%) | [Yahoo Finance / IonQ IR] |
| Rigetti (RGTI) | ~$17 (1Y +111%), C-DAC/Novera 수주 모멘텀 | [Yahoo Finance / Nasdaq] |
| D-Wave (QBTS) | FY2025 $24.6M(+179%), 현금 $884.5M, gate-model 확장 | [Fast Company / D-Wave] |
| Quantinuum IPO | 2026 후반 예상, 밸류 $10B -> $20B+ 목표 | [Bloomberg / Quantinuum] |
| Infleqtion (INFQ) | 2026.02 NYSE 상장, 중성원자 최초 IPO | [Infleqtion] |
| PASQAL SPAC | $2B 합병 추진 | [PASQAL] |
| 양자주 4/14~16 랠리 | IonQ +18/+10/+4%, D-Wave +15/+9/+5%, Rigetti +12/+7/+3% (NVIDIA Ising 촉매) | [24/7 Wall St] |

---

### 12. 리스크 팩터

| 리스크 | 설명 | 심각도 |
|---|---|---|
| **밸류에이션 과열** | 대부분 양자 순수기업 적자 상태 (IonQ 매출 $130M vs 손실 $510M). D-Wave/Rigetti 매출 한자리수 $M | 높음 |
| **상용화 불확실성** | IBM 2026말 양자우위 목표이나 실용적 킬러앱 부재. "양자 겨울" 우려 | 중간 |
| **오류보정 기술 장벽** | 100만 물리큐빗급 시스템까지 상당한 시간/비용 필요. NVIDIA AI 참여로 가속 가능성 | 중간 |
| **지정학적 리스크** | 미중 양자 기술 경쟁, 수출통제 확대 가능성 | 중간 |
| **Harvest Now Decrypt Later** | PQC 전환 지연 시 현재 수집 중인 암호문 해독 위험. NSS 2027.01 시한 임박 | 높음 |
| **한국 기술 격차** | 선도국 대비 5년 뒤처짐 (과기정통부 자체 평가). 풀스택 자립 2028 목표 | 중간 |
| **펀딩 사이클** | 금리 환경에 따른 딥테크 VC 위축 가능성. 단 PsiQuantum $1B+, D-Wave $884M 현금 등 대형 유동성 확보 | 낮음 |

---

### 13. 산업 전망 타임라인

| 시점 | 예상 이벤트 |
|---|---|
| 2026 H1 | NVIDIA Ising 양자 AI 모델 확산 / IonQ Q1 실적(5/6) / 한국 양자산업펀드 조성 |
| 2026 H2 | IBM 양자우위 시연 / Quantinuum IPO / PASQAL SPAC 상장 / 한국 양자클러스터 지정(7월) / QuEra 100논리큐빗 / D-Wave gate-model GA / Eagle-1 QKD 위성 발사 |
| 2027 | PsiQuantum 호주+시카고 시스템 가동 / IBM Cockatoo 모듈간 얽힘 / NSS CNSA 2.0 PQC 전환 시한(1월) |
| 2028 | 한국 풀스택 양자컴퓨터 / 1세대 FTQC 등장 |
| 2029 | IBM fault-tolerant 양자컴퓨팅 목표 |
| 2030 | IonQ 200만 물리큐빗/8만 논리큐빗 / RSA-2048 위협 가시화 / 양자컴퓨팅 시장 $7~20B |
| 2035 | NIST 양자취약 알고리즘 완전 폐기 / 한국 퀀텀칩 제조 세계1위 목표 / 양자 경제 파급 $1T |
