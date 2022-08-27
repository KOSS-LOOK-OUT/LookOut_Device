<p align="center">
  <img src="imgs/logo2.png" width="30%"/>
  <br>
</p>

LookOut
==================================

화재나 교통사고 등 위험 상황 발생 시 상황을 소리로 인지하지 못하여 피해를 보는 청각장애인들이 많습니다. 청각장애인들이 아니어도 노이즈 캔슬링 이어폰이나 시끄러운 실내에서 위험 상황을 뒤늦게 알아차리고 제대로 대처가 안되는 경우가 발생하기도 합니다. 이러한 상황에 대한 해결책으로는 주변의 소리를 인식 및 분류하여 위험 상황일 경우 사용자에게 스마트폰 알림을 주는 애플리케이션이 있습니다. 하지만 "조심해", "불이야"와 같은 말소리를 인식하여 사용자에게 정보를 제공하기 어렵다는 문제점이 있습니다. 

LookOut은 청각장애인을 위한 인공지능 음성 기반 위험 안내 어플입니다. LookOut은 라즈베리 파이를 활용하여 가정이나 실내 장소에 설치 가능한 기기를 만듭니다. 특정 음성 키워드가 인식되었을 경우 어플리케이션 서버에 감지된 키워드 정보를 전달합니다. 
사용자는 위험상황이 발생하였거나 등록되어있는 특정 음성이 인식이 되었을 경우 스마트폰과 워치를 통해 알림을 받을 수 있습니다.

Quick Start
-----------
### Installation

use virtual environment

- Window
```shell
$ python -m venv myenv
$ myenv/Scripts/activate
```

- Linux/Mac
```shell
$ python -m venv myenv
$ source myenv/Scripts/activate
```


install dependencies
```shell
git clone https://github.com/KOSS-LOOK-OUT/LookOut_Device.git
cd LookOut_Device
pip install -r requirements.txt
```

You need to make .env file in root directory
```python
# .env

DATABASE_URL=firebase_realtime_db_url
GOOGLE_APPLICATION_CREDENTIALS=google_service_account_file_path

```

