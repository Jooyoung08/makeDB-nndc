# makeDB-nndc

이 코드는 NNDC ENSDF 파일을 이용하여 sqlite 데이터베이스를 만드는 코드입니다.
ENSDF 파일에 대한 자세한 설명은 아래 링크를 참조하세요.
[Evaluated Nuclear Structure Data File (ENSDF) Manual](https://www.nndc.bnl.gov/ensdf/ensdf-manual.pdf)

## Environment

- Python 3.12.3
- sqlite3 3.45.3
- NumPy 2.1.3
- (Optional) ROOT 
- NNDC ESNDF file 2024/05/01
- NNDC ESNDF file 2024/11/01

## DB Usage

- DB Browser for SQLite (https://sqlitebrowser.org/) 를 이용하여 데이터베이스를 확인할 수 있습니다.

## DB Structure

| Name  | Variable  | details  |
| ----- | ----- | ----- |
| Parent Nucl.  | mother  | XXXYY, (ex. 137CS)  |
| Parent Mass  | mmass  | XXX (ex. 137)  |
| Parent Isotope  | misotope  | YY (ex. CS)  |
| Parent Decay Mode  | decay  | A: alpha, B-: Beta(-) etc  |
| Parent Half-life  | life  | Half Life  |
| Parent Half-life D  | lifeu  | Y: year, D: day, S: second etc...  |
| Parent Spin  | spin  | J, spin and parity  |
| Parent Q-value  | qval  | g.s. Q-value in keV, total energy available for g.s. -> g.s. transition |
| Daughter Nucl.  | daughter  | XXXYY  |
| Daughter mass  | dmass  | XXX  |
| Daughter Isotope  | disotope  | YY  |
| Level | level | Energy level of the daughter nuclide (keV) |
| Level Spin  | l_spin  | Spin |
| Gamma Energy  | gamma  | Gamma Energy (keV)  |
| Gamma Intensity  | g_rint  | Relative Photon Intensity (%)  |
| Gamma Multipolarity  | g_mtrans  | Multipolarity of transition |
| Gamma Mixing Ratio  | g_mratio  | Mixing Ratio  |
| Gamma Conversion Coefficient | g_tconv | Total Conversion Coefficient  |
| Gamma Relative Total Transition Intensity | g_rttint | Relative Total Transition Intensity (%)  |
| Gamma Others | gDTYPE | Other gamma data (KC : Theoretical K- conversion coefficient etc) |
| Gamma Others | gDTYPEv | Value of other gamma data |
| Beta End-point Energy | beta_end  | Beta End-point Energy (keV)  |
| Beta Ave. Energy  | beta_ave | Beta Ave. Energy (keV)  |
| Beta Intensity  | b_int  | Intensity of beta(-) branch (%)  |
| Beta Logft | b_logft | The log ft for the beta(-) transition |
| EC Energy  | ec | EC Energy (keV), Given only  |
| EC Intensity  | ec_int  | Intensity of Electron Capture branch (%)  |
| EC beta(+) Intensity  | ec_bint  | Intensity of beta(+) branch (%)  |
| EC Total Intensity  | ec_tint  | Total ($\epsilon$ + beta+) decay Intensity (%) |
| EC Logft | ec_logft | The log ft for ($\epsilon$ + beta+) transition |
| EC Others | ecDTYPE | Other EC data |
| EC Others | ecDTYPEv | Value of other ec data |
| Alpha Energy  | alpha  | Alpha Energy (keV)  |
| Alpha Intensity  | a_int  | Intensity of Alpha-decay brach in percent of the total Alpha-decay (%)  |
| Alpha Hindrance Factor | a_hf | Hindrance Factor for Alpha-decay |
| Delayed Energy | delayed | The energy of the Delayed particle (keV) |
| Delayed Particle | d_particle | The symbor for the Delayed particle (A=alpha, N=neutron, P=proton) |
| Delayed Intensity | d_int | Intensity of the Delayed particles in percent of the total Delayed particle emission (%) |
| Delayed Energy Level | d_elevel | Energy of the level in the 'intermediate' (mass=A+1 for n, p; A+4 for Alpha) nuclide in case of Delayed particle |
| Delayed Width | d_width | Width of the transition (keV) |
| Delayed Angular Momentum | d_ang | Angular Momentum transfer of the emitted particle |

## ISSUE

* 비검증 데이터가 포함됨. -> 반드시 NNDC에서 확인 필요.

## Code Usage

자세한 사항은 코드 참조.

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
