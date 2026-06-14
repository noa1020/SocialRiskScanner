import json
from flask import request
from flask_restx import Resource, fields


from .services import analyze_text
from .database import save_post, get_all_posts


def register_routes(namespace):

    text_model = namespace.model(
        "TextModel",
        {
            "content": fields.String(required=True),
            "username": fields.String(required=True),
        },
    )

    def parse_request():
        data = request.get_json(silent=True)
        return data if isinstance(data, dict) else {}

    @namespace.route("/calculateSuicidePost")
    class CalculateSuicidePost(Resource):

        @namespace.expect(text_model)
        def post(self):
            payload = parse_request()

            text = (payload.get("content") or "").strip()
            username = (payload.get("username") or "").strip()

            if not text or not username:
                return {"error": "Missing content or username"}, 400

            analysis = analyze_text(text)

            return save_post(text, username, analysis), 200


    @namespace.route("/getAllPosts")
    class GetAllPosts(Resource):

        def get(self):
            return get_all_posts(), 200