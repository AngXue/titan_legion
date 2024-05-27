// 头像菜单栏
document.addEventListener('DOMContentLoaded', function() {
    const userAvatar = document.getElementById('userAvatar');
    const userMenu = document.getElementById('userMenu');

    userAvatar.addEventListener('click', function(event) {
      // 阻止点击事件冒泡
      event.stopPropagation();
      // 切换菜单显示/隐藏
      userMenu.style.display = userMenu.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', function() {
      // 隐藏用户菜单
      userMenu.style.display = 'none';
    });

    userMenu.addEventListener('click', function(event) {
      // 阻止点击事件冒泡到document，避免点击菜单项时菜单隐藏
      event.stopPropagation();
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // 选择按钮元素
    var addItemBtn = document.getElementById('addItemBtn');
    // 选择表单元素
    var addItemForm = document.getElementById('addItemForm');

    // 绑定点击事件处理函数
    addItemBtn.addEventListener('click', function() {
        // 切换表单的显示状态
        if (addItemForm.style.display === 'none' || addItemForm.style.display === '') {
            addItemForm.style.display = 'block';
        } else {
            addItemForm.style.display = 'none';
        }
    });
});


document.getElementById('addItemForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    // 转换价格为浮点型字符串
    const itemPrice = parseFloat(formData.get('itemPrice')).toFixed(2);
    formData.set('itemPrice', itemPrice);

    try {
        const response = await fetch('/api/item/', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            alert('商品添加成功: ' + JSON.stringify(result));
        } else {
            const error = await response.json();
            alert('错误: ' + error.message);
        }
    } catch (error) {
        alert('请求失败: ' + error.message);
    }
});




