#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from flask import Flask
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import session
from dnspod import utils
from dnspod import dnspod


app = Flask('app')
dnspod_api = dnspod()
utils = utils()


@app.route('/css/bootstrap.css')
def favicon():
    return send_from_directory(os.path.join('./', 'css'), 'bootstrap.css')


@app.route('/', methods=['GET','POST'])
@utils.html_wrap
def get_login():
    text = utils.get_template('login')
    text = text.replace('{{title}}', u'请选择')
    return text


# @app.route('/logind', methods=['GET'])
# @utils.html_wrap
# def get_logind():
#     if not session['login_email'] or not session['login_password']:
#         raise dnspod.DNSPodException('danger', u'参数错误。', -1)
#     text = dnspod.utils.get_template('logind')
#     text = text.replace('{{title}}', u'用户登录')
#     text = text.replace('{{action}}', u'domainlist')
#     return text

@app.route('/product',methods=['GET','POST'])
@utils.html_wrap
def product():
    key = request.form.get('key')
    print(request.values('key'))
    pro_dict = {'b79':'your key_api',
                'b79_mk':'your key_api',
                'nwf':'your key_api'}
    return pro_dict[key]

@app.route('/domainstatusd', methods=['GET'])
@utils.html_wrap
def get_domainstatusd():
    if not request.args.get('domain_id') or not request.args.get('status'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)
    text = utils.get_template('logind')
    text = text.replace('{{title}}', u'域名' + (u'启用' if request.args.get('status') == 'enable' else u'暂停'))
    text = text.replace('{{action}}',
        u'domainstatus?domain_id=%s&status=%s' % (request.args.get('domain_id'), request.args.get('status')))
    return text


@app.route('/domainremoved', methods=['GET'])
@utils.html_wrap
def get_domainremoved():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)
    text = dnspod.utils.get_template('logind')
    text = text.replace('{{title}}', u'域名删除')
    text = text.replace('{{action}}', u'domainremove?domain_id=%s' % request.args.get('domain_id'))
    return text


@app.route('/domainlist', methods=['GET', 'POST'])
@utils.html_wrap
def get_domainlist():
    if request.method == 'POST':
        if not request.form.get('login_code'):
            if not request.form['login_email']:
                raise dnspod.DNSPodException('danger', u'请输入登录账号。', -1)
            else:
                session['login_email'] = request.form['login_email']

            if not request.form['login_password']:
                raise dnspod.DNSPodException('danger', u'请输入登录密码。', -1)
            else:
                session['login_password'] = request.form['login_password']

            session['login_code'] = ''
        else:
            session['login_code'] = request.form['login_code']

    response = dnspod_api.api_call('Domain.List')
    if response['status']['code'] == '50':
        return redirect('/logind')

    list_text = ''
    domain_sub = dnspod.utils.read_text('./template/domain_sub.html')
    for domain in response['domains']:
        list_sub = domain_sub.replace('{{id}}', str(domain['id']))
        list_sub = list_sub.replace('{{domain}}', domain['name'])
        list_sub = list_sub.replace('{{grade}}', dnspod_api.grade_list[domain['grade']])
        list_sub = list_sub.replace('{{status}}', dnspod_api.status_list[domain['status']])
        list_sub = list_sub.replace('{{status_new}}', 'enable' if domain['status'] == 'pause' else 'disable')
        list_sub = list_sub.replace('{{status_text}}', u'启用' if domain['status'] == 'pause' else u'暂停')
        list_sub = list_sub.replace('{{records}}', domain['records'])
        list_sub = list_sub.replace('{{updated_on}}', domain['updated_on'])
        list_text += list_sub

    text = dnspod.utils.get_template('domain')
    text = text.replace('{{title}}', u'域名列表')
    text = text.replace('{{list}}', list_text)
    return text


@app.route('/domaincreate', methods=['POST'])
@utils.html_wrap
def post_domaincreate():
    if not request.form['domain']:
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    dnspod_api.api_call('Domain.Create', {'domain': request.form['domain']})

    raise dnspod.DNSPodException('success', u'添加成功。', '/domainlist')


