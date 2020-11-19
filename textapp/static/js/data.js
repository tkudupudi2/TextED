$(function() {
    var a = new Date();
    var d = a.getFullYear();
    var c = a.getMonth() + 1;
    var b = a.getDate();
    $(".year").text(d);
    $(".month").text(c);
    datt(d, c, "");
    $(".next").click(function() {
        next()
    });
    $(".prev").click(function() {
        prev()
    });
    $(".tomon").click(function() {
        datt(d, c, "");
        $(".year").text(d);
        $(".month").text(c)
    })
});
var is_edit=false;
var edit_id="";
function datt(n, y, p) {
    var t = new Date(n + "-" + y + "-1").getDay();
    var a = new Date(n,y,0).getDate();
    var b = new Date(n,y - 1,0).getDate();
    var d = "";
    var ok=false;
    for (var g = 1; g <= a; g++) {
        var r = new Date(n,y,g).getTime();
        for(let i=0;i<times.length;i++){

            if(n + "-" + y + "-" + g===times[i]){
                ok=true;
                break;
            }
            else{
                ok=false
            }


        }
        if(ok){
            d += "<li data-jr=" + y + "-" + g + " data-id=" + r + " data-date=" + n + "-" + y + "-" + g + "><span>" + g + "</span><i>note</i></li>"
        }
        else{
            d += "<li data-jr=" + y + "-" + g + " data-id=" + r + " data-date=" + n + "-" + y + "-" + g + "><span>" + g + "</span></li>"
        }


    }

    $(".date ul").html(d);
    var w = new Date().getFullYear();
    var m = new Date().getMonth() + 1;
    var c = new Date().getDate();
    var q = new Date(w,m,c).getTime();
    for (var l = 0; l < a; l++) {
        var s = $(".date ul li").eq(l).attr("data-id");
        var o = 0;
        var u = new Date($(".date ul li").eq(l).attr("data-date")).getDay();
        if (u == 6 || u == 0) {
            $(".date ul li").eq(l).addClass("act_wk")
        }
        if (s > q) {
            $(".date ul li").eq(l).click(function() {
                var i = $(this);
                i.addClass("act_date");
                i.siblings("li").removeClass("act_date");
                i.siblings("li").children("i").css('color','#5f788a');
                i.children('i').css('color','white');
                var j = i.attr("data-date");
                $("#time").val(j);
                if($('.act_date i').text()==='note'){
                    is_edit=true
                     $.ajax({
                         url: "/calendar",    //请求的url地址
                         dataType: "json",   //返回格式为json
                         async: true,//请求是否异步，默认为异步，这也是ajax重要特性
                         data: {time: i.data('date'), method: 'in'},    //参数值
                         type: "POST",   //请求方式
                         success: function (data) {
                             edit_id=data.id;
                             $("#info").val(data.info)
                         }
                     })
                }
                else{
                    is_edit=false
                }
                console.log(is_edit)
            })
        } else {
            if (s == q) {
                $(".date ul li").eq(l).addClass("act_date");
                $(".date ul li").eq(l).click(function() {
                    var i = $(this);
                    i.addClass("act_date");
                    i.siblings("li").removeClass("act_date");
                    var j = i.attr("data-date")
                })
            } else {
                $(".date ul li").eq(l).addClass("no_date")
            }
        }
    }
    var e = "";
    for (var h = b - t + 1; h <= b; h++) {
        e += "<li class='no_date'>" + h + "</li>"
    }
    $(".date ul li").eq(0).before(e);
    var f = "";
    for (var v = 1; v < 43 - a - t; v++) {
        f += "<li class='no_date'>" + v + "</li>"
    }
    $(".date ul li").eq(a + t - 1).after(f)
}
function next() {
    var b = $(".year").text();
    var a = $(".month").text();
    if (a == 12) {
        b++;
        a = 1
    } else {
        a++
    }
    $(".year").text(b);
    $(".month").text(a);
    datt(b, a, "")
}
function prev() {
    var b = $(".year").text();
    var a = $(".month").text();
    if (a == 1) {
        b--;
        a = 12
    } else {
        a--
    }
    $(".year").text(b);
    $(".month").text(a);
    datt(b, a, "")
}
;