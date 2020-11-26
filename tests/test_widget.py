from endpoints.widget import *

ApiMethods = Widget()


@pytest.yield_fixture()
def script_activation():
    with allure.step('Активация сценария'):
        ApiMethods.send_message(text='запусти сценарий')


@pytest.yield_fixture()
def script_deactivation():
    yield
    with allure.step('Деактивация сценария'):
        ApiMethods.send_message(text='привет')


@pytest.yield_fixture()
def script_buttons():
    with allure.step('Вернуть кнопки'):
        return get_reply()[1]


@allure.feature('Виджет')
@allure.story('Приветствие')
@allure.link(URLs.bot, name="Bot")
class TestHello:

    @allure.title("Поздороваться с ботом")
    def test_send_hello(self):

        with allure.step('Отправить боту сообщение "привет"'):
            ApiMethods.send_message(text='привет')

        with allure.step('Проверить, что бот ответил "Привет!"'):
            assert_that(get_reply()['text'], equal_to('Привет!'))


@allure.feature('Виджет')
@allure.story('Сценарий')
@allure.link(URLs.bot, name="Bot")
class TestRunScript:

    @allure.title("Активация сценария")
    @m.usefixtures('script_deactivation')
    def test_script_activation(self):

        with allure.step('Отправить боту сообщение "запусти сценарий"'):
            ApiMethods.send_message(text='запусти сценарий')

        with allure.step('Получить ответы'):
            replies = get_reply()

        with allure.step('Проверить первый ответ"'):
            assert_that(replies[0]['text'], equal_to('Хорошо. Давайте выберем подходящую еду.'))

        with allure.step('Проверить второй ответ'):
            assert_that(replies[1]['text'], equal_to('Что вы хотите?'))

        with allure.step('Во втором ответе присутствуют кнопки:"Пельмени", "Блины", "Гречка с котлетой"'):
            assert_that(len(replies[1]['buttons']), equal_to(3))
            assert_that(replies[1]['buttons'][0]['text'], equal_to('Пельмени'))
            assert_that(replies[1]['buttons'][1]['text'], equal_to('Блины'))
            assert_that(replies[1]['buttons'][2]['text'], equal_to('Гречка с котлетой'))

    @allure.title("Выбор еды")
    @m.usefixtures('script_activation')
    def test_food_selection(self, script_buttons):

        with allure.step('Нажать кнопку "Пельмени"'):
            ApiMethods.click_button(button_name='Пельмени', buttons=script_buttons)

        with allure.step('Получить ответы'):
            replies = get_reply()

        with allure.step('Проверить первый ответ'):
            assert_that(replies[0]['text'], equal_to('Неправильный выбор. Давайте попробуем еще раз!))'))

        with allure.step('Проверить второй ответ'):
            assert_that(replies[1]['text'], equal_to('Что вы хотите?'))

        with allure.step('Нажать кнопку "Блины"'):
            ApiMethods.click_button(button_name='Блины', buttons=replies[1])

        with allure.step('Получить ответы'):
            replies = get_reply()

        with allure.step('Проверить первый ответ'):
            assert_that(replies[0]['text'], equal_to('Напоминаю твой вопрос: запусти сценарий'))

        with allure.step('Проверить второй ответ'):
            assert_that(replies[1]['text'], equal_to('Приятного аппетита, бро! :)'))
