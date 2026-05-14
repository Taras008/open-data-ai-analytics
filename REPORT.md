# Звіт до лабораторної роботи 4

## Тема

Інфраструктура як код. Розгортання Docker-проєкту в Microsoft Azure за допомогою Terraform, Azure Cloud Shell та cloud-init.

## Мета роботи

Метою лабораторної роботи було навчитися розгортати контейнеризований застосунок у хмарному середовищі Microsoft Azure без ручного налаштування сервера. Для цього було використано підхід Infrastructure as Code, де вся інфраструктура описується у вигляді коду Terraform, а початкова конфігурація Linux VM виконується автоматично через cloud-init.

У межах роботи потрібно було:

- використовувати Azure Cloud Shell як основне середовище керування;
- створити Azure-інфраструктуру за допомогою Terraform;
- автоматизувати налаштування Linux VM через cloud-init;
- встановити Docker на VM без ручного налаштування;
- запустити Docker Compose проєкт у хмарі;
- зробити веб-інтерфейс доступним через public IP;
- після демонстрації видалити ресурси через Terraform.

## 1. Початковий стан проєкту

Перед початком цієї лабораторної роботи вже був підготовлений контейнеризований Docker-проєкт. Він складається з кількох сервісів, які описані у файлі `compose.yaml`.

Основні сервіси:

- `data_load` - підготовка даних і створення SQLite-бази;
- `data_quality_analysis` - перевірка якості даних;
- `data_research` - базове дослідження даних;
- `visualization` - побудова графіків;
- `web` - FastAPI веб-інтерфейс для перегляду результатів.

Сервіси `data_load`, `data_quality_analysis`, `data_research` і `visualization` працюють як одноразові job-контейнери. Вони запускаються, виконують свою задачу і завершуються зі статусом `Exited (0)`. Це означає, що вони не впали, а успішно завершили роботу.

Постійно працює тільки контейнер `web`, бо саме він обслуговує HTTP-запити користувача.

Веб-сервіс працює на порті:

```text
5050
```

## 2. Створення окремої гілки

Для виконання лабораторної роботи було створено окрему Git-гілку:

```text
lab-terraform-azure
```


## 3. Структура інфраструктурної частини

Для опису Azure-інфраструктури було створено каталог:

```text
infra/terraform/
```

Структура каталогу:

```text
infra/terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── cloud-init.yaml
└── .gitignore
```

Призначення файлів:

- `main.tf` - опис Azure-ресурсів;
- `variables.tf` - змінні конфігурації;
- `outputs.tf` - значення, які Terraform виводить після створення ресурсів;
- `cloud-init.yaml` - сценарій автоматичного налаштування VM;
- `.gitignore` - виключення Terraform state-файлів і службових файлів.

## 4. Опис ресурсів Azure у Terraform

У файлі `main.tf` було описано створення повної мінімальної Azure-інфраструктури для запуску Docker-проєкту.

Terraform створює такі ресурси:

- Resource Group;
- Virtual Network;
- Subnet;
- Public IP;
- Network Security Group;
- Network Interface;
- Linux Virtual Machine.

Resource Group використовується як контейнер для всіх ресурсів лабораторної роботи.

Virtual Network і Subnet створюють приватну мережу для VM.

Public IP потрібен для доступу до веб-інтерфейсу з браузера.

Network Security Group керує вхідним трафіком до VM.

Network Interface підключає VM до subnet і public IP.

Linux VM є сервером, на якому запускається Docker-проєкт.

## 5. Налаштування портів

У Network Security Group було відкрито потрібні порти:

```text
22   - SSH-доступ до VM
5050 - веб-інтерфейс FastAPI-застосунку
```

Порт `22` потрібен для технічної перевірки VM через SSH.

Порт `5050` потрібен для доступу до веб-застосунку через браузер:

## 6. Змінні Terraform

У файлі `variables.tf` було винесено основні параметри, щоб їх можна було змінювати без редагування всієї Terraform-конфігурації.

Основні змінні:

- `project_name` - префікс назв ресурсів;
- `resource_group_name` - назва Resource Group;
- `location` - Azure-регіон;
- `vm_size` - розмір VM;
- `admin_username` - користувач Linux VM;
- `web_port` - порт веб-застосунку;
- `repository_url` - URL GitHub-репозиторію;
- `repository_branch` - гілка, яку потрібно розгорнути;
- `app_directory` - каталог застосунку на VM.

Під час запуску в Azure було використано регіон і розмір VM, доступні в поточній Azure subscription.

Наприклад:

```hcl
location = "eastus"
vm_size  = "Standard_D2s_v3"
```

Для x64 VM використовується Ubuntu image:

```hcl
source_image_reference {
  publisher = "Canonical"
  offer     = "0001-com-ubuntu-server-jammy"
  sku       = "22_04-lts-gen2"
  version   = "latest"
}
```

## 7. Outputs Terraform

У файлі `outputs.tf` було налаштовано виведення важливої інформації після створення інфраструктури:

- назва Resource Group;
- назва VM;
- public IP;
- SSH-команда;
- URL застосунку.

Після `terraform apply` можна виконати:

```bash
terraform output
```

і отримати URL:

```text
http://PUBLIC_IP:5050
```


## 8. Автоматизація через cloud-init

Для автоматичного налаштування VM було використано `cloud-init`.

Файл:

```text
infra/terraform/cloud-init.yaml
```

передається у VM через параметр `custom_data`.

Під час першого запуску VM cloud-init виконує такі дії:

1. Оновлює пакети.
2. Встановлює `git`, `curl`, `ca-certificates`, `gnupg`.
3. Встановлює Docker.
4. Запускає і вмикає Docker service.
5. Додає користувача `azureuser` до групи Docker.
6. Клонує GitHub-репозиторій.
7. Перемикається на потрібну гілку.
8. Переходить у каталог застосунку.
9. Запускає Docker Compose.

