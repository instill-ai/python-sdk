# Changelog

## [0.3.1](https://github.com/instill-ai/python-sdk/compare/v0.3.0...v0.3.1) (2023-11-08)


### Bug Fixes

* **ray:** fix wrong scope of actor config ([85dd1f1](https://github.com/instill-ai/python-sdk/commit/85dd1f15c7b3d8460fa005bf58d4ef9d56f00838))


### Documentation

* **readme:** update readme for optional config file ([4efd5d6](https://github.com/instill-ai/python-sdk/commit/4efd5d6d24d88d992ca96e4044d6547bc741e391))

## [0.3.0](https://github.com/instill-ai/python-sdk/compare/v0.2.1...v0.3.0) (2023-11-07)


### ⚠ BREAKING CHANGES

* **client:** fix wrongful delete of resources and connection not close ([#42](https://github.com/instill-ai/python-sdk/issues/42))

### Features

* **ray:** add help functions for ray model ([#40](https://github.com/instill-ai/python-sdk/issues/40)) ([39b2cc7](https://github.com/instill-ai/python-sdk/commit/39b2cc7a6bcff73956d0b67f34d45ad2821ffaef))


### Bug Fixes

* **client:** fix wrongful delete of resources and connection not close ([#42](https://github.com/instill-ai/python-sdk/issues/42)) ([d32fb83](https://github.com/instill-ai/python-sdk/commit/d32fb838f1711c0a529cc1ad0327e43c9c44de39))
* **config,pipeline:** allow no config file and fix required pipeline recipe ([#43](https://github.com/instill-ai/python-sdk/issues/43)) ([5290868](https://github.com/instill-ai/python-sdk/commit/5290868ac9d6375bbf7be3a9463aab7eddfd5d59))

## [0.2.1](https://github.com/instill-ai/python-sdk/compare/v0.2.0...v0.2.1) (2023-10-27)


### Miscellaneous Chores

* **release:** release v0.2.1 ([871d7b9](https://github.com/instill-ai/python-sdk/commit/871d7b9f5a6ebd1a3eb85891a584698b4c2c0090))

## [0.2.0](https://github.com/instill-ai/python-sdk/compare/v0.1.0...v0.2.0) (2023-10-15)


### ⚠ BREAKING CHANGES

* **config:** update config file extension
* **config:** update config file path to avoid collision ([#35](https://github.com/instill-ai/python-sdk/issues/35))

### Documentation

* **readme:** update README ([#29](https://github.com/instill-ai/python-sdk/issues/29)) ([5820fff](https://github.com/instill-ai/python-sdk/commit/5820fff36ab9352463187554603e659800595870))


### Code Refactoring

* **config:** update config file extension ([9b0f17f](https://github.com/instill-ai/python-sdk/commit/9b0f17feac128045d9853afd0ae2ef3c78a0e69e))
* **config:** update config file path to avoid collision ([#35](https://github.com/instill-ai/python-sdk/issues/35)) ([0b5b3bd](https://github.com/instill-ai/python-sdk/commit/0b5b3bd869eb45b4695ade0e9c3dc1ef26283781))

## 0.1.0 (2023-10-01)


### Features

* **auth:** adopt `Instill Core` auth ([#16](https://github.com/instill-ai/python-sdk/issues/16)) ([86c0e85](https://github.com/instill-ai/python-sdk/commit/86c0e85e7d626633264303c6faefb5610f18f036))
* **auth:** support api-token for instill cloud authentication ([#6](https://github.com/instill-ai/python-sdk/issues/6)) ([e041510](https://github.com/instill-ai/python-sdk/commit/e0415105fa968b11eb2c5e902141d0dec60d07ea))
* **component,recipe:** support better component/recipe creation ([#22](https://github.com/instill-ai/python-sdk/issues/22)) ([857e260](https://github.com/instill-ai/python-sdk/commit/857e260f3ba6876dc814538aa2346ac4132a9a27))
* **config:** adopt pydantic for yaml config validation ([#9](https://github.com/instill-ai/python-sdk/issues/9)) ([8903975](https://github.com/instill-ai/python-sdk/commit/8903975753434b6f9ad25ed97feb81b76fc7f0b2))


### Bug Fixes

* **clients:** fix metadata overwrite ([#26](https://github.com/instill-ai/python-sdk/issues/26)) ([e332cb0](https://github.com/instill-ai/python-sdk/commit/e332cb09e60497f5c002a61de8ab43a03c475ced))


### Documentation

* **contributing,readme:** update docs and workflow for contributing ([#12](https://github.com/instill-ai/python-sdk/issues/12)) ([6fb0c84](https://github.com/instill-ai/python-sdk/commit/6fb0c84e44f654d7eea286405133912fe7967334))
* **readme,notebook:** add a notebook example ([9f8d728](https://github.com/instill-ai/python-sdk/commit/9f8d7283ad38865c18e4490afb5720dbbc65eb8a))
* **readme:** add usage in README ([#24](https://github.com/instill-ai/python-sdk/issues/24)) ([5af5f42](https://github.com/instill-ai/python-sdk/commit/5af5f4209391b7cfb657643456b5013ce83a8450))
