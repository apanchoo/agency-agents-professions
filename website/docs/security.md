---
title: Security and maintenance
---

# Keep the site current

The site is static. Search runs locally in the browser, documents are treated as text, raw HTML in agent Markdown is not rendered, and published assets contain no authentication tokens.

## Update automation

The official Renovate application checks JavaScript, Python and GitHub Actions dependencies during the configured early-morning update window. Security update requests are not restricted by that window. Patch, minor and digest updates can merge only after the required site validation succeeds. Major updates remain reviewable pull requests. Native GitHub security alerts and automated security fixes provide an additional security-update channel.

Renovate is installed only for this repository. Its pull requests trigger the normal validation workflow, including production builds and browser checks, before merging. No personal access token is stored in repository secrets.

## Validation and deployment

- A deterministic catalog check verifies complete coverage and unique identifiers.
- Browser tests exercise search, filters, role documents and mobile layout.
- Production dependency auditing and a complete Docusaurus build run before deployment.
- GitHub Pages deployment is restricted to a successful build on `main`.
- JavaScript code scanning runs independently on changes and on a regular schedule.

Dependency automation reduces maintenance work; it does not guarantee that every vulnerability is detected or automatically repairable. Build failures and alerts remain visible in GitHub Actions and the dependency dashboard.

## Reporting a problem

Use the repository's private vulnerability reporting feature when available. Do not disclose credentials or exploitable security details in a public issue. For ordinary documentation or agent-content problems, open an issue with a minimal reproduction and the relevant file path.
