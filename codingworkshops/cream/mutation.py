import tarfile, gzip, json, time, io, re, time, collections

import docker
import graphene


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


TEMPLATE = '''
module FableDemo

open Fable.Core
open Fable.Core.JsInterop
open Fable.Import.Browser

[<Emit("window.sprite($0, $1, $2)")>]
let sprite i x y = jsNative
'''

# lines until user code
# TODO deduce the 2 automatically
CODE_OFFSET = len(TEMPLATE.split('\n')) + 2


def prepare_code(code):
    return TEMPLATE + code


class Language(graphene.Enum):
    FSHARP = 1


class Location(graphene.ObjectType):
    line = graphene.Int(required=True)
    ch = graphene.Int(required=True)


class Error(graphene.ObjectType):
    from_ = graphene.Field(Location, required=True)
    to = graphene.Field(Location, required=True)
    message = graphene.String(required=True)


MAX_TIMES = 20

total_times = {1: collections.deque([9], maxlen=MAX_TIMES)}


class Query(graphene.ObjectType):
    compilation_time = graphene.Field(
        graphene.Float, language=Language(required=True)
    )

    def resolve_compilation_time(self, info, language):
        if total_times[language]:
            return sum(total_times[language]) / len(total_times[language])
        return 0


class CompileCode(graphene.Mutation):
    class Arguments:
        language = Language(required=True)
        code = graphene.String(required=True)

    success = graphene.Boolean(required=True)
    code = graphene.String()
    errors = graphene.List(Error)
    warnings = graphene.List(Error)

    def mutate(self, info, language, code):
        start = time.time()
        if (language == 1):
            client = docker.DockerClient(base_url='tcp://docker:2375')
            container = client.containers.create(
                image='fable',
                command=['yarn', 'compile'],
                detach=True,
                auto_remove=True,
                privileged=False,
            )

            copy_to_container(
                container, 'FableDemo.fs', prepare_code(code), '/app/src'
            )

            container.start()

            logs = {}
            code_data = False
            code = []

            for log in container.logs(stream=True):
                log = log.decode('utf-8')
                print(log)
                if log.startswith('DATA'):
                    logs = json.loads(log[len('DATA'):])
                elif log.startswith('CODE'):
                    code_data = True
                elif code_data:
                    code.append(log)

            def format(message):
                line, ch = map(
                    int,
                    re.search(r'(?<=: \()\d*,\d*(?=\))',
                              message).group(0).split(',')
                )
                text = re.search(
                    r'(?<=FSHARP: ).*', message, flags=re.S
                ).group(0)
                return Error(
                    from_=Location(line=line - CODE_OFFSET, ch=ch - 1),
                    to=Location(line=line - CODE_OFFSET, ch=ch),
                    message=text
                )

            formatted_logs = {
                log_type + 's':
                [format(message) for message in logs[log_type]]
                for log_type in logs
            }

            total_times[language].append(time.time() - start)

            if 'errors' in formatted_logs:
                return CompileCode(success=False, **formatted_logs)

            code[-1] = re.search('.*?(?=Done in)', code[-1]).group(0)

            return CompileCode(
                success=True, code=''.join(code), **formatted_logs
            )


class Mutation(graphene.ObjectType):
    compile_code = CompileCode.Field()
