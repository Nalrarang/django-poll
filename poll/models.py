from django.db import models
from django.utils import timezone

# Create your models here.
class Poll(models.Model):
    #휴대폰 번호(최대 11자리)
    phonenumber = models.CharField(max_length=11)
    #설문 조사 항목들
    question = models.TextField()
    #응답 내용들
    answer = models.TextField()
    #응답한 날짜
    created_date = models.DateTimeField(default=timezone.now)

    #설문 조사 데이터 Insert Method
    def insert_poll(data):
        #중복 확인 같은 전화번호가 있다면 duplicate를 리턴, 없다면 Insert
        check = Poll.objects.filter(phonenumber = data['phonenumber'])
        if check:
            # check.update(question = data['question'], answer = data['answer'])
            return 'duplicate'
        else: 
            Poll.objects.create(phonenumber = data['phonenumber'], question = data['question'], answer = data['answer'])

        return 'success'
    #설문 조사 데이터 Show Method
    def show_poll(getType):
        if getType == 'answer':
            result = list(Poll.objects.all().values('answer'))
        else: 
            result = Poll.objects.all().values()

        return result
    def __str__(self):
        #응답에 참여한 대상의 Phonenumber를 리턴
        return self.phonenumber