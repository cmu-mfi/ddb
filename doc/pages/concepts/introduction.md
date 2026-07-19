# Introduction

## What is MFI Digital Data Backbone?

The **Manufacturing Futures Institute (MFI)** at Carnegie Mellon University has embarked on a mission to become a leader in the digital transformation of manufacturing. Engineers and scientists are building the foundational technology infrastructure at Mill 19 and the university that will support and enable data-driven advanced manufacturing research for decades to come.

Commonly known as a **digital backbone**, this foundational infrastructure for connecting, collecting, and contextualizing research data generated throughout the Mill 19 facility will enable researchers to build, apply, and leverage curated and trusted data sources for the transformation of manufacturing. This same foundational infrastructure provides a platform upon which comprehensive virtual representations of equipment, processes, products, and materials can be built to mirror their physical counterparts, creating "digital twins," in real-time or near-real-time.

## Core Principles

```{raw} html
<p style="font-size: 20px; font-weight: bold;">
Build data collection and curation infrastructure, on top of existing R&D infrastructure, to support large initiatives in AI
</p>
```

The DDB is built around three core principles:

### Connect
Connect equipment and sensors to the digital backbone through communication protocols and interfaces. Data generators produce information that flows into the system via data adapters.

### Collect
Collect time series data, video files, photographs, images, and sketches from manufacturing processes. The pub-sub architecture ensures reliable delivery of all data types.

### Contextualize
Contextualize data through user-entered data descriptions (metadata) to ensure integrity and usefulness. Metadata is stored alongside the data itself for full traceability.

## What DDB Provides

| Capability | Description |
|-----------|-------------|
| **Archive** | Store data systematically in secure databases or physical repositories for preservation and future retrieval |
| **Access** | Retrieve and interact with archived data through user-friendly interfaces and APIs |
| **Analyze** | Interpret data using analytical tools and methodologies to derive meaningful insights and informed decisions |

## Who Uses This Documentation?

This documentation is organized by role and task:

- **Getting Started?** → Start with the [Overview](/) and [Quick Start Guide](quickstart.md)
- **Understanding the system?** → Read these Concepts next
- **Setting up a data source?** → Go to [Guides](guides/connect-data-adapter.md)
- **Looking for technical details?** → Check the [References](references/payload-schema.md) section