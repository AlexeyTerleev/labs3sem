from screens import BankScreens

from account import Account
from card import Card
class Bank:

    def __init__(self, accounts: list, cards: list, account: Account = None):
        self.__accounts = accounts
        self.__cards = cards

        self.__access = False

        self.__logged = False
        if account is not None:
            self.__logged = True
        self.__account = account

    def as_dict(self) -> dict:
        account_id = None
        if self.__logged:
            account_id = self.__account.id
        dct = {
            "logged": self.__logged,
            "account-id": account_id
        }
        return dct

    @property
    def logged(self) -> bool:
        return self.__logged

    def register_acc(self, login: str, password: str) -> None:

        if self.__logged:
            print(f'Для начала выйдите из аккаунта {self.__account.login}')
            return

        if [x.login for x in self.__accounts].count(login):
            print('Этот логин уже занят, придумайте другой')
            return

        self.__accounts.append(Account(login, password))
        print(f'Создан счет:\n\n\tЛогин: {login}\n\tПароль: {password}\n')


    def login(self, login: str, password: str) -> None:

        if self.__logged:
            print(f'Для начала выйдите из аккаунта {self.__account.login}')
            return

        acc = None
        for x in self.__accounts:
            if x.login == login:
                acc = x
        if acc is None:
            print(f'Счета с таким логином не существует')
        elif acc.get_access(password):
            self.__logged = True
            self.__account = acc
            print(f'Вы вошли в аккаунт {self.__account.login}!')
        else:
            print('Неверный пароль!')

    def logout(self):

        if not self.__logged:
            print(f'Вы еще не зашли в аккаунт!')
            return

        acc = self.__account
        self.__logged = False
        self.__account = None
        print(f'Вы вышли из аккаунта {acc.login}')


    def register_card(self, pin: str) -> None:

        if not self.__logged:
            print(f'Вы еще не зашли в аккаунт!')
            return

        if len(pin) != 4:
            print('PIN - код должен состоять из 4 цифр!')
            return

        if not pin.isdigit():
            print('PIN - код должен состоять только из цифр!')
            return

        card = Card(pin, self.__account)
        self.__cards.append(card)

        print(f'Зарегистрирова новая карта:\n\n'
              f'\tНомер карты: {card.number}\n'
              f'\tСрок обслуживания до: {card.date}\n'
              f'\tCVV: {card.cvv}\n')


    def start(self) -> None:
        while True:
            match BankScreens.selection_screen():
                case '1':
                    BankScreens.add_account_screen(self.__accounts)
                    account = self.__accounts[-1]
                    self.__access = True
                case '2':
                    account = BankScreens.find_account_screen(self.__accounts)
                    self.__access = BankScreens.get_access_screen(account)
                case '3':
                    break
                case _:
                    raise Exception('invalid command')

            if self.__access:
                BankScreens.add_card_screen(account, self.__cards)
                self.__access = False
