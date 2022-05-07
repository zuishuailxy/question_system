function bindCaptchaBtnClick() {
    $("#captcha-btn").on('click', function (event) {
        const $this = $(this);
        const email = $("input[name='email']").val();
        if (!email) {
            alert("请先输入邮箱");
            return
        }
        // send request: ajax
        $.ajax({
            url: "/user/captcha",
            method: "POST",
            data: {
                'email': email
            },
            success: function (res) {
                const {code} = res
                console.log(code)
                if (code === 200) {
                    // 取消点击事件
                    $this.off('click');
                    // 开始倒计时
                    let countDown = 60
                    let timer = setInterval(function () {
                        countDown--;
                        if (countDown > 0) $this.text(countDown + 's后重新发送')
                        else {
                            $this.text('获取验证码');
                            // 重新执行这个函数， 重新绑定点击事件
                            bindCaptchaBtnClick();
                            // 如果不不要倒计时，记得停掉
                            clearInterval(timer)
                        }
                    }, 1000)

                    alert('验证码发送成功')

                } else {
                    alert(res.message)
                }

            }
        })

    });
}


// 等文档加载完之后再执行
$(function () {
    bindCaptchaBtnClick()
})
