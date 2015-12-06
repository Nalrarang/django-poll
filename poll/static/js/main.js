/* 설문 조사 페이지 Javascript */
$( document ).ready(function() {
    /* 설문조사 Type이 체크박스인 것 복수선택 데이터 저장용 변수 */
    var checkbox = {};
    /* 설문조사 답변 저장용 배열 변수 */
    var survey = [];
    /* 설문조사 문항 저장 */
    var question = [];

    /* 이벤트 리스너 */
    var eventListener = function(){
        /* Type이 Checkbox일때 복수 응답 수 예외 처리 - 다소복잡..정리필요!! */
        for(var i=0; i < $('.checkbox').length; i++){
            (function(index){
                var checkboxName = $('.checkbox:nth('+index+') input').attr('name');
                /* Checkbox별 사용자가 순서대로 응답할 데이터 저장용 변수 */
                checkbox[checkboxName] = [];
                /* 각 Checkbox별 클릭 이벤트 */
                $('input[name="'+ checkboxName +'"]').on('click', function(){
                    /* 제한수보다 더 많이 클릭하면 안된다. */
                    var limit = $('.checkbox:nth('+index+')').attr('limit');
                    if($('input[name="'+ checkboxName +'"]:checked').length > limit) {
                        this.checked = false;
                        alert('해당 항목의 선택은 '+ limit +'개까지만 가능합니다.');
                        return;
                    }
                    /* Checkbox에 Check할 시 순서대로 배열에 Push 해준다. */
                    var idx = $('input[name="'+ checkboxName +'"]').index(this);
                    if($('input[name="'+ checkboxName +'"]').eq(idx).is(':checked')) {
                        checkbox[checkboxName].push($('.checkbox:nth('+index+') input').eq(idx).attr('value'));
                    } else {
                    /* Check한 것을 해제할때는 배열에서 해당 요소를 빼준다.  */
                        var val = $('.checkbox:nth('+index+') input').eq(idx).attr('value');                            
                        var del_idx = checkbox[checkboxName].indexOf(val);
                        checkbox[checkboxName] = (checkbox[checkboxName].slice(0,del_idx)).concat(checkbox[checkboxName].slice(del_idx+1, checkbox[checkboxName].length));
                    }
                });
            })(i);
        } // End For문

        /* 투표하기 버튼 클릭 이벤트 */
        $('.vote').off('click').on('click', function(evt){
            evt.preventDefault();
            /* 휴대폰 번호의 유효성 체크 */
            var phoneNumber = $('#phoneNumber').val();
            phoneNumber = phoneNumber.replace(/-/gi, "");
            if(phoneNumber == '') { 
                alert('휴대폰 번호를 입력해주세요'); 
                return false;
            }
            if(phoneNumber.length < 10) { // 휴대폰 자리수는 10자리 ~ 11자리
                alert('올바른 휴대폰 번호를 입력해주세요.');
                return false;
            }
            /* 전화번호는 오직 숫자여야만 함 */
            var num_regx=/^[0-9]*$/;
            if(!num_regx.test(phoneNumber)) {
                alert('휴대폰 번호는 숫자여야만 합니다.');
                return false;
            }

            /* 설문조사 항목들의 유효성 체크 및 응답 내용들 가져오기  */
            var answer = validate_check();

            /* 데이터가 이상 없으면 투표하기 실행 */
            if(answer) {
                vote(phoneNumber, question, answer);
            }
        });            
    } /* End EventListenr() */

    /* 설문조사 항목들의 유효성 체크 및 응답내용 저장 */
    function validate_check(){
        var questionWrap = $('.question-wrap');
        var questionLength = questionWrap.length;
        for(var i=0; i<questionLength; i++){
            /* 설문조사의 문항을 저장 */
            question.push(questionWrap.eq(i).children('.question').text());

            var type = questionWrap.eq(i).children('.question').attr('type');
            var answer;
            /* Type별 응답내용들을 문자열로 저장 */
            if(type == 'select') {
                answer = questionWrap.eq(i).children('select').val();
            }
            else if(type == 'radio') {
                answer = $('input[name=q'+(i+1)+'-Radio]:checked').val();
                if(answer == undefined){
                    alert('모든 항목의 설문에 응답해 주세요');
                    return false;
                }
            } else if(type == 'checkbox') {
                if(checkbox['q'+(i+1)+'-checkbox'].length == 0) {
                    alert('체크박스의 항목은 1개 이상 선택해야 합니다.');
                    return false;
                }
                /* 체크박스의 경우 복수 선택이므로 구분자 ':'로 구분하여 문자열로 저장한다. */
                answer = checkbox['q'+(i+1)+'-checkbox'].join(":");
            }
                
            survey.push(answer);
        }

        return survey;
    }
    /* 투표하기 */
    function vote(phone,question,data){
        $.ajax({
           type : "POST",
           url :  "poll/vote/",
           dataType: "json",
           data : {
               csrfmiddlewaretoken: csrfmiddlewaretoken, // 이게 없으면 모바일에서 안됨..
               phonenumber: phone,
               question: question.join(),
               answer : survey.join()
           },
           success : function(result) {
               /* 설문 완료 후 결과 페이지로 보내기 취소 시 Redirect */
               if(result == 'success') {
                   if(confirm('설문에 참여해 주셔서 감사합니다.\n결과 페이지로 이동하시겠습니까?')){
                        location.href = '/result/';
                   }else {
                        location.href = '/';
                   }
               } else if(result == 'duplicate') { 
                    alert('이미 설문에 참여한 휴대폰 번호 입니다.');
               }
           },
           error : function(e) {
               console.log('Error Message : ' + e);
           }
        });   
    }
    /* 이벤트 리스너 호출 */
    eventListener();
});