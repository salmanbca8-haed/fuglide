from __future__ import annotations

import base64
import json
import secrets
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parent
DOCX_PATH = ROOT / 'FU_GLIDE_AIELP_All_47_Students_With_Scores_Updated.docx'
JSON_PATH = ROOT / 'FU_GLIDE_AIELP_All_47_Students_With_Scores.json'
RESULTS_PATH = ROOT / 'results.json'


def calculate_rank(percentage: float) -> str:
    if percentage >= 80:
        return 'TOP LEVEL MANAGER'
    if percentage >= 50:
        return 'MIDDLE LEVEL MANAGER'
    return 'LOW LEVEL MANAGER'


def parse_docx_rows(docx_path: Path):
    with zipfile.ZipFile(docx_path) as archive:
        root = ET.fromstring(archive.read('word/document.xml'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    rows = []
    for tr in root.findall('.//w:tbl//w:tr', ns):
        values = []
        for tc in tr.findall('./w:tc', ns):
            text = ''.join(t.text or '' for t in tc.findall('.//w:t', ns)).strip()
            values.append(text)
        if any(values):
            rows.append(values)
    return rows


def normalize_records_from_docx():
    rows = parse_docx_rows(DOCX_PATH)
    records = []
    for row in rows[1:]:  # skip header row
        if len(row) < 5:
            continue
        _, name, reg_no, unique_id, marks_text = row[:5]
        unique_id = unique_id.strip().upper()
        reg_no = reg_no.strip().upper()
        name = name.strip()
        marks = int(marks_text) if marks_text and marks_text.isdigit() else 0
        percentage = (marks / 75) * 100
        record = {
            'uniqueId': unique_id,
            'regNo': reg_no,
            'name': name,
            'course': 'Fuglide course exam',
            'department': 'MBA',
            'subjects': [
                {'name': 'AIELP', 'maxMarks': 75, 'marks': marks}
            ],
            'summary': {
                'totalMaxMarks': 75,
                'totalMarksObtained': marks,
                'percentage': f'{percentage:.2f}',
                'rank': calculate_rank(percentage),
            }
        }
        records.append(record)
    return records


def derive_key(lookup: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(lookup.encode('utf-8'))


def encrypt_record(record: dict, lookup_id: str) -> dict:
    salt = secrets.token_bytes(16)
    iv = secrets.token_bytes(12)
    key = derive_key(lookup_id.strip().upper(), salt)
    payload = json.dumps(record, ensure_ascii=False).encode('utf-8')
    cipher = AESGCM(key)
    encrypted = cipher.encrypt(iv, payload, None)
    return {
        'salt': base64.b64encode(salt).decode('ascii'),
        'iv': base64.b64encode(iv).decode('ascii'),
        'data': base64.b64encode(encrypted).decode('ascii'),
    }


def generate_encrypted_results(records: list[dict]) -> list[dict]:
    encrypted = []
    for record in records:
        unique_id = str(record.get('uniqueId', '')).strip().upper()
        encrypted.append(encrypt_record(record, unique_id))
        reg_no = str(record.get('regNo', '')).strip().upper()
        if reg_no and reg_no != unique_id:
            encrypted.append(encrypt_record(record, reg_no))
    return encrypted


def main():
    records = normalize_records_from_docx()
    JSON_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')

    encrypted = generate_encrypted_results(records)
    RESULTS_PATH.write_text(json.dumps(encrypted, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Wrote {len(records)} student records to {JSON_PATH.name}')
    print(f'Wrote {len(encrypted)} encrypted lookup entries to {RESULTS_PATH.name}')


if __name__ == '__main__':
    main()
