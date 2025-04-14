## Development

### build

```shell
docker build --platform linux/amd64 --target farm-notifier -t farm-notifier:latest .
```

### run

```shell
docker run --platform linux/amd64 --rm farm-notifier:latest STULTS
```

### push

```shell
docker tag farm-notifier:latest "ghcr.io/dancavallaro/farm-notifier/farm-notifier:$(cat version)"
docker push "ghcr.io/dancavallaro/farm-notifier/farm-notifier:$(cat version)"
```

## TODOs

* Replace S3 with in-cluster storage (Minio?)
* Less ugly email template
* Don't send email if there's no change
* For string (non-list) updates, show a colorized word diff
* Web UI to scroll through past updates, show dates that items were added and removed