
Лабораторна робота з контейнеризації модулів аналітичного проєкту за допомогою Docker та Docker Compose.

Проєкт працює як набір окремих сервісів: завантаження даних, перевірка якості, дослідження, візуалізація та веб-інтерфейс. Кожен сервіс запускається в окремому Docker-контейнері, а спільний запуск організований через `compose.yaml`.

## Що реалізовано

У проєкті є такі модулі:

- `data_load` - завантажує початкові дані, формує CSV-файл і створює SQLite-базу даних.
- `data_quality_analysis` - перевіряє якість даних: пропуски, дублікати, типи колонок, діапазон років.
- `data_research` - виконує базове дослідження даних, рахує статистики, топ регіонів і простий прогноз.
- `visualization` - будує два графіки та зберігає їх у PNG.
- `web` - запускає FastAPI веб-інтерфейс для перегляду результатів через браузер.

Код основних модулів розміщений у директорії `src/`, а Dockerfile-и винесені в окрему директорію `docker/`.

## Структура проєкту

```text
open-data-ai-analytics/
├── compose.yaml
├── requirements.txt
├── README.md
├── data/
│   ├── raw/
│   │   └── income_by_region.xlsx
│   └── processed/
│       └── income_by_region_clean.csv
├── db/
│   └── income.db
├── docker/
│   ├── data_load.Dockerfile
│   ├── data_quality_analysis.Dockerfile
│   ├── data_research.Dockerfile
│   ├── visualization.Dockerfile
│   └── web.Dockerfile
├── reports/
│   ├── data_quality_report.json
│   ├── data_research_report.json
│   └── figures/
│       ├── top10_regions.png
│       └── ua_trend.png
├── src/
│   ├── data_load.py
│   ├── data_quality_analysis.py
│   ├── data_research.py
│   └── visualization.py
└── web/
    ├── app.py
    ├── requirements.txt
    └── templates/
        └── index.html
```

## Як працюють сервіси

### 1. data_load

Сервіс запускає файл:

```text
src/data_load.py
```

Він:

- завантажує XLSX-файл з відкритого джерела, якщо його ще немає;
- очищає дані;
- зберігає результат у CSV:

```text
data/processed/income_by_region_clean.csv
```

- створює SQLite-базу:

```text
db/income.db
```

- створює таблицю:

```text
income_by_region
```

### 2. data_quality_analysis

Сервіс запускає:

```text
src/data_quality_analysis.py
```

Він перевіряє:

- кількість рядків і колонок;
- назви колонок;
- пропущені значення;
- дублікати;
- типи даних;
- діапазон років;
- кількість унікальних регіонів.

Результат зберігається у файл:

```text
reports/data_quality_report.json
```

### 3. data_research

Сервіс запускає:

```text
src/data_research.py
```

Він виконує дослідження:

- визначає діапазон років для України;
- знаходить топ-10 регіонів за доходом за останній рік;
- будує просту модель Linear Regression;
- рахує `R2`;
- формує прогноз на наступний рік;
- рахує базові статистики.

Результат зберігається у файл:

```text
reports/data_research_report.json
```

### 4. visualization

Сервіс запускає:

```text
src/visualization.py
```

Він генерує два графіки:

```text
reports/figures/ua_trend.png
reports/figures/top10_regions.png
```

### 5. web

Сервіс запускає FastAPI-застосунок:

```text
web/app.py
```

Веб-інтерфейс показує:

- короткий опис проєкту;
- результати перевірки якості даних;
- результати дослідження;
- графіки;
- попередній перегляд завантажених даних.

Також FastAPI надає API-ендпоїнти та Swagger-документацію.

## Docker Compose

Спільний запуск описаний у файлі:

```text
compose.yaml
```

У ньому налаштовано:

- окремий контейнер для кожного сервісу;
- залежності між сервісами через `depends_on`;
- спільну Docker network `analytics-net`;
- volumes для обміну файлами між контейнерами;
- порт для веб-інтерфейсу;
- healthcheck для web-сервісу.

## Обмін даними між контейнерами

Контейнери обмінюються результатами через спільні volumes:

```yaml
./data:/app/data
./db:/app/db
./reports:/app/reports
```

Логіка така:

1. `data_load` створює CSV і SQLite-базу.
2. `data_quality_analysis` читає CSV і створює JSON-звіт.
3. `data_research` читає CSV і створює JSON-звіт з результатами дослідження.
4. `visualization` читає CSV і створює PNG-графіки.
5. `web` читає CSV, SQLite, JSON-звіти й PNG-графіки та показує їх у браузері.

## Запуск проєкту

Перед запуском потрібно відкрити Docker Desktop і переконатися, що Docker працює.

Запуск усіх сервісів:

