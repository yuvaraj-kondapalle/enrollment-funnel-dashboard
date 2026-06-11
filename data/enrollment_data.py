import pandas as pd
import numpy as np

def generate_enrollment_data():
    np.random.seed(42)
    n = 1000

    df = pd.DataFrame({
        'student_id': range(1, n + 1),
        'year': np.random.choice([2021, 2022, 2023, 2024], n),
        'stage': np.random.choice(
            ['Inquiry', 'Application', 'Admitted', 'Deposited', 'Enrolled'],
            n,
            p=[0.40, 0.25, 0.18, 0.10, 0.07]
        ),
        'program': np.random.choice(
            ['Business Analytics', 'Computer Science', 'Public Health', 'Education', 'Engineering'],
            n
        ),
        'demographics': np.random.choice(
            ['Domestic', 'International'],
            n,
            p=[0.65, 0.35]
        ),
        'financial_aid': np.random.choice(['Yes', 'No'], n, p=[0.60, 0.40])
    })

    return df