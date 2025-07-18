---
applyTo: '**'
---
# Coding standards, domain knowledge, and preferences that AI should follow.

These instructions guide AI-assisted code contributions to ensure precision, maintainability, and alignment with project architecture. Follow each rule exactly unless explicitly told otherwise.

1. **Minimize Scope of Change**  
  - Identify the smallest unit (function, class, or module) that fulfills the requirement.  
  - Do not modify unrelated code, or comments.  
  - Avoid refactoring unless required for correctness or explicitly requested.

2. **Preserve System Behavior**  
  - Ensure the change does not affect existing features or alter outputs outside the intended scope.  
  - Maintain original patterns, APIs, and architectural structure unless otherwise instructed.

3. **Graduated Change Strategy**  
  - **Default:** Implement the minimal, focused change.  
  - **If Needed:** Apply small, local refactorings (e.g., rename a variable, extract a function).  
  - **Only if Explicitly Requested:** Perform broad restructuring across files or modules.

4. **Clarify Before Acting on Ambiguity**  
  - If the task scope is unclear or may impact multiple components, stop and request clarification.  
  - Never assume broader intent beyond the described requirement.

5. **Log, Don’t Implement, Unscoped Enhancements**  
  - Identify and note related improvements without changing them.  
  - Example: `// Note: Function Y may benefit from similar validation.`

6. **Ensure Reversibility**  
  - Write changes so they can be easily undone.  
  - Avoid cascading or tightly coupled edits.

7. **Code Quality Standards**  
  - **Clarity:** Use descriptive names. Keep functions short and single-purpose.  
  - **Consistency:** Match existing styles, patterns, and naming.  
  - **Error Handling:** Use try/except (Python) or try/catch (JS/TS). Anticipate failures (e.g., I/O, user input).  
  - **Security:** Sanitize inputs. Avoid hardcoding secrets. Use environment variables for config.  
  - **Testability:** Enable unit testing. Prefer dependency injection over global state.  
  - **Documentation:**  
    - Use DocStrings (`"""Description"""`) for Python.  
    - Use JSDoc (`/** @param {Type} name */`) for JavaScript/TypeScript.  
    - Comment only non-obvious logic.

8. **Testing Requirements**  
  - Add or modify only tests directly related to your change.  
  - Ensure both success and failure paths are covered.  
  - If existing test is obsolete for any reason, point it out, and ask for guidance.  
  - Do not delete existing tests unless explicitly allowed.  
  - Unit tests should have minimal (or none at all) external dependcies. If possible write a simple mockup functions.  
  - Intergration tests should be written against actual API. External dependencies are okay here.  
    - Ask before writing integration tests. Simple unit testing might be sufficient for given project prupose.
    - When asking to write intergration tests, provide simple overview describing scope and goal.

9. **Forbidden Actions Unless Explicitly Requested**  
  - Global refactoring across files  
  - Changes to unrelated modules  
  - Modifying formatting or style-only elements without functional reason  
  - Adding new dependencies  

10. **Handling Ambiguous References**  
  - When encountering ambiguous terms (e.g., "this component", "the helper"),  
    always refer to the exact file path and line numbers when possible  
  - If exact location is unclear, ask for clarification before proceeding  
  - Never assume the meaning of ambiguous references

11. **Always test when in "user interactive mode"**
  **user interactive mode**: Implementing changes based on short prompts from the user.
  - When implementing changes in "user interactive mode", always try to test the change
  - If unsure how to test, ask for a proper **test command**

Always act within the described scope and prompt constraints. If unsure—ask first.

---
# Included from commits.md

# Commit Message Instructions (Conventional Commits)

Use the Conventional Commit Messages specification to generate commit messages

The commit message should be structured as follows:


```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
``` 
--------------------------------

The commit contains the following structural elements, to communicate intent to the consumers of your library:

  - `fix:` a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
  - `feat:` a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
  - `BREAKING CHANGE:` a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
  - types other than `fix:` and `feat`: are allowed :
    - `docs`: documentation changes
    - `style`: formatting, missing semi colons, etc.
    - `refactor`: code change that neither fixes a bug nor adds a feature
    - `test`: adding or correcting tests
    - `chore`: maintenance tasks
    - `ci`: update to ci/cd pipeline
    - `ai`: updates to instructions/prompts
    for example @commitlint/config-conventional (based on the Angular convention) recommends build:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others.
  - footers other than BREAKING CHANGE: <description> may be provided and follow a convention similar to git trailer format.
  - Additional types are not mandated by the Conventional Commits specification, and have no implicit effect in Semantic Versioning (unless they include a BREAKING CHANGE). A scope may be provided to a commit’s type, to provide additional contextual information and is contained within parenthesis, e.g., feat(parser): add ability to parse arrays.
  - description starts with Capital letter after `:`



