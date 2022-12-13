from time import sleep

from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


aos_pkg_list = [
        'com.microsoft.office.officehubrow',
        'com.microsoft.office.powerpoint',
        'com.microsoft.office.word',
        'com.microsoft.office.excel',
        'com.microsoft.teams',
        'com.microsoft.skydrive',
        'com.microsoft.sharepoint',
        'com.microsoft.office.outlook',
        'com.microsoft.office.onenote',
        'com.microsoft.stream',
        'com.yammer.v1',
    ]


# 크롬 드라이버 시작후, 구글 계정 로그인
def loginAccount(pkg_nm):

    driver = uc.Chrome()
    driver.get('https://play.google.com/store/apps/details?id=' + pkg_nm)
    driver.implicitly_wait(1)

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, '//*[@id="kO001e"]/header/nav/div/c-wiz/div/div/div[1]/button')
    login_button.click()
    driver.implicitly_wait(1)
    sleep(3)

    # 구글 계정 입력
    account_button = driver.find_element(By.XPATH,
                                         '//*[@id="kO001e"]/header/nav/div/c-wiz/div/div/div[2]/div/ul/li[1]/span[3]')
    account_button.click()
    driver.implicitly_wait(1)
    sleep(3)
    email_input = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    email_input.send_keys('본인 구글계정 기입')
    driver.implicitly_wait(1)
    next_button = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
    next_button.click()
    driver.implicitly_wait(1)
    sleep(3)

    # 비밀번호 입력
    password_input = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    password_input.send_keys('본인 구글 패스워드 기입')
    driver.implicitly_wait(1)
    next_btn = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
    next_btn.click()
    driver.implicitly_wait(1)
    sleep(3)

    # 본인 확인을 위한 번호 정보
    try:
        check_number = driver.find_element(By.XPATH,
                                           '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/span/figure/samp')
        print('check number : ' + check_number.text)
        sleep(10)
    except:
        print('keep going')
    sleep(30)
    # 본인 핸드폰에서 본인 확인 번호 입력
    return driver


# 제일 낮은 버전 선택
def selectMinimumVersion(versions):
    # for version in versions:
    #     print(version.text)
    return versions[1].text


# 제일 낮은 업데이트 날짜 선택
def selectMinimumUpdate(updates):
    # for update in updates:
    #     print(update.text)
    return updates[1].text


# 날짜 포맷 변환
def convertDate(date):
    try:
        ymd_dates = date.split('.')
        yyyy = ymd_dates[0].strip()
        mm = ymd_dates[1].strip()
        dd = ymd_dates[2].strip()

        if int(mm) < 10:
            mm = '0' + mm.strip()

        if int(dd) < 10:
            dd = '0' + dd.strip()

        return yyyy + mm + dd
    except:
        return 'null'


# 앱의 버전정보, 업데이트 일자 등을 크롤링을 통해 가져온다.
def getUpdateInfoWithCrawl(driver, pkg_id):
    driver.get('https://play.google.com/store/apps/details?id=' + pkg_id)
    driver.implicitly_wait(1)

    # 앱 정보 상세 팝업 클릭
    try:
        button = driver.find_element(By.XPATH,
                                     '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[6]/div/section/header/div/div[2]/button')
    except:
        button = driver.find_element(By.XPATH,
                                     '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[2]/button/i')
    button.click()
    sleep(1)
    driver.implicitly_wait(1)

    # 앱 명칭
    names = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[4]/div[2]/div/div/div/div/div[1]/div/div/h5')
    name = names.text
    # 앱 버전
    versions = driver.find_elements(By.XPATH, '//div[text()="버전"]/following-sibling::div')
    version = selectMinimumVersion(versions)
    # 업데이트 날짜
    updates = driver.find_elements(By.XPATH, '//div[text()="업데이트 날짜"]/following-sibling::div')
    update = convertDate(selectMinimumUpdate(updates))
    # 출시 날짜
    try:
        open_dates = driver.find_element(By.XPATH, '//div[text()="출시일"]/following-sibling::div')
        open_date = convertDate(open_dates.text)
    except:
        open_date = '00000000'

    print('name : ' + name)
    print('packageId : ' + pkg_id)
    print('version : ' + version)
    print('openDate : ' + open_date)
    print('upDate : ' + update)
    print('appOs : ' + 'AOS')
    print('')

    # TODO: - 정보 확보 후 처리할 동작 추가


driver = loginAccount(aos_pkg_list[0])
lists = []
for pkg_id in aos_pkg_list:
    getUpdateInfoWithCrawl(driver, pkg_id)


