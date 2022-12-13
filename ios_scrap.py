
import json
import ssl

from bs4 import BeautifulSoup
import requests
from datetime import datetime

# iOS 앱 아이디 목록
app_id_list = [
    '541164041',  # microsoft-office
    '586449534',  # microsoft-powerpoint
    '586447913',  # microsoft-word
    '586683407',  # microsoft-excel
    '1113153706',  # microsoft-teams
    '477537958',  # microsoft-onedrive
    '1091505266',  # microsoft-sharepoint
    '951937596',  # microsoft-outlook
    '410395246',  # microsoft-onenote
    '1401013624',  # microsoft-stream
    '289559439',  # yammer
]


# 시간 포맷 변경
def convertDate(date_str):
    real_date = datetime.strptime(date_str.replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')
    return real_date.strftime("%Y%m%d")


# 앱 데이터 요청
def requestAppData():
    # SSL 통신 혀용
    ssl._create_default_https_context = ssl._create_unverified_context
    # SSL인증서 확인 무시, 경고 표시 없애기
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    for app_id in app_id_list:
        request_url = 'http://itunes.apple.com/kr/lookup?id=' + app_id
        source_code = requests.get(request_url, verify=False)
        html = source_code.text.encode('utf-8', 'replace')
        soup = BeautifulSoup(html, "html.parser")
        json_object = json.loads(str(soup))
        # resultJson = json.dumps(jsonObject, indent="\t", ensure_ascii=False)
        # print(resultJson)

        for j_key, j_value in json_object.items():
            if j_key == 'results':
                for key, value in j_value[0].items():
                    if key == 'trackName':
                        name = value
                    if key == 'bundleId':
                        bundle_id = value
                    if key == 'version':
                        version = value
                    if key == 'releaseDate':
                        open_date = convertDate(value)
                    if key == 'currentVersionReleaseDate':
                        update = convertDate(value)

        print('id : ' + app_id)
        print('name : ' + name)
        print('bundleId : ' + bundle_id)
        print('version : ' + version)
        print('update : ' + update)
        print('openDate : ' + open_date)
        print('appOs : ' + 'IOS')
        print()

        # TODO: - 정보 확보 후 처리할 동작 추가


requestAppData()
