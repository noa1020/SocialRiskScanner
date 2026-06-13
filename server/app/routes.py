import json

from flask import request
from flask_restx import Resource, fields

from .database import get_all_posts, save_post
from .services import analyze_text


def register_routes(namespace):
    text_model = namespace.model(
        "TextModel",
        {
            "content": fields.String(required=True, description="Post content to analyze"),
            "username": fields.String(required=True, description="Author username"),
        },
    )

    def parse_request_payload():
        data = request.get_json(silent=True)
        if data is None:
            raw_data = request.get_data(as_text=True)
            if raw_data:
                try:
                    data = json.loads(raw_data)
                except json.JSONDecodeError:
                    data = {}
            else:
                data = {}

        if not isinstance(data, dict):
            return {}

        return data

    @namespace.route("/calculateSuicidePost")
    class CalculateSuicideText(Resource):
        @namespace.expect(text_model)
        @namespace.doc(description="Receives a post and stores it only when the signal is high")
        def post(self):
            payload = parse_request_payload()
            text = (payload.get("content") or payload.get("text") or "").strip()
            username = (payload.get("username") or "").strip()

            if not text or not username:
                return {"error": "Missing content or username"}, 400

            analysis = analyze_text(text)
            return save_post(text, username, analysis), 200

    @namespace.route("/getAllPosts")
    class GetAllPosts(Resource):
        @namespace.doc(description="Returns all stored review items")
        def get(self):
            return get_all_posts(), 200
