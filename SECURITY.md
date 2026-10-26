# Security policy

The published website is static. Agent documents are displayed as text; raw HTML is not rendered. No account credentials are included in its build artifacts.

Renovate checks dependencies daily and creates reviewable updates. Patch and minor updates may merge only after the required site validation passes; major updates require review. Native vulnerability alerts and automated security fixes are enabled where supported. Production dependency auditing, browser tests and a static build precede deployment. CodeQL runs separately.

Use private vulnerability reporting on GitHub when available. Avoid posting credentials or exploitable security details in public issues. For ordinary content defects, report the affected file and a minimal reproduction.

Dependency checks and automation reduce risk; they do not guarantee that every vulnerability is detected or automatically fixed. Maintainers remain responsible for failed checks and security alerts.
