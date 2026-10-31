# Documentation build

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://ohara-lab-su.github.io/dds_frame/en/index.html)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://ohara-lab-su.github.io/dds_frame/ja/index.html)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fdds_frame-181717?logo=github)](https://github.com/ohara-lab-su/dds_frame/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/dds_frame/en/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.en.html)

This project follows the shared Sphinx + MyST + Read the Docs theme layout used by `ese774_frame`.

- `docs/conf.py`: Sphinx settings.
- `docs/build.sh`: generates API documentation with `sphinx-apidoc` and builds English and Japanese sites.
- `docs/en/` and `docs/ja/`: independent language source trees.
- `docs/_build/html/`: GitHub Pages output; `.nojekyll` is created by the build script.
- `.github/workflows/pages.yml`: deploys the Sphinx output from `main`.

Run `bash docs/build.sh` after installing `sphinx myst-parser sphinx-rtd-theme linkify-it-py` and project dependencies.
