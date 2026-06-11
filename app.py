import asyncio
import websockets
import json

# 접속한 사용자들을 관리할 집합
connected_clients = set()

async def chat_handler(websocket):
    # 1. 새로운 사람이 들어오면 로그를 찍습니다.
    connected_clients.add(websocket)
    print(f"📡 [접속 발생] 새로운 사용자가 연결되었습니다. (현재 접속자: {len(connected_clients)}명)")
    
    try:
        async for message in websocket:
            # 2. 누군가 메시지를 보내면 서버 터미널에 로그를 출력합니다.
            try:
                data = json.loads(message)
                print(f"💬 [메시지 수신] ID: {data.get('id')} -> 내용: {data.get('text')}")
            except Exception:
                print(f"💬 [메시지 수신] 원본 데이터: {message}")

            # 접속한 모든 사람에게 전달
            for client in connected_clients:
                await client.send(message)
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # 3. 누군가 창을 닫고 나가면 로그를 찍습니다.
        connected_clients.add(websocket) # 에러 방지용 안전장치
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"❌ [접속 종료] 사용자가 나갔습니다. (현재 접속자: {len(connected_clients)}명)")

async def main():
    async with websockets.serve(chat_handler, "0.0.0.0", 8765):
        print("🚀 가벼운 채팅 서버가 실행되었습니다! (포트 8765)")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())