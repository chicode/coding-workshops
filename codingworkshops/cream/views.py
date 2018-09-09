import tarfile, gzip, json, time, io

import docker

client = docker.DockerClient(base_url='tcp://docker:2375')
api_client = docker.APIClient(base_url='tcp://docker:2375')

images = client.images.list()
if 'fable' not in [
    image.tags[0].split(':')[0] for image in images if len(image.tags)
]:
    print('BUILDING FABLE IMAGE')
    for line in api_client.build(path='/fable', tag='fable'):
        for key, value in json.loads(line).items():
            print(f'{key}: {value}')
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
    if (language == 'fsharp'):
        container = client.containers.create(
            image='fable',
            command='yarn compile',
            detach=True,
        )

        copy_to_container(
            container, 'FableDemo.fs', prepare_code(code), '/app/src'
        )

        container.start()

        result = None

        for log in container.logs(stream=True):
            log = log.decode('utf-8')
            print('log: ', log)
            if log.split(':')[0] == 'RESULT':
                result = json.loads(log.split(':')[0])

        if not result:
            raise Exception('Transpiler did not return a result!')

        return result


def copy_to_container(container, name, file_data, path):
    with create_archive(name, file_data) as archive:
        container.put_archive(path=path, data=archive)


def create_archive(name, file_data):
    pw_tarstream = io.BytesIO()
    pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')
    tarinfo = tarfile.TarInfo(name=name)
    tarinfo.size = len(file_data)
    tarinfo.mtime = time.time()

    pw_tar.addfile(tarinfo, io.BytesIO(str.encode(file_data)))
    pw_tar.close()
    pw_tarstream.seek(0)
    return pw_tarstream


def prepare_code(code):
    return '''
    module FableDemo

    open Fable.Core
    open Fable.Core.JsInterop
    open Fable.Import
    ''' + code


mutate('fsharp', 'let mutable a = 1')
