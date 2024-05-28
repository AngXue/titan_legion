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


document.getElementById('addItemForm').addEventListener('submit', function(event) {
    event.preventDefault(); // 阻止表单的默认提交行为

    var form = document.getElementById('addItemForm');
    var fileInput = document.getElementById('itemImage');
    var file = fileInput.files[0];

    // 验证是否选择了文件
    if (!file) {
        alert('请选择要上传的图片');
        return;
    }

    // 验证文件类型
    if (!file.type.match('image/png') && !file.type.match('image/jpeg')) {
        alert('只能上传png或jpg格式的图片');
        return;
    }

    // 上传图片
    var uploadData = new FormData();
    uploadData.append('file', file);

    fetch('/upload_image/', {
        method: 'POST',
        body: uploadData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }

        var imageUrl = data.url || data; // 确保正确获取图片URL
        // 图片上传成功，继续发送商品信息
        var itemData = {
            item_name: document.getElementById('itemName').value,
            item_price: document.getElementById('itemPrice').value,
            item_description: document.getElementById('itemDescription').value,
            item_image: imageUrl // 使用返回的图片URL
        };

        return fetch('/api/item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(itemData)
        });
    })
    .then(response => response.json())
    .then(data => {
        // 处理最终的响应结果
        if (data.message) {
            alert(data.message);
        } else {
            alert('商品添加成功');
        }
    })
    .catch(error => {
        console.error('错误:', error);
        alert('发生错误: ' + error.message);
    });
});


