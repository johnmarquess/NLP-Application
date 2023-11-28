from flask import Blueprint, render_template

reporting_bp = Blueprint('reporting', __name__)


@reporting_bp.route('/reporting')
def reporting():
    return render_template('reporting.html')
