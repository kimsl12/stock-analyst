# DART OpenAPI 가이드 (전자공시시스템)

Bash를 통해 DART OpenAPI를 호출한다.

## 환경변수 (사전 설정 완료)
인증키는 환경변수 `DART_API_KEY`로 등록되어 있다.
- 설정 위치: `.claude/settings.json` → `env.DART_API_KEY`
- 일일 호출 한도: 10,000건 (개인)
- 키를 코드나 에이전트 파일에 직접 하드코딩하지 않는다.

## Step 0: 고유번호(corp_code) 조회
DART API는 종목코드(예: 005930)가 아닌 **고유번호(corp_code)**를 사용한다.
종목코드 → corp_code 변환이 반드시 선행되어야 한다.

```bash
# 1) 고유번호 전체 목록 다운로드 (ZIP → XML)
curl -s "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=${DART_API_KEY}" -o /tmp/corpcode.zip
unzip -o /tmp/corpcode.zip -d /tmp/corpcode/

# 2) 종목코드로 corp_code 검색 (예: 삼성전자 005930)
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('/tmp/corpcode/CORPCODE.xml')
root = tree.getroot()
target_stock = '005930'  # 종목코드
for corp in root.findall('list'):
    if corp.findtext('stock_code') == target_stock:
        print(f'corp_code: {corp.findtext(\"corp_code\")}')
        print(f'corp_name: {corp.findtext(\"corp_name\")}')
        break
"
# 결과 예시: corp_code: 00126380, corp_name: 삼성전자
```

캐싱: 한번 다운로드한 CORPCODE.xml은 `/tmp/corpcode/`에 보관하여 재사용한다.

## 주요 엔드포인트
```bash
# 기업 개황
curl -s "https://opendart.fss.or.kr/api/company.json?crtfc_key=${DART_API_KEY}&corp_code=${CORP_CODE}"

# 재무제표 — 단일회사 전체 계정 (OFS: 개별, CFS: 연결)
curl -s "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key=${DART_API_KEY}&corp_code=${CORP_CODE}&bsns_year=2024&reprt_code=11011&fs_div=CFS"

# 주요 재무지표 (ROE, 부채비율 등)
curl -s "https://opendart.fss.or.kr/api/fnlttCmpnyIndx.json?crtfc_key=${DART_API_KEY}&corp_code=${CORP_CODE}&bsns_year=2024&reprt_code=11011&idx_cl_code=M210000"

# 배당 정보
curl -s "https://opendart.fss.or.kr/api/alotMatter.json?crtfc_key=${DART_API_KEY}&corp_code=${CORP_CODE}&bsns_year=2024&reprt_code=11011"

# 최대주주 현황
curl -s "https://opendart.fss.or.kr/api/hyslrSttus.json?crtfc_key=${DART_API_KEY}&corp_code=${CORP_CODE}&bsns_year=2024&reprt_code=11011"

# 임원 현황
curl -s "https://opendart.fss.or.kr/api/exctvSttus.json?crtfc_key=${DART_API_KEY}&corp_code=${CORP_CODE}&bsns_year=2024&reprt_code=11011"

# 최근 공시 목록
curl -s "https://opendart.fss.or.kr/api/list.json?crtfc_key=${DART_API_KEY}&corp_code=${CORP_CODE}&bgn_de=20240101&end_de=20261231&page_count=20"

# 대량보유 현황 (5% 이상)
curl -s "https://opendart.fss.or.kr/api/majorstock.json?crtfc_key=${DART_API_KEY}&corp_code=${CORP_CODE}"
```

## DART reprt_code 참조
| 코드 | 보고서 |
|------|--------|
| 11013 | 1분기보고서 |
| 11012 | 반기보고서 |
| 11014 | 3분기보고서 |
| 11011 | 사업보고서(연간) |

## 공개 금융 데이터
```bash
# 네이버 금융 (주가/재무 요약) — 웹 스크래핑
curl -s "https://finance.naver.com/item/main.naver?code=${STOCK_CODE}"

# KRX 한국거래소 시장 데이터
curl -s "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd" \
  -d "bld=dbms/MDC/STAT/standard/MDCSTAT01501&mktId=STK&trdDd=$(date +%Y%m%d)"
```
