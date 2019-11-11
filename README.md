## Usage

In local

1. Create .env file with `PROJECT_PATH=<path to current folder>`
2. Run docker-compose up -d
3. Wait a bit until containers will be created
4. Copy configs to ./configs folder or generate new with `docker exec -it vector.sdk python -m anki_vector.configure`
5. Go to http://localhost:8013/api/vector/battery

## TODO

- [ ] Gitlab-CI usage
- [ ] Checklist of all commands planned to bridge  

## API

- [x] Get battery state: GET `/api/vector/battery`
- [x] Say some text: GET `/api/vector/say?text=Hello`
- [x] Set volume level: GET `/api/vector/volume/<level>` level: 0-4