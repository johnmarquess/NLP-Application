from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/data-management')
def data_management():
    return render_template('data_management.html')  # Assumes you have a template for this


@main.route('/data-modeling')
def data_modeling():
    return render_template('data_modeling.html')  # Assumes you have a template for this


@main.route('/reporting')
def reporting():
    return render_template('reporting.html')  # Assumes you have a template for this
