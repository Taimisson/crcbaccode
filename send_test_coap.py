import asyncio
import time
from aiocoap import Context, Message, PUT

KEY = "1dcdbff4c6fb0d47e6bea745d3033bad4c8b2166ff6c1408b2bd52a162a594d6"

def xor_encode(data: str) -> str:
    return "".join(chr(ord(ch) ^ ord(KEY[i % len(KEY)])) for i, ch in enumerate(data))

def xor_decode(data: str) -> str:
    return "".join(chr(ord(ch) ^ ord(KEY[i % len(KEY)])) for i, ch in enumerate(data))

async def main():
    t1 = time.strftime("%H:%M:%S")
    line = f"idN,ctxN,capA,idT,ctxT,Gtype,{t1}"
    payload = xor_encode(line).encode()

    ctx = await Context.create_client_context()
    try:
        req = Message(code=PUT, payload=payload, uri="coap://localhost/auth")
        resp = await ctx.request(req).response
        decoded = xor_decode(resp.payload.decode())

        print("=== Response (decoded) ===")
        print(decoded)
    finally:
        # Fecha sockets/transports do aiocoap antes de fechar o loop (evita o warning)
        await ctx.shutdown()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())