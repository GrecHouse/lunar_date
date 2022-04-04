![version](https://img.shields.io/badge/version-1.1.2-blue)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

# Lunar Date Sensor

오늘의 음력 날짜를 알려주는 Home Assistant Sensor 입니다. 
<br><br>

파이썬 라이브러리 소스 `korean-lunar-calendar` 를 이용해 만들었습니다. \
https://pypi.org/project/korean-lunar-calendar/ \
https://github.com/usingsky/korean_lunar_calendar_py

<br>
<img src="https://user-images.githubusercontent.com/49514473/76295572-33e0bf80-62f8-11ea-855f-8747cb3add95.png" />
<br>

## Installation

### 직접 설치
- HA 설치 경로 아래 custom_component 에 파일을 넣어줍니다.
<br>`<config directory>/custom_components/lunar_date/sensor.py`
<br>`<config directory>/custom_components/lunar_date/__init__.py`
<br>`<config directory>/custom_components/lunar_date/manifest.json`
- configuration.yaml 파일에 설정을 추가합니다. 
- Home Assistant 를 재시작합니다.

### HACS로 설치
- HACS > Integrations 메뉴 선택
- 우측 상단 메뉴 버튼 클릭 후 Custom repositories 선택
- Add Custom Repository URL 에 `https://github.com/GrecHouse/lunar_date` 입력, \
  Category에 `Integration` 선택 후 ADD
- HACS > Integrations 메뉴에서 우측 하단 + 버튼 누르고 `[KR] Luna Date Sensor` 검색하여 설치

<br>

## Usage

### configuration
- HA 설정에 lunar_date 센서를 추가합니다.

```yaml
sensor:
  - platform: lunar_date
```
<br>

**Configuration variables:**

|옵션|값|
|--|--|
|platform|  (필수) lunar_date
|name| (옵션) 센서 이름, 기본값은 lunar_date

<br>

## 버그 또는 문의사항
네이버 카페 [HomeAssistant](https://cafe.naver.com/koreassistant/) `그렉하우스` \
네이버 카페 [모두의스마트홈](https://cafe.naver.com/stsmarthome/) `그렉하우스`

