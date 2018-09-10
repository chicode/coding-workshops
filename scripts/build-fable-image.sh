#! /bin/bash

docker-compose run docker sh << EOF
	docker --host docker build -t fable fable
EOF
