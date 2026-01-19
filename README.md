# AMR-Monitoring-System

## 기술 스택

- Backend: FastAPI + Postgres + WebSocket
- Frontend: React + Three.js + WebXR

## 마이그레이션(alembic)

- root 디렉토리로 이동 후 아래의 CLI를 입력
- 본 프로젝트에서는 backend 디렉토리에서 생성

```bash
alembic init migrations

# alembic.ini 파일과 migrations 디렉토리가 생성
```

- `migrations/env.py`과 `alembic.ini`를 수정

- 테이블이 변경되었을 때 업데이트 방법

```bash
cd backend # alembic.ini이 위치한 디렉토리로 이동 필요

alembic revision --autogenerate -m "massage" # 마이그레이션 스크립트 버전 생성

alembic upgrade head # 현 db에 적용
```
