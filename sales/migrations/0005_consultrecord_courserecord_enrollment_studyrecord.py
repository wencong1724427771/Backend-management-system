# Generated by Django 3.2 on 2021-06-19 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_auto_20210612_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.IntegerField(help_text='此处填写第几节课或第几天课程...,必须为数字', verbose_name='节次')),
                ('date', models.DateField(auto_now_add=True, verbose_name='上课日期')),
                ('course_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节课程标题')),
                ('course_memo', models.TextField(blank=True, max_length=300, null=True, verbose_name='本节课程内容')),
                ('has_homework', models.BooleanField(default=True, verbose_name='本节有作业')),
                ('homework_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节作业标题')),
                ('homework_memo', models.TextField(blank=True, max_length=500, null=True, verbose_name='作业描述')),
                ('scoring_point', models.TextField(blank=True, max_length=300, null=True, verbose_name='得分点')),
                ('re_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.classlist', verbose_name='班级')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.userinfo', verbose_name='讲师')),
            ],
            options={
                'unique_together': {('re_class', 'day_num')},
            },
        ),
        migrations.CreateModel(
            name='ConsultRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='跟进内容...')),
                ('status', models.CharField(choices=[('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'), ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效')], help_text='选择客户此时的状态', max_length=8, verbose_name='跟进状态')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='跟进日期')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='sales.userinfo', verbose_name='跟进人')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customer', verbose_name='所咨询客户')),
            ],
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.CharField(choices=[('checked', '已签到'), ('vacate', '请假'), ('late', '迟到'), ('absence', '缺勤'), ('leave_early', '早退')], default='checked', max_length=64, verbose_name='考勤')),
                ('score', models.IntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'C+'), (50, 'C'), (40, 'C-'), (0, ' D'), (-1, 'N/A'), (-100, 'COPY'), (-1000, 'FAIL')], default=-1, verbose_name='本节成绩')),
                ('homework_note', models.CharField(blank=True, max_length=255, null=True, verbose_name='作业批语')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('homework', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='作业文件')),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.courserecord', verbose_name='某节课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customer', verbose_name='学员')),
            ],
            options={
                'unique_together': {('course_record', 'student')},
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('why_us', models.TextField(blank=True, default=None, max_length=1024, null=True, verbose_name='为什么报名')),
                ('your_expectation', models.TextField(blank=True, max_length=1024, null=True, verbose_name='学完想达到的具体期望')),
                ('contract_approved', models.BooleanField(default=False, help_text='在审阅完学员的资料无误后勾选此项,合同即生效', verbose_name='审批通过')),
                ('enrolled_date', models.DateTimeField(auto_now_add=True, verbose_name='报名日期')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customer', verbose_name='客户名称')),
                ('enrolment_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.classlist', verbose_name='所报班级')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.campuses')),
            ],
            options={
                'unique_together': {('enrolment_class', 'customer')},
            },
        ),
    ]
