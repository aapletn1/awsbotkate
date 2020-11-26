#### Подготовка

Клонируем проект

`git clone https://github.com/aapletn1/awsbotkate.git`

`cd awsbotkate`


Создаем новое окружение

`python3.x -m venv env`



Устанавливаем зависимости

`source env/bin/activate`

`pip install -r requirements.txt`

#

#### Запуск тестов

Обычный

`py.test tests/test_widget.py --verbose`

С Allure отчетом

`py.test tests/test_widget.py --verbose --alluredir=allure && allure serve allure`


