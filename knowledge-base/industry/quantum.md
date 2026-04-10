---
updated: 2026-04-10
valid_until: 2026-05-10
sector: quantum
sources:
  - https://csrc.nist.gov/projects/post-quantum-cryptography
  - https://www.ibm.com/quantum
  - https://ionq.com
  - https://www.quantinuum.com
  - https://openquantumsafe.org
  - https://xanadu.ai
  - https://en.wikipedia.org/wiki/Quantum_computing
  - https://www.grandviewresearch.com/industry-analysis/quantum-computing-market
  - https://www.lucedaphotonics.com/
  - https://www.ligentec.com/
  - https://www.sec.gov
confidence: medium
last_synced_from_db: 2026-04-10
---
# Quantum Knowledge Base
## ★ CURRENT ★
- **요약:** 양자기술(양자컴퓨팅·양자통신·양자센서·PQC)은 상업화 단계로 진입 중입니다. 주요 벤더들은 클라우드 기반 접근성과 상용 제품을 적극 확장하고 있으며, PQC(포스트-양자 암호)는 2024년 이후 표준화가 진전되어 보안 전환이 가속화되고 있습니다.

## 핵심 사실
- **PQC 표준화:** NIST가 2024년 8월에 첫 번째 PQC(주요 암호 규격) 최종안을 발표했고, 추가 표준화 작업이 진행 중입니다. (출처: NIST)
- **PQC 마이그레이션:** NIST 권고에 따르면 취약 알고리즘의 표준적 폐기는 2035년을 목표로 하며, 주요 시스템은 조기 마이그레이션을 준비해야 합니다. (출처: NIST)
- **벤더·상용화:** IBM, IonQ, Quantinuum, Xanadu 등 주요 공급자가 클라우드·하드웨어 접근을 제공하고 있으며, 상용화 로드맵을 공개하고 있습니다. (출처: IBM, IonQ, Quantinuum, Xanadu)
- **시장 규모:** 시장리서치(Grand View Research) 기준 2024년 글로벌 양자컴퓨팅 시장은 약 USD 1.42B이며, 2030년까지 USD 4.24B 수준으로 성장할 전망입니다(참고: 리포트별 추정 차이 존재).
- **IBM 규모:** IBM은 100+ 큐비트급 시스템을 포함한 대규모 플릿과 연구·커뮤니티 지원을 운영합니다. (출처: IBM)
- **IonQ 주장:** IonQ는 자체 로드맵에서 수백만 물리 큐비트(자사 주장)를 목표로 하는 등 대규모 확장 비전을 공개했습니다(회사 주장). (출처: IonQ)
- **IonQ 인수·로드맵 요약:** IonQ는 Lightsynq, Oxford Ionics, SkyWater 등 인수를 통해 포토닉·파운드리·네트워킹 역량을 강화했으며, 자사 블로그/뉴스에서 2030년 목표(2,000,000 물리 큐비트)를 공개했습니다(회사 전향적(Forward-looking) 진술).
- **공급망(요약):** 핵심 구성요소는 트랩 이온(이온 트랩·진공·레이저), 포토닉(PIC 설계·PDK·파운드리), 제어장치(AWG·FPGA·제어 SW), 파운드리(예: SkyWater, GlobalFoundries), 광소자·PIC 공급자(LIGENTEC, Luceda 등)로 구성됩니다. (출처: 벤더·파트너 페이지)
- **양자 센서:** 양자 센서는 상용화 성숙도가 비교적 높은 분과로 평가되며, 레이더·지질탐사·의료이미징 등 응용 연구가 활발합니다. (출처: 학술·요약자료)
- **오픈 퀀텀 세이프:** Open Quantum Safe 프로젝트(liboqs 등)는 PQC 전환을 지원하는 오픈소스 툴과 통합을 활발히 업데이트하고 있습니다. (출처: openquantumsafe.org)

## 짧은 권고
- 리스크 민감 시스템은 **PQC 적용 계획**을 수립하세요(취약점 탐지→우선순위 지정→시스템별 마이그레이션 스케줄).
- 양자 센싱 등 상용 영역은 파일럿 적용 우선 고려(데이터·정합성 검증 필수).

## 소스
- NIST PQC overview: https://csrc.nist.gov/projects/post-quantum-cryptography
- IBM Quantum: https://www.ibm.com/quantum
- IonQ: https://ionq.com
- Quantinuum: https://www.quantinuum.com
- Open Quantum Safe: https://openquantumsafe.org
- Xanadu: https://xanadu.ai
- Wikipedia summary: https://en.wikipedia.org/wiki/Quantum_computing
 - Grand View Research (quantum market): https://www.grandviewresearch.com/industry-analysis/quantum-computing-market
 - Luceda Photonics (PIC design): https://www.lucedaphotonics.com/
 - LIGENTEC (photonic foundry/PIC): https://www.ligentec.com/
 - SEC EDGAR (company filings/search): https://www.sec.gov

## 메모
- 이 파일은 `knowledge-db/quantum_2026.jsonl`의 레코드를 요약한 CURRENT 뷰입니다. 상세 수치·출처는 DB 파일을 참고하세요.
