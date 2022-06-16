import json

from flask_testing import TestCase
from unittest.mock import patch
from config import create_app
from db import db
from models import ComplaintModel, State
from services.s3 import S3Service
from tests.factory import ComplainerFactory
from tests.helpers import encoded_photo, generate_token

# TODO 02:50:00
class TestComplain(TestCase):
    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestApplicationConfiguration")

    @patch.object(S3Service, 'upload_photo', return_value='some-test.url')
    def test_create_complaint(self, s3_mock):
        url = '/complainers/complaints'
        data = {
            "title": "Some Test complant",
            "description": "Test description",
            "photo": encoded_photo,
            "photo_extension": "jpg",
            "amount": 10.20
        }

        complainer = ComplainerFactory()
        token = generate_token(complainer)
        self.headers.update({"Authorization": f"Bearer {token}"})
        complaints = ComplaintModel.query.all()
        assert len(complaints) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)
        complaints = ComplaintModel.query.all()
        assert len(complaints) == 1
        data.pop('photo')
        data.pop('photo_extension')
        expected_resp = {
            'id': complaints[0].id,
            'photo_url': 'some-test.url',
            'status': State.pending.value,
            'complainer_id': complaints.id,
            **data
        }
        actual_resp = resp.json
        actual_resp.pop('created_on')

        assert resp.status_code == 201
        assert actual_resp == expected_resp
