from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Poll

import csv,json

def getCsvFile():
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


# 설문조사 페이지 
def poll_main(request):
    surveyArray = getCsvFile()

    return render(request, 'poll/poll_main.html', {'readers': surveyArray})

# 투표하기
def poll_vote(request):
    if request.method == "POST":
        #조사받은 설문 내용 및 휴대폰 번호를 저장        
        poll = {}
        poll['phonenumber'] = request.POST['phonenumber']
        poll['question'] = request.POST['question']    
        poll['answer'] = request.POST['answer']
        # DB에 투표한 데이터를 저장
        result = Poll.insert_poll(poll)

        # 저장 후 성공 및 실패 여부를 리턴해준다.
        return HttpResponse(json.dumps(result), content_type = "application/json")

# 조사 결과 확인 페이지
def poll_result(request):
    poll = Poll.show_poll()
    surveyArray = getCsvFile()

    for row in surveyArray:
        answer = {}
        for item in row['item']:
            answer[item] = 0

        row['item'] = answer


    # result = {}
    for row in poll:
        data = row['answer'].split(",")
        for index,r in enumerate(data):
            # print(index , r)
            if surveyArray[index]['type'] == 'checkbox':
                r = r.split(":")
                r = r[0]



            surveyArray[index]['item'][r] += 1
    #         key = 'Q'+str(index)
    #         if (key in result) == False:
    #             result[key] = {}

    #         print(r in result[key])
    #         if (r in result[key]) == True:
    #             result[key][r] += 1
    #         else: 
    #             result[key][r] = 1


    # print(result)


    return render(request, 'poll/poll_result.html', {'results': surveyArray , 'total': len(poll)})
