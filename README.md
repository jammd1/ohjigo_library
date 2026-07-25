# Oh-ji-go · Austrian Library

> 한국외국어대학교 서울캠퍼스 본관 301호 **오스트리아 도서관**(독어과 귀속)의 디지털화 프로젝트
> Digitizing a German-language departmental library — replacing an analog catalog & paper loan ledger with a full web service.

![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
<!-- TODO: add your frontend badge — e.g. React / Vanilla JS / Django Templates -->

HUFS H-UP 10th · Team project (박재민, 장지수, 양수찬)

---

## Background

The Austrian Library holds ~5,000 German-language volumes donated by the Austrian Embassy in 1982 — one of the few German-studies specialist collections in Korea. Its day-to-day operation was still fully analog:

- **Catalog** — the entire book list lived in a *single Excel file* on the library PC
- **Loans** — checkouts and returns were written by hand in a *paper ledger*, causing frequent mix-ups
- **Discovery** — the library had no web presence, so almost no one outside the department knew it existed

Oh-ji-go digitizes all three: a searchable catalog, an online loan/status system, and a public homepage.

## Features

- 🔎 **Catalog search** — filter by language, field, and availability; shows call number, author, field, location, and loan status
- 👤 **Membership & login** — student ID + role (undergrad / grad / faculty) based accounts
- 📚 **Loan status** — check a book's availability and loan history online (on-site checkout at the library)
- 🏛 **Library info & rules** — hours, location, loan limits, and donation guide

### ML / automation (team feature)

- 🤖 **Book-field classification** — an **mBERT** model fine-tuned on the Berlin City Library open dataset to auto-classify books into fields (Geschichte / Literatur / Sozialwissenschaften / Sprachwissenschaft). **Macro F1: 0.7284**
- 🏷 **Automated call-number generation** — normalizes German text (Ä/Ü/Ö/ß → AE/UE/OE/SS), hashes title + author via `hashlib`, converts hex→dec with fixed-width modulo, and resolves duplicates by order — producing unique call numbers without manual effort

## Architecture

Data model (ERD):

- **MEMBER** — students/faculty accounts, status, activity
- **MANAGER** — staff accounts with management roles
- **BOOK** — title, author, call number (UK), field, available copies, status
- **LOAN** — member ↔ book loans, loan/due/return dates, overdue days
- **NOTICE** — library announcements

Relations: a MEMBER *borrows* BOOKs (LOAN), a MANAGER *processes* loans and *registers/modifies* BOOKs and *posts* NOTICEs.

## Tech Stack

| Layer | Stack |
| --- | --- |
| Backend | Django, Python |
| Database | *(relational — see ERD)* |
| Frontend | *(see `/frontend`)* |
| ML | mBERT (HuggingFace Transformers) |

## Getting Started

```bash
# clone
git clone https://github.com/jammd1/ohjigo_library.git
cd ohjigo_library/backend

# environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r ../requirements.txt

# database & run
python manage.py migrate
python manage.py runserver
```

<!-- TODO: adjust paths/commands to match your actual setup, and add frontend run steps -->

## Project Structure

```
ohjigo_library/
├── backend/        # Django app — models, views, APIs
├── frontend/       # web client
└── requirements.txt
```

## Contributors

| | Role |
| --- | --- |
| **장지수** ([@jsjang0104](https://github.com/jsjang0104)) | mBERT classification model & call-number generation logic & Frontend |
| **박재민** ([@jammd1](https://github.com/jammd1)) | Database design (ERD) & Django backend logic |
| **양수찬** ([@EricYang544](https://github.com/EricYang544)) | mBERT classification model & call-number generation logic  |
