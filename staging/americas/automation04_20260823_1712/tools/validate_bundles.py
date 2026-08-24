#!/usr/bin/env python3
import json,gzip,base64,hashlib,sys
for f in sys.argv[1:]:
 w=json.load(open(f,encoding="utf-8")); raw=gzip.decompress(base64.b64decode(w["payload_base64"])); assert hashlib.sha256(raw).hexdigest()==w["uncompressed_sha256"]; rows=[json.loads(x) for x in raw.decode("utf-8").splitlines() if x.strip()]; assert len(rows)==w["rows"]; print(f, len(rows), "OK")
