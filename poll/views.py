#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Poll

import csv,json

# 설문조사 페이지 
def poll_main(request):
    surveyArray = read_csv()

    return render(request, 'poll/poll_main.html', {'readers': surveyArray})
# 조사 결과 확인 페이지
def poll_result(request):
    result = result_survey()

    return render(request, 'poll/poll_result.html', {'results': result[0] , 'total': result[1]})

#CSV파일 읽어오기
def read_csv():
    surveyObject = {}
    surveyArray = []
    surveyItem = []

    # CSV 파일 열기
    csv_file = open('poll/static/resource/survey.csv', 'r')
    reader = csv.reader(csv_file)
    # CSV파일의 데이터 정합
    for row in reader:
        key = row[0].strip()
        value = row[1].strip()
        #설문 조사 주제
        if(key != '' and key[0] == 'Q'):
            surveyObject['question'] = value
        #설문 조사 타입
        elif(key == 'type'):
            surveyObject['type'] = value
        #응답 최대 갯수
        elif(key == 'limit'):
            surveyObject['limit'] = value
        #설문 조사 내용들(순서대로 배열로 저장)
        elif(key == '' and value != ''):
            surveyItem.append(value);
        #한가지 설문의 마지막일때 설문조사배열에 저장 후 변수들 초기화
        elif(key == '' and value == ''):
            surveyObject['item'] = surveyItem
            surveyArray.append(surveyObject)
            surveyObject = {}
            surveyItem = []
    # CSV 파일 닫기
    csv_file.close()

    return surveyArray
#CSV파일 내보내기
def export_csv(request):
    #CSV 파일 쓰기
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="survey_result.csv"'
    writer = csv.writer(response)
    writer.writerow(['질문', '설문 타입', '복수 응답 갯수', '응답/응답 수'])
    result = result_survey()

    #각 행별로 데이터를 적어줌
    for row in result[0]:
        writeobj = [row['question'], row['type'], row['limit']]
        data = row['item']
        for key,value in data.items():
            writeobj.append(key)
            writeobj.append(str(value) + '명')

        writer.writerow(writeobj)
    
    return response

# 투표하기
def poll_vote(request):
    if request.method == "POST":
        #조사받은 설문 내용 및 휴대폰 번호를 저장        
        poll = {}
        poll['phonenumber'] = request.POST['phonenumber']
        poll['question'] = request.POST['question']    
        poll['answer'] = request.POST['answer']
        # DB에 투표한 데이터를 저장
        m_poll = Poll()
        result = m_poll.insert_poll(poll)

        # 저장 후 성공 및 실패 여부를 리턴해준다.
        return HttpResponse(json.dumps(result), content_type = "application/json")

# 조사 결과 데이터 정합
def result_survey():
    m_poll = Poll()
    poll = m_poll.show_poll('answer')
    surveyArray = read_csv()
    result = []
    # 조사 결과의 응답문항별 인원수 체크를 위해 숫자를 넣어줌
    for row in surveyArray:
        answer = {}
        for item in row['item']:
            answer[item] = 0

        row['item'] = answer
    # 응답 문항을 정합하여 결과 수 체크
    for idx,row in enumerate(poll):
        data = row['answer'].split(",")

        for index,r in enumerate(data):
            r = r.encode("UTF-8")
            if index < len(surveyArray):
                if surveyArray[index]['type'] == 'checkbox':
                    r = r.split(":")
                    for i in r:
                       surveyArray[index]['item'][i] = 1
                else:
                    surveyArray[index]['item'][r] += 1

    result.append(surveyArray)
    result.append(len(poll))

    return result