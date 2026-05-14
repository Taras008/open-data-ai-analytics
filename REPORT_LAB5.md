# Звіт до лабораторної роботи 5

## Тема

Моніторинг контейнеризованого проєкту в Azure за допомогою Prometheus та Grafana.

## Мета роботи

Метою лабораторної роботи було організувати базовий моніторинг Docker-проєкту, розгорнутого на Azure Linux VM, за допомогою Prometheus, Grafana, Node Exporter та cAdvisor.

У межах роботи потрібно було навчитися:

- збирати метрики з Linux VM;
- збирати метрики Docker-контейнерів;
- збирати метрики FastAPI-застосунку;
- налаштовувати Prometheus;
- підключати Prometheus до Grafana;
- створювати Grafana dashboard для аналізу стану системи.

## 1. Початкові умови

Перед виконанням цієї лабораторної роботи вже був підготовлений Docker-проєкт, який запускається в Azure на Linux VM.

Проєкт складається з таких сервісів:

- `data_load` - завантаження та підготовка даних;
- `data_quality_analysis` - перевірка якості даних;
- `data_research` - дослідження даних;
- `visualization` - побудова графіків;
- `web` - FastAPI веб-інтерфейс;
- SQLite-база даних.

Основний застосунок запускається через `compose.yaml` і доступний на порті `5050`.

Мережеве розгортання Azure було підготовлене в попередній лабораторній роботі за допомогою Terraform і cloud-init.

<img width="1307" height="250" alt="Знімок екрана 2026-05-14 о 12 43 32" src="https://github.com/user-attachments/assets/4e780aa3-18b9-4078-a1b1-d16a6ffab0dc" />


## 2. Створення гілки для лабораторної роботи

Для виконання лабораторної роботи було створено окрему Git-гілку:

```text
lab-5-monitoring
```

У цій гілці були додані всі файли, пов'язані з моніторингом.

Після внесення змін гілку було запушено на GitHub, щоб Azure VM могла отримати код через `git pull`.

## 3. Додавання метрик у FastAPI-застосунок

Для того щоб Prometheus міг збирати метрики застосунку, у FastAPI web-сервіс було додано endpoint:

```text
/metrics
```

Для цього в `web/requirements.txt` було додано залежність:

```text
prometheus-fastapi-instrumentator
```

У файлі `web/app.py` було підключено інструментатор:

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

Після цього FastAPI почав віддавати метрики у форматі Prometheus.

Приклад метрик:

```text
python_gc_objects_collected_total
process_cpu_seconds_total
http_requests_total
http_request_duration_seconds
```

<img width="1304" height="869" alt="Знімок екрана 2026-05-14 о 12 44 30" src="https://github.com/user-attachments/assets/556aa5fb-eb4e-4763-9d45-8fe212d1e372" />


## 4. Створення структури monitoring

Для моніторингової частини було створено каталог:

```text
monitoring/
```

Його структура:

```text
monitoring/
├── docker-compose.monitoring.yml
├── prometheus/
│   └── prometheus.yml
└── grafana/
    ├── dashboards/
    │   └── open-data-ai-dashboard.json
    └── provisioning/
        ├── dashboards/
        │   └── dashboard.yml
        └── datasources/
            └── prometheus.yml
```

Ця структура містить:

- Docker Compose файл для запуску сервісів моніторингу;
- конфігурацію Prometheus;
- автоматичне підключення Prometheus у Grafana;
- готовий Grafana dashboard.

## 5. Додавання сервісів моніторингу

У файлі `monitoring/docker-compose.monitoring.yml` було описано запуск таких сервісів:

- `prometheus`;
- `grafana`;
- `node-exporter`;
- `cadvisor`.

### Prometheus

Prometheus збирає метрики з усіх налаштованих targets і доступний на порті:

```text
9090
```

### Grafana

Grafana використовується для візуалізації метрик і доступна на порті:

```text
3000
```

Логін і пароль за замовчуванням:

```text
admin / admin
```

### Node Exporter

Node Exporter збирає метрики Linux VM:

- CPU;
- RAM;
- disk;
- network;
- system load.

### cAdvisor

cAdvisor збирає метрики Docker-контейнерів:

- використання CPU контейнерами;
- використання пам'яті;
- стан контейнерів;
- статистика контейнерів.


<img width="1309" height="212" alt="Знімок екрана 2026-05-14 о 12 47 50" src="https://github.com/user-attachments/assets/87e3f9f1-e249-4480-b975-eaf3f2648adc" />

## 6. Налаштування Prometheus

У файлі `monitoring/prometheus/prometheus.yml` було описано `scrape_configs`.

Prometheus збирає метрики з таких targets:

```text
prometheus:9090
node-exporter:9100
cadvisor:8080
web:5000/metrics
```

Таким чином були покриті три рівні моніторингу:

