from django.apps import AppConfig
import docker, json


class CreamConfig(AppConfig):
    name = 'codingworkshops.cream'

    def ready(self):
        client = docker.DockerClient(base_url='tcp://docker:2375')
        api_client = docker.APIClient(base_url='tcp://docker:2375')

        images = client.images.list()
        print(images)
        if 'fable' not in [
            image.tags[0].split(':')[0] for image in images if len(image.tags)
        ]:
            print('BUILDING FABLE IMAGE')
            for line in api_client.build(path='/fable', rm=True, tag='fable'):
                for key, value in json.loads(line).items():
                    print(f'{key}: {value}')
