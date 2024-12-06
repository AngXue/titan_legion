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
                tr.dataset.id = profile.id;
                tr.dataset.userId = profile.user;
                tr.innerHTML = `
                    <td>${profile.character_id}</td>
                    <td>${profile.nickname}</td>
                    <td>${profile.__str__}</td>
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
            const user = row.dataset.userId;
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
            const id = tr.dataset.id;
            const user = tr.dataset.user;
            
            // 从原始表格中获取正确的数据
            const originalRow = document.querySelector(`.lpcenter1-table-tr[data-id="${id}"]`);
            const nickname = originalRow.cells[1].innerText;  // 从原始表格获取昵称
            const modifyLp = parseFloat(input.value) || 0;
            const currentLp = parseFloat(originalRow.cells[3].innerText) || 0;  // 从原始表格获取当前LP
            const newLp = currentLp + modifyLp;

            // 构建完整的请求数据
            const requestData = {
                nickname: nickname,  // 使用从原始表格获取的昵称
                lp: newLp,          // 确保是数字
                user: parseInt(user),
                character_id: parseInt(originalRow.cells[0].innerText) || 0,  // 从原始表格获取角色ID
                pap: 0,
                isk: 0,
                skill: 0,
                used_lp: parseFloat(originalRow.cells[4].innerText) || 0  // 从原始表格获取已使用LP
            };

            console.log('Sending request data:', requestData);  // 调试用

            const updatePromise = fetch(`/api/profiles/${id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ lp: newLp })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(JSON.stringify(data));
                    });
                }
                return response.json();
            });

            updatePromises.push(updatePromise);
            updatedProfiles.push({ id: id, lp: newLp });
        });

        Promise.all(updatePromises)
            .then(results => {
                console.log('LP updated successfully:', results);

                // 更新界面
                updatedProfiles.forEach(profile => {
                    const row = document.querySelector(`.lpcenter1-table-tr[data-id="${profile.id}"]`);
                    if (row) {
                        row.cells[3].innerText = profile.lp;
                    }
                });

                modifyLpBox.style.display = 'none';
            })
            .catch(error => {
                console.error('Error updating LP:', error);
                alert('更新失败：' + error.message);
            });
    });

    // 添加菜单状态管理
    const lpCenterMenu = document.getElementById('hd-box-1');  // 修改为正确的ID
    const lpCenterButton = document.getElementById('LP-center');    // 修改为正确的ID

    // 从 localStorage 恢复菜单状态
    if (localStorage.getItem('lpMenuOpen') === 'true') {
        lpCenterMenu.style.display = 'block';
    }

    // LP中心按钮点击事件
    lpCenterButton.addEventListener('click', function(e) {
        e.preventDefault();  // 阻止默认行为
        
        // 切换菜单显示状态
        const isOpen = lpCenterMenu.style.display === 'block';
        lpCenterMenu.style.display = isOpen ? 'none' : 'block';
        
        // 保存菜单状态
        localStorage.setItem('lpMenuOpen', !isOpen);
    });

    // 确保当前页面是LP中心相关页面时，菜单保持展开
    if (window.location.pathname.includes('lpcenter')) {
        lpCenterMenu.style.display = 'block';
        localStorage.setItem('lpMenuOpen', 'true');
    }
});

