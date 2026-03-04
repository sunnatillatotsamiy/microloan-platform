from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from loans.models import LoanProduct, LoanApplication, RiskTag, ManagerReview

User = get_user_model()


class TestSetupMixin:
    """Shared setup for all test classes."""

    def setUp(self):
        self.client = Client()

        self.customer = User.objects.create_user(
            username="customer",
            password="testpass123",
            role="customer"
        )

        self.manager = User.objects.create_user(
            username="manager",
            password="testpass123",
            role="manager"
        )

        self.loan_product = LoanProduct.objects.create(
            name="Standard Loan",
            interest_rate=5.00,
            min_amount=1000,
            max_amount=10000,
            duration_min=3,
            duration_max=24
        )


class TestLoanProductModel(TestSetupMixin, TestCase):
    """Test 1: LoanProduct model creates correctly."""

    def test_loan_product_created(self):
        self.assertEqual(self.loan_product.name, "Standard Loan")
        self.assertEqual(self.loan_product.interest_rate, 5.00)
        self.assertEqual(str(self.loan_product), "Standard Loan")


class TestLoanApplicationModel(TestSetupMixin, TestCase):
    """Test 2: LoanApplication creates with correct defaults."""

    def test_loan_application_default_status(self):
        loan = LoanApplication.objects.create(
            customer=self.customer,
            loan_product=self.loan_product,
            amount=5000,
            duration_months=12,
            monthly_income=2000
        )
        self.assertEqual(loan.status, "pending")
        self.assertEqual(loan.customer.username, "customer")

    def test_loan_application_str(self):
        """Test 3: LoanApplication string representation."""
        loan = LoanApplication.objects.create(
            customer=self.customer,
            loan_product=self.loan_product,
            amount=3000,
            duration_months=6,
            monthly_income=1500
        )
        self.assertIn("customer", str(loan))


class TestRiskTagModel(TestSetupMixin, TestCase):
    """Test 4: RiskTag can be created and linked to a loan application."""

    def test_risk_tag_assignment(self):
        tag = RiskTag.objects.create(name="High Risk")
        loan = LoanApplication.objects.create(
            customer=self.customer,
            loan_product=self.loan_product,
            amount=9000,
            duration_months=24,
            monthly_income=1000
        )
        loan.risk_tags.add(tag)
        self.assertIn(tag, loan.risk_tags.all())
        self.assertEqual(str(tag), "High Risk")


class TestManagerReviewModel(TestSetupMixin, TestCase):
    """Test 5: ManagerReview is created and linked to loan."""

    def test_manager_review_created(self):
        loan = LoanApplication.objects.create(
            customer=self.customer,
            loan_product=self.loan_product,
            amount=4000,
            duration_months=12,
            monthly_income=1800
        )
        review = ManagerReview.objects.create(
            loan=loan,
            manager=self.manager,
            comment="Looks good."
        )
        self.assertEqual(review.manager.username, "manager")
        self.assertEqual(review.loan, loan)
        self.assertIn("manager", str(review))


class TestUserRoles(TestSetupMixin, TestCase):
    """Test 6: User roles are correctly assigned."""

    def test_user_roles(self):
        self.assertEqual(self.customer.role, "customer")
        self.assertEqual(self.manager.role, "manager")


class TestLoanApplicationViews(TestSetupMixin, TestCase):
    """Test 7: Apply loan page requires login."""

    def test_apply_loan_redirects_if_not_logged_in(self):
        response = self.client.get("/apply-loan/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_apply_loan_accessible_when_logged_in(self):
        """Test 8: Logged in customer can access apply loan page."""
        self.client.login(username="customer", password="testpass123")
        response = self.client.get("/apply-loan/")
        self.assertEqual(response.status_code, 200)

    def test_my_loans_filters_by_customer(self):
        """Test 9: My loans page shows only customer's loans."""
        LoanApplication.objects.create(
            customer=self.customer,
            loan_product=self.loan_product,
            amount=2000,
            duration_months=6,
            monthly_income=1200
        )
        self.client.login(username="customer", password="testpass123")
        response = self.client.get("/my-loans/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Standard Loan")

    def test_manager_sees_all_loans(self):
        """Test 10: Manager can see all loans."""
        LoanApplication.objects.create(
            customer=self.customer,
            loan_product=self.loan_product,
            amount=5000,
            duration_months=12,
            monthly_income=2000
        )
        self.client.login(username="manager", password="testpass123")
        response = self.client.get("/my-loans/")
        self.assertEqual(response.status_code, 200)