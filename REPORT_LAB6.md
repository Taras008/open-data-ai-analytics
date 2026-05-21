# Звіт до лабораторної роботи 6

## Тема

Ознайомлення із практиками GitOps. Автоматизоване розгортання застосунку в Kubernetes за допомогою Argo CD.

## Мета роботи

Метою лабораторної роботи було ознайомитися з GitOps-підходом і реалізувати автоматизоване розгортання застосунку в Kubernetes-середовище на основі змін у GitHub-репозиторії.

У роботі використовувалися:

- Azure Linux VM;
- k3s як полегшений Kubernetes-кластер;
- Argo CD як GitOps-інструмент;
- GitHub repository як джерело істини;
- Kubernetes YAML manifests;
- попередньо налаштований Docker/FastAPI застосунок.

## 1. Ідея GitOps

GitOps - це підхід, за якого бажаний стан системи описується у Git-репозиторії. Спеціальний агент, у цій роботі Argo CD, постійно порівнює стан Kubernetes-кластера з тим, що описано в Git.

Якщо в Git з'являється зміна, Argo CD автоматично застосовує її до кластера.

Основні принципи GitOps:

- Git є джерелом істини;
- конфігурація описується декларативно;
- зміни виконуються через commit і push;
- розгортання відбувається автоматично;
- rollback виконується через повернення попереднього стану в Git.

## 2. Початкові умови

Перед виконанням цієї лабораторної роботи вже були виконані попередні етапи:

- Docker-проєкт контейнеризовано;
- застосунок розгорнуто в Azure VM;
- інфраструктура описана через Terraform;
- VM налаштовується через cloud-init;
- моніторинг реалізовано через Prometheus і Grafana.

Для GitOps було створено окрему гілку:

```text
lab-6-gitops
```

**Місце для скріншота 1:** GitHub branch `lab-6-gitops`.

```text
Вставити скріншот гілки lab-6-gitops у GitHub
```

## 3. Структура GitOps-конфігурації

У репозиторії було створено каталог:

```text
gitops/
```

Структура:

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

Каталог `gitops/app` містить Kubernetes manifests застосунку.

Каталог `gitops/argocd` містить Argo CD Application.

Каталог `gitops/scripts` містить допоміжний скрипт для встановлення k3s, Argo CD та першого запуску GitOps-розгортання.

## 4. Kubernetes namespace

У файлі:

```text
gitops/app/namespace.yaml
```

було описано namespace:

```text
open-data-ai
```

У цьому namespace розгортається GitOps-версія веб-застосунку.

## 5. Kubernetes Deployment

У файлі:

```text
gitops/app/deployment.yaml
```

було описано deployment:

```text
open-data-ai-web
```

Deployment містить:

- назву застосунку;
- labels і selectors;
- кількість реплік;
- Docker image;
- відкритий порт контейнера `5000`;
- readinessProbe;
- livenessProbe;
- змінну середовища `GITOPS_RELEASE_MESSAGE`.

Для демонстрації GitOps-оновлення можна змінювати:

```yaml
replicas: 1
```

або:

```yaml
GITOPS_RELEASE_MESSAGE
```

Після commit і push Argo CD автоматично синхронізує ці зміни з Kubernetes.

## 6. Kubernetes Service

У файлі:

```text
gitops/app/service.yaml
```

було описано Service типу `NodePort`.

Service відкриває застосунок на порті:

```text
30080
```

Зовнішній доступ:

```text
http://PUBLIC_IP:30080
```

**Місце для скріншота 2:** застосунок, відкритий через NodePort.

```text
Вставити скріншот http://PUBLIC_IP:30080
```

## 7. Argo CD Application

У файлі:

```text
gitops/argocd/application.yaml
```

було описано Argo CD Application:

```text
open-data-ai-web
```

Application:

- підключається до GitHub repository;
- використовує гілку `lab-6-gitops`;
- читає manifests з папки `gitops/app`;
- розгортає застосунок у namespace `open-data-ai`;
- має ввімкнену автоматичну синхронізацію;
- має ввімкнений self-heal.

Це означає, що Argo CD автоматично застосовує зміни з Git і виправляє ручні зміни в кластері.

## 8. Встановлення k3s

На Azure Linux VM було встановлено k3s.

Перевірка роботи кластера:

```bash
kubectl get nodes
```

Очікуваний результат:

```text
open-data-ai-vm   Ready
```

**Місце для скріншота 3:** `kubectl get nodes`.

```text
Вставити скріншот kubectl get nodes
```

## 9. Встановлення Argo CD

У Kubernetes було створено namespace:

```text
argocd
```

Після цього було встановлено Argo CD.

Перевірка pod-ів:

