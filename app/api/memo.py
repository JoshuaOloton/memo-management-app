from . import api
from ..models import Memo 
from flask import jsonify


@api.route('/memos/<int:memo_id>')
def get_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    return jsonify(memo.to_json())


@api.route('/memos/')
def get_memos():
    memos = Memo.query.all()
    return jsonify({
        'count': Memo.query.count(),
        'memos': [memo.to_json() for memo in memos]
    })