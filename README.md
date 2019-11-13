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

- [x] Get battery state: GET `/api/battery`
- [x] Say some text: GET `/api/say?text=Hello`
- [x] Set volume level: GET `/api/volume/<level>` level: 0-4
- [x] Behavior: Drive on charger: GET `/api/behavior/drive_on_charger`
- [x] Behavior: Drive off charger: GET `/api/behavior/drive_off_charger`
- [x] Animation: Play: GET `/api/animation/<animation_id>`
- [x] Animation: Get animations list GET `/api/animation/list`
- [x] Animation: Play trigger GET `/api/animation-trigger/<animation_id>`
- [x] Animation: Get animations triggers list GET `/api/animation-trigger/list`
- [x] Status GET `/api/status`
- [ ] More Behaviors
- [ ] Set eyes color
- [ ] ...

Fancy (custom methods) API

- [x] Notify about gitlab pipline passed GET `/api/fancy/gitlab-build-finished`
- [x] Get status resting/active GET `/api/fancy/status`