```bash
kubectl get pods -n argocd
```

Очікувано pod-и Argo CD мають бути в стані `Running`.

**Місце для скріншота 4:** pod-и Argo CD.

```text
Вставити скріншот kubectl get pods -n argocd
```

## 10. Доступ до Argo CD

Argo CD було відкрито через NodePort:

```text
http://PUBLIC_IP:30880
```

Логін:

```text
admin
```

Початковий пароль отримується командою:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

**Місце для скріншота 5:** Argo CD login або Argo CD UI.

```text
Вставити скріншот Argo CD
```

## 11. Перше GitOps-розгортання

Після створення Argo CD Application система автоматично прочитала manifests з:

```text
gitops/app
```

Після синхронізації застосунок перейшов у стан:

```text
Synced
Healthy
```

Перевірка ресурсів:

```bash
kubectl get all -n open-data-ai
```

**Місце для скріншота 6:** Argo CD Application зі станом `Synced`.

```text
Вставити скріншот Argo CD Synced / Healthy
```

## 12. Автоматичне оновлення

Для демонстрації автоматичного оновлення було змінено файл:

```text
gitops/app/deployment.yaml
```

Наприклад:

```yaml
replicas: 1
```

було змінено на:

```yaml
replicas: 2
```

Або було змінено значення:

```yaml
GITOPS_RELEASE_MESSAGE
```

Після цього зміни було закомічено й запушено:

```bash
git add gitops/app/deployment.yaml
git commit -m "Update GitOps deployment"
git push
```

Argo CD автоматично виявив зміну в GitHub і синхронізував Kubernetes-кластер без ручного `kubectl apply`.

Перевірка:

```bash
kubectl get deployment -n open-data-ai
kubectl get pods -n open-data-ai
curl http://localhost:30080/health
```

**Місце для скріншота 7:** commit у GitHub, який викликав оновлення.

```text
Вставити скріншот commit/push
```

**Місце для скріншота 8:** оновлений стан Argo CD після sync.

```text
Вставити скріншот automatic sync в Argo CD
```

## 13. Rollback

Rollback було виконано через Git.

Для цього останній commit було скасовано:

```bash
git revert HEAD
git push
```

Після push Argo CD автоматично повернув Kubernetes-кластер до попереднього стану.

Це демонструє головну перевагу GitOps: повернення до попередньої версії виконується через Git-історію.

**Місце для скріншота 9:** rollback commit або Argo CD після rollback.

```text
Вставити скріншот rollback
```

## 14. Сумісність із моніторингом

Після GitOps-оновлення було перевірено, що попередній monitoring stack продовжує працювати.

Перевірено:

```text
http://PUBLIC_IP:3000
http://PUBLIC_IP:9090/targets
```

Prometheus продовжує збирати метрики, Grafana dashboard залишається доступним.

Додатково Prometheus може бачити GitOps-застосунок як target:

```text
gitops-web
```

**Місце для скріншота 10:** Grafana dashboard після GitOps-оновлення.

```text
Вставити скріншот Grafana dashboard
```

## 15. Що було продемонстровано

Під час виконання лабораторної роботи було продемонстровано:

- встановлений k3s-кластер на Azure VM;
- встановлений Argo CD;
- GitHub repository як джерело істини;
- Kubernetes manifests у папці `gitops/app`;
- Argo CD Application;
- автоматичне розгортання застосунку;
- автоматичне оновлення після commit і push;
- rollback через Git;
- сумісність із Prometheus і Grafana.

## 16. Труднощі під час виконання

Під час виконання лабораторної роботи були такі особливості:

- потрібно було підготувати локальний Docker image для k3s;
- Argo CD працює з Kubernetes manifests, тому застосунок потрібно було описати декларативно;
- для доступу через браузер потрібно було відкрити NodePort-порти в Azure NSG;
- потрібно було стежити, щоб Argo CD Application використовував правильну гілку `lab-6-gitops`;
- для демонстрації оновлення потрібно було виконати зміну саме через Git, а не вручну через `kubectl`.

## Висновок

У результаті лабораторної роботи було реалізовано GitOps-підхід для розгортання FastAPI-застосунку в Kubernetes-середовище на Azure Linux VM.

k3s використовується як легкий Kubernetes-кластер, а Argo CD відповідає за автоматичну синхронізацію стану кластера з GitHub-репозиторієм. Усі Kubernetes manifests зберігаються в Git, а зміни застосовуються через commit і push.

Було показано, що Argo CD автоматично розгортає застосунок, реагує на зміни в Git і дозволяє виконувати rollback через Git-історію. Також було перевірено, що після GitOps-оновлень моніторинг через Prometheus і Grafana залишається працездатним.
