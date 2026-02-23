import asyncio, time, csv
from aiocoap import Context, Message, PUT

KEY = "1dcdbff4c6fb0d47e6bea745d3033bad4c8b2166ff6c1408b2bd52a162a594d6"

def xor_encode(data: str) -> bytes:
    return "".join(chr(ord(ch) ^ ord(KEY[i % len(KEY)])) for i, ch in enumerate(data)).encode()

async def one_request(ctx):
    t1 = time.strftime("%H:%M:%S")
    line = f"idN,ctxN,capA,idT,ctxT,Gtype,{t1}"
    req = Message(code=PUT, payload=xor_encode(line), uri="coap://localhost/auth")
    await ctx.request(req).response

async def main(n=50, out="bench_processing_time_ms.csv"):
    ctx = await Context.create_client_context()
    times = []
    try:
        # warmup
        for _ in range(5):
            await one_request(ctx)

        for _ in range(n):
            t0 = time.perf_counter()
            await one_request(ctx)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000.0)
    finally:
        await ctx.shutdown()

    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["i", "processing_time_ms"])
        for i, ms in enumerate(times):
            w.writerow([i, f"{ms:.3f}"])

    print(f"Wrote {out} with {len(times)} samples.")
    print(f"min={min(times):.3f} ms, median={sorted(times)[len(times)//2]:.3f} ms, max={max(times):.3f} ms")

if __name__ == "__main__":
    asyncio.run(main())