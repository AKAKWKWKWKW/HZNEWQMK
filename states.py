from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminGiveBalance(StatesGroup):
    user_id = State()
    balance = State()
    confirm = State()


class Email_sending_photo(StatesGroup):
    photo = State()
    text = State()
    action = State()
    set_down_sending = State()
    set_down_sending_confirm = State()


class Admin_sending_messages(StatesGroup):
    text = State()
    action = State()
    set_down_sending = State()
    set_down_sending_confirm = State()


class Buy(StatesGroup):
    confirm = State()


class CreateGame(StatesGroup):
    bet = State()


class AdminRaffle(StatesGroup):
    bet = State()
    amount_purchase = State()
    amount_dice_games = State()
    game_time = State()
    confirm = State()


class AdminCreatePromo(StatesGroup):
    name = State()
    percent = State()
    life_time = State()
    confirm = State()


class EnterPromo(StatesGroup):
    enter_promo = State()