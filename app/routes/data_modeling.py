from flask import Blueprint, render_template

data_modeling_bp = Blueprint('data_modeling', __name__)


@data_modeling_bp.route('/data-modeling')
def data_modeling():
    return render_template('data_modeling.html')
