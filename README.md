# makeDB-nndc

이 코드는 NNDC ENSDF 파일을 이용하여 sqlite 데이터베이스를 만드는 코드입니다.
ENSDF 파일에 대한 자세한 설명은 아래 링크를 참조하세요.
[Evaluated Nuclear Structure Data File (ENSDF) Manual](https://www.nndc.bnl.gov/ensdf/ensdf-manual.pdf)

## Environment

- Python 3.12.3
- sqlite3 3.45.3
- NumPy 2.1.3
- (Optional) ROOT 
- NNDC ESNDF file 2024/11/01

## Status

- ENSDF 에서 DECAY 정보 중 다음과 같은 정보를 추출함.

1. Parent Nucl.
	1.1 Mass, Isotope, Decay Mode, Half-life, Spin, Q-value
2. Daughter Nucl.
	2.1 Mass, Isotope
3. Gamma
	3.1 Energy, Intensity
4. Beta(-)
	4.1 End-point Energy, Intensity
5. EC
	5.1 Energy, Beta(+) intensity, EC intensity, Total intensity
6. Alpha
	6.1 Energy, Intensity
7. Delayed
	7.1 Energy, Particle, Intensity, Width

## DB Structure

| Name  | Variable  | details  |
| ----- | ----- | ----- |
| Parent Nucl.  | mother  | XXXYY, (ex. 137CS)  |
| Parent Mass  | mmass  | XXX (ex. 137)  |
| Parent Isotope  | misotope  | YY (ex. CS)  |
| Parent Decay Mode  | decay  | A: alpha, B-: Beta(-) etc  |
| Parent Half-life  | mlife  | Half Life  |
| Parent Half-life D  | mlifeu  | Y: year, D: day, S: second etc...  |
| Parent Spin  | mspin  | J, spin and parity  |
| Parent Q-value  | mqval  | g.s. Q-value in keV, total energy available for g.s. -> g.s. transition |
| Daughter Nucl.  | daughter  | XXXYY  |
| Daughter mass  | dmass  | XXX  |
| Daughter Isotope  | disotope  | YY  |
| Gamma Energy  | gamma  | Gamma Energy (keV)  |
| Gamma Intensity  | gint  | Relative Photon Intensity (%)  |
| Beta End-point Energy | betaend  | Beta End-point Energy (keV)  |
| Beta Intensity  | bint  | Intensity of beta(-) branch (%)  |
| EC Energy  | ec | EC Energy (keV), Given only  |
| EC Intensity  | ecint  | Intensity of Electron Capture branch (%)  |
| EC beta(+) Intensity  | ecbint  | Intensity of beta(+) branch (%)  |
| EC Total Intensity  | ectint  | Total ($\epsilon$ + beta+) decay Intensity (%) |
| Alpha Energy  | alpha  | Alpha Energy (keV)  |
| Alpha Intensity  | aint  | Intensity of Alpha-decay brach in percent of the total Alpha-decay (%)  |
| Delayed Energy | delay | The energy of the Delayed particle (keV) |
| Delayed Particle | dptl | The symbor for the Delayed particle (A=alpha, N=neutron, P=proton) |
| Delayed Intensity | dint | Intensity of the Delayed particles in percent of the total Delayed particle emission (%) |
| Delayed Width | dwidth | Width of the transition (keV) |

- 일부 Symbol을 INFO.md에 정리 하는 중 

## ISSUE

* 비검증 데이터가 포함됨. -> 반드시 NNDC에서 확인 필요.

## Code Usage

코드를 커스텀 할 필요가 없다면, 다운로드 받은 DB 파일을 바로 사용.
DB 사용법 확인.

1. Conda 설치

2. Conda Env

```bash
conda create -n nndc python=3.12.3
```

3. Conda 실행

```bash
conda activate nndc
```

3. SQLite 설치

```bash
conda install -c conda-forge sqlite
```

4. NumPy 설치

```bash
conda install -c conda-forge numpy
```

5. NNDC ENSDF 파일 다운로드

 NNDC ENSDF 파일을 다운받고, 압축 해제 후, makedb.py 파일과 같은 디렉토리에 위치시킨다.

6. Code 수정

 NNDC ENSDF 파일의 경로와 이름을 수정한다.

7. Code 실행

```python
python3 makedb.py
```

## DB 사용법

- DB Browser for SQLite를 이용하여 데이터베이스를 확인할 수 있습니다.

1. SQLITE DB Browser 다운로드 및 설치 [링크](https://sqlitebrowser.org/)
   
2. DB Browser를 실행하고, 해당 DB 파일 연결

3. 해당 DB를 연결한 상태
![dbbrowser1](https://github.com/Jooyoung08/makeDB-nndc/blob/bc1d8b963b19973e04215de9b46237b2ad63e5d0/sqlite-01.png)

4. SQL 실행으로 이동 후, 쿼리문 작성

예제) select * from decay where gamma > 1000 and gamma < 2000

작성 후 실행 클릭 (Ctrl+retur, F5, Ctrl+R)

![dbbrowser2](https://github.com/Jooyoung08/makeDB-nndc/blob/bc1d8b963b19973e04215de9b46237b2ad63e5d0/sqlite-02.png)


---

## Preliminary

ROOT 파일로 만들기 위해서 기존의 코드를 조금 수정하였습니다.
다만 만들어진 ROOT 파일의 크기가 수 기가바이트(GB)를 넘어가기 때문에 사용에 주의가 필요합니다.
(DB파일의 경우 수 메가바이트(MB))

### (ROOT) Code Usage

같은 환경에 ROOT를 설치합니다.

```bash
conda install -c conda-forge root
```

그 후에 root_makedb.py 파일을 실행합니다.

```python
python3 root_makedb.py
```

ROOT 파일 실행

```sh
root root-nndc-20241101.root
```
