// Создаем массив для хранения ссылок на видео
let videos = [];

// Переменная для таймера
let hoverTimer;
// Функция проверки видимости элемента на экране
// function isElementInViewport(el) {
//     var rect = el.getBoundingClientRect();
//     return (
//         rect.top >= 100 &&
//         rect.bottom <= (window.innerHeight || document.documentElement.clientHeight)
//     );
// }
// Функция инициализации
function init() {
    // Получаем все элементы с классом '.video_preload'
    const elements = document.querySelectorAll('.video_preload');

    // Проходимся по каждому элементу
    elements.forEach((element) => {
        // Находим видео внутри элемента
        const video = element.querySelector('video');

        // Добавляем видео в массив
        videos.push(video);
        // window.addEventListener('scroll', function(event) {
        // console.log(isElementInViewport(element), element.querySelector('h6').innerHTML)
        // })


        // Устанавливаем обработчик события 'mouseenter'
        element.addEventListener('mouseenter', function(event) {video.parentElement.parentElement.style.transform = 'scale(1.03)';
            // Сбрасываем предыдущий таймер, если он был установлен
            clearTimeout(hoverTimer);

            // Устанавливаем новый таймер на 1 секунду
            hoverTimer = setTimeout(() => {
                // Если курсор все еще на элементе, начинаем воспроизведение видео
                if (!event.relatedTarget || !element.contains(event.relatedTarget)) {
                    video.play();

                    // Увеличиваем видео

                }
            }, 1000); // Задержка в 1 секунду
        });

        // Устанавливаем обработчик события 'mouseleave'
        element.addEventListener('mouseleave', function(event) {
            // Очищаем таймер, чтобы видео не начинало воспроизводиться
            clearTimeout(hoverTimer);

            // Останавливаем воспроизведение видео
            video.pause();

            // Возвращаем исходный размер видео
            video.parentElement.parentElement.style.transform = 'scale(1)';

            // Перематываем видео в начало
            video.load();
        });
    });
}

// Запускаем инициализацию
init();