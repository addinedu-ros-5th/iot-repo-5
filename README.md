# 자동으로 식물의 성장 환경을 제어해주는 스마트팜
## 01. 프로젝트 개요
* 식물의 성장에 맞는 온도, 습도, 물, 빛을 자동으로 공급해준다.
* 사용자는 실시간으로 현재 상황을 관찰하고 설정을 변경할 수 있다.
* 사용자는 내부를 촬영한 사진에 코멘트를 달아 저장할 수 있다.
## 02. 프로젝트 목표
* 실시간으로 여러가지 액추에이터들을 동시에 작동시킨다.
* PyQt를 이용해 만든 GUI와 시리얼 통신을 통해 사용자가 현재 상황들을 쉽게 확인하고 조작할 수 있게 한다.
* 클라우드 데이터베이스에 여러가지 환경데이터들을 보관하고 실시간으로 불러와서 적용시킨다.
* github, jira, confluence를 사용해 협업 환경을 만들고 사용해본다.

## 03. 팀소개
### 팀명 FARM FRIENDS
|이름|역할|
|:---:|:---:|
|김세현|팀장, 하드웨어 제작, 통신 프로토콜 작성, MCU 코드 제작, 발표, ReadMe 제작|
|김준영|GUI제작, PC 제어, 통신코드 제작|
|이민영|DB 제작, 자료조사, GUI제작, 다이어리 제작코드 제작|
|조성오|협업툴 구성, 발표자료 제작, 시스템 구성도 제작|
## 04. 기술스택
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"> <img src="https://img.shields.io/badge/amazonrds-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">


## 5. 시스템 구성
### 5-1 기능리스트
![image](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/dc6c1ae5-5667-4b34-8b18-163b73b0a2ff)
### 5-2 시스템 구성도
![image](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/2aac719a-8b6f-49eb-8eaf-3a25ed6f8d91)
### 5-3 하드웨어 구성도
![image](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/5c75b869-7b65-4b3b-b24e-f14cde7652da)
### 5-4 소프트웨어 구성도
![image](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/bc4be3cf-405b-40ff-8e93-1163b7985167)
## 06. 제작 결과
### 6-1 스마트팜 본체
![20240425_101344](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/680a0672-2da0-4c84-9103-9b590693cbe8)
### 6-2 본체 내부
![20240425_101304](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/0a83edb9-a5f2-4e81-aba8-e3f794ed1e60)
### 6-3 현재상태 관찰 화면
![image](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/d22ddd94-b268-4e09-9c43-ddcf79d9e7dc)
아무것도 선택 안된 상태 - 환경제어를 하지 않고 있다.
![image](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/20634130-0abc-408b-8734-c6bb98c3bbdc)
식물을 선택하고 제어하는 상태 - 목표 온도, 습도를 맞추기 위해 내부를 쿨링하고 가습을 하고 있다.

### 6-4 환경설정 선택화면
![image](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/ac071993-3d23-41f3-8028-1dba5cec89ee)
### 6-5 일기 작성화면
![image](https://github.com/addinedu-ros-5th/iot-repo-5/assets/55865857/1415c382-759b-4403-8469-a25f991ea984)
## 07. 프로젝트 기간
2024.4.17(수) ~ 2024.4.25(목)

