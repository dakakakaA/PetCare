#!/usr/bin/env python3
"""Импорт 60 Use Cases в GitHub Issues. Переменные: GITHUB_TOKEN, GITHUB_REPOSITORY=owner/repo."""
import json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path
FILE=Path(__file__).with_name("60_USE_CASES.md")
RX=re.compile(r"^\s*(\d+)\.\s+\[UC-(\d{2})\](\s+\[MVP\])?\s+Как\s+(.+?)\.\s*$")
def parse():
    rows=[]
    for line in FILE.read_text(encoding="utf-8").splitlines():
        m=RX.match(line)
        if m: rows.append((int(m.group(1)),m.group(2),bool(m.group(3)),m.group(4)))
    if len(rows)!=60: raise ValueError(f"Ожидалось 60 историй, найдено {len(rows)}")
    if [r[0] for r in rows]!=list(range(1,61)): raise ValueError("Номера должны идти от 1 до 60 без пропусков")
    if sum(r[2] for r in rows)!=20: raise ValueError(f"Ожидалось 20 [MVP], найдено {sum(r[2] for r in rows)}")
    return rows
def call(method,url,token,payload=None):
    data=json.dumps(payload).encode() if payload is not None else None
    req=urllib.request.Request(url,data=data,method=method,headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"PetCare-UseCase-Uploader","Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"GitHub API HTTP {e.code}: {e.read().decode(errors='replace')}") from e
def main():
    token=os.getenv("GITHUB_TOKEN"); repo=os.getenv("GITHUB_REPOSITORY")
    if not token or not repo or "/" not in repo:
        print("Задайте GITHUB_TOKEN и GITHUB_REPOSITORY=owner/repository",file=sys.stderr);return 2
    rows=parse();base=f"https://api.github.com/repos/{repo}/issues"
    existing=set();page=1
    while True:
        data=call("GET",f"{base}?state=all&per_page=100&page={page}",token)
        if not data: break
        for issue in data:
            if "pull_request" in issue: continue
            m=re.match(r"UC-(\d{2}):",issue.get("title",""))
            if m: existing.add(m.group(1))
        if len(data)<100: break
        page+=1
    created=skipped=0
    for n,code,mvp,story in rows:
        if code in existing:
            print(f"Пропуск UC-{code}: уже есть issue");skipped+=1;continue
        body=f"**Пользовательская история**\n\nКак {story}.\n\n**Приоритет:** {'MVP' if mvp else 'После MVP'}\n**Источник:** `docs/60_USE_CASES.md`\n**Идентификатор:** `UC-{code}`"
        payload={"title":f"UC-{code}: {story[:160]}","body":body}
        try:
            result=call("POST",base,token,payload)
        except RuntimeError as exc:
            print(exc,file=sys.stderr);return 1
        print(f"Создан issue #{result.get('number')}: UC-{code}")
        created+=1;time.sleep(.15)
    print(f"Готово. Создано: {created}; пропущено: {skipped}; всего историй: {len(rows)}.")
    return 0
if __name__=="__main__": raise SystemExit(main())
