from setuptools import find_packages, setup


def read_requirements():
    with open("automata/pyproject.toml", "r") as pyproject_file:
        requirements = []
        for skippable_line in pyproject_file:
            if "[tool.poetry.dependencies]" in skippable_line:
                break
        # Skips the python version line
        next(pyproject_file)
        for line in pyproject_file:
            if line == "\n":
                break
            requirements.append(line.rstrip() + "\n")

        return requirements


setup(
    name="automata",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [],
    },
    python_requires=">=3.10",  # Adjust this to your desired minimum Python version
)
