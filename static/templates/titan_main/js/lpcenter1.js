// 获取CSRF令牌
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // 检查这个cookie字符串是否以我们想要的名字开头
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {
    const tableTr = document.getElementById('lpcenter1-tbody');
    const grantLpButton = document.getElementById('grant-lp-button');
    console.log(document.getElementById('grant-lp-button'));
    const modifyLpBox = document.querySelector('.modify-lp-box');
    const modifyLpTbody = document.getElementById('modify-lp-tbody');
    const modifyLpClose = document.querySelector('.modify-lp-close');

    // 绑定点击事件：关闭表单
    modifyLpClose.addEventListener('click', function () {
        
        // 切换表单的显示状态
        modifyLpBox.style.display = 'none';
    });

    // 获取数据并填充表格
    fetch('/api/profiles/')
    .then(response => response.json())
    .then(data => {
        console.log('Fetched data:', data);
        if (Array.isArray(data)) {
            data.forEach(profile => {
                const tr = document.createElement('tr');
                tr.classList.add('lpcenter1-table-tr');
                tr.dataset.id = profile.id; // 将用户ID存储在行的data属性中
                tr.dataset.user = profile.user; // 将user存储在行的data属性中
                tr.innerHTML = `
                    <td>${profile.id}</td>
                    <td>${profile.nickname}</td>
                    <td>${profile.lp}</td>
                    <td>${profile.used_lp}</td>
                `;
                tableTr.appendChild(tr);
            });
        }
    })
    .catch(error => console.error('Error fetching data:', error));

    // 点击商品时，切换选中状态
    tableTr.addEventListener('click', function (event) {
        const tr = event.target.closest('.lpcenter1-table-tr');
        if (tr) {
            tr.classList.toggle('selected');
        }
    });

     // 发放LP按钮点击事件
     grantLpButton.addEventListener('click', function () {
        const selectedRows = document.querySelectorAll('.lpcenter1-table-tr.selected');
        if (selectedRows.length === 0) {
            alert('请指定一个或多个角色');
            return;
        }

        modifyLpTbody.innerHTML = '';
         selectedRows.forEach(row => {
            const id = row.dataset.id; // 从data属性中获取用户ID
            const user = row.dataset.user;
            const nickname = row.cells[1].innerText;
            const remainingLp = row.cells[2].innerText;
            const tr = document.createElement('tr');
             tr.dataset.id = id; // 将用户ID存储在表单行的data属性中
             tr.dataset.user = user;
            tr.innerHTML = `
                <td>${nickname}</td>
                <td>${remainingLp}</td>
                <td>
                    <input type="number" name="modify-Lp" class="modify-lp-input" required>
                </td>
            `;
            modifyLpTbody.appendChild(tr);
        });

        modifyLpBox.style.display = 'block';
     });
    
     // 表单提交事件
     modifyLpBox.addEventListener('submit', function (event) {
        event.preventDefault();

        const inputs = modifyLpBox.querySelectorAll('.modify-lp-input');
        const updatePromises = [];
        const updatedProfiles = [];

        inputs.forEach((input) => {
            const tr = input.closest('tr');
            const id = tr.dataset.id; // 从data属性中获取用户ID
            const user = tr.dataset.user;
            const nickname = tr.cells[0].innerText;
            const remainingLp = parseInt(tr.cells[1].innerText);
            const modifyLp = parseInt(input.value);
            const newLp = remainingLp + modifyLp;

            const updatePromise = fetch(`/api/profiles/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // 在请求头中包含CSRF令牌
                },
                body: JSON.stringify({ lp: newLp, nickname: nickname, user: user})
            }).then(response => response.json());

            updatePromises.push(updatePromise);
            updatedProfiles.push({ id: id, lp: newLp });
        });

        Promise.all(updatePromises)
            .then(results => {
                console.log('LP updated successfully:', results);

                // 更新界面
                updatedProfiles.forEach(profile => {
                    const row = Array.from(document.querySelectorAll('.lpcenter1-table-tr'))
                                     .find(row => row.dataset.id === profile.id.toString());
                    if (row) {
                        row.cells[2].innerText = profile.lp;
                    }
                });

                modifyLpBox.style.display = 'none';
            })
            .catch(error => console.error('Error updating LP:', error));
    });

})

