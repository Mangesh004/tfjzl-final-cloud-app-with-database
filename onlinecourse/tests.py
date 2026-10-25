from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Course, Enrollment, Question, Choice, Submission


class AssessmentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teststudent",
            password="TestPassword123!"
        )

        self.course = Course.objects.create(
            name="Test Course",
            description="Course for automated testing",
            image="test-course.png",
        )

        self.enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.course,
            mode="honor",
        )

        self.question = Question.objects.create(
            course=self.course,
            question_text="Which keyword defines a function in Python?",
            grade=1,
        )

        self.correct_choice = Choice.objects.create(
            question=self.question,
            choice_text="def",
            is_correct=True,
        )

        self.incorrect_choice = Choice.objects.create(
            question=self.question,
            choice_text="function",
            is_correct=False,
        )

    def test_correct_answer_gets_marks(self):
        submission = Submission.objects.create(
            enrollment=self.enrollment
        )
        submission.choices.add(self.correct_choice)

        self.assertEqual(submission.is_get_score(), 1)

    def test_incorrect_answer_gets_zero_marks(self):
        submission = Submission.objects.create(
            enrollment=self.enrollment
        )
        submission.choices.add(self.incorrect_choice)

        self.assertEqual(submission.is_get_score(), 0)

    def test_submission_endpoint_saves_answer(self):
        self.client.login(
            username="teststudent",
            password="TestPassword123!"
        )

        response = self.client.post(
            reverse("onlinecourse:submit", args=[self.course.id]),
            {
                f"choice_{self.question.id}": str(
                    self.correct_choice.id
                )
            },
        )

        self.assertEqual(response.status_code, 302)

        submission = Submission.objects.get(
            enrollment=self.enrollment
        )

        self.assertIn(
            self.correct_choice,
            submission.choices.all()
        )

    def test_anonymous_user_cannot_submit(self):
        response = self.client.post(
            reverse("onlinecourse:submit", args=[self.course.id]),
            {
                f"choice_{self.question.id}": str(
                    self.correct_choice.id
                )
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
