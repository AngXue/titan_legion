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

    var closeBtn = document.getElementById('add-close-btn');

     // 绑定点击事件处理函数
     closeBtn.addEventListener('click', function() {
        // 切换表单的显示状态
        if (addItemForm.style.display === 'none' || addItemForm.style.display === '') {
            addItemForm.style.display = 'block';
        } else {
            addItemForm.style.display = 'none';
        }
    });

    // 绑定点击事件处理函数
    addItemBtn.addEventListener('click', function () {
        
        // 切换表单的显示状态
        addItemForm.reset();
        addSmtBtn.style.display = 'block';
        pushSmtBtn.style.display = 'none';
        addItemForm.dataset.action = 'add';
        addItemForm.style.display = 'block';
    });
});


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


document.addEventListener('DOMContentLoaded', function() {
    const itemsPerPage = 8;
    let currentPage = 0;
    const itemList = document.getElementById('itemList');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const delBtn = document.querySelector('.del-btn');
    let items = [];

    // 点击商品时，切换选中状态
    itemList.addEventListener('click', function(event) {
        const item = event.target.closest('.item');
        if (item) {
            item.classList.toggle('selected');
        }
    });

        // 点击删除按钮时
    delBtn.addEventListener('click', function() {
        const selectedItems = document.querySelectorAll('.item.selected');
        const itemIds = Array.from(selectedItems).map(item => item.dataset.id);

        if (itemIds.length === 0) {
            alert('请选择要删除的商品');
            return;
        }

        // 依次发送删除请求
        Promise.all(itemIds.map(id => {
            return fetch(`/api/items/${id}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // 在请求头中包含CSRF令牌
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    console.log(`商品ID ${id} 删除成功: ${data.message}`);
                } else {
                    console.error(`商品ID ${id} 删除失败`);
                }
            })
            .catch(error => {
                console.error(`删除商品ID ${id} 时发生错误:`, error);
            });
        }))
        .then(() => {
            alert('所有选中商品已删除');
            // 重新获取全部商品
            fetchItems();
        })
        .catch(error => {
            console.error('删除商品时发生错误:', error);
            alert('删除商品时发生错误: ' + error.message);
        });
    });


      // 点击修改按钮时
    modifyBtn.addEventListener('click', function() {
        const selectedItems = document.querySelectorAll('.item.selected');
        
        if (selectedItems.length === 0) {
            alert('请选择要修改的商品');
            return;
        }
        if (selectedItems.length > 1) {
            alert('只能选择一个商品进行修改');
            return;
        }

        const item = selectedItems[0];
        const itemId = item.dataset.id;
        const itemName = item.querySelector('.item-name').textContent;
        const itemDescription = item.querySelector('.item-descri').textContent;
        const itemPrice = item.querySelector('.item-price').textContent.replace(' lp', '');

        document.getElementById('itemId').value = itemId;
        document.getElementById('itemName').value = itemName;
        document.getElementById('itemDescription').value = itemDescription;
        document.getElementById('itemPrice').value = itemPrice;

        addSmtBtn.style.display = 'none';
        pushSmtBtn.style.display = 'block';
        addItemForm.dataset.action = 'modify';
        addItemForm.style.display = 'block';
    });

    // 提交添加商品表单
    addItemForm.addEventListener('submit', function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为

        const action = addItemForm.dataset.action;

        if (action === 'add') {
            const fileInput = document.getElementById('itemImage');
            const file = fileInput.files[0];

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
            const uploadData = new FormData();
            uploadData.append('image', file);

            fetch('/upload_image/', {
                method: 'POST',
                body: uploadData,
                headers: {
                    'X-CSRFToken': csrftoken // 在请求头中包含CSRF令牌
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }

                const imageUrl = data.url || data; // 确保正确获取图片URL
                // 图片上传成功，继续发送商品信息
                const itemData = {
                    item_name: document.getElementById('itemName').value,
                    item_price: document.getElementById('itemPrice').value,
                    item_description: document.getElementById('itemDescription').value,
                    item_image: imageUrl // 使用返回的图片URL
                };

                return fetch('/api/items/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken // 在请求头中包含CSRF令牌
                    },
                    body: JSON.stringify(itemData)
                });
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('请求失败');
                }
                return response.json();
            })
            .then(data => {
                // 处理最终的响应结果
                if (data.message) {
                    alert(data.message);
                } else {
                    alert('商品添加成功');
                    // 添加data到items数组
                    items.push(data);
                    updateContent();
                    updateButtons();
                    addItemForm.reset();
                    addItemForm.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('错误:', error);
                alert('发生错误: ' + error.message);
            });
        } else if (action === 'modify') {
            const itemId = document.getElementById('itemId').value;
            const itemName = document.getElementById('itemName').value;
            const itemDescription = document.getElementById('itemDescription').value;
            const itemPrice = document.getElementById('itemPrice').value;

            const formData = new FormData();
            formData.append('itemName', itemName);
            formData.append('itemDescription', itemDescription);
            formData.append('itemPrice', itemPrice);

            const itemImage = document.getElementById('itemImage').files[0];
            if (itemImage) {
                formData.append('itemImage', itemImage);
            }

            fetch(`/api/items/${itemId}/`, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': csrftoken // 在请求头中包含CSRF令牌
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                } else {
                    alert('商品修改成功');
                    addItemForm.reset();
                    addItemForm.style.display = 'none';
                    fetchItems();
                }
            })
            .catch(error => {
                console.error('错误:', error);
                alert('发生错误: ' + error.message);
            });
        }
    });

   

    
    // 创建商品项的HTML
    function createItemHTML(item) {
        return `
            <div class="item item1 float-left" data-id="${item.id}">
                <img src="${item.item_image}" alt="${item.name}">
                <div class="info">
                    <div class="item-name">${item.item_name}</div>
                    <div class="item-descri">${item.item_description}</div>
                    <div class="item-price">${item.item_price} lp</div>
                </div>
            </div>
        `;
    }

    // 更新页面内容
    function updateContent() {
        itemList.innerHTML = '';
        const start = currentPage * itemsPerPage;
        const end = start + itemsPerPage;
        const paginatedItems = items.slice(start, end);
        paginatedItems.forEach(item => {
            itemList.innerHTML += createItemHTML(item);
        });
    }

    // 更新按钮状态
    function updateButtons() {
        prevBtn.disabled = currentPage === 0;
        nextBtn.disabled = (currentPage + 1) * itemsPerPage >= items.length;
    }

    // 获取全部商品
    function fetchItems() {
        fetch('/api/items/')
            .then(response => response.json())
            .then(data => {
                items = data;
                currentPage = 0; // 重置当前页
                updateContent();
                updateButtons();
            })
            .catch(error => console.error('Error fetching items:', error));
    }

    // 初始化页面内容和按钮状态
    fetchItems();

    // 为按钮添加点击事件处理程序
    prevBtn.addEventListener('click', () => {
        if (currentPage > 0) {
            currentPage--;
            updateContent();
            updateButtons();
        }
    });

    nextBtn.addEventListener('click', () => {
        if ((currentPage + 1) * itemsPerPage < items.length) {
            currentPage++;
            updateContent();
            updateButtons();
        }
    });

//     // 提交添加商品表单
//     document.getElementById('addItemForm').addEventListener('submit', function(event) {
//         event.preventDefault(); // 阻止表单的默认提交行为

//         const form = document.getElementById('addItemForm');
//         const fileInput = document.getElementById('itemImage');
//         const file = fileInput.files[0];
//         let closeAddForm = document.getElementById('addItemForm');

//         // 验证是否选择了文件
//         if (!file) {
//             alert('请选择要上传的图片');
//             return;
//         }

//         // 验证文件类型
//         if (!file.type.match('image/png') && !file.type.match('image/jpeg')) {
//             alert('只能上传png或jpg格式的图片');
//             return;
//         }

//         // 上传图片
//         const uploadData = new FormData();
//         uploadData.append('image', file);

//         fetch('/upload_image/', {
//             method: 'POST',
//             body: uploadData,
//             headers: {
//                 'X-CSRFToken': csrftoken // 在请求头中包含CSRF令牌
//             },
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.error) {
//                 throw new Error(data.error);
//             }

//             const imageUrl = data.url || data; // 确保正确获取图片URL
//             // 图片上传成功，继续发送商品信息
//             const itemData = {
//                 item_name: document.getElementById('itemName').value,
//                 item_price: document.getElementById('itemPrice').value,
//                 item_description: document.getElementById('itemDescription').value,
//                 item_image: imageUrl // 使用返回的图片URL
//             };

//             return fetch('/api/items/', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': csrftoken // 在请求头中包含CSRF令牌
//                 },
//                 body: JSON.stringify(itemData)
//             });
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('请求失败');
//             }
//             return response;
//         })
//         .then(response => response.json())
//         .then(data => {
//             // 处理最终的响应结果
//             if (data.message) {
//                 alert(data.message);
//             } else {
//                 alert('商品添加成功');
//                 // 添加data到items数组
//                 items.push(data);
//                 updateContent();
//                 updateButtons();
//                 closeAddForm.style.display = 'none';
//             }
//         })
//         .catch(error => {
//             console.error('错误:', error);
//             alert('发生错误: ' + error.message);
//         });
//     });
// });





