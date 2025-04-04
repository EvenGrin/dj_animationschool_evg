
$(document).ready(function () {
    $('#comment-form').on('submit', function (ev) {
        ev.preventDefault();

        let textarea = $(this).find('textarea[name="comment"]')
        // Получение значения из textarea
        let commentText = textarea.val().trim(); // trim удаляет лишние пробелы
        // Проверяем, не является ли поле пустым
        if (!commentText) {
            alert("Пожалуйста, введите текст комментария, если хотите отправить.");
            return;
        }

        // Получаем форму и отправляем её методом POST
        let formData = new FormData(this);
        let url = $(this).attr('action');

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                // Очищаем поле textarea после успешной отправки
                textarea.val('');
                // Если сервер вернул успешный ответ, обновляем страницу
                addComments(response); // Функция обновления комментариев

            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });
    // показ скрытие коммента
    $(document).on('click', '.button_toggle', function (ev) {
        $(this).find('i').toggleClass('bi-chevron-down bi-chevron-up')
    })
    // редакт коммента
    $(document).on('click', '.edit-comment-btn', function (ev) {
        toggleEditForm($(this).data('id'));
    })
    $(document).on('submit', '#edit-comment-form', function (event) {
        event.preventDefault()
        let formData = new FormData(this);
        fetch('/update_comment/', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(data.comment)
                    // window.location.reload();
                    $(document).find(`#comment_${data.comment.id} .comment_text`).html(data.comment.text).after(`<span class='small' >Изменён</span></br>`)
                    
                } else {
                    alert('Произошла ошибка при редактировании комментария.');
                }
            })
            .catch(error => {
                console.log('Error:', error);
            });
    })
    // удаление коммента
    $(document).on('click', '.delete-comment-btn', function (ev) {
        id = $(this).data('id')
        if (confirm('Вы действительно хотите удалить этот комментарий?')) {
            $.get(
                `/delete_comment/${id}`,
                function (data) {
                    $(`#comment_${id}`).html('Комментарий удален')
                }
            )
        }
    })
})


function toggleEditForm(commentId) {
    console.log(commentId)
    let form = $('.edit-comment-form');
    let currentTextArea = $(`#comment_${commentId}`).find('.comment_text').html();
    form.find('textarea[name=new_text]').html(currentTextArea)
    form.find('input[name=comment_id]').val(commentId)
}


function addComments(newComment) {
    // Обновляем количество комментариев
    let currentCount = parseInt($('#comments-count').text());
    $('#comments-count').text(currentCount + 1);

    // Добавляем новый комментарий в начало списка
    let html = `
    <div class="border rounded-3 p-2 w-100 row m-0" id="comment_${newComment.id}">
        <div class="col">
            <div class="">
                <span class="fw-bold">${newComment.user}</span>
                <span class="text-secondary">${newComment.created_at}</span>
            </div>
            <div class="ps-3 comment_text">${newComment.text}</div>
        </div>
        <div class="col-auto">
            <button class="btn" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="bi bi-three-dots-vertical"></i>
            </button>
            <ul class="dropdown-menu">
                <li>
                    <button class="btn edit-comment-btn" data-id="${newComment.id}""
                        data-bs-toggle="modal" data-bs-target="#commentModal">
                        <i class="bi bi-pencil"></i> Изменить
                    </button>
                </li>
                <li>
                    <button class="btn delete-comment-btn" data-id="${newComment.id}">
                        <i class="bi bi-trash"></i> Удалить
                    </button>
                </li>
            </ul>
        </div>
    </div>
    `;
    $('#comments-container').prepend(html);
}

