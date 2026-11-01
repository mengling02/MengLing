import hashlib, subprocess

OPENSSL = r"C:\Users\17700\AppData\Local\Programs\WorkBuddyAI\resources\vendor\PortableGit\usr\bin\openssl.exe"
pws = ["elfstudy", "ELFStudy", "ELFStudy1.4.2", "elfstudy1.4.2", "1.4.2",
       "ELF structure inspector", "flag", "secret", "key", "password",
       "elfstudy2026", "ELFStudy2026", "elf", "ELF64", "structure", "inspector"]

modes = ["-aes-128-ecb", "-aes-128-cbc", "-aes-128-ctr", "-aes-128-cfb", "-aes-128-ofb",
         "-aes-256-ecb", "-aes-256-cbc", "-aes-256-ctr", "-aes-256-cfb", "-aes-256-ofb"]

res = []
for pw in pws:
    md5 = hashlib.md5(pw.encode()).hexdigest()
    sha = hashlib.sha256(pw.encode()).hexdigest()
    for key in (md5, sha):
        klen = len(key) * 4
        for m in modes:
            need = 128 if "128" in m else 256
            if klen < need:
                continue
            args = [OPENSSL, "enc", "-d", m, "-K", key, "-nopad", "-in", "blob816.bin"]
            if "ecb" not in m:
                args += ["-iv", "00" * 16]
            p = subprocess.run(args, capture_output=True)
            out = p.stdout
            if not out:
                continue
            r = sum(1 for c in out if 32 <= c < 127) / len(out)
            res.append((r, pw, m, key[:8], out.decode("latin1")))
res.sort(reverse=True)
for r, pw, m, k, t in res[:8]:
    print(f"{r:.2f} {pw:24s} {m:14s} key={k} {t[:60]!r}")
print("total", len(res))
