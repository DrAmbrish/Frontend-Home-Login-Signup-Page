from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timedelta
from . import db
from .model import Assignment,LiveSession,User

class InstructorDetails(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        instructor_id = jwt_claims.get("id")
        instructor = User.query.get(instructor_id )
        
        if not instructor:
            return {"message": "Professor not found"}, 404

        return jsonify({
            "id": instructor.id,
            "name": instructor.name,
            "username": instructor.username,
            "email": instructor.email,
            "role": instructor.role.name,
            "created_at": instructor.created_at,
            "last_login": instructor.last_login
        })
    
# Add Assignment
class AssignmentResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        required_fields = ["course_id", "week_number", "assignment_link", "description"]
        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields"}, 400

        assignment = Assignment(
            course_id=data["course_id"],
            week_number=data["week_number"],
            assignment_link=data["assignment_link"],
            description=data["description"]
        )
        db.session.add(assignment)
        db.session.commit()
        return {"message": "Assignment added successfully"}, 201

# Add Live Session
class LiveSessionResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        required_fields = ["course_id", "yt_link", "description"]
        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields"}, 400

        session = LiveSession(
            course_id=data["course_id"],
            yt_link=data["yt_link"],
            description=data["description"]
        )
        db.session.add(session)
        db.session.commit()
        return {"message": "Live session added successfully"}, 201