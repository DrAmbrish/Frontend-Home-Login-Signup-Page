from flask_restful import Resource
from flask import request , jsonify
from flask_jwt_extended import jwt_required, get_jwt

from datetime import datetime
from . import db
from .model import User, Course, Assignment,CourseMaterial,UserCourse,ChatbotHistory,IssueQuery,LiveSession,SupplementaryMaterial

class StudentProfile(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        student_id = jwt_claims.get("id")
        student = User.query.get(student_id)
        
        if not student:
            return jsonify({"message": "Student not found."}), 404
        return jsonify({
            "id": student.id,
            "name": student.name,
            "username": student.username,
            "email": student.email,
            "role": student.role.name,
            "last_login": student.last_login
        })

class StudentDashboard(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        student_id = jwt_claims.get("id")
        student = User.query.get(student_id)

        if not student:
            return jsonify({"message": "Student not found."}), 404

        # Fetch courses enrolled by the student
        enrolled_courses = UserCourse.query.filter_by(user_id=student_id).all()
        courses_data = []

        for enrollment in enrolled_courses:
            course = Course.query.get(enrollment.course_id)
            if course:
                # Fetch assignments for the course
                assignments = Assignment.query.filter_by(course_id=course.id).all()
                assignments_data = [
                    {
                        "id": assignment.id,
                        "week_number": assignment.week_number,
                        "created_at": assignment.created_at
                    }
                    for assignment in assignments
                ]

                # Fetch course materials for the course
                materials = CourseMaterial.query.filter_by(course_id=course.id).all()
                materials_data = [
                    {
                        "id": material.id,
                        "title": material.title,
                        "video_link": material.video_link,
                        "week_number": material.week_number,
                        "created_at": material.created_at
                    }
                    for material in materials
                ]

                # Fetch live sessions for the course
                live_sessions = LiveSession.query.filter_by(course_id=course.id).all()
                live_sessions_data = [
                    {
                        "id": session.id,
                        "yt_link": session.yt_link,
                        "description": session.description,
                        "created_at": session.created_at
                    }
                    for session in live_sessions
                ]

                # Fetch supplementary materials for the course
                supplementary_materials = SupplementaryMaterial.query.filter_by(course_id=course.id).all()
                supplementary_materials_data = [
                    {
                        "id": material.id,
                        "material_type": material.material_type,
                        "content": material.content,
                        "created_at": material.created_at
                    }
                    for material in supplementary_materials
                ]

                # Add course details with all related data
                courses_data.append({
                    "id": course.id,
                    "name": course.name,
                    "description": course.description,
                    "created_at": course.created_at,
                    "assignments": assignments_data,
                    "materials": materials_data,
                    "live_sessions": live_sessions_data,
                    "supplementary_materials": supplementary_materials_data
                })
        return jsonify({ 'courses_data': courses_data})
    

class CourseDetails(Resource):
    @jwt_required()
    def get(self, course_id):
        # Fetch course by ID
        course = Course.query.get(course_id)

        if not course:
            return jsonify({"message": "Course not found."}), 404

        # Fetch assignments for the course
        assignments = Assignment.query.filter_by(course_id=course.id).all()
        assignments_data = [
            {
                "id": assignment.id,
                "week_number": assignment.week_number,
                "created_at": assignment.created_at
            }
            for assignment in assignments
        ]

        # Fetch course materials for the course
        materials = CourseMaterial.query.filter_by(course_id=course.id).all()
        materials_data = [
            {
                "id": material.id,
                "title": material.title,
                "video_link": material.video_link,
                "week_number": material.week_number,
                "created_at": material.created_at
            }
            for material in materials
        ]

        # Fetch live sessions for the course
        live_sessions = LiveSession.query.filter_by(course_id=course.id).all()
        live_sessions_data = [
            {
                "id": session.id,
                "yt_link": session.yt_link,
                "description": session.description,
                "created_at": session.created_at
            }
            for session in live_sessions
        ]

        # Fetch supplementary materials for the course
        supplementary_materials = SupplementaryMaterial.query.filter_by(course_id=course.id).all()
        supplementary_materials_data = [
            {
                "id": material.id,
                "material_type": material.material_type,
                "content": material.content,
                "created_at": material.created_at
            }
            for material in supplementary_materials
        ]

        # Construct response with course details
        course_data = {
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "created_at": course.created_at,
            "assignments": assignments_data,
            "materials": materials_data,
            "live_sessions": live_sessions_data,
            "supplementary_materials": supplementary_materials_data
        }

        return jsonify({"course_data": course_data})

