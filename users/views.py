import re
from datetime import timezone, datetime
from io import TextIOWrapper

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
import csv
import xml.etree.ElementTree as ET
from .models import User
from .forms import FileFieldForm


class UserList(ListView):

    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        if request.user.is_superuser:
            return render(request, "users/users.html", {"user_list": user_list,
                                                        "a_user_list": "active"})
        return render(request, "users/users.html", {"user_list": [], "a_user_list": "active"})


class UserUploadFormView(FormView):
    form_class = FileFieldForm
    template_name = 'users/upload_users.html'
    success_url = "/"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return render(request, self.template_name, {"a_upload_users": "active"})
        return redirect('/')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            files = request.FILES.getlist('files')
            if form.is_valid():
                try:
                    self.handle_uploaded_files(request, files)
                except Exception as e:
                    messages.error(request, e)
                    return self.form_invalid(form)
                return super().form_valid(form)
            else:
                return self.form_invalid(form)
        return redirect('/')

    def handle_uploaded_files(self, request, files):
        defined_files = self.define_files_number_and_format(files)
        parsed_xml = self.parse_xml(defined_files['xml'])
        parsed_csv = self.parse_csv(defined_files['csv'])
        combined_users = self.combine_and_filter_files_data(xml_data=parsed_xml, csv_data=parsed_csv)
        self.add_users_to_db(request, combined_users)

    @staticmethod
    def define_files_number_and_format(files):
        defined_files = {}
        if len(files) != 2:
            raise AssertionError('Found more or less than 2 files')
        for file in files:
            if file.name.endswith('.csv'):
                defined_files['csv'] = file
            elif file.name.endswith('.xml'):
                defined_files['xml'] = file
        if len(defined_files) != 2:
            raise AssertionError('Found wrong formats. Expected ".csv" and ".xml"')
        return defined_files

    def parse_xml(self, file_xml):
        parsed_xml = []
        tree = ET.parse(file_xml.file)
        root = tree.getroot()
        for user in root.iter('user'):
            if 'id' in user.attrib:
                first_name = self.clean_bracketed(text=user.find('first_name').text)
                last_name = self.clean_bracketed(text=user.find('last_name').text)
                avatar = user.find('avatar').text
                if first_name and last_name and avatar:
                    parsed_xml.append({'first_name': first_name,
                                       'last_name': last_name,
                                       'avatar': avatar})
        return parsed_xml

    def parse_csv(self, file_csv):
        parsed_csv = []
        with TextIOWrapper(file_csv.file, encoding='utf-8') as read_file:
            reader = csv.DictReader(read_file, delimiter=',', lineterminator='\r\n')
            for user_row in reader:
                if 'username' in user_row \
                        and 'password' in user_row \
                        and 'date_joined' in user_row:
                    username = self.clean_bracketed(user_row['username'])
                    password = user_row['password']
                    date_joined = user_row['date_joined']
                if username and password and date_joined:
                    parsed_csv.append({'username': username,
                                       'password': password,
                                       'date_joined': date_joined})
        return parsed_csv

    @staticmethod
    def clean_bracketed(text: str or None) -> str or None:
        if text:
            no_square_text = re.sub(r'\([^()]*\)', '', text).strip()
            no_round_text = re.sub(r'\[.*\]', '', no_square_text).strip()
            return no_round_text

    @staticmethod
    def combine_and_filter_files_data(xml_data, csv_data):
        combined_filtered_users = []
        for personal_data in xml_data:
            for i, auth_data in enumerate(csv_data):
                if personal_data['last_name'] in auth_data['username']:
                    combined_user = csv_data.pop(i)
                    combined_user.update(personal_data)
                    combined_filtered_users.append(combined_user)
        return combined_filtered_users

    @staticmethod
    def add_users_to_db(request, users: [dict]) -> None:
        errors_number = 0
        for user in users:
            try:
                user = User.objects.create_user(
                    username=user['username'],
                    password=user['password'],
                    date_joined=datetime.fromtimestamp(int(user['date_joined']), tz=timezone.utc),
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                )
                user.save()
            except IntegrityError as err:
                errors_number += 1
        if errors_number:
            messages.error(request, f'Not loaded {errors_number} users (already exist)')
            messages.success(request, f'Uploaded {len(users) - errors_number} users')
        else:
            messages.success(request, f'Successfully uploaded all users')