@app.route('/domainstatus', methods=['GET', 'POST'])
@utils.html_wrap
def get_domainstatus():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)
    if not request.args.get('status'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    session['login_code'] = request.form.get('login_code')
    response = dnspod_api.api_call('Domain.Status', {'domain_id': request.args.get('domain_id'),
        'status': request.args.get('status')})
    if response['status']['code'] == '50':
        return redirect('domainstatusd?domain_id=%s&status=%s' % (request.args.get('domain_id'), request.args.get('status')))

    raise dnspod.DNSPodException('success',
        (u'启用' if request.args.get('status') == 'enable' else u'暂停') + u'成功。', '/domainlist')


@app.route('/domainremove', methods=['GET', 'POST'])
@utils.html_wrap
def get_domainremove():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    session['login_code'] = request.form.get('login_code')
    response = dnspod_api.api_call('Domain.Remove', {'domain_id': request.args.get('domain_id')})
    if response['status']['code'] == '50':
        return redirect('domainremoved?domain_id=%s' % request.args.get('domain_id'))

    raise dnspod.DNSPodException('success', u'删除成功。', '/domainlist')


@app.route('/recordlist', methods=['GET'])
@utils.html_wrap
def get_recordlist():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    response = dnspod_api.api_call('Record.List', {'domain_id': request.args.get('domain_id')})
    list_text = ''
    domain_sub = dnspod.utils.read_text('./template/record_sub.html')
    for record in response['records']:
        list_sub = domain_sub.replace('{{domain_id}}', request.args.get('domain_id'))
        list_sub = list_sub.replace('{{id}}', str(record['id']))
        list_sub = list_sub.replace('{{name}}', record['name'])
        list_sub = list_sub.replace('{{value}}', record['value'])
        list_sub = list_sub.replace('{{type}}', record['type'])
        list_sub = list_sub.replace('{{line}}', record['line'])
        list_sub = list_sub.replace('{{enabled}}', u'启用' if int(record['enabled']) else u'暂停')
        list_sub = list_sub.replace('{{status_new}}', 'disable' if int(record['enabled']) else 'enable')
        list_sub = list_sub.replace('{{status_text}}', u'暂停' if int(record['enabled']) else u'启用')
        list_sub = list_sub.replace('{{mx}}', record['mx'])
        list_sub = list_sub.replace('{{ttl}}', record['ttl'])
        list_text += list_sub

    text = dnspod.utils.get_template('record')
    text = text.replace('{{title}}', u'记录列表 - %s' % (response['domain']['name']))
    text = text.replace('{{list}}', list_text)
    text = text.replace('{{domain_id}}', str(response['domain']['id']))
    text = text.replace('{{grade}}', response['domain']['grade'])
    return text


@app.route('/recordcreatef', methods=['GET'])
@utils.html_wrap
def get_recordcreatef():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    if 'type_' + request.args.get('grade') not in session:
        response = dnspod_api.api_call('Record.Type', {'domain_grade': request.args.get('grade')})
        session['type_' + request.args.get('grade')] = response['types']

    if 'line_' + request.args.get('grade') not in session:
        response = dnspod_api.api_call('Record.Line', {'domain_grade': request.args.get('grade')})
        session['line_' + request.args.get('grade')] = response['lines']

    type_list = ''
    for value in session['type_' + request.args.get('grade')]:
        type_list += '<option value="%s">%s</option>' % (value, value)

    line_list = ''
    for value in session['line_' + request.args.get('grade')]:
        line_list += '<option value="%s">%s</option>' % (value, value)

    text = dnspod.utils.get_template('recordcreatef')
    text = text.replace('{{title}}', u'添加记录')
    text = text.replace('{{action}}', 'recordcreate')
    text = text.replace('{{domain_id}}', request.args.get('domain_id'))
    text = text.replace('{{record_id}}', request.args.get('record_id', ''))
    text = text.replace('{{type_list}}', type_list)
    text = text.replace('{{line_list}}', line_list)
    text = text.replace('{{sub_domain}}', '')
    text = text.replace('{{value}}', '')
    text = text.replace('{{mx}}', '10')
    text = text.replace('{{ttl}}', '600')
    return text


@app.route('/recordcreate', methods=['POST'])
@utils.html_wrap
def post_recordcreate():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    sub_domain = None
    if not request.form.get('sub_domain'):
        sub_domain = '@'

    if not request.form.get('value'):
        raise dnspod.DNSPodException('danger', u'请输入记录值。', -1)

    mx = None
    if request.form.get('type') == 'MX' and not request.form.get('mx'):
        mx = 10

    ttl = None
    if not request.form.get('ttl'):
        ttl = 600

    dnspod_api.api_call('Record.Create',
        {'domain_id': request.args.get('domain_id'),
        'sub_domain': sub_domain or request.form['sub_domain'],
        'record_type': request.form['type'],
        'record_line': request.form['line'],
        'value': request.form['value'],
        'mx': mx or request.form['mx'],
        'ttl': ttl or request.form['ttl']}
    )

    raise dnspod.DNSPodException('success', u'添加成功。', '/recordlist?domain_id=%s' % request.args.get('domain_id'))


@app.route('/recordeditf', methods=['GET'])
@utils.html_wrap
def get_recordeditf():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)
    if not request.args.get('record_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    record = dnspod_api.api_call('Record.Info', {'domain_id': request.args.get('domain_id'),
        'record_id': request.args.get('record_id')})
    record = record['record']

    if 'type_' + request.args.get('grade') not in session:
        response = dnspod_api.api_call('Record.Type', {'domain_grade': request.args.get('grade')})
        session['type_' + request.args.get('grade')] = response['types']

    if 'line_' + request.args.get('grade') not in session:
        response = dnspod_api.api_call('Record.Line', {'domain_grade': request.args.get('grade')})
        session['line_' + request.args.get('grade')] = response['lines']

    type_list = ''
    for value in session['type_' + request.args.get('grade')]:
        type_list += '<option value="%s" %s>%s</option>' % (value,
            'selected="selected"' if record['record_type'] == value else '', value)

    line_list = ''
    for value in session['line_' + request.args.get('grade')]:
        line_list += '<option value="%s" %s>%s</option>' % (value,
        'selected="selected"' if record['record_line'] == value else '', value)

    text = dnspod.utils.get_template('recordcreatef')
    text = text.replace('{{title}}', u'修改记录')
    text = text.replace('{{action}}', 'recordedit')
    text = text.replace('{{domain_id}}', request.args.get('domain_id'))
    text = text.replace('{{record_id}}', request.args.get('record_id'))
    text = text.replace('{{type_list}}', type_list)
    text = text.replace('{{line_list}}', line_list)
    text = text.replace('{{sub_domain}}', record['sub_domain'])
    text = text.replace('{{value}}', record['value'])
    text = text.replace('{{mx}}', record['mx'])
    text = text.replace('{{ttl}}', record['ttl'])
    return text


