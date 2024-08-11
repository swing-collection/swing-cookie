from setuptools import setup, find_packages

setup(
    name="swing-cookie",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description="A Django package to manage cookies and cookie consent.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/swing-cookie",
    author="Your Name",
    author_email="youremail@example.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "django>=3.0",
    ],
)