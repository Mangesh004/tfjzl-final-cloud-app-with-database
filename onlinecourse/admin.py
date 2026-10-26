
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


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline, EnrollmentInline]
    list_display = ("name", "pub_date")
    list_filter = ["pub_date"]
    search_fields = ["name", "description"]


class LessonAdmin(admin.ModelAdmin):
    list_display = ["title"]


class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "full_time", "total_learners")


class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation")


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "date_enrolled", "mode")


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
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
