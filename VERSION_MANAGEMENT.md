# 🏷️ Velora Version Management Guide

## 📋 Current Version History

### v1.0.1 (2025-11-13) - Latest

- **PyPI**: ✅ Published
- **Git Tag**: ✅ Created
- **GitHub**: ✅ Pushed
- **Changes**: Code cleanup, repository organization, documentation streamlining

### v1.0.0 (2025-11-13) - Initial Release

- **PyPI**: ✅ Published
- **Git Tag**: ✅ Created
- **GitHub**: ✅ Pushed
- **Changes**: Initial release with chat, file sharing, multiple connection modes

## 🚀 Release Process for Future Versions

### 1. Make Your Changes

```bash
# Edit code, fix bugs, add features
vim velora/client.py
# Test your changes
velora chat
```

### 2. Update Version Number

```bash
# Edit setup.py - increment version (1.0.1 → 1.0.2)
vim setup.py
```

### 3. Update Documentation

```bash
# Add entry to CHANGELOG.md
vim CHANGELOG.md
```

### 4. Commit Changes

```bash
git add .
git commit -m "Release v1.0.2 - Brief description of changes"
git push origin master
```

### 5. Create Git Tag

```bash
# Create annotated tag with release message
git tag -a v1.0.2 -m "Release v1.0.2 - Brief description"
git push origin v1.0.2
```

### 6. Build and Publish to PyPI

```bash
# Clean previous builds
rm -rf dist/ *.egg-info/

# Build new package
python -m build

# Upload to PyPI
twine upload dist/*
```

## 🔍 Useful Git Commands

### View Version History

```bash
# List all tags
git tag --sort=version:refname

# Show tag details
git tag -n1

# View commits for a specific version
git log v1.0.0..v1.0.1 --oneline

# Compare versions
git diff v1.0.0..v1.0.1
```

### GitHub Releases

- Visit: https://github.com/pavansai-tanguturi/Velora/releases
- Create releases from your tags with detailed release notes
- Attach distribution files if needed

## 📊 Version Numbering Strategy

Using **Semantic Versioning** (semver.org):

- `MAJOR.MINOR.PATCH` (e.g., 1.0.1)
- **MAJOR** (1.x.x): Breaking changes, incompatible API changes
- **MINOR** (x.1.x): New features, backwards compatible
- **PATCH** (x.x.1): Bug fixes, backwards compatible

### Examples:

- `1.0.2` - Bug fix release
- `1.1.0` - New feature (e.g., add GUI mode)
- `2.0.0` - Major rewrite or breaking changes

## ✅ Checklist for Each Release

- [ ] Code changes tested locally
- [ ] Version updated in `setup.py`
- [ ] `CHANGELOG.md` updated with changes
- [ ] Changes committed and pushed to GitHub
- [ ] Git tag created and pushed
- [ ] Package built with `python -m build`
- [ ] Published to PyPI with `twine upload dist/*`
- [ ] GitHub release created (optional but recommended)

---

**This ensures your Git history matches your PyPI releases perfectly!** 🎯
