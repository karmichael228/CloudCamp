# Развёртывание Echo-Server в Kubernetes

В этой директории находятся манифесты Kubernetes для развёртывания приложения Echo-Server.

## Исходные манифесты

Предоставлены следующие манифесты:

- `namespace.yaml`: создаёт пространство имён `echo-server`
- `deployment.yaml`: развёртывает 3 реплики приложения Echo-Server
- `service.yaml`: создаёт сервис типа ClusterIP для Echo-Server
- `ingress.yaml`: создаёт ресурс Ingress для внешнего доступа (опционально)
- `registry-secret.yaml`: создаёт секрет для доступа к приватному реестру образов

### Инструкции по развёртыванию (исходные манифесты)

1. Создайте пространство имён:
   ```
   kubectl apply -f namespace.yaml
   ```

2. Создайте секрет Docker Registry (обновите учётные данные перед выполнением):
   ```
   kubectl create secret docker-registry docker-registry-secret \
     --namespace=echo-server \
     --docker-server=https://index.docker.io/v1/ \
     --docker-username=karmichael228 \
     --docker-password=ВАШ_ПАРОЛЬ \
     --docker-email=ВАШ_EMAIL
   ```

3. Разверните приложение:
   ```
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

4. (Опционально) Разверните ресурс Ingress:
   ```
   kubectl apply -f ingress.yaml
   ```

## Helm Chart

В директории `helm-chart` также предоставлена Helm-чарт.

### Инструкции по развёртыванию (Helm Chart)

1. Обновите файл `values.yaml` с вашими настройками

2. Установите Helm-чарт:
   ```
   helm install echo-server ./helm-chart/echo-server
   ```

3. Для обновления существующей установки:
   ```
   helm upgrade echo-server ./helm-chart/echo-server
   ```

4. Для удаления установки:
   ```
   helm uninstall echo-server
   ```

## Проверка

Проверьте ресурсы в пространстве имён `echo-server`:
```
kubectl get all -n echo-server
```

Проверьте работу приложения:
```
kubectl port-forward -n echo-server svc/echo-server 8080:80
```

Затем откройте в браузере: http://localhost:8080