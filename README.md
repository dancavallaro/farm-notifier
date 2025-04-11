## Development

### build

```shell
docker build --platform linux/amd64 -t farm-notifier:latest .
```

### run

```shell
docker run --platform linux/amd64 --rm farm-notifier:latest STULTS
```

## TODOs

* Replace S3 with in-cluster storage (Minio?)
* For string (non-list) updates, show a colorized word diff
* Web UI to scroll through past updates
* Show dates that items were added and removed