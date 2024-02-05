'use strict' // Установка JS на строгий режим написания кода;

//===================================================================================================//
//                                  Импортированные файлы и модули                                   //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//


//===================================================================================================//
//                                       Глобальные переменные                                       //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//



//===================================================================================================//
//                                 Одноразовые функции и события                                     //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//


//===================================================================================================//
//                      Многоразовые функции и события вызовов функций                               //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//


//===================================================================================================//
//                             Функции вызываемые другими функциями                                  //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//

// POST запросы;
function post_request_f(name_path, data) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', `${name_path}`, true); 
    xhr.setRequestHeader('Content-type', "application/x-www-form-urlencoded");
    xhr.send(JSON.stringify({ "data": data }));
}

// fetch-"GET" запрос для загрузки видео с базы данных;
function fetch_request_f(name_path, data) {
    fetch(`${name_path}`)
        .then(response => { return response.blob() })
        .then(blob => {
            _9_modal_table.style.display = 'none'; // (Скрытие модального окна загрузки);
            let blob_url = new Blob([blob]);
            let new_url = URL.createObjectURL(blob_url);
            // Здесь может быть функция;
        })
        .catch(error => {
            console.error('Ощибка при получении blob данных: ', error)
        });
}

// GET запросы;
function get_request_f() {
    let xhr = new XMLHttpRequest(); // XMLHttp метод для ajax "GET" запроса;
    xhr.open('GET', '/9_video_get_1_file', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let data = JSON.parse(xhr.responseText); // Cписок имен в JSON формате;
            // Здесь может быть функция;
        }
    }
    xhr.send();
}

// Функция загрузки файла;
function downloadFile() {
    const serverFileUrl = 'static/TZ_work.xlsx'; // Замените URL на фактический URL вашего файла на сервере
    // Создаем элемент a для скачивания файла
    const downloadLink = document.createElement('a');
    downloadLink.href = serverFileUrl;
    // Выставляем атрибут download, чтобы браузер предложил сохранить файл
    downloadLink.download = 'downloaded_file.txt';
    // Добавляем элемент в DOM и эмулируем клик для начала загрузки
    document.body.appendChild(downloadLink);
    downloadLink.click();
    // Удаляем элемент из DOM после завершения загрузки
    document.body.removeChild(downloadLink);
}