@app.route('/recordedit', methods=['POST'])
@utils.html_wrap
def post_recordedit():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)
    if not request.args.get('record_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    sub_domain = None
    if not request.form.get('sub_domain'):
        sub_domain = '@'

    if not request.form.get('value'):
        raise dnspod.DNSPodException('danger', u'请输入记录值。', -1)

    mx = None
    if request.form.get('type') == 'MX' and not request.form.get('mx'):
        mx = 10

    ttl = None
    if not request.form.get('ttl'):
        ttl = 600

    dnspod_api.api_call('Record.Modify',
        {'domain_id': request.args.get('domain_id'),
        'record_id': request.args.get('record_id'),
        'sub_domain': sub_domain or request.form['sub_domain'],
        'record_type': request.form['type'],
        'record_line': request.form['line'],
        'value': request.form['value'],
        'mx': mx or request.form['mx'],
        'ttl': ttl or request.form['ttl']}
    )

    raise dnspod.DNSPodException('success', u'修改成功。', '/recordlist?domain_id=%s' % request.args.get('domain_id'))


@app.route('/recordremove', methods=['GET'])
@utils.html_wrap
def get_recordremove():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)
    if not request.args.get('record_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    dnspod_api.api_call('Record.Remove',
        {'domain_id': request.args.get('domain_id'),
        'record_id': request.args.get('record_id')}
    )

    raise dnspod.DNSPodException('success', u'删除成功。', '/recordlist?domain_id=%s' % request.args.get('domain_id'))


@app.route('/recordstatus', methods=['GET'])
@utils.html_wrap
def get_recordstatus():
    if not request.args.get('domain_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)
    if not request.args.get('record_id'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)
    if not request.args.get('status'):
        raise dnspod.DNSPodException('danger', u'参数错误。', -1)

    dnspod_api.api_call('Record.Status',
        {'domain_id': request.args.get('domain_id'),
        'record_id': request.args.get('record_id'),
        'status': request.args.get('status')}
    )

    raise dnspod.DNSPodException('success', (u'启用' if request.args.get('status') == 'enable' else u'暂停') + u'成功。',
        '/recordlist?domain_id=%s' % request.args.get('domain_id'))


if __name__ == '__main__':
    app.secret_key = '7roTu0tLyfksj48G0rbRb556b3tv94q0'
    app.run(host='192.168.20.110',debug=True)
   
