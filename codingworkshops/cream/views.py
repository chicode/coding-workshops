import docker
from subprocess import call
import json

client = docker.DockerClient(base_url='tcp://docker:2375')
client_low = docker.APIClient(base_url='tcp://docker:2375')

images = client.images.list()
print(images)
"""
if 'fable' not in images:
    gen = client_low.build(path='/codingworkshops/fable', pull=False)

    for line in gen:
        for key, value in json.loads(line).items():
            print(f'{key}: {value}')
            """
"""
class Language(graphene.Enum):
    FSHARP = 1

class CompileCode(graphene.Mutation):
    class Arguments:
        language = Language(required=True)
        code = graphene.String(required=True)

    code = graphene.String(required=True)
"""


def mutate(language, code):
    print(1)
    if (language == 'fsharp'):
        options = {
            'image': 'fable',
        }
        container = client.containers.run(image)

        container.put_archive('/app/src/FableDemo.fs', code.encode('zlib'))
        print(container.exec_run('yarn compile', workdir='/app'))


#mutate('fsharp', 'let mutable a = 1')