Основна команда запуску застосунку:

```bash
docker compose up -d --build
```

Завдяки цьому після створення VM не потрібно вручну встановлювати Docker або копіювати файли проєкту на сервер.

## 9. Робота в Azure Cloud Shell

Усі Terraform-команди виконувалися в Azure Cloud Shell. Це відповідає умові лабораторної роботи, оскільки локальний комп'ютер не використовується як машина керування.

Було відкрито Azure Portal і запущено Cloud Shell у режимі PowerShell.

Далі було виконано:

```powershell
cd /home/taras/open-data-ai-analytics
git pull
cd infra/terraform
```

Перед запуском було перевірено `terraform.tfvars`, де вказано:

```hcl
project_name        = "open-data-ai"
resource_group_name = "rg-open-data-ai"
location            = "eastus"
vm_size             = "Standard_D2s_v3"
admin_username      = "azureuser"
allowed_source_ip   = "*"
web_port            = 5050
repository_url      = "https://github.com/Taras008/open-data-ai-analytics.git"
repository_branch   = "lab-terraform-azure"
app_directory       = "/opt/open-data-ai-analytics"
```

Після цього було виконано команди Terraform:

```powershell
terraform init -upgrade
terraform fmt
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```


## 10. Створення Azure-ресурсів

Після виконання `terraform apply` було створено Resource Group:

```text
rg-open-data-ai
```

У ній були створені ресурси:

- Linux VM `open-data-ai-vm`;
- public IP;
- virtual network;
- subnet;
- network interface;
- network security group;
- disk.

**Місце для скріншота 5:** Resource Group в Azure Portal.


**Місце для скріншота 6:** сторінка Linux VM.


## 11. Підключення до VM через SSH

Для перевірки VM було виконано SSH-підключення:

```bash
ssh azureuser@PUBLIC_IP
```

Після підключення робочий каталог застосунку знаходився за шляхом:

```text
/opt/open-data-ai-analytics
```

У цьому каталозі знаходиться код проєкту, який був отриманий з GitHub через cloud-init.


## 12. Перевірка cloud-init

Стан cloud-init було перевірено командою:

```bash
sudo cloud-init status --long
```

У результаті було видно, що cloud-init завершив виконання. Навіть якщо Azure показує warning про IMDS, важливо, що немає критичних помилок у полі `errors`.

Для детальної діагностики можна використовувати:

```bash
sudo tail -100 /var/log/cloud-init-output.log
```

## 13. Перевірка Docker Compose

На VM було виконано:

```bash
cd /opt/open-data-ai-analytics
sudo docker compose ps -a
```

Результат показав, що:

- `data_load` завершився зі статусом `Exited (0)`;
- `data_quality_analysis` завершився зі статусом `Exited (0)`;
- `data_research` завершився зі статусом `Exited (0)`;
- `visualization` завершився зі статусом `Exited (0)`;
- `web` працює у статусі `Up`.

Це очікувана поведінка. Аналітичні модулі є одноразовими job-контейнерами, а `web` є постійним HTTP-сервісом.

**Місце для скріншота 8:** Docker Compose status.


## 14. Перевірка data_load

Окремо було перевірено логи сервісу `data_load`:

```bash
sudo docker compose logs --tail=100 data_load
```

У логах було видно, що модуль використав готовий CSV-файл і створив SQLite-базу:

```text
Using existing processed CSV: data/processed/income_by_region_clean.csv
Saved database: db/income.db table: income_by_region
```

Початково при запуску в Azure виникла проблема з отриманням XLSX-файлу із зовнішнього джерела: сервер повертав `HTTP Error 403: Forbidden`. Щоб зробити розгортання стабільним, було додано готовий CSV-файл у репозиторій, а `data_load` було змінено так, щоб він спочатку використовував існуючий CSV.

Це зробило cloud deployment незалежним від доступності зовнішнього джерела даних.


## 15. Перевірка веб-сервісу

Працездатність FastAPI web-сервісу було перевірено на VM:

```bash
curl http://localhost:5050/health
```

Сервіс повернув:

```json
{"status":"ok"}


## 17. Видалення інфраструктури

Після завершення демонстрації ресурси потрібно видалити, щоб не витрачати Azure credit.

Видалення виконується з Azure Cloud Shell у каталозі Terraform:

```powershell
cd /home/taras/open-data-ai-analytics/infra/terraform
terraform destroy
```

Після запиту підтвердження потрібно ввести:

```text
yes
```

Якщо Terraform state недоступний, Resource Group можна видалити через Azure CLI:

```powershell
az group delete --name rg-open-data-ai --yes
```


## Висновок

У результаті лабораторної роботи було реалізовано хмарне розгортання Docker-проєкту в Microsoft Azure за допомогою Terraform і cloud-init.

Terraform дозволив описати всю інфраструктуру як код: Resource Group, мережу, subnet, public IP, NSG, network interface та Linux VM. Це робить розгортання повторюваним і керованим.

Cloud-init автоматизував початкове налаштування Linux VM: встановив Docker, отримав код проєкту з GitHub і запустив Docker Compose. Завдяки цьому не потрібно вручну встановлювати залежності на сервері.

Після розгортання застосунок став доступним через public IP на порті `5050`. Перевірка через Docker Compose показала, що всі модулі успішно виконались, а web-сервіс працює та відповідає на healthcheck-запит.

Таким чином, у лабораторній роботі було виконано повний цикл Infrastructure as Code: опис інфраструктури, автоматичне створення ресурсів, автоматичне налаштування VM, запуск контейнеризованого застосунку та подальше видалення ресурсів.
