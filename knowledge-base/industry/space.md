# Space (CURRENT)

요약: 발사체(Launchers), 위성통신(Satcom), 우주인터넷(LEO constellations), 탐사(Artemis 등), 시장(상업·정부 수요), 공급망(엔진·항공전자·페이로드·지상국)을 중심으로 한 분야 정리.

- 핵심 사실:
  - SpaceX: Starship/Super Heavy 개발 및 Starlink 운영(150+개국, 소비자속도 사례 400+ Mbps) — 출처: SpaceX/Starlink
  - 위성통신: Telesat Lightspeed 등 LEO 네트워크가 항공·해상·정부 시장을 목표로 함 — 출처: Telesat
  - 발사체: Ariane 6, Rocket Lab(Neutron 개발) 등 상업용 발사체 공급자들이 상업·대형·중형 수요를 분담 — 출처: Arianespace, Rocket Lab
  - 탐사: NASA Artemis 프로그램(유인/달 임무) 일정이 진행 중 — 출처: NASA
  - 규제·운영: FAA는 상업 발사·스페이스포트 라이선스 데이터 공개(누적 1,000건 등) — 출처: FAA
  - 중국 활동: Thousand Sails/Guowang 등 대규모 컨스텔레이션 발사 활동 관찰 — 출처: SpaceNews

- 시장 및 리스크 요약:
  - 시장보고서는 글로벌 우주경제의 빠른 성장(수백억~수천억 USD 규모)을 보고하나, 정확한 수치는 보고서별로 상이하며 유료 보고서 참조 필요(BryceTech, Euroconsult 등).
  - 공급망 리스크: 엔진·전력·고출력 RF 페이로드·정밀센서·지상망 의존성 — 제조·시험 인프라 병목 가능.

- 참고(주요 출처):
  - https://www.spacex.com/
  - https://www.starlink.com/
  - https://www.telesat.com/
  - https://www.arianespace.com/
  - https://www.nasa.gov/artemis
  - https://www.faa.gov/space
  - https://spacenews.com/

노트: 이 파일은 `knowledge-db/space_2026.jsonl`의 요약(CURRENT)으로 생성됨. 세부 수치(시장규모 등)는 유료보고서에 의존하므로 필요시 보고서 구매 권장.

## 교차검증된 핵심치 (공개자료 기준)

- **`SpaceX Starship payload`**: 100–150 t (fully reusable); 250 t (expendable) — 출처: https://www.spacex.com/vehicles/starship (회사 사양). **신뢰도**: 높음(회사 표기).
- **`Starfactory 생산능력(회사 주장)`**: Starfactory는 연간 최대 1,000대 수준의 생산 능력으로 설계됨 — 출처: https://www.spacex.com/vehicles/starship. **신뢰도**: 중간(회사 주장, 실운용 미확인).
- **`Starlink 가용성·성능`**: 150+개국 가용, 평균 가동률 >99.9%, 소비자 속도 사례 400+ Mbps — 출처: https://www.starlink.com/. **신뢰도**: 높음(회사 표기).
- **`Starlink Roam (한국)`**: 요금 시작가 예시 ₩72,000/월(로밍 플랜) — 출처: https://www.starlink.com/. **신뢰도**: 높음(회사 표기).
- **`Telesat Lightspeed 초기 위성수`**: 초기 구성 156대(회사 보도자료), 군용 Ka-band 500MHz 추가 발표 — 출처: https://www.telesat.com/press/. **신뢰도**: 높음(회사 발표).
- **`Eutelsat + OneWeb`**: GEO 플릿과 OneWeb LEO 결합한 멀티오빗 네트워크 제공(제품/투자자 페이지) — 출처: https://www.eutelsat.com/. **신뢰도**: 높음(회사 설명).
- **`미·규제`**: FCC는 2026-03-27 등 관련 NPRM·정책을 통해 스펙·주파수 접근성 계획을 진행 중 — 출처: https://www.fcc.gov/space. **신뢰도**: 높음(규제 문건).

노트: 위 항목들은 회사 공식 페이지·보도자료·규제문서 기준으로 교차검증한 공개자료입니다. 시장규모나 전망치(Grand View, BryceTech, Euroconsult 등)는 많은 경우 유료보고서에 기반하므로, 정확한 수치가 필요하면 특정 보고서 구매 또는 요약(신뢰할 수 있는 2차 출처) 추가 수집을 권장합니다.

## 추가 교차검증된 핵심치 (공개자료 B-심층 크로스체크)

- **`SpaceX Starship height`**: 123 m — 출처: https://www.spacex.com/vehicles/starship. **신뢰도**: 높음(회사 표기).
- **`SpaceX Starship diameter`**: 9 m — 출처: https://www.spacex.com/vehicles/starship. **신뢰도**: 높음(회사 표기).
- **`Starlink constellation size`**: 8,000+ 위성(회사 업데이트 기준). **신뢰도**: 중간(회사 표기/업데이트).
- **`Starlink Direct-to-Cell satellites`**: 600+ (first-generation 배치) — 출처: SpaceX 업데이트. **신뢰도**: 중간(회사 주장).
- **`Starlink Direct-to-Cell users`**: 약 6,000,000명 (회사 주장). **신뢰도**: 중간(회사 주장).
- **`Starlink production/launch 기록`**: 생산능력 최대 45대/주(회사 표기), 한 달에 최대 240대 발사 기록(회사 기록). **신뢰도**: 중간(회사 표기/운용 기록).
- **`Telesat Lightspeed(생산)`**: 첫 두 대의 생산 위성은 2026년 12월 발사 계획(회사 보도자료). **신뢰도**: 높음(회사 발표).
- **`FCC(2026-04-08)`**: 'Poised to Empower Super-Fast, Space-Based Broadband' 공문(2026-04-08) — 규제·주파수·접근성 관련 주요 문건. **신뢰도**: 높음(규제 기관).
- **`Eutelsat Investor Presentation (Mar 2026)`**: 투자자 프레젠테이션 PDF(2026-03) 다운로드 가능 — 출처: https://www.eutelsat.com/. **신뢰도**: 높음(회사 자료).
- **`Gigabay (SpaceX, Florida)`**: Gigabay 시설(Florida) — 높이 약 380 ft, 약 46.5M cu ft 작업공간, 최대 81 m 높이 차량 지원(회사 업데이트). **신뢰도**: 중간(회사 설명).
