import logging
from platform import system
from os.path import isfile
from os.path import join
from os import listdir

from flask import jsonify
from flask.ext.restful import Resource
from flask.ext.restful import reqparse

from application import db
from application.modules.settings.model import Setting

parser = reqparse.RequestParser()
parser.add_argument('blender_path_linux', type=str)
parser.add_argument('blender_path_win', type=str)
parser.add_argument('blender_path_osx', type=str)
parser.add_argument('render_settings_path_linux', type=str)
parser.add_argument('render_settings_path_win', type=str)
parser.add_argument('render_settings_path_osx', type=str)
parser.add_argument('group', type=str)

setting_parser = reqparse.RequestParser()
setting_parser.add_argument('value', type=str)


class SettingsListApi(Resource):
    def get(self):
        args = parser.parse_args()
        settings = {}
        if not args['group']:
            for setting in Setting.query.all():
                settings[setting.name] = setting.value
        elif args['group'] == 'render':
            name = ''
            if system() == 'Linux':
                name = 'render_settings_path_linux'
            elif system() == 'Windows':
                name = 'render_settings_path_win'
            else:
                name = 'render_settings_path_osx'

            path = Setting.query.filter_by(name=name).first()
            onlyfiles = [f for f in listdir(path.value) if isfile(join(path.value, f))]
            settings = dict(settings_files=onlyfiles)

        return jsonify(settings)

    def post(self):
        args = parser.parse_args()
        for k, v in args.iteritems():
            setting = Setting.query.filter_by(name=k).first()
            if setting:
                setting.value = v
                logging.info("Updating {0} {1}".format(k, v))
            else:
                setting = Setting(name=k, value=v)
                logging.info("Creating {0} {1}".format(k, v))
            db.session.add(setting)
        db.session.commit()
        return '', 204

class SettingApi(Resource):
    """API to edit individual settings.
    """
    def get(self, name):
        setting = Setting.query.filter_by(name=name).first()
        return jsonify(dict(name=setting.name, value=setting.value))

    def patch(self, name):
        args = parser.parse_args()
        setting = Setting.query.filter_by(name=name).first()
        setting.value = args['value']
        db.session.commit()
        return jsonify(dict(value=setting.value))
