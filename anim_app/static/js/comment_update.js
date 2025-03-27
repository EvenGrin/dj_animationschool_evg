
$(document).ready(function () {
    $('form').on('submit', function (ev) {
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
                updateComments(response); // Функция обновления комментариев

            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });
    $('.button_toggle').on('click', function (ev) {
        console.log($(this).find('i').toggleClass('bi-chevron-down bi-chevron-up'))
    })
})
function updateComments(newComment) {
    // Обновляем количество комментариев
    let currentCount = parseInt($('#comments-count').text());
    $('#comments-count').text(currentCount + 1);

    // Добавляем новый комментарий в начало списка
    let html = `
        <div class="border rounded-3 p-2">
            <div class="">
                <span class="fw-bold">${newComment.user}</span> <span class="text-secondary">${newComment.created_at}</span>
            </div>
            <div class="ps-3">
                ${newComment.text}
            </div>
        </div>
    `;
    $('#comments-container').prepend(html);
}

