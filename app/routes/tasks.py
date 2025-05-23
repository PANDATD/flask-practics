from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import TaskForm
from flask_login import login_required

tasks_bp = Blueprint('tasks', __name__, url_prefix="/tasks")

# Temporary in-memory store
tasks = {}
task_id = 1

@tasks_bp.route('/')
@login_required
def list_tasks():
    return render_template('tasks/list.html', tasks=tasks)

@tasks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    global task_id
    form = TaskForm()
    if form.validate_on_submit():
        tasks[task_id] = {
            'id': task_id,
            'title': form.title.data,
            'description': form.description.data
        }
        task_id += 1
        flash("Task added!", "success")
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/add.html', form=form)

@tasks_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = tasks.get(id)
    if not task:
        flash("Task not found.", "danger")
        return redirect(url_for('tasks.list_tasks'))

    form = TaskForm(data=task)
    if form.validate_on_submit():
        task['title'] = form.title.data
        task['description'] = form.description.data
        flash("Task updated.", "info")
        return redirect(url_for('tasks.list_tasks'))

    return render_template('tasks/edit.html', form=form, id=id)

@tasks_bp.route('/delete/<int:id>')
@login_required
def delete_task(id):
    if tasks.pop(id, None):
        flash("Task deleted.", "warning")
    else:
        flash("Task not found.", "danger")
    return redirect(url_for('tasks.list_tasks'))
