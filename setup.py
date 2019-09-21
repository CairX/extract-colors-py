from setuptools import setup

setup(
	name="extcolors",
	version="0.1.3",
	description="Extract colors from an image. "
				"Colors are grouped based on visual similarities using the CIE76 formula.",
	long_description=open("README.rst").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/CairX/extract-colors-py",
	author="CairX",
	author_email="lazycairx@gmail.com",
	license="MIT",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Environment :: Console",

		"Topic :: Multimedia :: Graphics",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Utilities",

		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.4"
	],
	python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
	keywords="extract colors image",
	packages=["extcolors"],
	install_requires=["Pillow"],
	entry_points={
		"console_scripts": [
			"extcolors=extcolors:main"
		],
	},
)