```bash
docker compose up --build
```

Запуск у фоновому режимі:

```bash
docker compose up --build -d
```

Перевірити статус контейнерів:

```bash
docker compose ps
```

Переглянути логи:

```bash
docker compose logs -f
```

Зупинити всі контейнери:

```bash
docker compose down
```

## Порти

Веб-інтерфейс доступний за адресою:

```text
http://localhost:5050
```

Всередині контейнера FastAPI працює на порті `5000`, але на комп'ютері порт `5000` був зайнятий, тому в `compose.yaml` використано мапінг:

```yaml
ports:
  - "5050:5000"
```

Swagger-документація FastAPI:

```text
http://localhost:5050/docs
```

## API

FastAPI має такі ендпоїнти:

```text
GET /
GET /health
GET /docs
GET /api/data-preview
GET /api/quality
GET /api/research
GET /api/figures
GET /figures/{filename}
```

Приклади:

```text
http://localhost:5050/api/quality
http://localhost:5050/api/research
http://localhost:5050/api/data-preview
```

## Dockerfile-и

Для кожного сервісу створений окремий Dockerfile:

```text
docker/data_load.Dockerfile
docker/data_quality_analysis.Dockerfile
docker/data_research.Dockerfile
docker/visualization.Dockerfile
docker/web.Dockerfile
```

Python-модулі використовують спільний `requirements.txt` з кореня проєкту.

Web-сервіс використовує власний файл:

```text
web/requirements.txt
```

## Що потрібно показати під час демонстрації

1. Запуск Docker Compose:

```bash
docker compose up --build
```

2. Список контейнерів:

```bash
docker compose ps
```

3. Згенеровану SQLite-базу:

```text
db/income.db
```

4. JSON-звіти:

```text
reports/data_quality_report.json
reports/data_research_report.json
```

5. PNG-графіки:

```text
reports/figures/ua_trend.png
reports/figures/top10_regions.png
```

6. Веб-інтерфейс:

```text
http://localhost:5050
```

7. FastAPI Swagger:

```text
http://localhost:5050/docs
```

## Короткий звіт

У цій лабораторній роботі було виконано контейнеризацію модулів проєкту з аналізу відкритих даних. Для кожного основного компонента створено окремий Dockerfile. Запуск усіх сервісів організовано через `compose.yaml`.

Для збереження даних використовується SQLite-база `db/income.db`, яка створюється модулем `data_load`. Результати аналізу якості та дослідження зберігаються у JSON-файли в директорії `reports/`. Графіки зберігаються у `reports/figures/`.

Взаємодія між контейнерами організована через спільні volumes. Усі сервіси підключені до однієї Docker network `analytics-net`. Веб-інтерфейс реалізовано за допомогою FastAPI та запускається в окремому контейнері.

Основна складність під час виконання полягала в тому, що локальний порт `5000` був зайнятий іншим процесом. Тому для доступу до веб-інтерфейсу було використано порт `5050`.

## Лабораторна 5: Prometheus та Grafana

Для моніторингу Docker-проєкту додано каталог:

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

Моніторинговий стек містить:

- `prometheus` - збирає метрики;
- `grafana` - показує дашборд;
- `node-exporter` - експортує метрики Linux VM;
- `cadvisor` - експортує метрики Docker-контейнерів;
- FastAPI endpoint `/metrics` у сервісі `web`.

Prometheus збирає метрики з:

```text
prometheus:9090
node-exporter:9100
cadvisor:8080
web:5000/metrics
```

### Порти

Для Azure NSG у Terraform додано:

```text
5050 - web interface
3000 - Grafana
9090 - Prometheus
22   - SSH
```

Після розгортання сервіси доступні:

```text
http://PUBLIC_IP:5050          - застосунок
http://PUBLIC_IP:5050/metrics  - метрики FastAPI
http://PUBLIC_IP:3000          - Grafana
http://PUBLIC_IP:9090/targets  - Prometheus targets
```

Логін Grafana за замовчуванням:

```text
admin
admin
```

### Запуск на вже створеній Azure VM

Спочатку потрібно оновити код на VM:

```bash
cd /opt/open-data-ai-analytics
sudo git pull
```

Потім перезапустити основний Docker-проєкт:

```bash
sudo docker compose up --build -d
```

Після цього запустити моніторинг:

```bash
sudo docker compose -f monitoring/docker-compose.monitoring.yml up -d
```

Перевірити контейнери:

```bash
sudo docker compose ps -a
sudo docker compose -f monitoring/docker-compose.monitoring.yml ps
```

Перевірити метрики:

```bash
curl http://localhost:5050/metrics
curl http://localhost:9090/-/ready
```

### Оновлення Terraform для відкриття портів

У Cloud Shell потрібно перейти в Terraform-каталог:

