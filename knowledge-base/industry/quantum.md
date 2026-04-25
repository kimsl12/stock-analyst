---
updated: 2026-04-25
valid_until: 2026-05-25
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
  - CISA (EO 14306, 연방 PQC 조달 의무화 2026.01.30)
  - IBM Quantum Roadmap (Kookaburra 1,386큐빗/4,158큐빗)
  - Google Quantum AI (Willow, 중성원자 듀얼트랙, PQC 2029 마이그레이션)
  - IonQ IR (FY2025 실적, FY2026 가이던스, SkyWater $1.8B 인수, 포토닉 인터커넥트)
  - Quantinuum (Helios, IPO S-1 제출 2026.02.17, Honeywell 확인 04-22)
  - QuEra Computing (2:1 QEC 달성 04-20, $230M 투자)
  - PsiQuantum ($1B+ Series E, 일본 NEDO 프로그램 04-16)
  - D-Wave (QCI 인수, FY2025 $24.6M, YTD 2026 수주 $32.8M)
  - Rigetti (C-DAC 108큐빗, Novera)
  - PASQAL (SPAC $2B, Thoughts 2026 파리)
  - Infleqtion (INFQ NYSE 상장, 양자센서 매출, 펀딩 $700M+)
  - NVIDIA Ising (양자 AI 모델 2026.04.14)
  - Meta Engineering (PQC 6단계 프레임워크 2026.04.16)
  - Gartner (Q-Day ~2030, PQC #1 사이버보안 우선순위)
  - Entrust/Ponemon (PQC 도입률 40%)
  - MarketsandMarkets, Grand View Research, Precedence Research, Fortune BI, BCC Research
  - GM Insights, IDTechEx (양자센서)
  - SandboxAQ (AQNav USAF TACFI, $1.045B)
  - Mordor Intelligence, Fortune Business Insights
  - SpinQ, QuantumBasel (VC 투자 집계)
  - McKinsey, Gartner, Global Risk Institute
  - 과기정통부 양자과학기술 종합계획 (2026.01.29)
  - 과기정통부 양자클러스터 지정 공모 (2026.04.17)
  - 한국경제, 전자신문, 벤처타임즈, 양자신문
  - Riverlane, Iceberg Quantum, Nature, IEEE Spectrum, phys.org
  - ESA (Eagle-1 EuroQCI), Qubitrium (QubitCore CubeSat)
  - Palo Alto Networks, Cloudflare
  - Motley Fool, 247WallSt, Fast Company, Northland
confidence: high
last_synced_from_db: 2026-04-25
---

# Quantum Technology Knowledge Base

## CURRENT (2026-04-25)

---

### 1. 시장 규모 & 성장률

| 지표 | 수치 | 출처 |
|---|---|---|
| 글로벌 양자컴퓨팅 시장 2025 | $1.44B ~ $3.52B (정의 범위에 따른 편차) | [Precedence Research / MarketsandMarkets] |
| 글로벌 양자컴퓨팅 시장 2026E | $1.88B ~ $2.7B (Fortune BI $2.04B) | [Precedence / Fortune BI / MarketsandMarkets] |
| 양자컴퓨팅 소프트웨어 시장 2026E | $0.78B -> 2030E $1.68B (CAGR 21.2%) | [Research and Markets] |
| 글로벌 양자컴퓨팅 시장 2030E | $4.24B ~ $20.2B (CAGR 20.5~41.8%) | [Grand View / BCC $7.3B / TBRC $16.27B / M&M $20.2B] |
| 양자센서 시장 2026E | $502M~$984M (정의 범위 차이). 국방/보안 **40.25%** 점유 | [GM Insights / Fortune BI / Mordor Intelligence] |
| 양자센서 시장 2031E~2034E | $1.54B~$1.56B (CAGR 12.7~15.7%) | [GM Insights / Fortune BI / IDTechEx] |
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
| **IBM** | Kookaburra(2026): **1,386큐빗** 멀티칩(3칩 연결 시 **4,158큐빗**). qLDPC 메모리+LPU 최초 통합 모듈. Nighthawk 양자우위 연말 목표 | 7,500 게이트/360큐빗 2026 달성 목표. 2029 fault-tolerant. Qiskit 1,300만 다운로드(개발자 선호 69%) [IBM Quantum] |
| **Google** | Willow(2024.12) + **중성원자 듀얼트랙 확장**(04-03). qLDPC FT 아키텍처 블루프린트 2건(이온트랩/중성원자) 공개 | 105큐빗, 99.88% 2큐빗 게이트. 초전도+중성원자 병행 전략 [Google Quantum AI / HPCwire] |
| **Rigetti** | C-DAC(인도) $8.4M 108큐빗 시스템 주문(H2 2026), Novera $5.7M Q1 출하 | FY2025 매출 $7.09M(-34% YoY), 주가 ~$17(1Y +111%). 255% 매출 성장 전망 [Rigetti / Nasdaq] |

#### 3-2. 이온트랩 방식

| 기업 | 2026 현황 | 핵심 지표 |
|---|---|---|
| **IonQ** | **SkyWater $1.8B 인수 합의**(01-26): 양자업계 최초 수직통합 풀스택. 2028 **200K 물리큐빗** QPU 테스트 목표 | FY2026 가이던스 **$225~245M**(중위 $235M, +81%). FY2025 $130M(+202%). RPO $370M. 주가 4월 +72%(7거래일). 목표가 $55~$67.67 [IonQ IR / Northland] |
| **IonQ 네트워킹** | **포토닉 인터커넥트**(04-14): 두 상용 이온트랩 간 원거리 양자얽힘 최초 시연. DARPA HARQ 프로그램 선정 + AFRL 공동 | SDT QuREKA 한국 플랫폼 통합. UMD QLab $750만 확장 [IonQ / DARPA / SDT] |
| **Quantinuum** | Helios 상용, **IPO S-1 비공개 제출**(02-17, Honeywell 04-22 공식 확인). 전통 IPO(SPAC 아님) | 98 물리큐빗/48논리큐빗(2:1). 1큐빗 **99.9975%**, 2큐빗 **99.921%**. $10B -> **$20B+ IPO** 목표. [Quantinuum / HPCwire / Bloomberg] |

#### 3-3. 중성원자 방식

| 기업 | 2026 현황 | 핵심 지표 |
|---|---|---|
| **QuEra** | **2:1 물리-논리큐빗 QEC 달성**(04-20, Harvard/MIT). Teraquop 에러율 범위 시뮬레이션 확인 | $230M 투자(Google/NVIDIA/SoftBank). Tsim GPU 시뮬레이터. 100논리큐빗+10,000물리큐빗(3세대) [QuEra / Nature] |
| **PASQAL** | Thoughts 2026(파리 04-21): 연구->실용 전환. True Nexus 단백질 시뮬레이션 파트너십(04-10) | SPAC $2B 추진. Fresnel 프로세서. Alain Aspect 창업 [PASQAL / TQI] |
| **Infleqtion** | 2026.02 NYSE 상장(**INFQ**) -- 중성원자 최초 IPO. **양자센서 매출 발생** 중 | 양자컴퓨팅+센싱 듀얼. NASA ISS. 총 펀딩 $700M+ [Infleqtion] |

#### 3-4. 양자어닐링

| 기업 | 2026 현황 | 핵심 지표 |
|---|---|---|
| **D-Wave** | QCI 인수($550M) 후 gate-model 2026 GA 목표. **YTD 2026 수주 $32.8M**(FAU $20M 포함, 역대급) | FY2025 매출 $24.6M(+179%). Q4 수주 $13.4M(+471% QoQ). 현금 **$884.5M**. 주가 4월 +56% [D-Wave / Fast Company / Motley Fool] |

#### 3-5. 광자 방식

| 기업 | 2026 현황 | 핵심 지표 |
|---|---|---|
| **PsiQuantum** | Series E $1B+, 시카고+브리즈번 2사이트. **일본 NEDO 인력양성 프로그램**(04-16, 도쿄대/미쓰비시/20개사 80명) | CEO Victor Peng(전 AMD/Xilinx). NVIDIA 파트너십. 밸류 ~$7B [PsiQuantum / IEEE Spectrum] |
| **Xanadu** | PennyLane QML 프레임워크 운영 | 오픈소스 양자머신러닝 대표 [PennyLane] |

**미국 상장 양자 순수기업 6사**: IonQ(IONQ), D-Wave(QBTS), Rigetti(RGTI), Quantum Computing Inc(QUBT), Arqit(ARQQ), Infleqtion(INFQ)

---

### 4. 양자 오류보정 & Fault-Tolerant 진전

| 마일스톤 | 내용 | 출처 |
|---|---|---|
| NVIDIA Ising (2026.04.14) | 세계 최초 양자 교정+에러보정용 오픈소스 AI 모델. Ising Calibration(수일->수시간), Ising Decoding(2.5x 빠르고 3x 정확). IonQ/IQM/Fermilab/ORNL 채택 | [NVIDIA Technical Blog] |
| IBM Kookaburra (2026) | **1,386큐빗**(3칩 4,158큐빗). 최초 qLDPC 메모리+LPU 통합 양자 프로세서 모듈 | [IBM Quantum Blog / HPCwire] |
| **QuEra 2:1 QEC (2026.04.20)** | 중성원자 QEC에서 2:1 물리-논리큐빗 비율 달성. Teraquop 에러율 범위. Harvard/MIT 공동 | [QuEra / Nature] |
| 중간측정 없는 FTQC (2026.04) | 이온트랩에서 중간측정 없이 Grover 알고리즘 3 논리큐빗 실행 성공 | [phys.org] |
| 게이지 이론 QEC (2026.03) | gauge theory 기법으로 물리큐빗 수 대폭 절감 가능한 새 에러보정법 | [phys.org] |
| Google Willow below-threshold (2024.12) | 규모 확대 시 오류 기하급수 감소 최초 입증 (30년 난제) | [Google Quantum AI] |
| Quantinuum Helios 48 논리큐빗 (2025.11) | 2:1 물리-논리 큐빗 비율, break-even 초과. **1큐빗 99.9975%, 2큐빗 99.921%** | [Quantinuum] |
| Iceberg Pinnacle (2026.02) | RSA-2048 해독 물리큐빗 100만->10만으로 **10배 절감** | [Iceberg Quantum] |
| qLDPC 코드 확산 (2026) | IBM 전환(2024) 이후 타사 추종 중. Google qLDPC FT 아키텍처 블루프린트 2건 공개(04-03) | [Riverlane / HPCwire] |
| QEC 연구 폭증 | 2025년 120편 peer-reviewed 논문 (2024년 36편 대비 3.3배) | [Riverlane] |
| IQM Shor 2048-bit (2026.04.05) | 최초 게이트레벨 Shor 알고리즘 2048비트 키 컴파일 | [IQM / Fraunhofer FOKUS] |

**핵심 트렌드**: 개별 논리큐빗 시연에서 "1세대 FTQC 전체 시스템 구축"으로 전환. NVIDIA AI 모델 + QuEra 2:1 QEC + Google qLDPC 블루프린트 = 오류보정 가속의 삼중 촉매.

---

### 5. PQC(포스트양자암호)

| 항목 | 내용 | 출처 |
|---|---|---|
| NIST 최종 표준 | ML-KEM(FIPS 203), ML-DSA(FIPS 204), SLH-DSA(FIPS 205) - 2024.08. **FN-DSA**(FALCON 기반) 추가 표준 2026E | [NIST] |
| 양자취약 알고리즘 폐기 | RSA/ECC 연방 시스템 **2030 폐기, 2035 금지** (NIST IR 8547) | [NIST] |
| **CISA 연방 PQC 조달 의무화** | **2026.01.30**: 연방기관 양자저항 제품만 조달 의무. EO 14306(트럼프 2025.06) 근거. 이론적 준비 -> **운영 의무** 전환 | [CISA / ComplianceHub.Wiki] |
| NSS 규정 준수 시한 | **2027.01** -- CNSA 2.0 국가안보시스템 PQC 전환 시한. 2030 RSA 폐기 | [NIST NCCoE / CNSA 2.0] |
| **Google PQC 2029 마이그레이션** | PQC 전환 **2029 타임라인** 공식 발표(03-25). **Android 17 ML-DSA** 통합(2026.06E). Chrome ML-KEM 기본 활성화 | [TQI / Google Blog] |
| **Meta PQC 프레임워크** | 04-16: **6단계 마이그레이션 프레임워크** 공개. 하이브리드(ML-KEM768+X25519, ML-DSA65+ECDSA) 추천 | [Meta Engineering Blog] |
| **기업 PQC 도입률** | 실배치 5%(2025.05) -> **전환 착수 40%**(2026 Entrust/Ponemon). Gartner 2026.02: PQC = **글로벌 #1 사이버보안 우선순위** | [Entrust/Ponemon / Gartner] |
| PQC 인증서 | 2026년 최초 발급 예정 (기본값 아님) | [Cloudflare / HashiCorp] |
| **RSA-2048 위협 시점** | 알고리즘 돌파(2025): 필요 큐빗 2000만->**100만 이하**(10배 절감). Q-Day 추정 **~2030**(Gartner 2026.02) | [Gartner / Iceberg Quantum / Citi Institute] |
| Harvest Now Decrypt Later | 적대세력 현재 암호문 수집 중. 2035 이후 기밀성 필요 데이터는 **지금** PQC 보호 필수 | [Citi Institute / CISA / stateofsurveillance.org] |

**변화 포인트**: "연구/권고" 단계에서 **"연방 의무화 + 빅테크 타임라인 확정"** 단계로 격상 (2026). CISA 연방 조달 의무 + Google 2029 + Meta 프레임워크 = PQC 전환 불가역.

---

### 6. 양자통신 & 양자 인터넷

| 항목 | 내용 | 출처 |
|---|---|---|
| **IonQ 포토닉 인터커넥트** | 두 독립 상용 이온트랩 양자시스템 **광자 연결 최초 시연**(04-14). DARPA HARQ 선정 + AFRL 공동. 분산/네트워크 양자 아키텍처 핵심 | [IonQ IR / QCR / HPCwire] |
| 중국 CN-QCN | **10,000+km / 145 백본 노드 / 20 메트로 NW / 17개 성 80개 도시**. 캐리어급 QKD 실운용 | [Nature npj QI / postquantum.com] |
| Jinan-1 마이크로위성 | 12,900km QKD 실증 (베이징-남아공, 2025.03) | [Nature / ScienceDaily] |
| 지상->위성 양자 업링크 | 기존 다운링크만 가능하다는 인식 뒤집음 -- 더 저렴/실용적 글로벌 양자네트워크 | [ScienceDaily 2025.12] |
| Qubitrium QubitCore (2026.04) | CubeSat 호환 양자 페이로드, BBM92 QKD 프로토콜, 상용 양자위성통신 첫걸음 | [TQI] |
| 100km 양자 얽힘 분배 | USTC 2026.02 Nature: memory-memory 얽힘 100km (50km 장벽 돌파) | [Nature 2026.02] |
| **유럽 Eagle-1 QKD 위성** | **2026말~2027초 Vega C 발사**. SES 주도 20개 파트너. 올광학 C-band QKD. EuroQCI 27개국 양자통신 인프라 | [ESA / SES] |
| 캐나다 QEYSSat | 2026 발사 예정 | [CSA] |
| **EPB-IonQ 챠타누가** | 양자컴퓨팅+네트워킹 통합 **상용시설 2026 초 운영 개시** | [EPB / IonQ] |
| 한국 양자통신망 | 800km / 48노드 정부망 (2022 완료), SKT-IDQ 지분 협력 | [InsightKorea / SKT] |
| 독일 TD.QR | 양자중계기 프로젝트 2026.01 시작 (14개월) | [Innovation News Network] |

---

### 7. 양자센서

| 항목 | 수치/내용 | 출처 |
|---|---|---|
| 시장 규모 2026E | $502M~$984M (정의 범위 차이). **국방/보안 40.25%** 점유 | [GM Insights / Fortune BI / Mordor Intelligence] |
| 시장 규모 2031E~2034E | $1.54B~$1.56B (CAGR 12.7~15.7%) | [GM Insights / Fortune BI / IDTechEx] |
| 기술 성숙도 (TRL) | 원자시계 **TRL 7-8**(현장배치), 자기계 **TRL 6-7**(상용 프로토타입 제한적 현장), 중력계 **TRL 5-6**(전-상용) | [TQI / PatSnap / IDTechEx] |
| **SandboxAQ AQNav** | GPS 불필요 양자 자기장 항법. 미 공군 **TACFI 계약 연장** + 신규 마일스톤. 총 펀딩 **$1.045B** | [SandboxAQ / USAF / GlobeNewsWire] |
| **Infleqtion 센서 매출** | 원자시계/양자RF수신기/관성센싱 **실배치 중, 매출 발생**. 총 펀딩 $700M+ | [Infleqtion CES 2026 / TQI] |
| QuantumDiamonds | QD m.1 반도체 비파괴 검사 -- NV 다이아몬드 마이크론급 자기장 이미징. Eurofins EAG Labs 설치 | [QuantumDiamonds / TQI] |
| Infleqtion-NASA | ISS 양자센싱 물리팩키지 업그레이드 -- 기록적 원자 집단, 지구 모니터링/관성 항법 | [Infleqtion / NASA] |
| 국방/군사 점유율 | **40.25%** (정밀항법/타이밍/스텔스탐지) | [Mordor Intelligence / Fortune BI] |
| **원자체인 전기장 감지** | 원자 체인 전기장 정밀 감지 돌파(04-17) | [ScienceDaily 2026.04.17] |
| 특허 활동 | 2015년 이후 **4배 이상** 증가 | [PatSnap] |
| 시장 드라이버 | 5G/6G 동기화, 자율주행 양자LiDAR, GPS-denied 국방, 반도체 검사, 드론 PNT | [IDTechEx / GM Insights / GlobeNewsWire] |

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
| **항법** | SandboxAQ AQNav GPS-free 양자항법, 미 공군 TACFI 계약 연장 | [SandboxAQ / USAF] |
| **단백질 시뮬레이션** | PASQAL-True Nexus 단백질 기능 양자시뮬레이션(04-10) | [PASQAL / TQI] |
| **IBM 양자우위** | 2026말 quantum advantage 달성 예상, 커뮤니티 검증 대기 | [IBM] |

---

### 10. 한국 양자산업

| 항목 | 내용 | 출처 |
|---|---|---|
| **양자산업 육성법** | 2026년 시행 -- 양자기술을 독립 산업영역으로 법제화. "연구실에서 시장으로" 역사적 전환 | [과기정통부 / 벤처타임즈] |
| **2035 목표** | 퀀텀칩 제조 세계1위 / 양자기업 2,000개 / 인력 1만명 | [과기정통부 종합계획 2026.01.29] |
| **투자 규모** | 민관 합동 3조원+ (2035까지), 현재 진행 1,980억원 | [대한민국 정책브리핑 / 과기정통부] |
| **2028 중간 목표** | 풀스택 양자컴퓨터(자체 기술 기반) 개발 완료 | [MBC 뉴스 / 과기정통부] |
| **양자클러스터 공모** | **04-17 지정 공모 개시**. 5대 분야(컴퓨팅/통신/센서/소부장/알고리즘). 05-18 신청 마감, **07월 양자전략위원회** 심의/최종 지정 | [정책브리핑 / 한국경제 2026.04.22] |
| **양자산업펀드** | 2026년 본격 조성 (벤처/스타트업 마중물) | [과기정통부] |
| **양자기술 협의체** | 삼성전자/LG전자/삼성디스플레이/코오롱(제조) + SKT/KT/LGU+(통신) + 삼성SDS/LG CNS/두산(IT) + 국민은행/신한(금융) + 한화/LIG(방산) | [전자신문] |
| **IonQ 한국 투자** | 공동연구센터 설립, 3년 $15M 투자. SDT QuREKA 플랫폼 통합(04월) | [유니콘팩토리 / IonQ] |
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
| **양자주 4/9~4/20 7거래일 랠리** | **IonQ +72%, D-Wave +56%, Rigetti +37%**. 촉매: NVIDIA Ising + IonQ 포토닉 인터커넥트 + D-Wave 수주 | [Motley Fool 04-24 / 247WallSt / Fast Company] |
| **밸류에이션 경고** | P/S: IonQ **106x**, D-Wave **283x**, Rigetti **870x** -- 버블 영역 | [Motley Fool 04-24] |
| QTUM ETF (Defiance) | YTD +6%, 1Y +62%, 경비율 0.4% | [Yahoo Finance / Defiance ETFs] |
| IonQ (IONQ) | $35~40 (04월), 시총 ~$14B, 목표가 $55~$67.67. Q1 실적 **5/6** 발표 | [Yahoo Finance / Northland / IonQ IR] |
| Rigetti (RGTI) | ~$17 (1Y +111%), C-DAC/Novera 수주 모멘텀. 255% 매출 성장 전망 | [Yahoo Finance / Nasdaq] |
| D-Wave (QBTS) | FY2025 $24.6M(+179%), YTD 수주 $32.8M, 현금 $884.5M, gate-model 확장 | [Fast Company / D-Wave] |
| Quantinuum IPO | 전통 IPO S-1 제출(02-17). $10B -> **$20B+** 목표 | [Bloomberg / HPCwire 04-22] |
| Infleqtion (INFQ) | 2026.02 NYSE 상장, 중성원자 최초 IPO | [Infleqtion] |
| PASQAL SPAC | $2B 합병 추진 | [PASQAL] |

---

### 12. 리스크 팩터

| 리스크 | 설명 | 심각도 |
|---|---|---|
| **밸류에이션 과열** | P/S 100~870x. IonQ 매출 $130M vs 손실 $510M. D-Wave/Rigetti 매출 한자리수~두자리수 $M. 7거래일 +72% 급등 후 조정 경고 | 높음 |
| **상용화 불확실성** | IBM 2026말 양자우위 목표이나 실용적 킬러앱 부재. "양자 겨울" 우려 | 중간 |
| **오류보정 기술 장벽** | 100만 물리큐빗급 시스템까지 상당한 시간/비용. 단 NVIDIA AI + QuEra 2:1 QEC + IonQ SkyWater 200K 큐빗 로드맵으로 가속 | 중간 |
| **지정학적 리스크** | 미중 양자 기술 경쟁, 수출통제 확대. 중국 양자 정부투자 $10B+(최대) | 중간 |
| **Harvest Now Decrypt Later** | CISA 연방 의무화 + Q-Day ~2030 + RSA 해독 큐빗 10배 절감. PQC 전환 지연 = 현재 데이터 위험 | 높음 |
| **한국 기술 격차** | 선도국 대비 5년 뒤처짐 (과기정통부 자체 평가). 풀스택 자립 2028 목표 | 중간 |
| **IonQ SkyWater 통합 리스크** | $1.8B 인수 = 양자 기업 최대 M&A. 파운드리 통합 실행 불확실성 | 중간 |
| **펀딩 사이클** | 금리 환경에 따른 딥테크 VC 위축 가능성. 단 PsiQuantum $1B+, D-Wave $884M, Infleqtion $700M 등 대형 유동성 확보 | 낮음 |

---

### 13. 산업 전망 타임라인

| 시점 | 예상 이벤트 |
|---|---|
| 2026 H1 | NVIDIA Ising 확산 / IonQ Q1 실적(**5/6**) / 한국 양자클러스터 공모 마감(05-18) / IonQ-SkyWater 인수 마감(Q2-Q3) / Android 17 ML-DSA(06E) |
| 2026 H2 | IBM 양자우위 시연 / **Quantinuum IPO** / PASQAL SPAC / 한국 양자클러스터 지정(**7월**) / QuEra 100논리큐빗 / D-Wave gate-model GA / **Eagle-1 QKD 위성 발사** |
| 2027 | PsiQuantum 호주+시카고 가동 / IBM Cockatoo 모듈간 얽힘 / **NSS CNSA 2.0 PQC 전환 시한(1월)** |
| 2028 | 한국 풀스택 양자컴퓨터 / 1세대 FTQC / **IonQ-SkyWater 200K 물리큐빗 QPU** |
| 2029 | IBM fault-tolerant 목표 / **Google PQC 마이그레이션 완료** |
| 2030 | IonQ 200만 물리큐빗/8만 논리큐빗 / **RSA-2048 위협 가시화(Q-Day)** / **연방 RSA 폐기** / 양자컴퓨팅 시장 $7~20B |
| 2035 | NIST 양자취약 알고리즘 완전 금지 / 한국 퀀텀칩 세계1위 목표 / 양자 경제 파급 $1T |

> **2026.04.25 핵심 변화 요약**:
> 1. **IonQ SkyWater $1.8B 인수** = 양자업계 최초 수직통합. 2028 200K 큐빗 QPU 목표. 포토닉 인터커넥트 + DARPA HARQ = 양자네트워킹 기술 주도.
> 2. **Quantinuum IPO S-1 공식 확인**(Honeywell 04-22) = $20B+ 양자업계 최대 IPO 임박.
> 3. **CISA PQC 연방 조달 의무화** + Google 2029 타임라인 + Meta 6단계 프레임워크 = PQC 전환 불가역 단계.
> 4. **양자주 7거래일 랠리**(IonQ +72%) -- 단 P/S 100~870x 버블 경고.
> 5. **QuEra 2:1 QEC 달성**(04-20) + Google 중성원자 듀얼트랙 = 중성원자 방식 부상.
> 6. **한국 양자클러스터 공모 개시**(04-17) = 양자산업 육성법 최초 실행 단계.
