import numpy as np
import requests, urllib3
from dataclasses import dataclass
from bs4 import BeautifulSoup
from main.exceptions import InvalidCaptcha, RevalNotApplied, SerialNumberNotAvailable
from cv2.typing import MatLike
import cv2 as cv
import pytesseract
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



@dataclass
class StudentResultInfo:
    name: str
    usn: str


@dataclass
class SubjectResultInfo:
    sem: str
    code: str
    name: str
    internal: str
    external: str
    total: str
    result: str
    announced_on: str


@dataclass
class RevaluationSubjectInfo:
    sem:str
    code:str
    name:str
    internal:str
    old_marks:str
    old_result:str
    new_marks:str
    new_result:str
    final_marks:str
    final_result:str


class ResultAPI:
    BASE_URL = "https://results.vtu.ac.in"

    def __init__(self, result_code=None) -> None:
        self.result_code = result_code
        self.result_url = f"{self.BASE_URL}/{self.result_code}/index.php"
        self.captcha_url = f"{self.BASE_URL}/captcha/vtu_captcha.php?_CAPTCHA"
        self.result_post_url = f"{self.BASE_URL}/{self.result_code}/resultpage.php"

    def get_page(self):
        response = requests.get(self.result_url, verify=False)
        self.cookies = response.cookies.get_dict()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        token_input = soup.find('input', {'name': 'Token'})

        token_value = token_input['value'] if token_input else None
        return token_value

    def get_captcha_image(self, cookies):
        res = requests.get(self.captcha_url, verify=False, cookies=cookies)
        return res.content

    def get_result(self, token_value, captcha, usn, cookies):
        res = requests.post(self.result_post_url, data={
            "Token": token_value,
            "captchacode": captcha,
            "lns": usn
        }, cookies=cookies, verify=False)

        if res.status_code == 200:
            if "University Seat Number is not available or Invalid" in res.text:
                raise SerialNumberNotAvailable("University Seat Number is not available or Invalid..!")
            elif "Invalid captcha code" in res.text:
                raise InvalidCaptcha("Invalid captcha code")
            elif "You have not applied for reval or reval results are awaited" in res.text:
                raise RevalNotApplied("You have not applied for reval or reval results are awaited !!!")
            else:
                return res.text
        else:
            return None
        
    def pre_process(self, img:MatLike):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (5, 5), 0)    
        _, thresh = cv.threshold(blur, 150, 255, cv.THRESH_BINARY_INV)
        kernel = np.ones((2, 2), np.uint8)
        processed_img = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
        return processed_img
    
    def pred_captcha(self, processed_img:MatLike):
        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        text:str = pytesseract.image_to_string(processed_img, lang='eng', config=config).strip()
        return "".join(text.split(" "))
        


class Parser:
    def __init__(self, html_content) -> None:
        self.html = html_content
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.is_reval = "UPDATED RESULTS AFTER REVALUATION" in self.html

    def get_student_info(self):
        try:
            info_table = self.soup.find('table')
            tds = info_table.find_all('td')
            self.usn = tds[1].text.replace(':', '').strip()
            self.name = tds[3].text.replace(":", '').strip()
            return StudentResultInfo(name=self.name, usn=self.usn)
        except:
            return None
    
    def get_subjects(self) -> list[SubjectResultInfo]:
        try:
            tables = self.soup.find_all('div', attrs={'class': 'divTable'})
            subjects = list()
            for table in tables:
                rows = table.find_all('div', attrs={'class': 'divTableRow'})[1:]
                semester = table.findPrevious('div').text.split(":")[1].strip()
                for row in rows:
                    raw_subject = row.find_all('div', attrs={'class': 'divTableCell'})
                    subject = SubjectResultInfo(
                        sem=semester,
                        code=raw_subject[0].text.strip(),
                        name=raw_subject[1].text.strip(),
                        internal=raw_subject[2].text.strip(),
                        external=raw_subject[3].text.strip(),
                        total=raw_subject[4].text.strip(),
                        result=raw_subject[5].text.strip(),
                        announced_on=raw_subject[6].text.strip()
                    )
                    subjects.append(subject)
            return subjects
        except:
            return None





