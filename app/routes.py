from flask import Blueprint, render_template

main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/')
def index():
    return render_template('index.html')


@main_routes.route('/data_management')
def data_management():
    return render_template('data_management.html')


@main_routes.route('/data_modeling')
def data_modeling():
    return render_template('data_modeling.html')


@main_routes.route('/reporting')
def reporting():
    return render_template('reporting.html')
