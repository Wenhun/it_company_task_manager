from django import template

register = template.Library()


@register.filter(name="task_image")
def task_image(task_type: str) -> str:
    images = {
        "Bug": "images/task_type_bug.svg",
        "Breaking change": "images/task_type_breaking_change.svg",
        "New feature": "images/task_type_new_feature.svg",
        "QA": "images/task_type_qa.svg",
        "Refactoring": "images/task_type_refactoring.svg",
    }
    return images.get(task_type, "images/default_task_type.svg")
