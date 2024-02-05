'use strict' // Установка JS на строгий режим написания кода;

//===================================================================================================//
//                                  Импортированные файлы и модули                                   //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//



//===================================================================================================//
//                                       Глобальные переменные                                       //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//

const audio = document.getElementById('audio_id'); // (блок загрузки аудио файла);
const audio_error = document.getElementById('audio_error_id'); // (блок ощибки загрузки аудио файла);

const img_audio = document.getElementById('img_audio_id'); // (блок загрузки файла изображения);
const img_audio_error = document.getElementById('img_audio_error_id'); // (блок ощибки загрузки аудио файла);

const name_ = document.getElementById('name_id'); // (блок ввода наименования сказки на Русском языке);
const name_error = document.getElementById('name_error_id'); // (блок ощибки наименования сказки на Русском языке);

const name_sakha = document.getElementById('name_sakha_id'); // (блок ввода наименования сказки на Якутском языке);
const name_sakha_error = document.getElementById('name_sakha_error_id'); // (блок ощибки наименования сказки на Якутском языке);

const description = document.getElementById('description_id'); // (блок ввода описания сказки на Русском языке);
const description_error = document.getElementById('description_error_id'); // (блок ощибки описания сказки на Русском языке);

const description_sakha = document.getElementById('description_sakha_id'); // (блок ввода описания сказки на Якутском языке);
const description_sakha_error = document.getElementById('description_sakha_error_id'); // (блок ощибки описания сказки на Якутском языке);

const genre_ru = document.getElementById('genre_ru_id'); // (блок ввода жанр);
const genre_error_ru = document.getElementById('genre_error_ru_id'); // (блок ощибки жанр);

const genre = document.getElementById('genre_id'); // (блок ввода жанр (на Русском));
const genre_error = document.getElementById('genre_error_id'); // (блок ощибки жанр (на Якутском));

const age = document.getElementById('age_id'); // (блок ввода возраста);

const volume_obj = document.getElementById('volume_id'); // (скрытый input для отправки размера файла в сервер);

const submit_button = document.getElementById('submit_button_id'); // (кнопка для отправки "form-post" запроса);

const gen_tr_td = document.getElementById('gen_tr_td_id'); // (блок-таблица для вывода данных с базы данных);

const delete_fairy_tale = document.getElementById('delete_fairy_tale_id'); // (туман модального окна удаления с базы данных сказки);
const delete_card_fairy_tale = document.getElementById('delete_card_fairy_tale_id'); // (карточка модального окна удаления с базы данных сказки);
const delete_text_fairy_tale = document.getElementById('delete_text_fairy_tale_id'); // (блок наименования удаляемой сказки);
const delete_yes_fairy_tale = document.getElementById('delete_yes_fairy_tale_id'); // (кнопка удаления сказки);
const delete_no_fairy_tale = document.getElementById('delete_no_fairy_tale_id'); // (кнопка отмены удаления сказки);

//===================================================================================================//
//                                 Одноразовые функции и события                                     //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//

// Функция запрета повторной отправки post запроса при перезагрузке страницы;
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
};

// Функция загрузки данных о загруженных сказках с базы данных;
document.addEventListener('DOMContentLoaded', () => {
    let xhr = new XMLHttpRequest(); // XMLHttp метод для ajax "GET" запроса;
    xhr.open('GET', 'request_for_fairy_tales', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let data = JSON.parse(xhr.responseText); // Cписок имен в JSON формате;
            // Цыкл генерации строк записанных сказок;
            for (let i=0; i<data.length; i++) {
                let new_tr = document.createElement('tr');
                gen_tr_td.append(new_tr);
                for (let n=0; n<data[i].length + 1; n++) {
                    let new_td = document.createElement('td');
                    new_td.id = `_${data[i][0]}_${n + 1}_id`;
                    if (n != data[i].length) {new_td.innerText = data[i][n]};
                    if (n == data[i].length) {new_td.innerText = 'X'};
                    new_tr.append(new_td);
                }
            }
        }
    }
    xhr.send();
});

// Функция скрытия модального окна удаления с базы данных сказки;
delete_fairy_tale.style.display = 'none';
delete_card_fairy_tale.style.display = 'none';

//===================================================================================================//
//                      Многоразовые функции и события вызовов функций                               //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//

// Функция проверки коректного формата аудио файла (а именно на формат .mp3);
audio.onchange = () => {
    let audio_name = audio.files[0].name; // (полное название загружаемого аудио файла);
    audio_name = audio_name.split('').slice(-4, ).join('');
    if (audio_name == '.mp3') {
        audio_error.style.display = 'none';
        open_button_submit_f();
    }
    else {
        audio_error.style.display = '';
    } 
};

