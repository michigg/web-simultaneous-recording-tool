import json
import os
from multiprocessing import Process

from engineio.payload import Payload
from flask import Flask
from flask_socketio import Namespace, SocketIO, emit, join_room
from datetime import datetime

Payload.max_decode_packets = 10000000000000000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")
socketio = SocketIO(app,
                    cors_allowed_origins="*",
                    logger=True,
                    engineio_logger=True,
                    max_http_buffer_size=100000000000000000,
                    ping_interval=(15, 5)
                    )
RESULT_DIR = './results'


class FileController:
    def __init__(self, base_dir='./results', sub_path='test', file_name_postfix='test'):
        self.base_dir = base_dir
        self.sub_path = sub_path
        self.file_name_postfix = file_name_postfix

    def save_json(self, analysis_data):
        self.prepare_directory()
        with open(self._get_path(), 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)

    def save_audio_file(self, record):
        self.prepare_directory()
        with open(self._get_path(wav=True), 'wb') as f:
            f.write(record)

    def _get_directory(self):
        return f'{self.base_dir}/{self.sub_path}'

    def _get_path(self, wav=False):
        current_time = datetime.now()
        directory = self._get_directory()
        if not wav:
            return f'{directory}/{current_time.strftime("%Y-%m-%d-%H-%M-%S")}-{self.file_name_postfix}.json'
        else:
            return f'{directory}/{current_time.strftime("%Y-%m-%d-%H-%M-%S")}-{self.file_name_postfix}.wav'

    def prepare_directory(self):
        directory = self._get_directory()
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_directory_structure(self, use_root_dir=False):
        directory = self._get_directory()
        if use_root_dir:
            directory = self.base_dir
        file_names = []
        file_paths = []
        for (dirpath, dirnames, filenames) in os.walk(directory):
            socketio.sleep(0)
            for filename in filenames:
                if filename.endswith('.json'):
                    file_names.append(filename)
                    file_paths.append(os.sep.join([dirpath, filename]))
        return file_paths, file_names


class JsonController:
    def __init__(self):
        pass

    def _get_spectrum_array(self, array):
        return [self._to_array(element) for element in array]

    def _to_array(self, array_as_string):
        return json.loads(array_as_string)

    def clean_json_data(self, analysis_data):
        analysis_data['audio']['amplitudeSpectrums'] = self._get_spectrum_array(
            analysis_data['audio']['amplitudeSpectrums'])


def save_process(sub_path, file_name_postfix, data):
    file_controller = FileController(sub_path=f'{sub_path}', file_name_postfix=file_name_postfix)
    file_controller.save_json(data)


def save(sub_path, file_name_postfix, data):
    p = Process(target=save_process, args=(sub_path, file_name_postfix, data))
    p.start()


class RootNamespace(Namespace):
    def __init__(self, *args):
        super().__init__(args)
        self.users = 0
        self.room_name = 'Default'
        self.json_controller = JsonController()
        self.test_id = ''
        self.test_iteration = ''
        self.file_paths = []
        self.file_names = []

    def on_handle_message(self, data):
        app.logger.info('Received unknown message!', data)

    def on_finished_analysis(self, data):
        app.logger.info('Finished analysis!')
        app.logger.info(data)

        test_id = data["base"]["testId"]
        test_iteration = data["base"]["testIteration"]
        device_name = data["local"]["deviceName"]

        if self.test_id != test_id or self.test_iteration != test_iteration:
            self.file_names = []
            self.file_paths = []
            self.test_id = test_id
            self.test_iteration = test_iteration

        sub_path = test_id
        file_name_postfix = f'{device_name}-TestID_{test_id}'
        if 'noisePreset' in data:
            noise_type = data["noisePreset"]["noiseType"]
            noise_preset = data["noisePreset"]["noisePreset"]
            sub_path = f'{sub_path}/NoiseType_{noise_type}/NoisePreset_{noise_preset}'
            file_name_postfix = f'{file_name_postfix}-NoiseType_{noise_type}-NoisePreset_{noise_preset}'

        if 'distance' in data:
            distance_key = data["distance"]["distanceKey"]
            sub_path = f'{sub_path}/DistanceKey_{distance_key}'
            file_name_postfix = f'{file_name_postfix}-DistanceKey_{distance_key}'

        if 'frog' in data:
            frog_id = data["frog"]["frogId"]
            frog_size = data["frog"]["frogSize"]
            sub_path = f'{sub_path}/FrogSize_{frog_size}/FrogId_{frog_id}'
            file_name_postfix = f'{file_name_postfix}-FrogSize_{frog_size}-FrogId_{frog_id}'

        if 'pen' in data:
            pen_id = data["pen"]["penId"]
            pen_brand = data["pen"]["penBrand"]
            sub_path = f'{sub_path}/PenBrand_{pen_brand}/PenId{pen_id}'
            file_name_postfix = f'{file_name_postfix}-PenBrand_{pen_brand}-PenId_{pen_id}'

        sub_path = f'{sub_path}/TestIteration_{test_iteration}'
        file_name_postfix = f'{file_name_postfix}-TestIteration_{test_iteration}'
        self.json_controller.clean_json_data(data)

        save(f'{sub_path}', file_name_postfix, data)
        # file_controller = FileController(sub_path=f'{sub_path}', file_name_postfix=file_name_postfix)
        # file_controller.save_json(data)
        # file_controller.save_audio_file(data["record"])

        app.logger.info(f'Data written: {test_id} - {device_name}')
        # file_paths, file_names = file_controller.get_directory_structure()
        self.file_names.append(file_name_postfix)
        self.file_paths.append(sub_path)
        emit('update_directory',
             {
                 "analysisTitle": test_id,
                 "filePaths": self.file_paths,
                 "fileNames": self.file_names
             },
             json=True,
             broadcast=True)
        return 'Thank You'

    def on_start_analysis(self, config):
        app.logger.info(f'on_start_analysis: {config}')
        emit('start_measurement', config, json=True, broadcast=True)
        app.logger.info(f'on_start_analysis: emit done')

    def on_connect(self):
        app.logger.debug(f'CONNECT: on_connect -----------------------------------------------------------------------')
        join_room(self.room_name)
        self.users += 1
        app.logger.info(f'CONNECT: on_connect {socketio.server.manager.rooms.keys()}')
        participants = [part for part in socketio.server.manager.get_participants(self.namespace, self.room_name)]
        app.logger.info(f'CONNECT: {participants}')
        emit('user_count', self.users, broadcast=True)

    def on_connect_error(self, error):
        app.logger.error(error)

    def on_disconnect(self):
        app.logger.info(f'on_disconnect')
        self.users -= 1
        emit('user_count', self.users, broadcast=True)


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    app.logger.error(e)


socketio.on_namespace(RootNamespace())
app.logger.info(f'CONNECT: on_connect {socketio.server.manager.server.manager.server}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
