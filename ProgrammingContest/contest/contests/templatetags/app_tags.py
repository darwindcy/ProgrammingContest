from django import template

register = template.Library()

@register.simple_tag
def get_team_problem_submission(queryset, team, problem):
    return queryset.filter(submissionTeam = team, submissionProblem = problem)

@register.simple_tag
def get_total_team_score(queryset, team):
    total = 0
    for item in queryset.filter(submissionTeam = team):
        total += item.get_submission_score()
    return total

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)