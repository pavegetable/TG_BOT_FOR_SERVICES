# Проект Телеграм Бот для курсов, школ, различных услуг / Telegram Bot project for courses, schools, various services

## RU Описание:

Данный бот обрабатывает заявки клиентов и отправляет их администратору.
Пользователь может:
1. Просмотреть меню курсов\занятий\услуг и отправить заявку, которую бот обработает и отправит администратору.
2. Просматривать акции, скидки, которые админ может сам менять в Админ-Панели.
3. Просмотр контактов, адреса
4. Получать рассылки, которые генерирует администратор в Админ-Панели

Админ-Панель:
Вход в Админ-Панель возможна строго только модераторам\администраторам. Их ID прописан в код и обойти эту систему невозможно.
Админ может:
1. Редактировать, удалять, добавлять новые курсы, услуги, занятия. Реализовано удобное меню
2. Изменить информацию о скидках
3. Создавать рассылку, которую получат все пользователи бота
4. Блокировать пользователей, которые злоупотребляет подачей заявками. Заблокированные пользователи больше никогда не смогут отправить заявку, но смогут просматривать меню, получать рассылки
5. Разблокировать пользователей
6. Узнать статус конкретного пользователя (Заблокирован\Разблокирован)
7. Узнать статистику бота. Узнать количество пользователей бота, узнать количество заблокированных пользователей

## ENG Description:

This bot processes customer requests and sends them to the administrator.
The user can:
1. View the menu of courses\ classes \services and send a request, which the bot will process and send to the administrator.
2. View promotions, discounts, which the admin can change himself in the Admin Panel.
3. View contacts, addresses
4. Receive mailings generated by the administrator in the Admin Panel

Admin Panel:
Login to the Admin Panel is strictly possible only for moderators \ administrators. Their ID is registered in the code and it is impossible to bypass this system.
The admin can:
1. Edit, delete, add new courses, services, classes. Implemented a convenient menu
2. Change information about discounts
3. Create a newsletter that all bot users will receive
4. Block users who abuse the submission of applications. Blocked users will never be able to send a request again, but they will be able to view the menu, receive newsletters
5. Unblock users
6. Find out the status of a specific user (Blocked\Unblocked)
7. Find out the statistics of the bot. Find out the number of bot users, find out the number of blocked users

### Клонировать репозиторий и перейти в него / Clone the repository and go to it:
```
git clone https://github.com/pavegetable/TgBot_for_children-s_center
```
### Cоздать и активировать виртуальное окружение / Create and activate a virtual environment:
```
python -m venv venv
```
```
source venv/scripts/activate
```
### Установить зависимости из файла requirements.txt / Install dependencies from a file requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
## Запуск бота из терминала / Launching the bot from the terminal
```
python main.py
```
## Запуск бота с помощью .bat / Launching the bot using .bat

Запустите файл start.bat / Run the start.bat file
