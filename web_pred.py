from flask import Flask, request, render_template
from model import predict
# from flask import jsonify, g

app = Flask(__name__,template_folder = 'templates')
app.env = 'development'
app.debug = True

#1) 1건 cpu 걸린시간 넣기
#2) .f4 float prob 마무리
#3) 다른예시 체크
'''
1) python web_pred.py 시행 

2) [테스트 예시 - test set(8327개) 중 2번]
제목 : KOS / 인터넷 bus333584 외 87개회선 / 인터넷 일괄해지 접수했는데 해지오더가 들어가지 않고 재처리시 ' 
내용 : ▶[시스템] ***\r\n▶[데이터] 인터넷 ********* 외 **개\r\n▶[확인사항 및 오류메세지] 인터넷 일괄해지 접수했는데 해지오더가 들어가지 않고 재처리시 '중복된 데이터 존재로 진행 불가하여 문의\r\n\r\n처리자 : 김영수(사번 ********) / 고객최우선본부 기업고객컨설팅센터 수도권고객컨설팅부 기업상품컨설팅*팀\r\n\r\n고객명 : 강화군청(사업자번호 ***-**-*****)\r\n[*]일괄해지 에서 인터넷 ********* 외 **개 총 **개 회선을 일괄해지 등록(****.**.**. **:**) 했는데 해당 인터넷들은일괄해지 접수되어있지 않습니다.\r\n[*]일괄해지에서 엑셀파일 다시 업로드해서 재처리시 처리메세지 부분에 '중복된 데이터 존재' 메시지 나오며 진행되지   않습니다.<화면첨부>\r\n\r\n▶[요청사항] 왜 일괄해지 오더가 들어가지 않는건지 확인 요청드립니다.\r\n▶[문의자 연락처] \r\n\r\n▶[답변]\r\n\r\n"

결과 :
* ASM30034 : 0.9352
* ASM39882 : 0.0542
* ASM39842 : 0.0014
* ASM30031 : 0.0014
* ASM39295 : 0.0013

'''

@app.route('/', methods = ['get','post'])
def prediction():
    result = ('_','_')
    if request.method == 'GET':
        return render_template('predict.html', result=result) 

    if request.method == 'POST':
        tt = request.form.get('title')
        print(type(tt))
        ct = request.form.get('content')
        text = tt + ' ' + ct
        result = predict(text) # list of tuples
    
    return render_template('predict.html',result=result)

app.run(port=5055)
