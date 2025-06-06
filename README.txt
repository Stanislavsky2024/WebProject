=============================
Некоторая полезная информация
=============================
1) Сайт на хостинге
На данный момент сайт работает на хостинге pythonanywhere.com, так что он доступен для посещения через интернет
Адрес сайта: https://stanislavsky2024.pythonanywhere.com
Внимание! Из-за особенностей хостинга сайт может тормозить, а также некоторые "небольшие" функции могут время от времени не работать
Чаще всего при проблемах с сайтом (например, при долгих зависаниях) помогает просто перезагрузка страницы

2) Различие учительских и ученических аккаунтов
Единственным отличием является право создавать и редактировать группы. Таким образом, учитель имеет право
создать группу, добавить в нее работы и создать объявления. Также только создатель группы может видеть
ссылку-приглашение в свою группу, которая генерируется автоматически. Ученик в свою очередь не может
создавать и владеть группами (даже через API!)

3) Предсозданные аккаунты
Были созданы специальные аккаунты, которые более наглядно демонстрируют сайт и его функционал 
(особенно систему с группами).
Всего таких аккаунтов пять. Два первых - учительские (т.е те, которые могут создавать группы),
а остальные три - ученические
Почта и пароль для каждого аккаунта:
1. first_teacher@mail.ru - first_teacher [содержит больше всего контента]
2. second_teacher@mail.ru - second_teacher
3. first_example@mail.ru - first_example [содержит больше всего контента]
4. second_example@mail.ru - second_example
5. third_example@mail.ru - third_example

4) API сайта
Адрес API сайта: /api/{категория}/[аргументы]
У сайта есть API для 3 категорий: пользователи, группы, новости
Сообщения об ошибках содержат более детальную информацию о том, в каком месте пользователь
ошибся при вводе запроса

1. Пользователи
Доступные операции: вывод списка информации о всех пользователях; вывод информации об одном
пользователе; создание, редактирование и удаление пользователя
- Вывод списка информации о всех пользователях: print(get('{адрес}/api/users').json())
- Вывод информации об одном пользователе: print(get('{адрес}/api/users/{id}').json())
- Создание пользователя: print(post('{адрес}/api/users', json={
	'name': str,
	'surname': str,
	'email': str,
	'password': str,
	'is_teacher': bool
  }).json())
- Редактирование пользователя: print(put('{адрес}/api/users/{id}', json={
	'name': str,
	'surname': str,
	'email': str,
	'password': str
  }).json())
Необязательно вводить все параметры! Если какой-либо из параметров пропущен, то он у пользователя
останется неизмененным
- Удаление пользователя: print(delete('{адрес}/api/users/{id}').json())

2. Группы
Доступные операции: вывод списка информации о всех группах; вывод информации об одной
группе; создание, редактирование и удаление группы
- Вывод списка информации о всех группах: print(get('{адрес}/api/groups').json())
- Вывод информации об одной группе: print(get('{адрес}/api/groups/{id}').json())
- Создание группы: print(post('{адрес}/api/groups', json={
	'name': str,
	'description': str,
	'user_id': str | int
  }).json())
- Редактирование группы: print(put('{адрес}/api/groups/{id}', json={
	'name': str,
	'description': str,
	'user_id': str | int
  }).json())
Необязательно вводить все параметры! Если какой-либо из параметров пропущен, то он у группы
останется неизмененным
- Удаление группы: print(delete('{адрес}/api/groups/{id}').json())

3. Новости
Доступные операции: вывод информации о новости; создание и редактирование новости (мин./макс. новостей - 1)
- Вывод информации о новости print(get('{адрес}/api/news').json())
- Создание новости: print(post('{адрес}/api/news', json={
	'name': str,
	'content': str,
	'image': str # (путь к картинке, находящиеся в пределах папки с проектом)
  }).json())
- Редактирование новости: print(put('{адрес}/api/news', json={
	'name': str,
	'content': str,
	'image': str # (путь к картинке, находящиеся в пределах папки с проектом)
  }).json())
Необязательно вводить все параметры! Если какой-либо из параметров пропущен, то он у новости
останется неизмененным

