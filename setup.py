from setuptools import setup

setup(
	name="extcolors",
	version="0.2.0",
	description="Extract colors from an image. "
				"Colors are grouped based on visual similarities using the CIE76 formula.",
	long_description=open("README.rst").read(),
	long_description_content_type="text/x-rst",
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
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3 :: Only",
	],
	python_requires=">=3.5",
	keywords="extract colors image",
	packages=["extcolors"],
	install_requires=["Pillow >=7.0.0"],
	extras_require={
		"dev": [
			"pytest ==5.4.3",
			"tox ==3.16.0",
			"yapf ==0.30.0",
		]
	},
	entry_points={
		"console_scripts": [
			"extcolors=extcolors.command:main"
		],
	},
)
