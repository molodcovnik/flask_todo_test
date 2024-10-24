const baseUrl = window.location.protocol + "//" + window.location.host + "/api/v1";

const todoTableBegin = document.querySelector('.todo-list__body');
const todoForm = document.getElementById('todo-popup__form'); 
const modal = document.getElementById('modal');
const addTodoBtn = document.getElementById('addTodoBtn');
const closePopup = document.getElementById('close-modal')
const popupTitle = document.querySelector('.todo-popup__title');
const submitBtn = document.getElementById('submitbtn');


modal.style.display = 'none';

function openPopupForCreate() {
    popupTitle.textContent = 'Добавить задачу';
    submitBtn.textContent = 'Добавить';
    todoForm.reset();
    todoForm.onsubmit = async function(e) {
        e.preventDefault();
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
    
        const response = await createTodo(title, description)
    
        if (response.status == 201) {
            const newTodo = await response.json()
            const createdAt = formatDate(newTodo.created_at);
            const newTodoHtml = insertInfoTodo(newTodo.id, newTodo.title, newTodo.description, createdAt)
            todoTableBegin.insertAdjacentHTML("afterbegin", newTodoHtml);
        }    
        console.log('Создание новой задачи');
        modal.style.display = 'none';
    };
    modal.style.display = 'flex';
}


function formatDate(createdAt) {
    const date = new Date(createdAt);

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы начинаются с 0
    const year = date.getFullYear();

    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${day}.${month}.${year} ${hours}:${minutes}`;
    }

function insertInfoTodo(id, title, description, created_at) {
    return `
    <tr class="todo-list__row" data-id="${id}">
        <td class="todo-list__cell todo-list__cell_title">${title}</td>
        <td class="todo-list__cell todo-list__cell_description">${description}</td>
        <td class="todo-list__cell todo-list__cell">${created_at}</td>
        <td class="todo-list__cell todo-list__cell">
            <button class="todo-list__button todo-list__button_change" data-id="${id}">Изменить</button>
            <button class="todo-list__button todo-list__button_delete" data-id="${id}">Удалить</button>
        </td>
    </tr>
    `;
}

async function getTodos() {
    return await fetch(`${baseUrl}/todos`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('token')
            }
        });
    };

async function deleteTodo(todoId) {
    return await fetch(`${baseUrl}/todos/${todoId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('token')
            }
        });
    };
    
async function createTodo(title, description) {
    return await fetch(`${baseUrl}/todos`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('token')
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        });
}

async function fetchUpdateTodo(todoId, title, description) {
    return await fetch(`${baseUrl}/todos/${todoId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('token')
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        });
}


async function updateTodo(todoId, parentEl) {
    const title = parentEl.querySelector('.todo-list__cell_title').textContent;
    const desc = parentEl.querySelector('.todo-list__cell_description').textContent;

    document.getElementById('title').value = title;
    document.getElementById('description').value = desc;

    popupTitle.textContent = 'Редактировать задачу';
    submitBtn.textContent = 'Обновить';

    todoForm.onsubmit = async function(e) {
        e.preventDefault();
        const updatedTitle = document.getElementById('title').value;
        const updatedDesc = document.getElementById('description').value;
        console.log(`Обновление задачи ID: ${todoId}, Новое название: ${updatedTitle}, Новое описание: ${updatedDesc}`);
        const response = await fetchUpdateTodo(todoId, updatedTitle, updatedDesc)
        if (response.status == 200) {
            parentEl.querySelector('.todo-list__cell_title').textContent = updatedTitle;
            parentEl.querySelector('.todo-list__cell_description').textContent = updatedDesc;
        }
        modal.style.display = 'none';
    };

    modal.style.display = 'flex';
}

async function insertTodos(todos) {
    todos.forEach(todo => {
        const id = todo.id;
        const title = todo.title;
        const description = todo.description;
        const createdAt = formatDate(todo.created_at);
        const todoHtml = insertInfoTodo(id, title, description, createdAt);
        todoTableBegin.insertAdjacentHTML("afterbegin", todoHtml)
    })

}

document.addEventListener('DOMContentLoaded', async () => {
    const response = await getTodos();
    const result = await response.json();

    await insertTodos(result);

    addTodoBtn.onclick = function () {
        openPopupForCreate();
    };

    closePopup.onclick = function () {
        modal.style.display = 'none';
    };

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };

    document.querySelectorAll('.todo-list__button_change').forEach(row => {
        row.addEventListener('click', async function() {
            const todoId = this.getAttribute('data-id');
            const parentEl = this.parentElement.parentElement;
            await updateTodo(todoId, parentEl);
        });
    });

    document.querySelectorAll('.todo-list__button_delete').forEach(row => {
        row.addEventListener('click', async function() {
            const todoId = this.getAttribute('data-id');
            await deleteTodo(todoId);
            this.parentElement.parentElement.remove();
        });
    });

});