// Функция проверки коректного формата файла изображения (а именно на формат .jpg);
img_audio.onchange = () => {
    let audio_name = img_audio.files[0].name; // (полное название загружаемого аудио файла);
    audio_name = audio_name.split('').slice(-4, ).join('');
    if (audio_name == '.jpg') {
        img_audio_error.style.display = 'none';
        open_button_submit_f();
    }
    else {
        img_audio_error.style.display = '';
    } 
};

// Функция проверки записи на поле ввода названия сказки на Русском;
name_.addEventListener('input', _=> {
    if (name_.value.split('').length > 0) {name_error.style.display = 'none'; open_button_submit_f();}
    else {name_error.style.display = '';}
});

// Функция проверки записи на поле ввода названия сказки на Якутском;
name_sakha.addEventListener('input', _=> {
    if (name_sakha.value.split('').length > 0) {name_sakha_error.style.display = 'none'; open_button_submit_f();}
    else {name_sakha_error.style.display = '';}
});

// Функция проверки записи на поле ввода описания сказки на Русском;
description.addEventListener('input', _=> {
    if (description.value.split('').length > 0) {description_error.style.display = 'none'; open_button_submit_f();}
    else {description_error.style.display = '';}
});

// Функция проверки записи на поле ввода описания сказки на Якутском;
description_sakha.addEventListener('input', _=> {
    if (description_sakha.value.split('').length > 0) {description_sakha_error.style.display = 'none'; open_button_submit_f();}
    else {description_sakha_error.style.display = '';}
});

// Функция проверки записи на поле ввода жанр (на Русском);
genre_ru.addEventListener('input', _=> {
    if (genre_ru.value.split('').length > 0) {genre_error_ru.style.display = 'none'; open_button_submit_f();}
    else {genre_error_ru.style.display = '';}
});

// Функция проверки записи на поле ввода жанр (на Якутском);
genre.addEventListener('input', _=> {
    if (genre.value.split('').length > 0) {genre_error.style.display = 'none'; open_button_submit_f();}
    else {genre_error.style.display = '';}
});

// Функция ограничения ввода возрасти от 0 до 100;
age.addEventListener('input', ()=>{
    if (Number(age.value) < 0) {age.value = '0'};
    if (Number(age.value) > 100) {age.value = '100'};
});

// Функция вычисления размера аудио файла;
audio.addEventListener('change', () => {
    const fileSize = audio.files[0].size; // размер в байтах
    const fileSizeInKB = fileSize / 1024; // размер в килобайтах
    const fileSizeInMB = (fileSizeInKB / 1024).toFixed(2); // размер в мегабайтах
    volume_obj.value = fileSizeInMB;
});

// Функция показа модального окна удаления с базы данных сказки;
let num_del = 0
document.addEventListener('click', (e)=>{
    for (let i=1; i<100; i++) {
        try {
            if (e.target.id == `_${i}_12_id`) {
                num_del = i;
                delete_text_fairy_tale.innerText = document.getElementById(`_${i}_3_id`).innerText;
                delete_fairy_tale.style.display = '';
                delete_card_fairy_tale.style.display = '';
            }
        }
        catch {break}
    }
});

// Функция удаления с базы данных сказки;
delete_yes_fairy_tale.onclick = () => {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/deleting_data', true);
    xhr.setRequestHeader('Content-type', "application/json");
    xhr.send(JSON.stringify({ "data": num_del }));
    window.location.href = '/audio_catalog';
    num_del = 0;
    delete_fairy_tale.style.display = 'none';
    delete_card_fairy_tale.style.display = 'none';
};

// Функция отмены удаления с базы данных сказки;
delete_no_fairy_tale.onclick = () => {
    delete_fairy_tale.style.display = 'none';
    delete_card_fairy_tale.style.display = 'none';
    num_del = 0;
}

//===================================================================================================//
//                             Функции вызываемые другими функциями                                  //
//VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//

// Функция проверки условия отсутствия не введенных данных сказки и разрешения клика кнопки;
function open_button_submit_f() {
    if (audio_error.style.display == 'none' && img_audio_error.style.display == 'none'
        && name_error.style.display == 'none' && name_sakha_error.style.display == 'none'
        && description_error.style.display == 'none' && description_sakha_error.style.display == 'none'
        && genre_error.style.display == 'none' && genre_error_ru.style.display == 'none') {

        submit_button.disabled = false;
    }
    else {
        submit_button.disabled = true;
    }
};