def get_valid_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Значение должно быть не меньше {min_val}. Попробуйте ещё раз.")
                continue
            if max_val is not None and value > max_val:
                print(f"Значение должно быть не больше {max_val}. Попробуйте ещё раз.")
                continue
            return value
        except ValueError:
            print("Пожалуйста, введите целое число.")

# Получаем seed
seed = get_valid_int("Введите сид для воспроизводимости данных: ", min_val=0)

# Получаем длину данных
length = get_valid_int("Введите длину данных: ", min_val=1)

# Получаем количество уникальных значений
len_uniques = get_valid_int(
    "Введите количество уникальных значений (до 500), не превышающее длину данных: ",
    min_val=1,
    max_val=min(length, 5000)
)


import pandas as pd
import numpy as np
import string
from datetime import time

# Для воспроизводимости
np.random.seed(seed)


count_of_sales = [0 for _ in range(length)] # Инициализируем массив количества продаж нулями


# Объявления функций



# Смоделируем зависимость продаж от времени (Колоника Time)
# Пусть в период 18:00 до 22:00 количество покупок наиболее интенсивно 

def sales_times_dependency(times: list, count_of_sales: list) -> list:
    '''
    Функция, поделирующая зависимость количества продаж 
    от времени суток, в которые эти продажи производятся
    '''
    for i in range(0, length - 1):
        if  pd.to_datetime('12:00').time() <= pd.to_datetime(times[i]).time() <= pd.to_datetime('22:00').time():
            count_of_sales[i] += np.random.randint(1,10) # Шире интервал
        elif pd.to_datetime('22:00').time() < pd.to_datetime(times[i]).time() <= pd.to_datetime('00:00').time():
                count_of_sales[i] += np.random.randint(1,5) 
        else:
            count_of_sales[i] += np.random.randint(1,3)
    
    return count_of_sales



# Смоделируем зависимость продаж от цены (Колонка final_prices)
# Создадим подобие нормалнього распределения интенсивности покупок от цен 
def sales_prices_dependency(final_prices: list, count_of_sales: list) -> list:
    '''
    Функция, поделирующая зависимость количества продаж от цены товара
    '''
    
    for i in range(0, length - 1):
        if 50 <= final_prices[i] < 200:
            count_of_sales[i] += np.random.randint(1,2)
        elif 200 <= final_prices[i] < 500:
            count_of_sales[i] += np.random.randint(1,3)
        elif 500 <= final_prices[i] < 1000:
            count_of_sales[i] += np.random.randint(1,4)
        elif 1000 <= final_prices[i] < 2500:
            count_of_sales[i] += np.random.randint(1,5)
        elif 2500 <= final_prices[i] < 3000:
            count_of_sales[i] += np.random.randint(1,4)
        elif 3000 <= final_prices[i] < 3500:
            count_of_sales[i] += np.random.randint(1,3)
        elif 3500 <= final_prices[i] < 4000:
            count_of_sales[i] += np.random.randint(1,2)
        else:
            count_of_sales[i] += np.random.randint(0,1)
    return count_of_sales



# Смоделируем зависимость продаж от скидки (Колонка discounts)
# При наличии скидки, посетитель более охотно будет приобретать товар

def sales_discounts_dependency(discounts: list, count_of_sales: list) -> list:
    '''
    Функция, поделирующая зависимость количества продаж от скидки
    '''
    
    for i in range(0, length - 1):
        if discounts[i]:
            count_of_sales[i] += np.random.randint(2,5)
        else:
            count_of_sales[i] += np.random.randint(1,3)
    return count_of_sales


# Смоделируем зависимость продаж от рейтинга (Колонка final_ratings)
# В магазине с плохим рейтингом клиент будет реже брать товар и наоборот

def sales_ratings_dependency(final_ratings: list, count_of_sales: list) -> list:
    '''
    Функция, поделирующая зависимость количества продаж от рейтинга магазина
    '''
    
    for i in range(0, length - 1):
        if final_ratings[i] == 1:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 0.25))
        elif final_ratings[i] == 2:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 0.5))
        elif final_ratings[i] == 3:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 0.75))
        elif final_ratings[i] == 4:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 0.9))
        elif final_ratings[i] == 5:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 1))
        elif final_ratings[i] == 6:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 1.25))
        elif final_ratings[i] == 7:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 1.75))
        elif final_ratings[i] == 8:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 2))
        elif final_ratings[i] == 9:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 2.75))
        else:
            count_of_sales[i] = int(np.round(count_of_sales[i] * 4))
        
    return count_of_sales



# ПОЛЕ 'date'

# Задание начальной и конечной даты

start_date = '2025-01-01'
end_date = '2027-12-31'

# Преобразование в нужный формат"

start = pd.to_datetime(start_date)
end = pd.to_datetime(end_date)

# Создание интервала дат 
range_of_dates = pd.date_range('2025-01-01', '2027-12-31').to_list()
data = np.array([np.random.choice(range_of_dates) for i in range(length)])
data.sort() # Сортируем данные в массиве даты


# ПОЛЕ 'time'

times = [time(np.random.randint(0, 23), np.random.randint(0, 59), np.random.randint(0, 59)).strftime("%H:%M:%S") 
         for i in range(length)]


# ПОЛЯ 'market' И 'rating'

market_names = [f'market_{i}' for i in range(1,21)] # Генерация названий магазинов
ratings = [np.random.randint(1,11) for _ in range(1,21)] # Генерация рейтингов

markets_ratings_indeces = [np.random.randint(0, len(market_names) - 1) for _ in range(length)]

final_markets = [market_names[i] for i in markets_ratings_indeces]
final_ratings = [ratings[i] for i in markets_ratings_indeces]


# ПОЛЯ good_id И price

letters = [i for i in string.ascii_uppercase] # Генерация букв

# Генерируем id товара, состоящее из двух букв в начале и 5 цифр далее
# Сгенерируем около len_uniques разных товаров
ids_sample = [''.join([np.random.choice(letters) for _ in range(2)]) + 
            str(np.random.randint(10000,100000)) for _ in range(len_uniques)]

# Генерируем цены
prices = np.arange(50,5001,10)

# Генерируем len_uniques уникальных цен 
prices_sample = np.random.choice(prices, size=len_uniques, replace=False)


# Размножение до 8760 элементов с сохранением соответствия

# Создаем список индексов для выбора элементов
goods_prices_indices = np.random.randint(0, len_uniques, size=length)

# Формируем итоговые списки
final_good_ids = [ids_sample[i] for i in goods_prices_indices]
final_prices = [prices_sample[i] for i in goods_prices_indices]


# ПОЛЕ 'discount'

discounts = [np.random.randint(0,2) for _ in range(length)]

# ЦЕЛЕВАЯ ПЕРЕМЕННАЯ 'sales'
# Функции для ее предобработки были описаны ранее

# Вызов всех функций:

sales_ratings_dependency(final_ratings,
                        sales_discounts_dependency(discounts,
                                                sales_prices_dependency(final_prices,
                                                                        sales_times_dependency(times, count_of_sales))))

# СБОРКА ДАТАФРЕЙМА:

df = pd.DataFrame({
    'market' : final_markets,
    'date' : data,
    'time' : times,
    'good_id' : final_good_ids,
    'price' : final_prices,
    'discount' : discounts,
    'rating' : final_ratings,
    'sales' : count_of_sales
})

df.to_csv('sales_data_for_train.csv', index=False)

