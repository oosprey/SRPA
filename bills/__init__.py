#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:11
# Last modified: 2017-09-07 09:11
# Filename: __init__.py
# Description:
BTYPE_OFFICE = 'office'
BTYPE_BOOKS = 'books'
BTYPE_PRINTS = 'prints'
BTYPE_POUNDAGE = 'poundage'
BTYPE_POSTAGE = 'postage'
BTYPE_TELEPHONE = 'telephone'
BTYPE_INTERNET = 'internet'
BTYPE_TRAFFIC = 'traffic'
BTYPE_MAINTAINANCE = 'maintainance'
BTYPE_CONFERENCE = 'conference'
BTYPE_MATERIAL = 'material'
BTYPE_COORPERATION = 'coorperation'
BTYPE_SUBCONTRACT = 'subcontract'
BTYPE_SCHOOL_MANAGEMENT = 'school_management'
BTYPE_BASE_MANAGEMENT = 'base_management'
BTYPE_WATER_ELECTRIC = 'water_electric'
BTYPE_RENT = 'rent'
BTYPE_EQUIPMENT = 'equipment'
BTYPE_SOFTWARE = 'software'
BTYPE_HOTEL = 'hotel'
BTYPE_OTHER = 'other'
BILL_TYPES = (
    (BTYPE_OFFICE, '日常办公用品费'),
    (BTYPE_BOOKS, '书报杂志订阅费'),
    (BTYPE_PRINTS, '印刷费'),
    (BTYPE_POUNDAGE, '手续费'),
    (BTYPE_POSTAGE, '邮电费'),
    (BTYPE_TELEPHONE, '电话费'),
    (BTYPE_INTERNET, '网络通讯费'),
    (BTYPE_TRAFFIC, '交通费'),
    (BTYPE_MAINTAINANCE, '维护费'),
    (BTYPE_CONFERENCE, '会议费'),
    (BTYPE_MATERIAL, '专用材料费'),
    (BTYPE_COORPERATION, '科研协作费'),
    (BTYPE_SUBCONTRACT, '委托业务费'),
    (BTYPE_SCHOOL_MANAGEMENT, '学校管理费'),
    (BTYPE_BASE_MANAGEMENT, '基层管理费'),
    (BTYPE_WATER_ELECTRIC, '水电费'),
    (BTYPE_RENT, '租赁费'),
    (BTYPE_EQUIPMENT, '专用设备购置费'),
    (BTYPE_SOFTWARE, '软件购置费'),
    (BTYPE_HOTEL, '住宿费'),
    (BTYPE_OTHER, '其他费用'),
)
_BILL_TYPES_DESC = (
    '日常办公用品支出,如复印纸，文具等',
    '购买书报杂志，资料册等支出',
    '打印，复印费，印刷费，版面费，外单位审稿费，专著出版费等',
    '电汇手续费等手续费',
    '向邮局，快递公司支出的邮寄费',
    '',
    '',
    '本市出租车，公交车，地铁，运费，租车费等',
    '除车辆维修费以外的仪器设备维修费',
    '本校承办的会议计划中所列支的费用（附会议计划）',
    '硒鼓，墨盒，实验室用品，消耗性体育用品，专用工具和仪器等',
    '',
    '加工费，测试费，图文制作费',
    '',
    '',
    '',
    '设备租赁费等',
    '购置单价超过1000元的通用设备或单价超过1500元的专用设备',
    '构建信息网络方面的费用，单件8000元以上的．．．',
    '',
    '',
)
BILL_TYPES_DESC = tuple((key, desc) for (key, disp), desc in
                        zip(BILL_TYPES, _BILL_TYPES_DESC))

ESTATUS_SUBMIT = 0
ESTATUS_AMEND = 1
ESTATUS_REJECT = 2
ESTATUS_APPROVE = 3
EXPENSE_STATUSES = (
    (ESTATUS_SUBMIT, '提交'),
    (ESTATUS_REJECT, '拒绝'),
    (ESTATUS_AMEND, '修改'),
    (ESTATUS_APPROVE, '批准'),
)

ESTATUS_TYPES = tuple(x[0] for x in EXPENSE_STATUSES)

DELETE_MSGS = {
    -1: '删除失败,系统中无此项信息',
    0: '删除成功, 点击确认进行跳转',
    1: '删除成功'
}
