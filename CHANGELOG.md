# Changelog

## [0.8.0](https://github.com/instill-ai/python-sdk/compare/v0.7.1...v0.8.0) (2024-04-25)


### Features

* **deps:** upgrade ray version ([cc61b85](https://github.com/instill-ai/python-sdk/commit/cc61b8541c9545ca2b6768c519242af6f6b9df93))
* **ray:** adapt to native docker client instead of docker sdk ([#138](https://github.com/instill-ai/python-sdk/issues/138)) ([7d19ccb](https://github.com/instill-ai/python-sdk/commit/7d19ccbfe24eebe29e4a2e1729b2c82503ad4782))
* **ray:** add accelerator and custom resource support ([#118](https://github.com/instill-ai/python-sdk/issues/118)) ([f974f98](https://github.com/instill-ai/python-sdk/commit/f974f9826d28e4a54c89aa917ec37c5b3eac3c68))
* **ray:** add llava 13b to predeploy list ([3fd5914](https://github.com/instill-ai/python-sdk/commit/3fd591419c940f1635472b25b5bf8f6a522bfd15))
* **ray:** add metadata and infer constructor for llm tasks ([#137](https://github.com/instill-ai/python-sdk/issues/137)) ([be122d1](https://github.com/instill-ai/python-sdk/commit/be122d1b19516fa789c183f5e7128cb34a8c01e1))
* **ray:** generate sha256 as tag if not presented ([#120](https://github.com/instill-ai/python-sdk/issues/120)) ([6abb538](https://github.com/instill-ai/python-sdk/commit/6abb5380ace6df7e0eefff56d19b34559daf8982))
* **ray:** inject accelerator type at runtime ([#121](https://github.com/instill-ai/python-sdk/issues/121)) ([f78a2d0](https://github.com/instill-ai/python-sdk/commit/f78a2d0a604107d208a9783f89e54f68cb68e196))
* **ray:** support containerized model serving ([#116](https://github.com/instill-ai/python-sdk/issues/116)) ([ad0f250](https://github.com/instill-ai/python-sdk/commit/ad0f2505d49dec675558e65cc62e3901311a7673))
* **ray:** support custom accelerator type ([#134](https://github.com/instill-ai/python-sdk/issues/134)) ([ae6c139](https://github.com/instill-ai/python-sdk/commit/ae6c139d3c7eafa3015ec779628321185f76d381))
* **ray:** use env for resource and deprecate deploy/undeploy ([#124](https://github.com/instill-ai/python-sdk/issues/124)) ([a58bc50](https://github.com/instill-ai/python-sdk/commit/a58bc50f97ed8747da961b6cfbf416ea51361c95))
* **ray:** use tmp folder for image building ([#122](https://github.com/instill-ai/python-sdk/issues/122)) ([9512cec](https://github.com/instill-ai/python-sdk/commit/9512cecc47299b5542b6045fead4c70bab07628e))


### Bug Fixes

* **deps:** downgrade ray to avoid grpc servicer issue ([#128](https://github.com/instill-ai/python-sdk/issues/128)) ([9ead421](https://github.com/instill-ai/python-sdk/commit/9ead42178d606827e7f747f5e4150f6c6d12437a))
* **dockerfile:** avoid build hang at ARG statement ([#130](https://github.com/instill-ai/python-sdk/issues/130)) ([f02a27c](https://github.com/instill-ai/python-sdk/commit/f02a27c2f82c7ebe902b01037b2cdd01ddb6e231))
* **ray:** fix etrypoint module not found ([#126](https://github.com/instill-ai/python-sdk/issues/126)) ([f1ed83d](https://github.com/instill-ai/python-sdk/commit/f1ed83de1f7a8e190d3152ba9e3e9b02df5d3617))
* **ray:** fix missing default resource value ([#129](https://github.com/instill-ai/python-sdk/issues/129)) ([b2f564a](https://github.com/instill-ai/python-sdk/commit/b2f564ae2a0cb933497c49653d6707c7275a0226))
* **ray:** fix multi-platform build stage ([6f358fd](https://github.com/instill-ai/python-sdk/commit/6f358fd4b20dd33e09fdc453c9ddac1f515f3260))
* **ray:** support target platform for image building ([#127](https://github.com/instill-ai/python-sdk/issues/127)) ([f4825fc](https://github.com/instill-ai/python-sdk/commit/f4825fce259946072a71f2892a9686914c81ff55))

## [0.7.1](https://github.com/instill-ai/python-sdk/compare/v0.7.0...v0.7.1) (2024-02-22)


### Bug Fixes

* **ray:** update default resources allocation for test ([#102](https://github.com/instill-ai/python-sdk/issues/102)) ([1aaa905](https://github.com/instill-ai/python-sdk/commit/1aaa905ca74cc8afaa29e0290792b57bd12143e2))


### Miscellaneous Chores

* **release:** release v0.7.1 ([b7dec13](https://github.com/instill-ai/python-sdk/commit/b7dec13d87cf4bf1a6a25ba71b85213fc4dc582e))

## [0.7.0](https://github.com/instill-ai/python-sdk/compare/v0.6.0...v0.7.0) (2024-01-30)


### Features

* **ray:** determine ram usage by file size ([#89](https://github.com/instill-ai/python-sdk/issues/89)) ([7a0023d](https://github.com/instill-ai/python-sdk/commit/7a0023d1e2dd6600f69dd2ab08a8e9431a36da2b))
* **ray:** determine vram usage by file size ([#87](https://github.com/instill-ai/python-sdk/issues/87)) ([71e84e6](https://github.com/instill-ai/python-sdk/commit/71e84e68f029daa7b482e300e72f928cacb5e738))


### Bug Fixes

* **ray:** add vram ceiling and override list ([#94](https://github.com/instill-ai/python-sdk/issues/94)) ([5804e4a](https://github.com/instill-ai/python-sdk/commit/5804e4a182e6c3eba7011cf2d879b94b264d214f))
* **ray:** fix application name ([f2bb563](https://github.com/instill-ai/python-sdk/commit/f2bb56369c356619c95b6ef9d3568146c85a1ba7))
* **ray:** fix gpu resource &gt; 1 ([#91](https://github.com/instill-ai/python-sdk/issues/91)) ([b121f56](https://github.com/instill-ai/python-sdk/commit/b121f566011714c208ee804beba2db9f72849a56))
* **ray:** fix ray autoscaling ([#95](https://github.com/instill-ai/python-sdk/issues/95)) ([5bd8c2a](https://github.com/instill-ai/python-sdk/commit/5bd8c2a8b8432d6855854448b4f92ac755b0b020))

## [0.6.0](https://github.com/instill-ai/python-sdk/compare/v0.5.0...v0.6.0) (2024-01-12)


### Features

* **connector,operator,component:** adopt jsonscema validation and dataclass type hint ([#74](https://github.com/instill-ai/python-sdk/issues/74)) ([0c47e51](https://github.com/instill-ai/python-sdk/commit/0c47e51263f7e428499a8461db4b4725ac1e3144))
* **helpers:** add wrapper func for protobuf message ([#85](https://github.com/instill-ai/python-sdk/issues/85)) ([279bd1e](https://github.com/instill-ai/python-sdk/commit/279bd1e5ec6f9501a001c46acff93cee2a67388f))
* **resource:** adopt dataclass as config in component for type hinting ([#79](https://github.com/instill-ai/python-sdk/issues/79)) ([8c25bd1](https://github.com/instill-ai/python-sdk/commit/8c25bd106577cf75d0f24cd52c82ccc2f56baef1))
* **resources:** support recipe update in pipeline resource ([#83](https://github.com/instill-ai/python-sdk/issues/83)) ([89431fa](https://github.com/instill-ai/python-sdk/commit/89431fa39f626736b16ee279ae4b6c9f19a3c1c3))


### Bug Fixes

* **resources:** fix resource schema path ([#76](https://github.com/instill-ai/python-sdk/issues/76)) ([25f4418](https://github.com/instill-ai/python-sdk/commit/25f4418ab713556ab5a82b9bc16f7d0f9e12adc3))


### Documentation

* **notebook:** update notebook ([e5da642](https://github.com/instill-ai/python-sdk/commit/e5da642266b1666fe66b08798668bce6f7e8c05b))

## [0.5.0](https://github.com/instill-ai/python-sdk/compare/v0.4.0...v0.5.0) (2024-01-02)


### ⚠ BREAKING CHANGES

* **ray:** retire non-decorator deploy and update scaling config ([#67](https://github.com/instill-ai/python-sdk/issues/67))

### Features

* **model:** Update Text-Generation Task Schema to Align with OpenAI Standards  ([#69](https://github.com/instill-ai/python-sdk/issues/69)) ([703789a](https://github.com/instill-ai/python-sdk/commit/703789a6d09cfa857b13f296834f87a6daffb18d))


### Bug Fixes

* **model:** fix image decoding issue ([#71](https://github.com/instill-ai/python-sdk/issues/71)) ([5c571b2](https://github.com/instill-ai/python-sdk/commit/5c571b2aec543fcf2208ad83219b1b94dfca3078))
* **ray:** allow cwd as runtime env ([#66](https://github.com/instill-ai/python-sdk/issues/66)) ([00c0497](https://github.com/instill-ai/python-sdk/commit/00c0497ac6bf7232b6ac2d0d18549a7edd3cc03e))
* **ray:** avoid agressive downscale and non upscale ([#70](https://github.com/instill-ai/python-sdk/issues/70)) ([f159314](https://github.com/instill-ai/python-sdk/commit/f1593141d2d5f60faeb51e83a091cd3755c9d9f5))


### Documentation

* **notebooks:** add async example ([49ca895](https://github.com/instill-ai/python-sdk/commit/49ca8956691810590799b494120eb5b95e8b6e5c))


### Code Refactoring

* **ray:** retire non-decorator deploy and update scaling config ([#67](https://github.com/instill-ai/python-sdk/issues/67)) ([89ef078](https://github.com/instill-ai/python-sdk/commit/89ef0787d436ba45933b92e405ce5c2e3f2a6aa9))

## [0.4.0](https://github.com/instill-ai/python-sdk/compare/v0.3.2...v0.4.0) (2023-12-11)


### ⚠ BREAKING CHANGES

* **client:** support asyncio and add better client type hint ([#55](https://github.com/instill-ai/python-sdk/issues/55))

### Features

* **client:** support asyncio and add better client type hint ([#55](https://github.com/instill-ai/python-sdk/issues/55)) ([aa41246](https://github.com/instill-ai/python-sdk/commit/aa41246b6ae3c27d62438436b2023316d2e1d664))
* **org:** adopt organization endpoints for VDP ([#60](https://github.com/instill-ai/python-sdk/issues/60)) ([0c313d6](https://github.com/instill-ai/python-sdk/commit/0c313d605ceb016a7bb534a20c545d3187d1be83))
* **ray:** add io helpers for llm tasks ([#59](https://github.com/instill-ai/python-sdk/issues/59)) ([1876a20](https://github.com/instill-ai/python-sdk/commit/1876a20256f3bb82ad37ca88fd83e849a3dd14cc))
* **ray:** add nested decorators ([#63](https://github.com/instill-ai/python-sdk/issues/63)) ([900dda8](https://github.com/instill-ai/python-sdk/commit/900dda8ac952e933aa9cbb35274c19b8ecbab252))
* **ray:** add text to image io helper ([#58](https://github.com/instill-ai/python-sdk/issues/58)) ([0430977](https://github.com/instill-ai/python-sdk/commit/04309779454ef6a0078efc6636735f4e4e2d7af5))


### Bug Fixes

* **clients,resources:** fix resource creating will get None type ([#57](https://github.com/instill-ai/python-sdk/issues/57)) ([4516d46](https://github.com/instill-ai/python-sdk/commit/4516d466b6e7ce0891f06d6616123e35e3b2291e))
* **makefile:** fix wheel build missing submodule ([9aa73eb](https://github.com/instill-ai/python-sdk/commit/9aa73ebd157d08fc1ab7975eeb2fa9e407c2e330))
* **ray:** fix missing ray init ([#64](https://github.com/instill-ai/python-sdk/issues/64)) ([db0b5c4](https://github.com/instill-ai/python-sdk/commit/db0b5c49a154b73f6607fc02c8b6d157d01e619e))


### Documentation

* **notebooks:** update notebooks to adopt latest ray decorators ([52b90c6](https://github.com/instill-ai/python-sdk/commit/52b90c6283984158670773629017289f76e508d5))

## [0.3.2](https://github.com/instill-ai/python-sdk/compare/v0.3.1...v0.3.2) (2023-11-29)


### Bug Fixes

* **client:** fix async pipeline trigger and get user ([#53](https://github.com/instill-ai/python-sdk/issues/53)) ([c86274b](https://github.com/instill-ai/python-sdk/commit/c86274bb1a0332b12f2f94f4644cadbe339118a6))
* **ray:** fix mismatched grpcio version ([024471a](https://github.com/instill-ai/python-sdk/commit/024471aafb96e8ad48cfbe4c10033d584ee5b35e))
* **ray:** fix model weight file extension ([4f3a40c](https://github.com/instill-ai/python-sdk/commit/4f3a40c005b3ca0b8ab96f28b6613474d932622a))

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
