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
    jitter = random.uniform(0, 120)
    print(f"네트워크 스파이크 방지: {jitter:.2f}초 대기 후 발송을 시작합니다...")
    time.sleep(jitter)

    # 2. 이미지의 내용을 그대로 구현한 본문 텍스트 (마크다운 및 이모지 적용)
    clan_message = """🎮 [707TEAM디코](https://discord.gg/yXKjPdHx)
💬 [707TEAM문의방](https://open.kakao.com/o/gXiK1Edi)
    # 👑707TEAM 클랜 모집합니다~

**정이 많은 클랜 이라 어떤 클랜들 보다 쉽게 어울릴수 있는 장점입니다.**

**또한 서버부스트는 3렙**

## 📌 클랜 기본 안내

• **클랜명 : 707TEAM**
• **게임 : 카배 (배틀그라운드)**
• **활동 : 일반 / 경쟁 / 친목**
• **접속시간 : 오후~ 새벽(오전) 평일 평균 3~5방 돌아감**

## 📌모집조건

1️⃣ 클랜에서 함께 배우며 성장하고 싶으신 분
2️⃣ 게임은 맛있게 수다는 즐겁게 하실 분 (치지)
3️⃣ 랜쿼드 플레이에 지치고 팀플레이를 원하시는 분
4️⃣ 배린이라 게임하기 힘들어 배우고 싶으신분
5️⃣ 클랜 탈퇴 혹은 추방 시 재가입 불가
📌 닉네임 & 클랜마크 변경 필수

## 📌가입제한

1️⃣ 욕설, 비매너, 남탓, 성희롱 하는 사람
2️⃣ 여미새, 남미새, 여왕벌, 철새
3️⃣ 정치질하고 이간질하며 분란조장하는 사람
4️⃣ 사람 가려서 게임하는 사람
(추방 사유에 포함이 된다는 것을 알립니다.)

### 📌클랜 합병 & 연합 문의 받습니다
🎮 다같이 매너 게임합시다!

# 가입은 여기 아래로 ~
⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️
클랜가입문의는 디스코드 가입신청서나 문의방 참여 주세요~

🎮 [707TEAM디코](https://discord.gg/yXKjPdHx)
💬 [707TEAM문의방](https://open.kakao.com/o/gXiK1Edi)
클랜 👑707TEAM 클랜에서
게임을 잘하든 못하든 소중한 인연
함께 만들어 가실 분들 많이 모집합니다.
https://cdn.discordapp.com/attachments/1422956502020522054/1470081769050210531/707-_01.png?ex=69f17d96&is=69f02c16&hm=3012c1fe4083b850427693cddce3b5066748e077f4beeb76c2275c73cf0b64c6&
https://cdn.discordapp.com/attachments/1422956502020522054/1470081784036196627/707-_02.png?ex=69f17d9a&is=69f02c1a&hm=51f12584cfc789ea7991273fa23b535c2958fa48996a63a810c67efac205c78c&
https://cdn.discordapp.com/attachments/1422956502020522054/1470081799223902328/707-_03.png?ex=69f17d9d&is=69f02c1d&hm=228f65c88baafb27df6806db9fe3747061ef0d5f3fc7c9f770513cb27e8ca81c&
"""

    payload = {
        "content": clan_message, 
        "embeds": [],
        "allowed_mentions": {
            "parse": []
        }
    }

    # 4. POST 요청 및 Rate Limit 기초 대응
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        
        if response.status_code in [200, 204]:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 웹훅 발송 성공")
        elif response.status_code == 429:
            retry_after = response.json().get('retry_after', 5)
            print(f"Rate Limit 도달. {retry_after}초 후 재시도가 필요합니다.")
        else:
            print(f"발송 실패 - 상태 코드: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"네트워크 오류 발생: {e}")

if __name__ == "__main__":
    send_promotion()
