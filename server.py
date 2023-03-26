from __future__ import annotations
from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from flask import Flask
from typing import Type
import pydantic

from db import Session
from models import Adv
from shema import CreateAdv, PatchAdv


app = Flask('advertisment_app')


def validate(input_data: dict, validation_model: Type[CreateAdv] | Type[PatchAdv]):
    try:
        model_item = validation_model(**input_data)
        return model_item.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


class HttpError(Exception):  # класс-обработчик ошибок
    def __init__(self, status_code: int, description: str | dict | list):

        self.status_code = status_code
        self.description = description

@app.errorhandler(HttpError) # специальный обработчик ошибок
def error_handler(error):

    response = jsonify({'status': 'error', 'description': error.description})
    response.status_code = error.status_code
    return response


def get_adv(adv_id: int, session: Session):
    adv = session.get(Adv, adv_id)
    if adv is None:
        raise HttpError(404, 'Advertisment not found')
    return adv


class AdvView(MethodView):

    def get(self, adv_id: int):
        with Session() as session:
            adv = get_adv(adv_id, session)
            return jsonify({'id': adv.id,
                            'header': adv.header,
                            'description': adv.description,
                            'creation_time': adv.creation_time.isoformat()})

    def post(self):
        json_data = request.json
        json_data = validate(json_data, CreateAdv)
        with Session() as session:
            adv = Adv(**json_data)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, 'ADV ALREADY EXISTS OR SOMETHING ELSE')
            return jsonify({'id': adv.id,
                            'header': adv.header,
                            'description': adv.description
                            })


    def patch(self, adv_id: int):
        json_data = validate(request.json, PatchAdv)
        with Session() as session:
            adv = get_adv(adv_id, session)
            for field, value in json_data.items():
                setattr(adv, field, value)
            session.add(adv)
            session.commit()
            return jsonify({'id': adv.id,
                            'header': adv.header,
                            'description': adv.description
                            })


    def delete(self, adv_id: int):
        with Session() as session:
            adv = get_adv(adv_id, session)
            session.delete(adv)
            session.commit()
            return jsonify({'status': 'deleted'})


# привязываем вью к урлу, а именно:
# указывается путь, по которому обращется клиентоское устройство
# затем - сама вью-функция к которой будет обращение
# затем метод которым можно к ней обращаться
app.add_url_rule('/adv/<int:adv_id>/', view_func=AdvView.as_view('adv'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/adv/', view_func=AdvView.as_view('adv_create'), methods=['POST'])

if __name__ =='__main__':
    app.run()  # старт приложения 'advertisment_app'