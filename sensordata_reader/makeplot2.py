import pandas as pd
import matplotlib.pyplot as plt
import pytz
import numpy as np

data = pd.read_csv('gorelik.csv', sep=' ', names=['timestamp', 'type', 'value'], parse_dates=['timestamp'])

data['value'] = data.apply(lambda row: 1 if row['type'] in ['m', 't'] and row['value'] == 'true' else row['value'], axis=1)
data['timestamp'] = data['timestamp'].apply(lambda x: x.replace(tzinfo=pytz.utc))

target_timezone = pytz.timezone('Asia/Irkutsk')
data['timestamp'] = data['timestamp'].apply(lambda x: x.astimezone(target_timezone))

p_data = data[data['type'] == 'p']
m_data = data[data['type'] == 'm']
t_data = data[data['type'] == 't']

# Создаем subplot с тремя графиками (3 строки, 1 столбец)
fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# График для p
axs[0].plot(p_data['timestamp'], p_data['value'], label='p', marker='o')
axs[0].set_title('График данных p')
axs[0].set_ylabel('Значение')
axs[0].legend()
axs[0].grid(True)
axs[0].set_yticks(np.arange(0, 1000+1, 100))

# График для m
axs[1].plot(m_data['timestamp'], m_data['value'], label='m', marker='o', linestyle='None')
axs[1].set_title('График данных m')
axs[1].set_ylabel('Значение')
axs[1].legend()
axs[1].grid(True)

# График для t
axs[2].plot(t_data['timestamp'], t_data['value'], label='t', marker='o', linestyle='None')
axs[2].set_title('График данных t')
axs[2].set_xlabel('Время')
axs[2].set_ylabel('Значение')
axs[2].legend()
axs[2].grid(True)

# Сохранение графика в изображение
plt.savefig('subplots_graphs.png')

# Отображение графика
plt.show()



