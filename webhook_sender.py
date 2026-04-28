import os
import time
import random
import requests
from datetime import datetime

# GitHub Secrets에서 주입받을 웹훅 URL
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send_promotion():
    if not WEBHOOK_URL:
        print("Error: DISCORD_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return

    # 1. 트래픽 분산 스파이크 제어 (Random Jitter)
    # 정각에 몰리는 트래픽을 방지하기 위해 0초에서 120초(2분) 사이의 무작위 대기 시간 부여
    jitter = random.uniform(0, 120)
    print(f"네트워크 스파이크 방지: {jitter:.2f}초 대기 후 발송을 시작합니다...")
    time.sleep(jitter)

    # 2. 임베드 메시지 최적화 (6,000자 제한 준수 및 시각적 브랜딩)
    payload = {
        "content": "", # 텍스트 본문은 비우고 임베드에 집중
        "embeds": [
            {
                "title": "DANBAM 사전 수요 알림 및 메가 이벤트",
                "description": "BCG 생체 신호 기반 실시간 능동 제어 시스템, 2세대 로보틱스 베개를 가장 먼저 만나보세요.\n\n확보된 특별 트래픽 한정 혜택은 [자사몰 공식 페이지](https://example.com)에서 확인하실 수 있습니다.",
                "color": 0x2B2D31,  # 다크 테마에 어울리는 세련된 헥스 컬러
                "fields": [
                    {
                        "name": "🚀 다가오는 일정",
                        "value": "2026년 10월 크라우드 펀딩 오픈 예정",
                        "inline": True
                    },
                    {
                        "name": "💡 핵심 가치",
                        "value": "수면을 중시하는 세노이 부족의 철학을 담은 설계",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "DANBAM Official 알림 시스템"
                }
            }
        ],
        # 3. AutoMod 및 멘션 스팸 필터링 회피 메커니즘
        "allowed_mentions": {
            "parse": [] # 어떠한 멘션(@everyone 등)도 실제 푸시 알림으로 트리거되지 않도록 강제 차단
        }
    }

    # 4. POST 요청 및 Rate Limit 기초 대응
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        
        if response.status_code in [200, 204]:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 웹훅 발송 성공")
        elif response.status_code == 429:
            # 429 에러 발생 시 헤더의 Retry-After 파싱
            retry_after = response.json().get('retry_after', 5)
            print(f"Rate Limit 도달. {retry_after}초 후 재시도가 필요합니다.")
        else:
            print(f"발송 실패 - 상태 코드: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"네트워크 오류 발생: {e}")

if __name__ == "__main__":
    send_promotion()