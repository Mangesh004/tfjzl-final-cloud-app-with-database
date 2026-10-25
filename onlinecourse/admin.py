
from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Enrollment,
    Question,
    Choice,
    Submission,
)


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ("name", "pub_date")
    list_filter = ["pub_date"]
    search_fields = ["name", "description"]


class LessonAdmin(admin.ModelAdmin):
    list_display = ["title"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "course", "grade")
    list_filter = ("course",)
    search_fields = ("question_text",)
    inlines = [ChoiceInline]


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "enrollment")
    filter_horizontal = ("choices",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissionAdmin)
