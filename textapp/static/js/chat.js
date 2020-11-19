
$('.sendBtn').on('click', function () {
    var news = $('#dope').val();
    if (news == '') {
        alert('不能为空');
    } else {
        $('#dope').val('');
        var str = '';
        str += '<li>' +
            '<div class="nesHead"><img src="img/6.jpg"/></div>' +
            '<div class="news"><img class="jiao" src="img/20170926103645_03_02.jpg">' + news + '</div>' +
            '</li>';
        $('.newsList').append(str);
        setTimeout(answers, 1000);
        $('.conLeft').find('li.bg').children('.liRight').children('.infor').text(news);
        $('.RightCont').scrollTop($('.RightCont')[0].scrollHeight);
    }

})
