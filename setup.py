from setuptools import setup, find_packages

setup(
    name="cnpower",
    version="1.0.0",
    author="Gawg-AI",
    author_email="ahx@qq.com",
    description="中国10kV/0.4kV配电网工程参数库 - Chinese 10kV/0.4kV Distribution Grid Engineering Parameter Library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Gawg-AI/cnpower",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
    ],
    extras_require={
        "pandapower": ["pandapower>=2.10.0"],
        "dev": ["pytest>=7.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Power Engineering",
    ],
    keywords="distribution-grid pandapower power-system chinese-standards gb-t electrical-engineering",
    project_urls={
        "Bug Tracker": "https://github.com/Gawg-AI/cnpower/issues",
        "Documentation": "https://github.com/Gawg-AI/cnpower#readme",
        "Source Code": "https://github.com/Gawg-AI/cnpower",
    },
)
