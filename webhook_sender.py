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
        "content": "", 
        "embeds": [
            {
                "title": "👑 707TEAM 클랜 신규 멤버 대모집 (카카오 배틀그라운드)",
                "description": "클랜 👑707TEAM 클랜에서 게임을 잘하든 못하든 소중한 인연 함께 만들어 가실 분들 많이 모집합니다. 707TEAM 클랜 모집합니다~\n\n정이 많은 클랜이라 어떤 클랜들 보다 쉽게 어울릴 수 있는 장점입니다. (현재 서버부스트는 3렙 🚀)\n\n📌 **[707TEAM 디스코드 가입신청 및 문의방 참여](https://discord.gg/yXKjPdHx)**\n💬 **[카카오톡 오픈채팅 가입문의](https://open.kakao.com/o/gXiK1Edi)**\n\n다같이 매너 게임합시다! 가입은 위 링크를 통해 디스코드나 카톡 문의방으로 와주세요~",
                "color": 0xF1A60A,
                "fields": [
                    {
                        "name": "📝 클랜 기본 안내",
                        "value": "• **클랜명** : 707TEAM\n• **게임** : 카배 (배틀그라운드)\n• **활동** : 일반 / 경쟁 / 친목\n• **접속시간** : 오후~ 새벽(오전) 평일 평균 3~5방 돌아감",
                        "inline": False
                    },
                    {
                        "name": "⭕ 모집조건",
                        "value": "• 클랜에서 함께 배우며 성장하고 싶으신 분\n• 게임은 맛있게 수다는 즐겁게 하실 분 (치지)\n• 랜쿼드 플레이에 지치고 팀플레이를 원하시는 분\n• 배린이라 게임하기 힘들어 배우고 싶으신 분\n\n*※ 닉네임 & 클랜마크 변경 필수 (탈퇴 혹은 추방 시 재가입 불가)*",
                        "inline": False
                    },
                    {
                        "name": "❌ 가입제한 (추방 사유에 포함됩니다)",
                        "value": "• 욕설, 비매너, 남탓, 성희롱 하는 사람\n• 여미새, 남미새, 여왕벌, 철새\n• 정치질하고 이간질하며 분란조장하는 사람\n• 사람 가려서 게임하는 사람",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "클랜 합병 & 연합 문의 받습니다"
                },
                "image": {
                    "url": "https://cdn.discordapp.com/attachments/1422956502020522054/1470081769050210531/707-_01.png?ex=69f17d96&is=69f02c16&hm=3012c1fe4083b850427693cddce3b5066748e077f4beeb76c2275c73cf0b64c6&"
                }
            },
            # 두 번째 이미지 객체
            {
                "color": 0xF1A60A,
                "image": {
                    "url": "https://cdn.discordapp.com/attachments/1422956502020522054/1470081784036196627/707-_02.png?ex=69f17d9a&is=69f02c1a&hm=51f12584cfc789ea7991273fa23b535c2958fa48996a63a810c67efac205c78c&"
                }
            },
            # 세 번째 이미지 객체
            {
                "color": 0xF1A60A,
                "image": {
                    "url": "https://cdn.discordapp.com/attachments/1422956502020522054/1470081799223902328/707-_03.png?ex=69f17d9d&is=69f02c1d&hm=228f65c88baafb27df6806db9fe3747061ef0d5f3fc7c9f770513cb27e8ca81c&"
                }
            }
        ],
        # 3. AutoMod 및 멘션 스팸 필터링 회피 메커니즘
        "allowed_mentions": {
            "parse": []
        }
    },
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
