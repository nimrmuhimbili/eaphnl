from csv import writer, DictReader
from questionnaire.utils import UnicodeWriter, UnicodeReader
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import django
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.defaultfilters import slugify

from questionnaire.models import Form, FormEntry, Field, FieldEntry
from questionnaire.forms import FormEntryForm, DesignedForm, EntriesForm, FieldForm, UserProfileForm, ImportEntriesForm
from questionnaire.utils import now


def is_data_manager(user):
    return user.groups.filter(name='Data Manager').exists()


@login_required
def manage_forms(request):
    template_name = 'questionnaire/manage_forms.html'
    forms = Form.objects.all()
    return render(request, template_name, {'forms': forms})


@login_required
def manage_entries(request, slug=None):
    template_path = 'questionnaire/manage_entries.html'
    if slug:
        form = get_object_or_404(Form, slug=slug)
        if request.user.is_superuser or is_data_manager(request.user):
            entries = form.entries.all()
        else:
            entries = form.entries.filter(user=request.user)
        entries_ids = []
        for entry in entries:
            for field, field_entry in zip(form.fields.all(), entry.fields.all()):
                if field.unique:
                    entries_ids.append((entry.get_absolute_url(), field_entry.response, entry.entry_time))
        return render(request, template_path, {'form': form, 'entries': entries_ids})


@login_required
def search_entry(request):
    template_path = 'questionnaire/search_entries.html'
    if 'q' in request.GET and request.GET['q']:
        form_number = request.GET['q']
        results = []
        for form in Form.objects.all():
            if form.entries.filter(fields__response=form_number):
                results.extend(form.entries.filter(fields__response=form_number))
                break
        return render(request, template_path, {'results': results, 'form_number': form_number})


@login_required
def manage_exports(request, slug):
    template_path = 'questionnaire/manage_exports.html'
    form = get_object_or_404(Form, slug=slug)
    entries_form = EntriesForm(form, request.POST or None)
    if request.POST.get('export'):
        response = HttpResponse(content_type="text/csv")
        fname = "%s-%s.csv" % (form.slug, slugify(now().ctime()))
        attachment = "attachment; filename=%s" % fname
        response["Content-Disposition"] = attachment
        csv = writer(response, delimiter=",")
        writerow = csv.writerow
        writerow(entries_form.columns())
        for row in entries_form.rows(csv=True):
            writerow(row)
        return response
    return render(request, template_path, {'form': form, 'entries_form': entries_form})


@login_required
def manage_imports(request, slug):
    form = get_object_or_404(Form, slug=slug)
    import_form = ImportEntriesForm(request.POST or None, request.FILES)
    if request.POST.get('upload') and request.FILES:
        # template_path = 'questionnaire/manage_imports.html'
        if import_form.is_valid():
            reader = DictReader(request.FILES['file'])
            for row in reader:
                entry = FormEntry(form=form, entry_time=now(), user=request.user)
                entry.save()
                entry_fields = []
                for field_name, response in row.items():
                    field = form.fields.get(name=field_name)
                    entry_fields.append(FieldEntry(entry=entry, field_id=field.id, response=response))
                if entry_fields:
                    if django.VERSION >= (1, 4, 0):
                        FieldEntry.objects.bulk_create(entry_fields)
                    else:
                        for entry_field in entry_fields:
                            entry_field.save()
            return redirect(reverse('entries', args=(form.slug,)))
            # return render(request, template_path, {'form': form, 'reader': reader})
    else:
        template_path = 'questionnaire/upload_datafile.html'
        return render(request, template_path, {'form': form, 'import_form': import_form})


@login_required
def manage_form_delete(request, pk):
    form = get_object_or_404(Form, pk=pk)
    if form:
        form.delete()
        return redirect(reverse('forms'))


@login_required
def manage_form(request, pk=None):
    template_name = 'questionnaire/form.html'
    if pk:
        instance = get_object_or_404(Form, pk=pk)
        action = reverse('update_form', args=(pk,))
    else:
        instance = Form()
        action = reverse('add_form')
    form = DesignedForm(request.POST or None, instance=instance)
    # fields_formset = FieldsFormset(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save()
        # fields_formset.instance = instance
        # fields_formset.save()
        return redirect(reverse('add_field', args=(instance.slug,)))
    return render(request, template_name, {'form': form, 'action': action})


@login_required
def manage_form_field(request, slug, pk=None):
    template_name = 'questionnaire/form_field.html'
    form_instance = get_object_or_404(Form, slug=slug)
    if pk:
        field_instance = form_instance.fields.get(pk=pk)
        action = reverse('edit_field', kwargs={'slug': slug, 'pk': pk})
    else:
        field_instance = Field(form=form_instance)
        action = reverse('add_field', kwargs={'slug': slug})
    field_form = FieldForm(request.POST or None, instance=field_instance)
    if field_form.is_valid():
        field_form.save()
        return redirect(reverse('add_field', args=(form_instance.slug,)))
    return render(request, template_name, {'field_form': field_form,
                                           'form_instance': form_instance,
                                           'action': action})


@login_required
def manage_form_field_delete(request, slug, pk):
    form = get_object_or_404(Form, slug=slug)
    field = form.fields.get(pk=pk)
    if field:
        field.delete()
        return redirect(reverse('add_field', args=(form.slug,)))


@login_required
def manage_entry(request, slug, pk=None):
    form = get_object_or_404(Form, slug=slug)
    if pk:
        entry = get_object_or_404(FormEntry, pk=pk)
        action = entry.get_absolute_url()
    else:
        entry = FormEntry()
        action = form.get_absolute_url()
    entry_form = FormEntryForm(form, request.POST or None, instance=entry)
    if entry_form.is_valid():
                entry_form.instance.user = request.user
                entry_form.save()
                return redirect(reverse('entries', args=(form.slug,)))
    return render(request, 'questionnaire/manage_entry.html',
        {'action': action, 'form': form, 'entry_form': entry_form}
    )


@login_required
def manage_users(request):
    template_name = 'questionnaire/manage_users.html'
    users = User.objects.all()
    return render(request, template_name, {'users': users})


@login_required
def manage_user(request, pk=None):
    template_name = 'questionnaire/manage_user.html'
    if pk:
        user = get_object_or_404(User, pk=pk)
        action = reverse('edit_user', args=(pk,))
    else:
        user = User()
        action = reverse('create_user')
    form = UserProfileForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect(reverse('manage_users'))
    return render(request, template_name, {'form': form, 'action': action})


@login_required
def manage_user_delete(request, pk=None):
    user = User.objects.get(pk=pk)
    if user:
        user.delete()
        return redirect(reverse('manage_users'))


@login_required
def manage_reports(request):
    template_name = 'questionnaire/report.html'
    return render(request, template_name)