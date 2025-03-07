from setuptools import setup, find_packages

setup(
    name="ntpc_opendata_tool",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pandas>=2.2.0",
        "mcp>=0.1.0"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="新北市交通局開放資料查詢工具",
    keywords="opendata, transportation, new taipei city",
) 