### Specification Details

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Commits MUST be prefixed with a type, which consists of a noun, feat, fix, etc., followed by the OPTIONAL scope, OPTIONAL !, and REQUIRED terminal colon and space.
The type feat MUST be used when a commit adds a new feature to your application or library.
The type fix MUST be used when a commit represents a bug fix for your application.
A scope MAY be provided after a type. A scope MUST consist of a noun describing a section of the codebase surrounded by parenthesis, e.g., fix(parser):
A description MUST immediately follow the colon and space after the type/scope prefix. The description is a short summary of the code changes, e.g., fix: array parsing issue when multiple spaces were contained in string.
A longer commit body MAY be provided after the short description, providing additional contextual information about the code changes. The body MUST begin one blank line after the description.
A commit body is free-form and MAY consist of any number of newline separated paragraphs.
One or more footers MAY be provided one blank line after the body. Each footer MUST consist of a word token, followed by either a :<space> or <space># separator, followed by a string value (this is inspired by the git trailer convention).
A footer’s token MUST use - in place of whitespace characters, e.g., Acked-by (this helps differentiate the footer section from a multi-paragraph body). An exception is made for BREAKING CHANGE, which MAY also be used as a token.
A footer’s value MAY contain spaces and newlines, and parsing MUST terminate when the next valid footer token/separator pair is observed.
Breaking changes MUST be indicated in the type/scope prefix of a commit, or as an entry in the footer.
If included as a footer, a breaking change MUST consist of the uppercase text BREAKING CHANGE, followed by a colon, space, and description, e.g., BREAKING CHANGE: environment variables now take precedence over config files.
If included in the type/scope prefix, breaking changes MUST be indicated by a ! immediately before the :. If ! is used, BREAKING CHANGE: MAY be omitted from the footer section, and the commit description SHALL be used to describe the breaking change.
Types other than feat and fix MAY be used in your commit messages, e.g., docs: update ref docs.
The units of information that make up Conventional Commits MUST NOT be treated as case sensitive by implementors, with the exception of BREAKING CHANGE which MUST be uppercase.
BREAKING-CHANGE MUST be synonymous with BREAKING CHANGE, when used as a token in a footer.

---
# Included from versioning.md

# AI Agent Instructions: Automatic Versioning (Semantic Versioning)

> **Note:** This versioning strategy depends on proper format of commit messages.

## 1. Version Bumping Rules (Semantic Versioning)
- Use the [Semantic Versioning 2.0.0](https://semver.org) format.
- Version format: `MAJOR.MINOR.PATCH`
- **MAJOR**: Increment when you make incompatible API changes (breaking changes).
- **MINOR**: Increment when you add functionality in a backward compatible manner.
- **PATCH**: Increment when you make backward compatible bug fixes.

## 2. Additional Notes
- Pre-release versions can be denoted with a hyphen (e.g., `1.0.0-alpha`).
- Build metadata can be appended with a plus sign (e.g., `1.0.0+build.1`).
- Always ensure the public API is documented and changes are reflected in the version number.

## 3. Language-Specific Versioning Overrides
Some package managers or ecosystems require different versioning formats for pre-releases or metadata:

- **RubyGems**: Pre-release versions use a dot instead of a hyphen, e.g., `1.0.0.pre`, `1.0.0.alpha`, `1.0.0.beta`.
- **Python (PyPI)**: Accepts both hyphen and dot, but prefers dot for pre-releases, e.g., `1.0.0a1`, `1.0.0b1`, `1.0.0rc1`.
- **npm (Node.js)**: Follows SemVer strictly, using hyphens for pre-releases, e.g., `1.0.0-alpha`.
- **Other ecosystems**: Always check the documentation for the target package manager and adjust the versioning format accordingly.

**Override Guidance:**
- When publishing, convert pre-release and build metadata to match the conventions of the target language or package manager.

---

**Summary:**  
The AI agent should enforce commit message structure, detect the type of the change and automatically bump the version number according to SemVer rules. Breaking changes trigger a major version bump, new features a minor bump, and bug fixes a patch bump.


---
# Included from changelog.md

# Guidelines for Automatic CHANGELOG.md Generation

1. **Source of Truth**  
   - Use commit messages (see `commits.md`) as the primary source for changelog entries.
   - Parse messages according to the Conventional Commits specification.

2. **Grouping by Version**  
   - Group changes under headings for each released version (e.g., `## [1.2.0] - 2025-07-14`).
   - List unreleased changes under an `Unreleased` section until a new version is published.

3. **Categorization**  
   - Categorize entries by type:
     - **Explicitly list:**
       - Breaking changes (highlighted in a `### Breaking Changes` section)
       - Features (`feat`)
       - Bug Fixes (`fix`)
     - **Summarize without listing every change:**
       - Documentation (`docs`)
       - Refactoring (`refactor`)
       - Performance (`perf`)
       - Tests (`test`)
       - Chores (`chore`)
       - CI/CD (`ci`)
   - For summarized categories, provide a brief note (e.g., "Several documentation updates.", "Various refactoring improvements."). If major improvement was made in a category, provide a brief overview.

4. **Entry Formatting**  
   - For breaking changes, features, and fixes: include the scope (if present) and a concise description.
   - Example: `- parser: add ability to parse arrays`
   - For summarized categories: do not list individual changes, just provide a summary statement, or brief overview for major improvements.

5. **References**  
   - Optionally include commit hashes, PR numbers, or author names for traceability.

6. **Automation**  
   - Generate changelog entries automatically during release or version bump processes.
   - Ensure changelog is updated and committed as part of the release workflow.

7. **Language/Ecosystem Overrides**  
   - If publishing to an ecosystem with specific changelog requirements, adjust formatting accordingly.

---

**Summary:**  
Automate `CHANGELOG.md` generation by parsing commit messages (see `commits.md`), grouping and categorizing changes by version and type, and highlighting breaking changes. Ensure the changelog is always up-to-date and matches the published version history.