```bash
cd open-data-ai-analytics/infra/terraform
git pull
terraform fmt
terraform validate
terraform plan
terraform apply
```

Це оновить Network Security Group і відкриє порти `3000` та `9090`.

### Що показати на захисті

Потрібно показати:

- список контейнерів основного застосунку;
- список контейнерів моніторингу;
- сторінку Prometheus targets:

```text
http://PUBLIC_IP:9090/targets
```

- Grafana data source Prometheus;
- Grafana dashboard `Open Data AI Monitoring`;
- панелі CPU VM, RAM VM, кількість контейнерів, CPU/RAM web-контейнера, FastAPI request rate;
- метрики застосунку:

```text
http://PUBLIC_IP:5050/metrics
```

## Лабораторна 6: GitOps з Argo CD та k3s

Для ознайомлення з GitOps додано каталог:

```text
gitops/
├── app/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── argocd/
│   └── application.yaml
└── scripts/
    └── install-k3s-argocd.sh
```

У цій лабораторній GitHub-репозиторій є джерелом істини для Kubernetes-маніфестів. Argo CD читає шлях `gitops/app` з гілки `lab-6-gitops` і автоматично синхронізує кластер k3s.

### Що розгортається

Kubernetes-конфігурація створює:

- namespace `open-data-ai`;
- deployment `open-data-ai-web`;
- service `open-data-ai-web` типу `NodePort`;
- Argo CD Application `open-data-ai-web`.

Застосунок доступний через Kubernetes NodePort:

```text
http://PUBLIC_IP:30080
```

Argo CD UI доступний через:

```text
http://PUBLIC_IP:30880
```

### Підготовка Azure VM

Terraform відкриває додаткові порти:

```text
30080 - GitOps web application
30880 - Argo CD HTTP UI
30443 - Argo CD HTTPS UI
```

Після `terraform apply` потрібно зайти на VM:

```bash
ssh azureuser@PUBLIC_IP
```

Перейти в репозиторій:

```bash
cd /opt/open-data-ai-analytics
sudo git fetch
sudo git checkout lab-6-gitops
sudo git pull
```

### Встановлення k3s та Argo CD

Запустити підготовлений скрипт:

```bash
sudo ./gitops/scripts/install-k3s-argocd.sh
```

Скрипт:

- встановлює k3s;
- збирає Docker image `open-data-ai-web:gitops`;
- імпортує image у k3s containerd;
- встановлює Argo CD;
- відкриває Argo CD через NodePort;
- застосовує `gitops/argocd/application.yaml`;
- показує початковий пароль Argo CD admin.

Перевірити k3s:

```bash
kubectl get nodes
```

Перевірити Argo CD:

```bash
kubectl get pods -n argocd
```

Перевірити GitOps-застосунок:

```bash
kubectl get all -n open-data-ai
```

### Доступ до Argo CD

Відкрити:

```text
http://PUBLIC_IP:30880
```

Логін:

```text
admin
```

Пароль можна отримати командою:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### Демонстрація автоматичного оновлення

Для демонстрації GitOps можна змінити у файлі:

```text
gitops/app/deployment.yaml
```

Наприклад, змінити:

```yaml
replicas: 1
```

на:

```yaml
replicas: 2
```

Або змінити:

```yaml
value: "GitOps release: initial version"
```

на:

```yaml
value: "GitOps release: updated from Git"
```

Після commit і push:

```bash
git add gitops/app/deployment.yaml
git commit -m "Update GitOps deployment"
git push
```

Argo CD має автоматично побачити зміну, синхронізувати застосунок і привести кластер до нового стану.

Перевірити:

```bash
kubectl get deployment -n open-data-ai
kubectl get pods -n open-data-ai
curl http://localhost:30080/health
```

### Rollback

Rollback виконується через Git:

```bash
git revert HEAD
git push
```

Після цього Argo CD автоматично поверне Kubernetes-стан до попередньої версії.

### Перевірка моніторингу після GitOps

Після GitOps-оновлення потрібно переконатися, що попередній monitoring stack працює:

```text
http://PUBLIC_IP:3000
http://PUBLIC_IP:9090/targets
```

Prometheus також має бачити GitOps-застосунок як target:

```text
gitops-web
```

### Що показати на захисті

Потрібно показати:

- `kubectl get nodes`;
- `kubectl get pods -n argocd`;
- Argo CD UI зі станом `Synced`;
- `kubectl get all -n open-data-ai`;
- застосунок у браузері `http://PUBLIC_IP:30080`;
- commit у GitHub, який змінив `deployment.yaml`;
- автоматичне оновлення в Argo CD;
- rollback через `git revert`;
- Grafana dashboard і Prometheus targets після GitOps-оновлення.
