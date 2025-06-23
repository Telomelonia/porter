from setuptools import setup, find_packages

setup(
    name="porter-api-unofficial",
    version="1.0.0",
    description="Unofficial Python API for automating Porter.in delivery quote retrieval using Selenium.",
    author="Educational Project",
    author_email="noreply@example.com",
    url="https://github.com/your-repo/porter-api-unofficial",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0.0",
        "webdriver-manager>=3.8.0"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 3 - Alpha"
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
)
