# makeDB-nndc

이 코드는 NNDC ENSDF 파일을 이용하여 sqlite 데이터베이스를 만드는 코드입니다.

## Environment

- Python 3.12.3
- sqlite3 3.45.3
- NNDC ESNDF file 2024/05/01 (https://www.nndc.bnl.gov/ensdfarchivals/)

## DB Usage

- DB Browser for SQLite (https://sqlitebrowser.org/) 를 이용하여 데이터베이스를 확인할 수 있습니다.

## DB Structure

| Name  | Variable  | details  |
| ----- | ----- | ----- |
| Parent Nucl.  | mother  | XXXYY, (ex. 137CS)  |
| Parent Mass  | mmass  | XXX (ex. 137)  |
| Parent Isotope  | misotope  | YY (ex. CS)  |
| Parent Decay Mode  | dmode  | A: alpha, B: Beta etc  |
| Parent Half-life  | hlife  | Half Life  |
| Parent Half-life D  | hlifed  | Dim, Y: year, D: day, S: second etc...  |
| Parent Spin  | spin  | J, spin and parity  |
| Parent Q-value  | qval  | g.s. Q-value in keV, total energy available for g.s. -> g.s. transition |
| Daughter Nucl.  | daughter  | XXXYY  |
| Daughter mass  | dmass  | XXX  |
| Daughter Isotope  | disotope  | YY  |
| Gamma Energy  | genergy  | Gamma Energy (keV)  |
| Gamma Intensity  | gint  | Gamma Intensity (%)  |
| Beta End-point Energy | bendenergy  | Beta End-point Energy (keV)  |
| Beta Ave. Energy  | baveenergy  | Beta Ave. Energy (keV)  |
| Beta Intensity  | bint  | Intensity of beta- branch (%)  |
| EC Energy  | ecenergy  | EC Energy (keV), Given only  |
| EC beta+ Intensity  | ecbpint  | Intensity of beta+ branch (%)  |
| EC Intensity  | ecint  | Intensity of EC branch (%)  |
| EC Total Intensity  | ectotint  | Total ($\epsilon$ + beta+) decay Intensity (%) |
| EC Ave. Energy  | ecaveenergy  | EC Ave. Energy (keV)  |
| Alpha Energy  | aenergy  | Alpha Energy (keV)  |
| Alpha Intensity  | aint  | Alpha Intensity (%)  |

## ISSUE

* 비검증 데이터가 포함됨. -> 반드시 NNDC에서 확인 필요.

* "0" 으로 표기된 데이터는 일반적으로 "NULL"을 의미.

* X-ray는 해당 DB에 미포함.

## Code Usage

자세한 사항은 코드 참조.

```python
python3 makedb.py
```
