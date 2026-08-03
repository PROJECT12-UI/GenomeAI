
from genome_analyzer import GenomeAnalyzer

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_file
)

import os
import uuid

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config

from database.database import db

from models import (
    User,
    AnalysisHistory
)

from pdf_generator import GenomePDFGenerator


# =====================================================
# APPLICATION CONFIGURATION
# =====================================================

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


# =====================================================
# ALLOWED FILES
# =====================================================

ALLOWED_EXTENSIONS = {
    "txt",
    "csv",
    "fa",
    "fasta"
}


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )
# =====================================================
# REGISTER
# =====================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")

        email = request.form.get("email")

        phone = request.form.get("phone")

        password = request.form.get("password")

        confirm_password = request.form.get(
            "confirm_password"
        )

        # --------------------------
        # Validation
        # --------------------------

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:

            flash(
                "Email already exists.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        existing_phone = None

        if phone:

            existing_phone = User.query.filter_by(
                phone=phone
            ).first()

        if existing_phone:

            flash(
                "Phone number already exists.",
                "warning"
            )

            return redirect(
                url_for("register")
            )

        # --------------------------
        # Create User
        # --------------------------

        user = User(

            full_name=full_name,

            email=email,

            phone=phone

        )

        user.set_password(password)

        db.session.add(user)

        db.session.commit()

        flash(

            "Registration successful. Please login.",

            "success"

        )

        return redirect(

            url_for("login")

        )

    return render_template(

        "register.html"

    )
# =====================================================
# LOGIN
# =====================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get("email")

        password = request.form.get("password")

        user = User.query.filter_by(

            email=email

        ).first()

        if user and user.verify_password(password):

            session["user_id"] = user.id

            session["user_name"] = user.full_name

            flash(

                f"Welcome {user.full_name}!",

                "success"

            )

            return redirect(

                url_for("dashboard")

            )

        flash(

            "Invalid email or password.",

            "danger"

        )

    return render_template(

        "login.html"

    )


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(

        "Logged out successfully.",

        "success"

    )

    return redirect(

        url_for("home")

    )
# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    user = User.query.get(
        session["user_id"]
    )

    history = AnalysisHistory.query.filter_by(
        user_id=user.id
    ).order_by(
        AnalysisHistory.created_at.desc()
    ).all()

    return render_template(

        "dashboard.html",

        user=user,

        history=history

    )


# =====================================================
# PROFILE
# =====================================================

@app.route("/profile")
def profile():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    user = User.query.get(
        session["user_id"]
    )

    return render_template(

        "profile.html",

        user=user

    )
# =====================================================
# UPLOAD
# =====================================================

@app.route(
    "/upload",
    methods=["GET", "POST"]
)
def upload():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        # -------------------------
        # FILE CHECK
        # -------------------------

        if (

            "mother_file" not in request.files

            or

            "father_file" not in request.files

        ):

            flash(

                "Please upload both genome files.",

                "danger"

            )

            return redirect(
                url_for("upload")
            )

        mother = request.files["mother_file"]

        father = request.files["father_file"]

        if (

            mother.filename == ""

            or

            father.filename == ""

        ):

            flash(

                "Please select both files.",

                "danger"

            )

            return redirect(
                url_for("upload")
            )

        if not allowed_file(mother.filename):

            flash(

                "Invalid Mother DNA file.",

                "danger"

            )

            return redirect(
                url_for("upload")
            )

        if not allowed_file(father.filename):

            flash(

                "Invalid Father DNA file.",

                "danger"

            )

            return redirect(
                url_for("upload")
            )

        # -------------------------
        # SAVE FILES
        # -------------------------

        mother_filename = (

            str(uuid.uuid4())

            + "_"

            + mother.filename

        )

        father_filename = (

            str(uuid.uuid4())

            + "_"

            + father.filename

        )

        mother_path = os.path.join(

            app.config["UPLOAD_FOLDER"],

            mother_filename

        )

        father_path = os.path.join(

            app.config["UPLOAD_FOLDER"],

            father_filename

        )

        mother.save(mother_path)

        father.save(father_path)

        # -------------------------
        # AI ANALYSIS
        # -------------------------

        analyzer = GenomeAnalyzer()

        result = analyzer.generate_report(

            mother_path,

            father_path

        )
                # -------------------------
        # SAVE HISTORY
        # -------------------------

        history = AnalysisHistory(

            user_id=session["user_id"],

            mother_file=mother_filename,

            father_file=father_filename,

            health_score=result["health_score"],

            risk_level=result["risk_level"],

            predicted_disease=result["predicted_disease"],

            recommendations=result["recommendation"]

        )

        db.session.add(history)

        db.session.commit()

        # -------------------------
        # REPORT
        # -------------------------

        return render_template(

            "report.html",

            result=result,

            mother_file=mother_filename,

            father_file=father_filename,

            report_date=result.get("report_date"),

            total_samples=result.get("total_samples"),

            health_score=result.get("health_score"),

            high_risk=result.get("high_risk"),

            medium_risk=result.get("medium_risk"),

            low_risk=result.get("low_risk"),

            diseases=result.get("diseases")

        )

    return render_template(

        "upload.html"

    )
# =====================================================
# HISTORY
# =====================================================

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    history = AnalysisHistory.query.filter_by(

        user_id=session["user_id"]

    ).order_by(

        AnalysisHistory.created_at.desc()

    ).all()

    return render_template(

        "history.html",

        history=history

    )


# =====================================================
# ANALYSIS DETAILS
# =====================================================

@app.route("/analysis/<int:id>")
def analysis_details(id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    analysis = AnalysisHistory.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first_or_404()

    return render_template(

        "analysis_details.html",

        analysis=analysis

    )
# =====================================================
# DELETE ANALYSIS
# =====================================================

@app.route(
    "/delete-analysis/<int:id>",
    methods=["POST"]
)
def delete_analysis(id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    analysis = AnalysisHistory.query.filter_by(

        id=id,

        user_id=session["user_id"]

    ).first()

    if analysis:

        db.session.delete(analysis)

        db.session.commit()

        flash(

            "Analysis deleted successfully.",

            "success"

        )

    else:

        flash(

            "Analysis not found.",

            "danger"

        )

    return redirect(

        url_for("history")

    )


# =====================================================
# DOWNLOAD REPORT
# =====================================================

@app.route("/download-report/<int:id>")
def download_report(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    analysis = AnalysisHistory.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first_or_404()

    report = {

        "report_date": analysis.created_at.strftime("%d-%m-%Y"),

        "health_score": analysis.health_score,

        "risk_level": analysis.risk_level,

        "predicted_disease": analysis.predicted_disease,

        "recommendation": analysis.recommendations,

        "high_risk": 2,

        "medium_risk": 3,

        "low_risk": 5,

        "total_samples": 100,

        "diseases": []

    }

    os.makedirs("generated_reports", exist_ok=True)

    pdf_file = os.path.join(

        "generated_reports",

        f"GenomeAI_Report_{analysis.id}.pdf"

    )

    generator = GenomePDFGenerator()

    generator.create_pdf(

        pdf_file,

        report

    )

    return send_file(

        pdf_file,

        as_attachment=True,

        download_name=f"GenomeAI_Report_{analysis.id}.pdf"

    )
# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html"

    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    db.session.rollback()

    return render_template(

        "500.html"

    ), 500


# =====================================================
# CREATE DATABASE
# =====================================================

with app.app_context():

    db.create_all()


# =====================================================
# RUN SERVER
# =====================================================

import os

if __name__ == "__main__":

    app.run(

        debug=False,

        host="0.0.0.0",

        port=int(os.environ.get("PORT", 5000))

    )