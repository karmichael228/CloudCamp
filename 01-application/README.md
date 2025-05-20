## Сборка Docker-образа

Создаю образ, вводя аргумент сборки для установки переменной окружения `AUTHOR`:

```bash
docker build --build-arg AUTHOR="karmichael228" -t karmichael228/echo-server:1.0 .
```

![Результат сборки](../images/сборка_образа.png)

## Запуск контейнера

Запускаю контейнер локально:

```bash
docker run --rm --name cloud-cont -p 8000:8000 karmichael228/echo-server:1.0
```

![Запуск](../images/запуск_контейнера.png)

Захожу в браузере по адресу http://localhost:8000 и убеждаюсь, что все работает

![Проверка в браузере](../images/проверка_в_браузере.png)
## Тестирование сервиса

Проверяю сервер при помощи curl:

```bash
curl http://localhost:8000
```

![Проверка curl](../images/проверка_curl.png)

## Публикация в Docker Hub

Выполняю аутентификацию:

```bash
docker login
```

После отправляю образ на DockerHub:

```bash
docker push karmichael228/echo-server:1.0
```

Получаю JWT-токен
![JWT-токен](../images/JWT-token.png)

Делаю репозиторий приватным:
![Результат](../images/private_registry.png)

## P.S.

В дальнейшем(в пункте 2) столкнулся с конфликтами архитектур, так как работаю на arm64. Поэтому я пересобрал образ учитывая архитектуру linux/amd64 облачного сервера от cloud.ru и заново запушил образ на Docker Hub в свой приватный репозиторий:

![Пересборка образа под архитектуру amd64](../images/пересборка_amd64.png)
