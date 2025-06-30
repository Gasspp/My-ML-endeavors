# Импорт необходимых библиотек
import streamlit as st                    # Web-фреймворк для создания интерактивных приложений
import pandas as pd                      # Работа с таблицами и временными данными
import plotly.express as px              # Построение интерактивных графиков
from catboost import CatBoostRegressor, Pool  # Загрузка модели CatBoost и обёртка Pool для работы с категориальными признаками
import os
# === КАСТОМНЫЙ CSS для оформления интерфейса ===
# Меняем фон, отступы и стиль кнопок
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #134e4a;
    }
    .stButton>button {
        background-color: #134e4a;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Заголовок основного окна
st.title("📊 Выполнение прогноза розничных продаж")

# === БОКОВАЯ ПАНЕЛЬ ===
with st.sidebar:
    st.header("📥 Загрузка данных")
    uploaded_file = st.file_uploader("Загрузите .csv файл", type=["csv"])  # Загрузка CSV-файла
    st.markdown("Файл должен содержать колонки:")
    st.code("market, date, time, good_id, price, discount, rating, sales_lag_1, rolling_mean_7")
    st.markdown("---")
    st.caption("После загрузки — модель выполнит предсказание и визуализацию")

# === ЕСЛИ ФАЙЛ ЗАГРУЖЕН ===
if uploaded_file:
    df = pd.read_csv(uploaded_file)  # Чтение CSV в DataFrame

    # Ожидаемый набор колонок
    expected_columns = {
        'market', 'date', 'time', 'good_id', 'price', 'discount',
        'rating', 'sales_lag_1', 'rolling_mean_7'
    }

    # Проверка наличия всех необходимых столбцов
    if not expected_columns.issubset(df.columns):
        st.error(f"❌ Не хватает колонок: {expected_columns - set(df.columns)}")
    else:
        # === Создание временных признаков на основе 'date' и 'time' ===
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        df['hour'] = df['datetime'].dt.hour
        df['month'] = df['datetime'].dt.month
        df['weekday'] = df['datetime'].dt.day_name()  # День недели в виде строки
        df['year'] = df['datetime'].dt.year

        # === Получаем путь к текущему файлу ===
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Строим путь к модели относительно скрипта
        model_path = os.path.join(script_dir, "catboost_model.cbm")

        # === Загрузка предобученной модели CatBoost ===
        model = CatBoostRegressor()
        model.load_model(model_path)

        # === Подготовка фичей для модели ===
        cat_features = ['market', 'good_id', 'weekday']  # Категориальные признаки
        X = df[['market', 'good_id', 'price', 'discount', 'rating',
                'hour', 'month', 'weekday', 'year', 'sales_lag_1', 'rolling_mean_7']]  # Модельные признаки
        pool = Pool(data=X, cat_features=cat_features)  # Обёртка CatBoost для работы с категориальными переменными

        # === Предсказание целевой переменной 'sales' ===
        df['sales'] = model.predict(pool)

        st.success("✅ Предсказание выполнено. Ниже — интерактивные графики:")

        # === ВИЗУАЛИЗАЦИЯ 1: продажи по времени суток ===
        st.markdown("### ⏰ Продажи по времени суток")
        sales_by_hour = df.groupby('hour')['sales'].mean().reset_index()
        fig1 = px.bar(sales_by_hour, x='hour', y='sales', color='sales',
                      labels={'hour': 'Час', 'sales': 'Средние продажи'},
                      color_continuous_scale='Blugrn')
        st.plotly_chart(fig1, use_container_width=True)

        # === ВИЗУАЛИЗАЦИЯ 2: продажи по рейтингу магазина ===
        st.markdown("### ⭐ Продажи по рейтингу магазина")
        sales_by_rating = df.groupby('rating')['sales'].mean().reset_index()
        fig2 = px.bar(sales_by_rating, x='rating', y='sales', color='sales',
                      labels={'rating': 'Рейтинг', 'sales': 'Средние продажи'},
                      color_continuous_scale='Blugrn')
        st.plotly_chart(fig2, use_container_width=True)

        # === ВИЗУАЛИЗАЦИЯ 3: продажи по ценовым диапазонам ===
        st.markdown("### 💸 Продажи по ценовым диапазонам")
        df['sales_bins'] = pd.cut(df['price'],
                                  bins=[0, 500, 1000, 2000, 3000, 4000, 5000],
                                  labels=['0–500', '500–1000', '1000–2000', '2000–3000', '3000–4000', '4000–5000'])
        sales_bins = df.groupby('sales_bins', observed=False)['sales'].sum().reset_index()
        fig3 = px.bar(sales_bins, x='sales_bins', y='sales', color='sales',
                      labels={'sales_bins': 'Ценовой диапазон', 'sales': 'Сумма продаж'},
                      color_continuous_scale='Blugrn')
        st.plotly_chart(fig3, use_container_width=True)

        # === ВИЗУАЛИЗАЦИЯ 4: продажи по дням недели ===
        st.markdown("### 📅 Продажи по дням недели")
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['weekday'] = pd.Categorical(df['weekday'], categories=weekday_order, ordered=True)  # Устанавливаем порядок дней
        sales_by_weekday = df.groupby('weekday')['sales'].sum().reset_index().sort_values('weekday')

        fig4 = px.pie(sales_by_weekday, names='weekday', values='sales',
                      color_discrete_sequence=px.colors.sequential.Blugrn,
                      title='Продажи по дням недели')
        fig4.update_traces(
            textinfo='label+percent+value',         # Показывать название, процент и значение
            pull=[0.05] * 7,                         # Лёгкое "выдвижение" всех секторов
            marker=dict(line=dict(color='#FFFFFF', width=2))  # Белая обводка между секторами
        )
        st.plotly_chart(fig4, use_container_width=True)

        # === СОХРАНЕНИЕ РЕЗУЛЬТАТА ===
        st.markdown("---")
        st.markdown("### 💾 Сохранить результат")
        output_filename = "predicted_sales.csv"
        df.to_csv(output_filename, index=False)  # Сохраняем DataFrame с предсказаниями в CSV
        with open(output_filename, "rb") as f:
            st.download_button("📥 Скачать предсказания (.csv)", f, file_name=output_filename)
