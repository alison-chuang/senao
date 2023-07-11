from flask import Blueprint

from controllers.Accounts import Accounts as AccountsController
from models.Account import Account as AccountsModel

controller = AccountsController(AccountsModel)
accounts_bp = Blueprint('accounts', __name__)

accounts_bp.route('/accounts', methods=['POST'])(controller.register)
accounts_bp.route('/accounts/verification', methods=['POST'])(controller.verify)
