LookOut_Device
==================================

LookOut은 청각장애인을 위한 음성 기반 위험 안내 어플입니다. Look Out은 라즈베리 파이를 활용하여 가정이나 실내 장소에 설치 가능한 기기를 만듭니다. 특정 음성이 인식되었을 경우 어플리케이션 서버에 감지된 키워드 정보를 전달합니다. 
사용자는 위험상황이 발생하였거나 등록되어있는 특정 음성이 인식이 되었을 경우 스마트폰과 워치를 통해 알림을 받을 수 있습니다.

Quick Start
-----------
### Installation

use virtual environment
```shell
python -m venv myenv
myenv/Scripts/activate
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
