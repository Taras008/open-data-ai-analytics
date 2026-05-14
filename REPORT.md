# Звіт до лабораторної роботи

## Тема

Інфраструктура як код. Розгортання Docker-проєкту в Microsoft Azure за допомогою Terraform, Azure Cloud Shell та cloud-init.

## Мета роботи

Метою лабораторної роботи було навчитися створювати хмарну інфраструктуру як код за допомогою Terraform, використовувати Azure Cloud Shell як основне середовище керування, автоматизувати налаштування Linux VM через cloud-init та розгорнути контейнеризований Docker-проєкт у Microsoft Azure.

## 1. Підготовка Docker-проєкту

Перед виконанням цієї лабораторної роботи вже був підготовлений Docker-проєкт, який складається з таких сервісів:

- `data_load` - завантаження та підготовка даних;
- `data_quality_analysis` - перевірка якості даних;
- `data_research` - дослідження даних;
- `visualization` - побудова графіків;
- `web` - FastAPI веб-інтерфейс;
- SQLite-база даних `db/income.db`.

Усі сервіси запускаються через `compose.yaml`. Веб-інтерфейс доступний на порті `5050`.

## 2. Створення Terraform-структури

Для інфраструктурної частини було створено каталог:

```text
infra/terraform/
```

У ньому розміщено файли:

```text
main.tf
variables.tf
outputs.tf
cloud-init.yaml
.gitignore
```

Файл `main.tf` містить опис Azure-ресурсів.

Файл `variables.tf` містить змінні конфігурації.

Файл `outputs.tf` виводить public IP, URL веб-інтерфейсу та SSH-команду.

Файл `cloud-init.yaml` відповідає за автоматичне налаштування VM після створення.

## 3. Опис Azure-інфраструктури через Terraform

У Terraform було описано створення таких ресурсів Azure:

- Resource Group;
- Virtual Network;
- Subnet;
- Public IP;
- Network Security Group;
- Network Interface;
- Linux Virtual Machine.

Також було налаштовано правила безпеки:

- відкрито порт `22` для SSH;
- відкрито порт `5050` для веб-інтерфейсу.

Linux VM створюється на базі Ubuntu Server 22.04 LTS. Для доступу до VM використовується SSH-ключ.

## 4. Налаштування cloud-init

У файл `cloud-init.yaml` було додано сценарій першого запуску VM.

Cloud-init виконує такі дії:

1. Оновлює пакети системи.
2. Встановлює `git`, `curl`, `gnupg`, `ca-certificates`.
3. Додає офіційний Docker repository.
4. Встановлює Docker Engine.
5. Встановлює Docker Compose plugin.
6. Вмикає і запускає Docker service.
7. Клонує GitHub-репозиторій проєкту.
8. Переходить у каталог застосунку.
9. Запускає Docker Compose:

```bash
docker compose up --build -d
```

Таким чином, після створення VM застосунок запускається автоматично без ручного входу на сервер.

## 5. Робота в Azure Cloud Shell

Для виконання лабораторної роботи було відкрито Azure Portal і запущено Azure Cloud Shell у режимі Bash.

У Cloud Shell було виконано клонування репозиторію:

```bash
git clone https://github.com/Taras008/open-data-ai-analytics.git
cd open-data-ai-analytics
git checkout lab-terraform-azure
cd infra/terraform
```

Після цього було виконано стандартні команди Terraform:

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Після підтвердження `terraform apply` Terraform створив усі необхідні Azure-ресурси.

## 6. Отримання public IP

Після завершення `terraform apply` Terraform вивів значення:

```text
public_ip_address
web_url
swagger_url
ssh_command
```

Веб-інтерфейс став доступний за адресою:

```text
http://PUBLIC_IP:5050
```

Swagger-документація FastAPI:

```text
http://PUBLIC_IP:5050/docs
```

## 7. Перевірка роботи застосунку

Після завершення cloud-init було перевірено доступність веб-інтерфейсу через браузер.

Також у Cloud Shell можна перевірити відповідь сервісу командами:

```bash
curl http://PUBLIC_IP:5050
curl http://PUBLIC_IP:5050/health
curl http://PUBLIC_IP:5050/api/quality
```

Веб-інтерфейс відображає:

- короткий опис проєкту;
- результати перевірки якості даних;
- результати дослідження;
- графіки;
- попередній перегляд даних.

## 8. Видалення інфраструктури

Після демонстрації роботи застосунку Azure-ресурси було видалено командою:

```bash
terraform destroy
```

Це необхідно для того, щоб не витрачати Azure credit на VM, disk, public IP та інші ресурси.

## Висновок

У результаті лабораторної роботи було реалізовано розгортання Docker-проєкту в Microsoft Azure за допомогою підходу Infrastructure as Code. Terraform створює всю необхідну інфраструктуру, а cloud-init автоматично налаштовує Linux VM, встановлює Docker і запускає контейнеризований застосунок.

Уся робота виконується через Azure Cloud Shell, тому локальний комп'ютер не використовується як машина керування. Такий підхід дозволяє швидко, повторювано й автоматизовано розгортати проєкт у хмарному середовищі.
