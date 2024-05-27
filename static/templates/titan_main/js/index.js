// 测试数据
// const currentUser = {
//     id: 123,
//     character_id: 456,
//     nickname: "JohnDoe",
//     pap: 1000,
//     isk: 500000000,
//     skill: 59900000,
//     lp: 2000,
//     used_lp: 500,
//     role: "普通用户",
//     user: 789
//   };


// 发送请求获取当前登录用户信息并返回一个 Promise 对象
function getCurrentUser() {
    return new Promise((resolve, reject) => {
        fetch('/get_current_user/', {
            method: 'GET'
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resolve(data.profile);
            })
            .catch(error => {
                reject(error);
            });
    });
}

// 调用 getCurrentUser 函数，处理用户信息
getCurrentUser()
    .then(currentUser => {
        // 将用户信息保存到 current_User 对象中
        console.log(currentUser); // 输出当前用户信息

        // 获取要展示 isk 的 div 元素
        const iskDiv = document.getElementById('isk');
        // 创建一个文本节点
        const iskTextNode = document.createTextNode(`${currentUser.isk}`);
        // 将文本节点添加到 div 元素中
        iskDiv.appendChild(iskTextNode);

        // pap、lp、skill
        const papDiv = document.getElementById('pap');
        const papTextNode = document.createTextNode(`${currentUser.pap}`);
        papDiv.appendChild(papTextNode);

        const lpDiv = document.getElementById('lp');
        const lpTextNode = document.createTextNode(`${currentUser.lp}`);
        lpDiv.appendChild(lpTextNode);

        const skillDiv = document.getElementById('skill');
        const skillTextNode = document.createTextNode(`${currentUser.skill}`);
        skillDiv.appendChild(skillTextNode);
    })
    .catch(error => {
        console.error('Error:', error);
    });


// 头像菜单栏
document.addEventListener('DOMContentLoaded', function () {
    const userAvatar = document.getElementById('userAvatar');
    const userMenu = document.getElementById('userMenu');

    userAvatar.addEventListener('click', function (event) {
        // 阻止点击事件冒泡
        event.stopPropagation();
        // 切换菜单显示/隐藏
        userMenu.style.display = userMenu.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', function () {
        // 隐藏用户菜单
        userMenu.style.display = 'none';
    });

    userMenu.addEventListener('click', function (event) {
        // 阻止点击事件冒泡到document，避免点击菜单项时菜单隐藏
        event.stopPropagation();
    });
});
  
