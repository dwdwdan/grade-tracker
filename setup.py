from setuptools import setup, find_packages


setup(
    name="grade-tracker",
    version="1.0.11",
    author="Dan Walters",
    author_email="dan.walters5@outlook.com",
    description="A small example package",
    url="https://github.com/pypa/sampleproject",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    py_modules=['cli'],
    install_requires=["xdg", "pyyaml"],
    entry_points={
        "console_scripts": [
                "grade-tracker=grade_tracker.cli:main",
            ]
        },
)
