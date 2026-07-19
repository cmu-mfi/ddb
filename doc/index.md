# MFI Digital Data Backbone Documentation

```{button-link} https://cmu-mfi.github.io/
:color: primary
:shadow:
cmu-mfi.github.io
```
<!-- ref: https://sphinx-design.readthedocs.io/en/latest/badges_buttons.html -->

```{raw} html
<h1 style="text-align: center;"> MFI Digital Data Backbone </h1>
<p style="font-size: 20px; color: #555;">Streaming data from manufacturing equipment to the cloud</p>
```

## Welcome

The **Manufacturing Futures Institute** at Carnegie Mellon University has embarked on a mission to become a leader in the digital transformation of manufacturing. The Digital Data Backbone (DDB) is the foundational infrastructure for connecting, collecting, and contextualizing research data generated throughout the Mill 19 facility.

This platform enables researchers to build, apply, and leverage curated and trusted data sources for the transformation of manufacturing — supporting large initiatives in AI-driven advanced manufacturing.

```{toctree}
:maxdepth: 2
:caption: Overview

pages/overview.md
pages/quickstart.md
```

```{toctree}
:maxdepth: 2
:caption: Concepts

pages/concepts/introduction.md
pages/concepts/architecture.md
```

```{toctree}
:maxdepth: 2
:caption: Guides

pages/guides/connect-data-adapter.md
pages/guides/connect-database-node.md
pages/guides/use-retrieval-api.md
pages/guides/grafana-dashboard.md
```

```{toctree}
:maxdepth: 2
:caption: References

pages/references/payload-schema.md
pages/references/adapters/index.md
pages/references/database-nodes/index.md
```

```{toctree}
:maxdepth: 2
:caption: Deployments

pages/deployments/cmu-mill19/introduction.md
pages/deployments/cmu-mill19/equipments.md