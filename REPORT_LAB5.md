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

**Місце для скріншота 2:** сторінка `http://PUBLIC_IP:5050/metrics`.

```text
Вставити скріншот FastAPI /metrics
```

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

**Місце для скріншота 3:** список monitoring-контейнерів.

```bash
sudo docker compose -f monitoring/docker-compose.monitoring.yml ps
```

```text
Вставити скріншот запущених prometheus/grafana/node-exporter/cadvisor
```

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

```text
Вставити скріншот Prometheus targets, де всі targets мають стан UP
```

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

У Grafana було створено dashboard:

```text
Open Data AI Monitoring
```

На dashboard додано панелі:

- VM CPU usage;
- VM memory usage;
- Observed containers;
- Container CPU usage;
- Container memory usage;
- FastAPI request rate;
- FastAPI p95 latency.

Ці панелі дозволяють оцінити стан інфраструктури, Docker-контейнерів і самого веб-застосунку.

**Місце для скріншота 6:** Grafana dashboard.

```text
http://PUBLIC_IP:3000
```

```text
Вставити скріншот dashboard Open Data AI Monitoring
```

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

**Місце для скріншота 7:** Terraform output.

```text
Вставити скріншот terraform output з app_url, grafana_url, prometheus_url
```

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

**Місце для скріншота 8:** основні Docker-контейнери.

```text
Вставити скріншот sudo docker compose ps -a
```

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

## 12. Що було продемонстровано

Під час демонстрації було показано:

- роботу основного Docker-застосунку;
- endpoint `/metrics` у FastAPI;
- Prometheus targets зі станом `UP`;
- Grafana data source Prometheus;
- Grafana dashboard з метриками VM, контейнерів і застосунку;
- список Docker-контейнерів на Azure VM;
- відкриті порти в Azure NSG.

## 13. Труднощі під час виконання

Під час виконання лабораторної роботи виникли такі труднощі:

- потрібно було переконатися, що Azure VM використовує правильну Git-гілку `lab-5-monitoring`;
- після оновлення коду потрібно було перезібрати web-контейнер, щоб з'явився endpoint `/metrics`;
- Grafana dashboard не одразу з'явився, тому потрібно було перевірити provisioning-файли та перезапустити Grafana;
- для доступу з браузера потрібно було відкрити порти `3000` і `9090` у Network Security Group.

## Висновок

У результаті лабораторної роботи було реалізовано моніторинг контейнеризованого Docker-проєкту, розгорнутого в Microsoft Azure. Для збору метрик було використано Prometheus, Node Exporter, cAdvisor та FastAPI `/metrics` endpoint. Для візуалізації метрик було налаштовано Grafana з Prometheus data source та dashboard `Open Data AI Monitoring`.

Система моніторингу дозволяє спостерігати за станом Azure VM, Docker-контейнерів і веб-застосунку. Такий підхід допомагає швидше виявляти проблеми, аналізувати навантаження та контролювати працездатність розгорнутого сервісу.