1. Сам Prometheus.
2. Linux VM через Node Exporter.
3. Docker-контейнери через cAdvisor.
4. FastAPI-застосунок через `/metrics`.

**Місце для скріншота 4:** Prometheus targets.

```text
http://PUBLIC_IP:9090/targets
```
<img width="1312" height="923" alt="Знімок екрана 2026-05-14 о 12 49 04" src="https://github.com/user-attachments/assets/da455cee-d519-4c97-a835-af895e336c6c" />


## 7. Налаштування Grafana

Grafana була налаштована через provisioning.

У файлі:

```text
monitoring/grafana/provisioning/datasources/prometheus.yml
```

було автоматично додано Prometheus як data source:

```text
http://prometheus:9090
```

Це дозволяє Grafana звертатися до Prometheus всередині Docker network.

Також було додано provisioning для dashboard:

```text
monitoring/grafana/provisioning/dashboards/dashboard.yml
```

Dashboard зберігається у файлі:

```text
monitoring/grafana/dashboards/open-data-ai-dashboard.json
```

**Місце для скріншота 5:** Grafana Prometheus data source.

```text
Вставити скріншот Grafana data source Prometheus
```

## 8. Побудова Grafana dashboard

У Grafana було створено


<img width="1307" height="565" alt="Знімок екрана 2026-05-14 о 12 51 33" src="https://github.com/user-attachments/assets/a24563ef-b458-4e35-b264-cdf0f7606d08" />



На dashboard додано панелі:

- VM CPU usage;
- VM memory usage;
- Observed containers;
- Container CPU usage;
- Container memory usage;
- FastAPI request rate;
- FastAPI p95 latency.

Ці панелі дозволяють оцінити стан інфраструктури, Docker-контейнерів і самого веб-застосунку.

```text
http://PUBLIC_IP:3000
```
<img width="1310" height="923" alt="Знімок екрана 2026-05-14 о 12 52 00" src="https://github.com/user-attachments/assets/1d030f52-49cb-462d-a901-871de583d8dd" />


## 9. Оновлення Terraform і cloud-init

Для доступу до моніторингових сервісів через браузер було оновлено Terraform-конфігурацію.

У Network Security Group було відкрито порти:

```text
22   - SSH
5050 - FastAPI web interface
3000 - Grafana
9090 - Prometheus
```

Також у Terraform outputs було додано URL для:

- застосунку;
- Grafana;
- Prometheus;
- Prometheus targets.

У `cloud-init.yaml` було додано запуск monitoring compose:

```bash
docker compose -f monitoring/docker-compose.monitoring.yml up -d
```

Це дозволяє автоматично запускати моніторинг після створення VM.


## 10. Запуск на Azure VM

Після оновлення репозиторію на Azure VM було виконано:

```bash
cd /opt/open-data-ai-analytics
sudo git fetch
sudo git checkout lab-5-monitoring
sudo git pull
```

Після цього було перезапущено основний застосунок:

```bash
sudo docker compose up --build -d
```

І запущено моніторинговий стек:

```bash
sudo docker compose -f monitoring/docker-compose.monitoring.yml up -d
```

Перевірка основних контейнерів:

```bash
sudo docker compose ps -a
```

Перевірка monitoring-контейнерів:

```bash
sudo docker compose -f monitoring/docker-compose.monitoring.yml ps
```
основні Docker-контейнери

<img width="1310" height="253" alt="Знімок екрана 2026-05-14 о 12 54 07" src="https://github.com/user-attachments/assets/82fca011-e3a1-4c7d-9e73-3e298f1d9fa6" />

## 11. Перевірка роботи

Після запуску було перевірено доступність сервісів:

```text
http://PUBLIC_IP:5050
http://PUBLIC_IP:5050/metrics
http://PUBLIC_IP:9090/targets
http://PUBLIC_IP:3000
```

Також перевірку можна виконати з VM:

```bash
curl -I http://localhost:5050/health
curl -I http://localhost:5050/metrics
curl -I http://localhost:9090/targets
curl -I http://localhost:3000
```

Після виконання запитів до застосунку Prometheus починає збирати HTTP-метрики, а Grafana відображає їх на dashboard.


## Висновок

У результаті лабораторної роботи було реалізовано моніторинг контейнеризованого Docker-проєкту, розгорнутого в Microsoft Azure. Для збору метрик було використано Prometheus, Node Exporter, cAdvisor та FastAPI `/metrics` endpoint. Для візуалізації метрик було налаштовано Grafana з Prometheus data source та dashboard `Open Data AI Monitoring`.

Система моніторингу дозволяє спостерігати за станом Azure VM, Docker-контейнерів і веб-застосунку. Такий підхід допомагає швидше виявляти проблеми, аналізувати навантаження та контролювати працездатність розгорнутого сервісу.
