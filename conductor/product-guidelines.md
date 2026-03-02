# Product Guidelines

## Developer Experience (DX) First
- **Intuitive & Discoverable:** The API surface should be logical and self-documenting. Use clear naming conventions for methods and classes.
- **Helpful Errors:** Raise specific, descriptive exceptions that guide developers toward a solution rather than just stating a failure.
- **Easy Onboarding:** Examples must be kept up-to-date and should provide working code snippets that developers can copy and paste.

## Design Philosophy
- **Pythonic Style:** Strictly adhere to PEP 8 standards. The SDK should feel natural to Python developers, utilizing modern features like type hints and async/await where appropriate.
- **Sensible Defaults:** Provide default configurations that work out-of-the-box for the majority of use cases, while allowing deep customization when needed.
- **Minimal Dependencies:** Keep the dependency tree small to reduce the risk of conflicts in the consumer's environment.

## Reliability and Stability
- **Robust Networking:** Gracefully handle transient network errors, timeouts, and API rate limits.
- **Semantic Versioning:** Clearly communicate breaking changes, new features, and bug fixes following SemVer principles to ensure predictable upgrades.
