
import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox

def create_connection():
    
    conn = None
    try:
        
        conn = psycopg2.connect(
            dbname='fly',
            user='postgres',
            password='Maksim1990',
            host='localhost',  
            port='5432'  
        )
    except Exception as e:
        print(e)
    return conn

def get_airports_by_coordinates(conn, min_lat, max_lat, min_lon, max_lon):
    
    cur = conn.cursor()
    query = """
    SELECT city, country, latitude, longitude 
    FROM airports 
    WHERE latitude BETWEEN %s AND %s AND longitude BETWEEN %s AND %s
    """
    cur.execute(query, (min_lat, max_lat, min_lon, max_lon))
    results = cur.fetchall()
    cur.close()  # Закрываем курсор
    return results

def update_table():
    
    try:
        min_lat = min_lat_entry.get()
        max_lat = max_lat_entry.get()
        min_lon = min_lon_entry.get()
        max_lon = max_lon_entry.get()

        if not min_lat or not max_lat or not min_lon or not max_lon:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return

       
        min_lat = float(min_lat)
        max_lat = float(max_lat)
        min_lon = float(min_lon)
        max_lon = float(max_lon)

        
        airports = get_airports_by_coordinates(conn, min_lat, max_lat, min_lon, max_lon)

        
        for row in tree.get_children():
            tree.delete(row)

        
        for airport in airports:
            tree.insert("", tk.END, values=airport)
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения.")

#  Основное окно приложения
app = tk.Tk()
app.title("Аэропорты")

#  Интерфейс ввода данных
tk.Label(app, text="Минимальная широта:").grid(row=0, column=0)
min_lat_entry = tk.Entry(app)
min_lat_entry.grid(row=0, column=1)

tk.Label(app, text="Максимальная широта:").grid(row=1, column=0)
max_lat_entry = tk.Entry(app)
max_lat_entry.grid(row=1, column=1)

tk.Label(app, text="Минимальная долгота:").grid(row=2, column=0)
min_lon_entry = tk.Entry(app)
min_lon_entry.grid(row=2, column=1)

tk.Label(app, text="Максимальная долгота:").grid(row=3, column=0)
max_lon_entry = tk.Entry(app)
max_lon_entry.grid(row=3, column=1)

filter_button = tk.Button(app, text="Применить фильтр", command=update_table)
filter_button.grid(row=4, columnspan=2)

#  Таблица для отображения результатов
columns = ("Город", "Страна", "Широта", "Долгота")
tree = ttk.Treeview(app, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=5, columnspan=2)


conn = create_connection()  # Подключение к Postgre
if conn is not None:
    app.mainloop()
    conn.close()
else:
    messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
    